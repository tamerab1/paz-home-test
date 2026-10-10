# Paz Group - Technical Assessment

My solutions to the three tasks in the Paz technical assessment: a Power Automate registration workflow, a Python scraper for the Paz careers site, and an HR assistant built in Microsoft Copilot Studio. Task 3's job answers use the data scraped in Task 2.

---

## Repository Structure

```
paz-home-test/
├── task1_power_automate/   # Task 1: Registration form → Power Automate → Excel
├── task2_scraping/         # Task 2: Paz careers scraper (Python)
├── task3_copilot_agent/    # Task 3: Paz HR Assistant (Copilot Studio)
└── README.md               # This file
```

---

## Tasks Overview

### [Task 1: Registration Automation (Power Automate)](./task1_power_automate/)
- **Goal:** Automatically save gym registration form submissions as rows in an Excel file.
- **How it works:** A Microsoft Lists form collects full name, phone, email, birth date, notes, and attachments (health approval and ID or driver's license). A Power Automate flow writes each submission to [`sample_registrations.xlsx`](./task1_power_automate/sample_registrations.xlsx), with links to the attached files.
- **Files:** the form screenshot ([`task1_automation.png`](./task1_power_automate/task1_automation.png)) and the Excel template.

### [Task 2: Paz Careers Scraper (Python)](./task2_scraping/)
- **Goal:** Collect all open positions from [paz.co.il/jobs](https://www.paz.co.il/jobs).
- **How it works:** Built with `requests` and BeautifulSoup. It retries failed requests with increasing delays, decodes Hebrew URLs, assigns each job to a department, and has an optional `--deep` mode that also fetches each job's own page.
- **Output:** 34 positions saved as [`jobs.csv`](./task2_scraping/jobs.csv), [`jobs.json`](./task2_scraping/jobs.json), and [`jobs.xlsx`](./task2_scraping/jobs.xlsx), plus a `pytest` test suite.

### [Task 3: Paz HR Virtual Assistant (Copilot Studio)](./task3_copilot_agent/)
- **Goal:** A Hebrew-first chatbot for both job candidates and current employees.
- **Candidates:** Job search, requirements, and application intake, answered only from Task 2's `jobs.csv` with web search disabled.
- **Employees:** Answers about Form 101, pay slips (Hilan / Paz portal), and sick-leave reporting.
- **Evidence:** 13 tested scenarios with screenshots, including three where the agent correctly says it doesn't have the information. The full system instructions and a demo link are also included.

---

## Quick Start

```bash
git clone https://github.com/tamerab1/paz-home-test.git
cd paz-home-test

# Task 2: create a virtual environment and run the scraper
python -m venv venv
venv\Scripts\activate            # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r task2_scraping/requirements.txt

cd task2_scraping
python scrape_jobs.py --deep     # writes jobs.json and jobs.csv
pytest -v                        # runs the unit tests
```

Tasks 1 and 3 run in Microsoft cloud services (Power Automate and Copilot Studio), so there is nothing to run locally. Their folders contain the configuration, the screenshots, and the instructions for reproducing them.

---

## Navigating the Tasks

Each task folder contains its own files: setup and run instructions for code, and configuration plus screenshots for the cloud-based tasks.

| Task | Folder | Start here |
|------|--------|------------|
| 1 | [`task1_power_automate/`](./task1_power_automate/) | [`task1_automation.png`](./task1_power_automate/task1_automation.png) |
| 2 | [`task2_scraping/`](./task2_scraping/) | [`README.md`](./task2_scraping/README.md) |
| 3 | [`task3_copilot_agent/`](./task3_copilot_agent/) | [`README.md`](./task3_copilot_agent/README.md) |
