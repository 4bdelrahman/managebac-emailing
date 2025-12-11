# ManageBac Email Classifier

## Goal
Automatically identify and label ManageBac-related emails in Gmail using AI classification. The workflow runs every 12 hours via GitHub Actions to keep your inbox organized.

## Inputs

### Credentials (from `.env`)
- `GMAIL_EMAIL` - Gmail account to monitor
- `GMAIL_CREDENTIALS_FILE` - OAuth credentials file (client_secret.json)
- `GROQ_API_KEY` - Groq AI API key for classification
- `GROQ_MODEL` - AI model name (openai/gpt-oss-120b)
- `MANAGEBAC_LABEL_NAME` - Label name to apply (ManageBac)

### Required Files
- `client_secret.json` - Google OAuth credentials
- `token.json` - User authorization token (generated on first run)

## Tools

### Execution Scripts
- `execution/gmail_auth.py` - Gmail OAuth authentication
- `execution/fetch_emails.py` - Fetch unprocessed emails
- `execution/classify_email.py` - Classify emails with Groq AI
- `execution/apply_label.py` - Apply Gmail labels
- `execution/main_classifier.py` - Main orchestrator

## Process

### Workflow Steps

```
1. AUTHENTICATE
   ├─ Load credentials from client_secret.json
   ├─ Check if token.json exists and is valid
   ├─ Refresh token if expired
   └─ Return authenticated Gmail service

2. GET/CREATE LABEL
   ├─ List all existing Gmail labels
   ├─ Check if "ManageBac" label exists
   └─ Create label if it doesn't exist

3. FETCH UNPROCESSED EMAILS
   ├─ Query: in:inbox -label:ManageBac newer_than:1d
   ├─ Limit: 50 emails per run
   └─ Return list of email IDs

4. FOR EACH EMAIL:
   ├─ Extract email content (subject, sender, body)
   ├─ Build AI classification prompt
   ├─ Call Groq AI with GPT-OSS 120B
   ├─ Parse response (YES/NO)
   ├─ If YES: Apply ManageBac label
   └─ If NO: Skip email

5. LOG RESULTS
   ├─ Total emails processed
   ├─ Number labeled as ManageBac
   ├─ Number skipped
   ├─ Number of errors
   └─ Total duration
```

### GitHub Actions Schedule
- **Trigger**: Every 12 hours (00:00 and 12:00 UTC)
- **Manual**: Can be triggered manually via workflow_dispatch

## Outputs

### Primary
- **Gmail Labels**: ManageBac label applied to relevant emails
- **Organized Inbox**: Easy filtering by label

### Intermediate
- `.tmp/main_classifier.log` - Execution logs
- `.tmp/classify_email.log` - AI classification logs
- `.tmp/fetch_emails.log` - Email fetching logs
- `.tmp/apply_label.log` - Label application logs

## Edge Cases

### Email Fetch Failures

**Issue**: Gmail API rate limit exceeded
- **Solution**: Workflow only runs every 12 hours (well within limits)
- **Prevention**: Limit to 50 emails per run
- **Retry**: Exponential backoff implemented in utils.py

**Issue**: No new emails to process
- **Solution**: Workflow completes gracefully with "No unprocessed emails" message
- **Action**: No changes made, just logs the status

### Classification Errors

**Issue**: Groq AI API returns error or rate limit
- **Solution**: 3 retry attempts with exponential backoff
- **Fallback**: Keyword-based classification if AI fails
- **Keywords**: managebac, cas, tok, assignment, grade, due date, etc.

**Issue**: Unexpected AI response format
- **Solution**: Parse for YES/NO keywords, default to NO if unclear
- **Log**: Warning logged with actual response

### Authentication Failures

**Issue**: token.json expired
- **Solution**: Auto-refresh token using refresh_token
- **GitHub Actions**: Token stored in GitHub Secrets, refreshed automatically

**Issue**: client_secret.json missing
- **Solution**: Script fails fast with clear error message
- **Action**: User must add credentials before continuing

**Issue**: OAuth scope insufficient
- **Solution**: Use gmail.modify and gmail.labels scopes (already configured)

### Label Application Errors

**Issue**: Label doesn't exist
- **Solution**: Automatically create label if missing
- **Visibility**: Label set to visible in sidebar and message list

**Issue**: Cannot modify email (read-only access)
- **Solution**: gmail.modify scope grants write access
- **Log**: Error logged, email skipped, workflow continues

## Learnings

### [2025-12-11] Initial Setup
- **Architecture**: 3-layer system with directives, orchestration, and execution
- **AI Model**: Groq GPT-OSS 120B provides fast, accurate classification
- **Fallback**: Keyword-based classification ensures reliability
- **Scopes**: gmail.modify + gmail.labels required for full functionality
- **Query Optimization**: newer_than:1d reduces API calls and processing time

### [2025-12-11] GitHub Actions Configuration
- **Secrets Required**:
  - GMAIL_CREDENTIALS (client_secret.json contents)
  - GMAIL_TOKEN (token.json contents)
  - GMAIL_EMAIL (user email)
  - GROQ_API_KEY (Groq API key)
- **Schedule**: `0 */12 * * *` = Every 12 hours at :00 minutes
- **Python Version**: 3.11 for best compatibility

### [2025-12-11] Performance Considerations
- **Batch Size**: 50 emails per run balances thoroughness with speed
- **AI Calls**: ~1 second per email (Groq is very fast)
- **Total Runtime**: Typically 1-2 minutes for 50 emails
- **API Costs**: Groq pricing is competitive (check current rates)

---

## Common Issues & Solutions

### Issue: "Token expired"
**Solution**: Token automatically refreshes. If GitHub Actions fails, regenerate token.json locally and update GitHub Secret.

### Issue: "No emails found"
**Solution**: Normal! Means no new emails in last 24 hours without ManageBac label.

### Issue: "API rate limit"
**Solution**: Wait and retry. Groq has generous limits for this use case.

### Issue: "Classification accuracy low"
**Solution**: 
1. Check email samples in logs
2. Adjust classification prompt in classify_email.py
3. Add more keywords to fallback classification

---

## Monitoring & Maintenance

### Check Workflow Status
- Visit GitHub Actions tab in repository
- View workflow runs and logs
- Check for errors or failures

### Review Classifications
- Gmail: Check emails under ManageBac label
- If misclassified: Refine AI prompt or keywords
- If missed: Check logs for errors

### Update Schedule
Edit `.github/workflows/classify_emails.yml`:
```yaml
schedule:
  - cron: '0 */12 * * *'  # Change to desired frequency
```

---

## Future Improvements

### Potential Enhancements
1. **Email Categorization**: Sub-labels for Assignments, Grades, CAS, etc.
2. **Summary Digest**: Weekly email summary of ManageBac activity
3. **Auto-Archive**: Archive old ManageBac emails after X days
4. **Smart Notifications**: Only notify for urgent/due-soon items
5. **Multi-Account**: Support multiple Gmail accounts

### Performance Optimizations
1. **Caching**: Cache classification results to avoid re-processing
2. **Parallel Processing**: Process multiple emails concurrently
3. **Incremental Updates**: Track last processed timestamp

---

## Next Steps After Deployment

1. **Monitor First Run**: Check GitHub Actions logs for errors
2. **Verify Labels**: Confirm ManageBac emails are labeled correctly
3. **Adjust Frequency**: Increase/decrease schedule if needed
4. **Update Directive**: Document any learnings or edge cases
5. **Share**: Use this system as template for other email workflows!
