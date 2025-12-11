# Example: Process ManageBac Emails

> This is a template directive to show you the format. Replace with your actual workflow.

## Goal
Classify and process emails from ManageBac to extract key information and organize them systematically.

## Inputs
- Gmail account credentials (from `.env`)
  - `GMAIL_EMAIL`
  - `GMAIL_APP_PASSWORD`
- ManageBac email patterns to identify
- Categories/tags for classification

## Tools
- `execution/fetch_emails.py` - Fetch emails from Gmail
- `execution/classify_email.py` - Classify emails using AI
- `execution/export_to_sheets.py` - Export results to Google Sheets

## Process

### Step 1: Fetch Emails
```
Run execution/fetch_emails.py with:
- Email account from .env
- Date range: Last 7 days
- Filter: From ManageBac domains
- Output: .tmp/emails.json
```

### Step 2: Classify Each Email
```
For each email in .tmp/emails.json:
- Run execution/classify_email.py
- Determine category (Assignment, Announcement, Grade, etc.)
- Extract key data (due dates, subjects, links)
- Store in .tmp/classified_emails.json
```

### Step 3: Export to Google Sheets
```
Run execution/export_to_sheets.py with:
- Input: .tmp/classified_emails.json
- Target: Google Sheet "ManageBac Emails"
- Columns: Date, Subject, Category, Due Date, Link, Status
```

## Outputs
- **Primary**: Google Sheet "ManageBac Emails" with classified data
- **Intermediate**: 
  - `.tmp/emails.json` - Raw email data
  - `.tmp/classified_emails.json` - Classified emails
  - `.tmp/process.log` - Execution log

## Edge Cases

### Email Fetch Failures
- **Issue**: Gmail API rate limit exceeded
- **Solution**: Implement retry with exponential backoff (already in utils.py)
- **Prevention**: Batch requests, use pagination

### Classification Errors
- **Issue**: AI API returns error or unexpected format
- **Solution**: Fallback to keyword-based classification
- **Log**: Save problematic emails to `.tmp/failed_classifications.json`

### Missing Credentials
- **Issue**: `.env` file missing or incomplete
- **Solution**: Script should fail fast with clear error message
- **Action**: User must add credentials before continuing

### Google Sheets Access
- **Issue**: `token.json` expired or missing
- **Solution**: Script initiates OAuth flow to regenerate token
- **Note**: Requires user interaction first time

## Learnings

### [2025-12-11] Initial Setup
- Created directive structure
- Identified need for:
  1. Email fetching with Gmail API
  2. AI classification (likely using OpenAI/Gemini)
  3. Google Sheets export
- Planned modular script architecture

### [DATE] Add your learnings here
As you run this directive, document:
- API quirks discovered
- Rate limits encountered
- Better approaches found
- Common error patterns

---

## Next Steps

To implement this directive:
1. Create the three execution scripts mentioned
2. Set up Gmail API credentials
3. Configure Google Sheets API
4. Test each script independently
5. Run full workflow and document learnings
6. Update this directive with real-world findings
