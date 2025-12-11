# GitHub Secrets Setup Guide

This document explains how to set up the required GitHub Secrets for the ManageBac Email Classifier workflow.

## Required Secrets

You need to add **4 secrets** to your GitHub repository:

| Secret Name | Description | How to Get It |
|-------------|-------------|---------------|
| `GMAIL_CREDENTIALS` | Google OAuth client credentials | Copy entire contents of `client_secret.json` |
| `GMAIL_TOKEN` | User authorization token | Generate by running script locally (see below) |
| `GMAIL_EMAIL` | Your Gmail address | `abdelrhmanahmed.myp1@gmail.com` |
| `GROQ_API_KEY` | Groq AI API key | Already provided |

---

## Step-by-Step Setup

### 1. Generate `token.json` (First Time Only)

Before adding secrets, you need to generate `token.json` by running the classifier locally:

```powershell
# Install dependencies
pip install -r requirements.txt

# Run the main script
python execution/main_classifier.py
```

**What happens:**
1. A browser window opens
2. Log in to your Google account (`abdelrhmanahmed.myp1@gmail.com`)
3. Click "Allow" to grant permissions
4. Browser shows "Authentication successful"
5. A `token.json` file is created in the root directory

---

### 2. Add Secrets to GitHub

#### Navigate to Repository Settings
1. Go to your repository: https://github.com/4bdelrahman/Managebac-email-reciever
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

#### Add Each Secret

##### Secret 1: `GMAIL_CREDENTIALS`
- **Name**: `GMAIL_CREDENTIALS`
- **Value**: Copy and paste the **entire contents** of `client_secret.json`

```powershell
# View file contents (Windows)
Get-Content client_secret.json | Set-Clipboard
```

Then paste into GitHub Secret value field.

---

##### Secret 2: `GMAIL_TOKEN`
- **Name**: `GMAIL_TOKEN`
- **Value**: Copy and paste the **entire contents** of `token.json`

```powershell
# View file contents (Windows)
Get-Content token.json | Set-Clipboard
```

Then paste into GitHub Secret value field.

---

##### Secret 3: `GMAIL_EMAIL`
- **Name**: `GMAIL_EMAIL`
- **Value**: `abdelrhmanahmed.myp1@gmail.com`

---

##### Secret 4: `GROQ_API_KEY`
- **Name**: `GROQ_API_KEY`
- **Value**: `your_groq_api_key_here` (use the key you were provided)

---

## Verification

After adding all 4 secrets, you should see them listed in **Settings → Secrets and variables → Actions**:

```
✅ GMAIL_CREDENTIALS
✅ GMAIL_TOKEN
✅ GMAIL_EMAIL
✅ GROQ_API_KEY
```

---

## Testing the Workflow

### Manual Trigger Test

1. Go to **Actions** tab in your repository
2. Click **Classify ManageBac Emails** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for the workflow to complete
5. Check logs for any errors

### Automatic Schedule

The workflow runs automatically every 12 hours at:
- **00:00 UTC** (02:00 Egypt time / 03:00 in summer)
- **12:00 UTC** (14:00 Egypt time / 15:00 in summer)

---

## Troubleshooting

### Error: "Invalid credentials"
- **Cause**: `GMAIL_CREDENTIALS` secret is malformed
- **Solution**: Copy the entire JSON from `client_secret.json` including `{` and `}`

### Error: "Token expired"
- **Cause**: `token.json` is old or invalid
- **Solution**: 
  1. Delete local `token.json`
  2. Run `python execution/main_classifier.py` locally
  3. Re-authorize in browser
  4. Update `GMAIL_TOKEN` secret with new token

### Error: "Module not found"
- **Cause**: Dependencies not installed
- **Solution**: Check that `requirements.txt` is in the root directory

### Workflow doesn't run on schedule
- **Cause**: GitHub Actions disabled or repository is private without paid plan
- **Solution**: Ensure repository has Actions enabled and is public OR has GitHub Actions minutes

---

## Security Notes

### ⚠️ Keep Secrets Secret!
- Never commit `client_secret.json` or `token.json` to Git
- Never share your secrets in issues or pull requests
- GitHub Secrets are encrypted and only visible to repository admins

### 🔒 Token Permissions
The token grants access to:
- Read emails from Gmail
- Modify labels on emails
- **Does NOT allow**: Sending emails, deleting emails, reading email content outside this workflow

### 🔄 Token Refresh
- Tokens are automatically refreshed by Google
- If token becomes invalid, re-run local authentication
- Update GitHub Secret with new token

---

## Questions?

If you encounter issues:
1. Check GitHub Actions logs for detailed error messages
2. Test locally first: `python execution/main_classifier.py`
3. Verify all 4 secrets are set correctly
4. Check that secret values don't have extra spaces or newlines

---

**Ready!** Once all secrets are configured, the workflow will run automatically every 12 hours! 🎉
