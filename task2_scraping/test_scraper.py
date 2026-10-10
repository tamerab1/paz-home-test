import pytest
from scrape_jobs import PazScraper, JobPosting

@pytest.fixture
def scraper():
    return PazScraper()

def test_clean_text_unescaping(scraper):
    """בדיקה שפענוח תווים ורווחים עובד כראוי."""
    raw = "  מנהל%20סניף%20\t\n  "
    cleaned = scraper._clean_text(raw)
    assert cleaned == "מנהל סניף"

def test_department_extraction_from_retail_url(scraper):
    """בדיקת שיוך חטיבת קמעונאות מתוך כתובת ה-URL."""
    url = "/jobs/retail/salesclerk"
    title = "מוכרנים/ות לחנויות yellow"
    dept = scraper._extract_department_from_url(url, title)
    assert "Yellow" in dept or "קמעונאות" in dept

def test_department_extraction_from_financial_url(scraper):
    """בדיקת שיוך מחלקת כספים מתוך כתובת ה-URL."""
    url = "/jobs/financial/accountant"
    title = "מנהל/ת חשבונות"
    dept = scraper._extract_department_from_url(url, title)
    assert "כספים" in dept

def test_job_posting_serialization():
    """בדיקת תקינות המרת מודל הנתונים למילון."""
    job = JobPosting(
        title="מפתח Python",
        department="מערכות מידע",
        link="https://www.paz.co.il/jobs/it/python-dev",
        description="תיאור משרה",
        date="2026-10-07"
    )
    data = job.to_dict()
    assert data["title"] == "מפתח Python"
    assert "link" in data