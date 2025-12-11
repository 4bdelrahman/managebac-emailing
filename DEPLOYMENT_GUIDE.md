# ManageBac Email Classifier - Deployment Guide

🎉 **All scripts are ready!** Follow these steps to get your automated email classifier running.

---

## 📋 What Was Built

✅ **5 Python Execution Scripts**
- `execution/gmail_auth.py` - Gmail OAuth authentication
- `execution/fetch_emails.py` - Fetch unprocessed emails  
- `execution/classify_email.py` - AI classification with Groq
- `execution/apply_label.py` - Apply Gmail labels
- `execution/main_classifier.py` - Main orchestrator

✅ **Configuration Files**
- `.env` - All credentials configured
- `requirements.txt` - Updated with Groq SDK
- `client_secret.json` - Moved to root directory

✅ **Documentation**
- `directives/managebac_email_classifier.md` - Complete SOP
- `GITHUB_SECRETS_SETUP.md` - GitHub setup guide
- `DEPLOYMENT_GUIDE.md` - This file

✅ **GitHub Actions**
- `.github/workflows/classify_emails.yml` - Automated workflow (every 12 hours)

---

## 🚀 Deployment Steps

### Step 1: Install Dependencies (5 minutes)

```powershell
pip install -r requirements.txt
```

**What gets installed:**
- Google API libraries (Gmail access)
- Groq Python SDK (AI classification)
- Data processing libraries (pandas, etc.)

---

### Step 2: Generate OAuth Token (5 minutes)

Run the classifier locally to generate `token.json`:

```powershell
python execution/main_classifier.py
```

**What happens:**
1. ✨ Browser window opens automatically
2. 🔐 Log in with: `abdelrhmanahmed.myp1@gmail.com`
3. ✅ Click "Allow" to grant permissions:
   - Read emails
   - Modify labels
4. 🎉 Browser shows "Authentication successful"
5. 📄 `token.json` file created in root directory

**Permissions you're granting:**
- ✅ Read emails from Gmail
- ✅ Modify labels on emails
- ❌ NOT: Send emails, delete emails, or access email content outside this app

---

### Step 3: Verify Local Execution (2 minutes)

The script should now run and classify emails!

**Expected output:**
```
============================================================
Starting ManageBac Email Classifier
Timestamp: 2025-12-11 16:30:00
============================================================
Step 1: Authenticating with Gmail...
✅ Gmail authentication successful
Step 2: Getting/creating label 'ManageBac'...
✅ Created label 'ManageBac' with ID: Label_123
Step 3: Fetching up to 50 unprocessed emails...
Found 5 emails to process

============================================================
Processing email 1/5
============================================================
From: noreply@managebac.com
Subject: New assignment posted in Math HL
✅ LABELED as ManageBac

... [processing continues] ...

============================================================
WORKFLOW COMPLETE
============================================================
Total emails processed: 5
  ✅ Labeled as ManageBac: 3
  ⏭️  Not ManageBac: 2
  ❌ Errors: 0
Duration: 12.34 seconds
============================================================

🎉 Successfully labeled 3 ManageBac emails!
```

---

### Step 4: Push to GitHub (5 minutes)

Initialize Git and push to your repository:

```powershell
# Initialize Git (if not already)
git init

# Add all files (excluding .env, token.json, client_secret.json - they're in .gitignore)
git add .

# Commit
git commit -m "Add ManageBac email classifier workflow"

# Add remote
git remote add origin https://github.com/4bdelrahman/Managebac-email-reciever.git

# Push
git push -u origin main
```

---

### Step 5: Configure GitHub Secrets (10 minutes)

#### Navigate to Repository Settings
1. Go to: https://github.com/4bdelrahman/Managebac-email-reciever
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

#### Add 4 Secrets:

##### 1️⃣ GMAIL_CREDENTIALS
```powershell
# Copy client_secret.json contents
Get-Content client_secret.json | Set-Clipboard
```
- **Name**: `GMAIL_CREDENTIALS`
- **Value**: Paste the copied JSON

