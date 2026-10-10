# Paz Group - Technical Assessment

My solutions to the three tasks in the Paz technical assessment: a Power Automate registration workflow, a Python scraper for the Paz careers site, and an HR assistant built in Microsoft Copilot Studio. Task 3's job answers use the data scraped in Task 2.

---

## Repository Structure

```
paz-home-test/
├── task1_power_automate/   # Task 1: Gym registrations → Power Automate → SharePoint + Excel
├── task2_scraping/         # Task 2: Paz careers scraper (Python)
├── task3_copilot_agent/    # Task 3: Paz HR Assistant (Copilot Studio)
└── README.md               # This file
```

---

## Tasks Overview

### [Task 1: Gym Registration Automation (Power Automate)](./task1_power_automate/)
- **Goal:** Process gym registrations automatically as they arrive.
- **How it works:** When a new item is added to the *Gym Registrations* Microsoft List, the flow copies each attached document into a SharePoint folder (`/Documents/Gym_Registrations`). It then adds one row per registration to `RegistrationTable` in [`sample_registrations.xlsx`](./task1_power_automate/sample_registrations.xlsx).
- **Files:** the exported flow package (`.zip`), the Excel file, a form screenshot, and import/setup instructions.

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

Tasks 1 and 3 run in Microsoft cloud services (Power Automate and Copilot Studio), so there is nothing to run locally. Their folders contain the exported configuration, screenshots, and deployment instructions.

---

## Navigating the Tasks

Each task folder has its own README with setup steps, run or deployment instructions, and how to verify the result.

| Task | Folder | Start here |
|------|--------|------------|
| 1 | [`task1_power_automate/`](./task1_power_automate/) | [`README.md`](./task1_power_automate/README.md) |
| 2 | [`task2_scraping/`](./task2_scraping/) | [`README.md`](./task2_scraping/README.md) |
| 3 | [`task3_copilot_agent/`](./task3_copilot_agent/) | [`README.md`](./task3_copilot_agent/README.md) |
