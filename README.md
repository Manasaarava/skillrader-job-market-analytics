# SkillRadar — Job Market & Skill Demand Analytics

SkillRadar is a local, educational prototype that analyzes a small included CSV dataset of illustrative job listings. It extracts skill mentions using a transparent keyword taxonomy, compares demand by role/location, and creates a basic skill-gap report from a user's self-declared skills.

> **Data limitation:** The included records and salary values are synthetic examples for demonstrating functionality. They are not live job listings or reliable market estimates. Replace them with a properly licensed, cited dataset before making real-world claims.

## Features
- Dashboard summary for records, roles, locations, and tracked skills.
- Filters for role and location.
- Keyword-based NLP-style skill extraction with alias normalization.
- Skill frequency chart and sample listing table.
- Skill-gap report compared with selected role requirements.
- Runs locally without a paid AI API.

## Requirements
Python 3.10+ recommended.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 in a browser.

## Dataset format
`data/job_listings.csv` columns: `company`, `role`, `location`, `experience`, `salary_lpa`, `description`.

## Methodology
1. Read CSV with Pandas and normalize job-description text.
2. Normalize common aliases such as `PowerBI` to `Power BI`.
3. Search descriptions against a defined skill taxonomy using token boundaries.
4. Count listings mentioning each skill; filter counts by role/location.
5. Compare detected skill names with user-entered skills to propose learning priorities.

## Evaluation
Manually label a sample of descriptions and calculate precision/recall for skill extraction. Test filtering, empty data, missing fields, and skill-gap results. Report observed values only after running these tests.

## Limitations
- Keyword taxonomy can miss synonyms and context, and can produce false matches.
- The dataset is small and synthetic; results are not representative of the current job market.
- No live job scraping or external generative model is included.
- Salary values are illustrative only.

## Repository link
After creating a public GitHub repository, replace the placeholder URL in the report and presentation with the real repository URL. Do not claim a repository is public until it has been created and verified.

## References
- Python documentation: https://docs.python.org/3/
- Pandas documentation: https://pandas.pydata.org/docs/
- Python HTTP server documentation: https://docs.python.org/3/library/http.server.html
- scikit-learn documentation (future evaluation extensions): https://scikit-learn.org/stable/
