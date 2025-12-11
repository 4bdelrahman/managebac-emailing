# Directives

This folder contains SOPs (Standard Operating Procedures) written in natural language Markdown.

## What is a Directive?

A directive defines **what to do** without worrying about **how to do it**. Think of them as instructions you'd give to a competent mid-level employee.

## Directive Template

Each directive should include:

### 1. **Goal**
What are we trying to accomplish?

### 2. **Inputs**
What information/data do we need to start?

### 3. **Tools/Scripts**
Which execution scripts should be used? (e.g., `execution/scrape_single_site.py`)

### 4. **Process**
Step-by-step instructions on how to accomplish the goal.

### 5. **Outputs**
What should be produced? Where should it be delivered?

### 6. **Edge Cases**
- What can go wrong?
- How should errors be handled?
- API limits, timing constraints, etc.

### 7. **Learnings**
Document what you've learned from running this directive:
- API constraints discovered
- Better approaches found
- Common errors and their solutions

## Example Directive Structure

```markdown
# Scrape Website Data

## Goal
Extract company information from a list of websites.

## Inputs
- List of URLs (from Google Sheet: "Leads Database")
- Column names to extract: name, email, phone

## Tools
- `execution/scrape_single_site.py`

## Process
1. Load URLs from Google Sheet
2. For each URL:
   - Run scrape_single_site.py
   - Extract specified fields
   - Handle timeouts (retry 3x with exponential backoff)
3. Write results to Google Sheet "Scraped Data"

## Outputs
- Updated Google Sheet with scraped data
- Error log in .tmp/scrape_errors.log

## Edge Cases
- Website blocks scraper → Use rotating user agents
- Timeout after 30s → Retry with longer timeout
- Invalid URL → Log error, continue with next

## Learnings
- [2024-12-11] Some sites require JavaScript → Add Playwright option
- [2024-12-11] Rate limit: max 10 requests/minute → Add delay between requests
```

## Best Practices

1. **Keep it simple** - Write in natural language
2. **Be specific** - Include actual file names, column names, etc.
3. **Document learnings** - Update directives when you discover edge cases
4. **Reference execution scripts** - Don't duplicate code logic here
5. **Living documents** - Directives evolve as the system learns
