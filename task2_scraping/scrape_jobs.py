#!/usr/bin/env python3
"""
Paz Careers Scraper - Full Description Edition
==============================================
Production-grade Web Scraper for extracting open job positions from Paz (paz.co.il/jobs).
Fetches accurate titles, departments, direct links, and full job descriptions.
"""

import argparse
import csv
from dataclasses import asdict, dataclass
import json
import logging
import re
import sys
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, unquote

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("PazJobScraper")

BASE_URL = "https://www.paz.co.il"
TARGET_URL = "https://www.paz.co.il/jobs"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
}

URL_DEPARTMENT_MAP = {
    "executive-operations": "מטה, משאבי אנוש והנהלה",
    "retail": "קמעונאות ורשת מתחמים (Yellow)",
    "financial": "כספים, חשבות וכלכלה",
    "operation-1": "תפעול, הנדסה ולוגיסטיקה",
    "operation": "תפעול והנדסה",
    "sales": "מכירות, סחר ושירות לקוחות",
    "marketing": "שיווק ודיגיטל",
    "it": "מערכות מידע וטכנולוגיה",
    "real-estate": "נדל\"ן ופיתוח עסקי",
}


@dataclass
class JobPosting:
    """סכמת נתונים תקנית למשרה."""
    title: str
    department: str
    link: str
    description: str
    date: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PazScraper:
    def __init__(self, timeout: int = 15, delay: float = 0.2):
        self.timeout = timeout
        self.delay = delay
        self.session = self._create_resilient_session()

    @staticmethod
    def _create_resilient_session() -> requests.Session:
        session = requests.Session()
        session.headers.update(DEFAULT_HEADERS)
        retries = Retry(
            total=4,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    @staticmethod
    def _clean_text(text: Optional[str]) -> str:
        if not text:
            return ""
        text = unquote(text)
        text = re.sub(r"[\r\n\t]+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _extract_department_from_url(url_path: str, title: str) -> str:
        path_lower = url_path.lower()
        for segment, dept_name in URL_DEPARTMENT_MAP.items():
            if f"/{segment}/" in path_lower or f"/{segment}" in path_lower:
                return dept_name

        title_lower = title.lower()
        if any(w in title_lower for w in ["גיוס", "הדרכה", "שכר", "רווחה", "משאבי אנוש", "מטה"]):
            return "מטה, משאבי אנוש והנהלה"
        if any(w in title_lower for w in ["yellow", "מתחם", "סניף", "קמעונאות", "סופר יודה", "מוכר"]):
            return "קמעונאות ורשת מתחמים (Yellow)"
        if any(w in title_lower for w in ["חשבון", "כספים", "גזבר", "כלכלן", "אשראי", "רכש"]):
            return "כספים, חשבות וכלכלה"
        if any(w in title_lower for w in ["נהג", "מלגז", "מפעיל", "טכנאי", "חשמל", "אחזקה", "מחסנאי", "תפעול"]):
            return "תפעול, הנדסה ולוגיסטיקה"
        if any(w in title_lower for w in ["מכירות", "שירות", "קשרי לקוחות", "נציג"]):
            return "מכירות, סחר ושירות לקוחות"
        if any(w in title_lower for w in ["שיווק", "אנליסט"]):
            return "שיווק ודיגיטל"
        if any(w in title_lower for w in ["תוכנה", "פיתוח", "devops", "qa", "it"]):
            return "מערכות מידע וטכנולוגיה"

        return "מטה וכללי"

    def fetch_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as err:
            logger.error(f"שגיאה בגישה לכתובת {url}: {err}")
            return None

    def fetch_job_details(self, job_url: str) -> Dict[str, str]:
        """חילוץ תיאור משרה מלא ישירות מדף המשרה הפנימי."""
        details = {"description": "", "date": ""}
        if not job_url or not job_url.startswith("http"):
            return details

        soup = self.fetch_soup(job_url)
        if not soup:
            return details

        # 1. חיפוש אזור תוכן המשרה
        content_area = soup.select_one(".job-details, .job-content, .job-description, article, main")
        target_soup = content_area if content_area else soup

        # איסוף פסקאות טקסט משמעותיות
        paragraphs = []
        for p in target_soup.find_all(["p", "li"]):
            text = self._clean_text(p.get_text())
            if len(text) > 20 and not any(skip in text for skip in ["כל הזכויות שמורות", "עוגיות", "accessibility"]):
                paragraphs.append(text)

        if paragraphs:
            # איחוד מספר פסקאות ראשונות של תיאור התפקיד
            details["description"] = " | ".join(paragraphs[:3])

        date_el = soup.select_one(".date, .job-date, time, .posted-date")
        if date_el:
            details["date"] = self._clean_text(date_el.get_text())

        return details

    def scrape(self, deep_scan: bool = True) -> List[JobPosting]:
        logger.info(f"מתחיל בסריקת עמוד המשרות: {TARGET_URL}")
        soup = self.fetch_soup(TARGET_URL)
        if not soup:
            logger.error("לא ניתן היה לטעון את עמוד הדרושים.")
            return []

        jobs: List[JobPosting] = []
        seen_links = set()

        job_links = soup.find_all("a", href=lambda h: h and ("/jobs/" in h or "/job/" in h))

        for a_tag in job_links:
            href = a_tag.get("href", "").strip()
            full_link = urljoin(BASE_URL, href)

            if full_link.rstrip("/") in ["https://www.paz.co.il/jobs", "https://www.paz.co.il"] or full_link in seen_links:
                continue

            # פענוח שם המשרה מתוך ה-URL
            slug = href.strip("/").split("/")[-1]
            slug_decoded = unquote(slug)
            slug_clean = re.sub(r"[-_]+", " ", slug_decoded).strip()

            card = a_tag.find_parent(class_=re.compile(r"item|card|box|row|job|post", re.I)) or a_tag.parent
            detected_title = ""

            if card:
                title_candidates = card.find_all(["h1", "h2", "h3", "h4", "h5", "strong", "span"])
                for cand_el in title_candidates:
                    t = self._clean_text(cand_el.get_text())
                    # סינון ביטויים לא רלוונטיים כמו כפתורי שיתוף
                    if t and len(t) > 3 and not any(g in t for g in ["למידע נוסף", "קרא עוד", "הגש", "שיתוף משרה", "שתף"]):
                        detected_title = t
                        break

            final_title = detected_title if detected_title else slug_clean
            if not final_title or len(final_title) < 2 or "שיתוף משרה" in final_title:
                final_title = slug_clean

            seen_links.add(full_link)
            dept = self._extract_department_from_url(href, final_title)

            jobs.append(
                JobPosting(
                    title=final_title,
                    department=dept,
                    link=full_link,
                    description="",
                    date="",
                )
            )

        # הרצת סריקת תיאורים מלאים מתוך עמודי המשרה
        if deep_scan and jobs:
            logger.info(f"אוסף תיאורי משרה מלאים מתוך {len(jobs)} עמודי המשרות...")
            for idx, job in enumerate(jobs, 1):
                logger.info(f"[{idx}/{len(jobs)}] מוריד תיאור עבור: {job.title}")
                details = self.fetch_job_details(job.link)
                if details["description"]:
                    job.description = details["description"]
                if details["date"]:
                    job.date = details["date"]
                time.sleep(self.delay)

        logger.info(f"סך הכל חולצו {len(jobs)} משרות עם תיאורים מלאים.")
        return jobs


class Exporter:
    @staticmethod
    def to_json(jobs: List[JobPosting], filepath: str = "jobs.json") -> None:
        data = [job.to_dict() for job in jobs]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"נשמר בהצלחה קובץ JSON: {filepath}")

    @staticmethod
    def to_csv(jobs: List[JobPosting], filepath: str = "jobs.csv") -> None:
        if not jobs:
            logger.warning("אין נתונים לייצוא CSV.")
            return

        data = [job.to_dict() for job in jobs]
        fieldnames = ["title", "department", "link", "description", "date"]
        
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"נשמר בהצלחה קובץ CSV: {filepath}")


def main():
    scraper = PazScraper()
    jobs = scraper.scrape(deep_scan=True)
    Exporter.to_json(jobs, filepath="jobs.json")
    Exporter.to_csv(jobs, filepath="jobs.csv")
    logger.info("הסריקה והייצוא הסתיימו בהצלחה!")


if __name__ == "__main__":
    main()