##### 2️⃣ GMAIL_TOKEN  
```powershell
# Copy token.json contents
Get-Content token.json | Set-Clipboard
```
- **Name**: `GMAIL_TOKEN`
- **Value**: Paste the copied JSON

##### 3️⃣ GMAIL_EMAIL
- **Name**: `GMAIL_EMAIL`
- **Value**: `abdelrhmanahmed.myp1@gmail.com`

##### 4️⃣ GROQ_API_KEY
- **Name**: `GROQ_API_KEY`
- **Value**: `your_groq_api_key_here` (use the key you were provided)

---

### Step 6: Test GitHub Actions (3 minutes)

#### Manual Test Run
1. Go to **Actions** tab in your repository
2. Click **Classify ManageBac Emails** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait ~2-3 minutes for completion
5. ✅ Check logs - should show "WORKFLOW COMPLETE"

---

### Step 7: Verify in Gmail (2 minutes)

1. Open Gmail: https://mail.google.com
2. Look for **"ManageBac"** label in left sidebar
3. Click the label to see classified emails
4. Verify ManageBac-related emails are labeled correctly

---

## ✅ Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `token.json` generated (ran locally with browser auth)
- [ ] Local execution successful (emails classified)
- [ ] Code pushed to GitHub
- [ ] All 4 GitHub Secrets configured
- [ ] GitHub Actions test run successful
- [ ] ManageBac label visible in Gmail
- [ ] Emails correctly classified

---

## 🔄 Automatic Schedule

The workflow will now run automatically:

- **Every 12 hours** at 00:00 and 12:00 UTC
- **Egypt Time**: 02:00 and 14:00 (standard) / 03:00 and 15:00 (summer)
- **Processes up to**: 50 emails per run
- **Checks emails from**: Last 24 hours

---

## 📊 Monitoring

### View Workflow Runs
- GitHub → **Actions** tab → **Classify ManageBac Emails**
- See all past runs, statuses, and logs

### Check Logs
Logs are saved in `.tmp/` directory (when running locally):
- `main_classifier.log` - Main workflow logs
- `classify_email.log` - AI classification details
- `fetch_emails.log` - Email fetching logs
- `apply_label.log` - Label application logs

---

## 🐛 Troubleshooting

### "Module not found: groq"
```powershell
pip install groq
```

### "Token expired" error
1. Delete `token.json`
2. Run `python execution/main_classifier.py`
3. Re-authorize in browser
4. Update GitHub Secret `GMAIL_TOKEN` with new token

### "No emails found"
- ✅ Normal! Means no unprocessed emails in last 24 hours
- Check query in `fetch_emails.py`: `in:inbox -label:ManageBac newer_than:1d`

### GitHub Actions fails
1. Check all 4 secrets are set correctly
2. Verify secret values don't have extra spaces
3. Check workflow logs for specific error messages

---

## 🎯 Next Steps

Now that it's running:

1. **Monitor first few runs** - Check classifications are accurate
2. **Adjust AI prompt** - If needed, edit `classify_email.py`
3. **Change schedule** - Edit `.github/workflows/classify_emails.yml`
4. **Add sub-labels** - Categorize by assignment types, CAS activities, etc.
5. **Build more workflows** - Use this as a template!

---

## 📞 Support

Need help?
- **Check logs** in GitHub Actions
- **Review directive** in `directives/managebac_email_classifier.md`
- **Test locally** first: `python execution/main_classifier.py`

---

## 🎉 You're Done!

Your ManageBac emails will now be automatically classified every 12 hours!

**Congratulations!** 🚀

---

Built with the 3-layer architecture:
- **Layer 1 (Directives)**: `directives/managebac_email_classifier.md`
- **Layer 2 (Orchestration)**: AI Agent (me!)
- **Layer 3 (Execution)**: Python scripts in `execution/`

The system will learn and improve over time. Document any learnings in the directive!
