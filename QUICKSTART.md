# Quick Start Guide

Welcome to your 3-layer architecture system! This guide will help you get started quickly.

## 📋 What Just Happened?

The environment has been initialized with:

```
✓ directives/       - Your instruction SOPs
✓ execution/        - Python automation scripts  
✓ .tmp/             - Temporary files
✓ .env              - API keys and secrets
✓ .gitignore        - Protect sensitive files
✓ requirements.txt  - Python dependencies
```

## 🚀 Getting Started

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

For Playwright (if you need web automation):
```powershell
playwright install
```

### 2. Configure Your Environment

Edit `.env` and add your credentials:

```env
# Example - add your actual keys
OPENAI_API_KEY=sk-your-key-here
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
GOOGLE_SHEETS_ID=your-sheet-id-here
```

### 3. Set Up Google APIs (if needed)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API and Google Sheets API
4. Create OAuth 2.0 credentials
5. Download credentials as `credentials.json` to the root directory
6. Run any script that uses Google APIs - it will generate `token.json`

## 📝 How to Use This System

### As a User
Simply tell the AI agent what you want to accomplish:

> "I need to classify my ManageBac emails and organize them in a Google Sheet"

The AI will:
1. Check for existing directives
2. Create/update directives as needed
3. Build execution scripts
4. Run the workflow
5. Handle errors and learn from them

### As the AI Agent (Reading This?)

Follow the 3-layer architecture:

1. **Read directives** in `directives/` for instructions
2. **Call execution scripts** in `execution/` to do the work
3. **Handle errors** gracefully and update directives with learnings
4. **Store intermediate files** in `.tmp/`
5. **Deliver results** to cloud services (Google Sheets, etc.)

## 📂 File Structure

```
Your Project/
│
├── Agent.md                    # AI agent instructions
├── README.md                   # Project overview
├── QUICKSTART.md              # This file
├── requirements.txt           # Python dependencies
├── .env                       # Your API keys (DO NOT COMMIT)
├── .gitignore                 # Protects sensitive files
│
├── directives/                # What to do (SOPs)
│   ├── README.md             # Directive guidelines
│   └── example_managebac_email_processing.md
│
├── execution/                 # How to do it (Scripts)
│   ├── README.md             # Script guidelines  
│   └── utils.py              # Common utilities
│
└── .tmp/                      # Temporary files
    ├── README.md             # Temp file info
    └── *.log, *.json, etc.   # Generated files
```

## 🎯 Example Workflow

### Scenario: Classify ManageBac Emails

1. **Create a directive** (or tell the AI to):
   ```
   directives/classify_managebac_emails.md
   ```

2. **Build execution scripts**:
   ```
   execution/fetch_emails.py
   execution/classify_email.py
   execution/export_to_sheets.py
   ```

3. **Run the workflow**:
   - AI reads the directive
   - AI calls scripts in order
   - Scripts use `.env` for credentials
   - Intermediate data saved to `.tmp/`
   - Final results go to Google Sheets

4. **Handle errors**:
   - Script fails? AI fixes it
   - API limit hit? AI updates directive with the constraint
   - Better approach found? AI documents it in directive

5. **System improves**:
   - Next time it runs smoother
   - Edge cases are handled
   - Knowledge is preserved

## 🔧 Common Commands

### Test a script
```powershell
python execution/your_script.py
```

### View logs
```powershell
Get-Content .tmp/app.log -Tail 50
```

### Clean temporary files
```powershell
Remove-Item .tmp/* -Recurse -Force -Exclude README.md
```

### Install new dependency
```powershell
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

## ⚠️ Important Reminders

1. **Never commit** `.env`, `credentials.json`, or `token.json`
2. **Intermediate files** in `.tmp/` are always regenerable
3. **Final deliverables** should go to cloud services
4. **Update directives** when you learn something new
5. **Test scripts independently** before using in workflows

## 🎓 Learning Resources

- **Directives**: See `directives/README.md` for how to write SOPs
- **Scripts**: See `execution/README.md` for coding guidelines
- **Utils**: Check `execution/utils.py` for helper functions
- **Agent Instructions**: Read `Agent.md` to understand the AI's role

## 🐛 Troubleshooting

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Environment variable not found"
Check your `.env` file has all required keys

### "Google auth failed"
Delete `token.json` and re-authenticate

### Script errors
Check logs in `.tmp/` directory

## 🎉 You're Ready!

The system is now initialized and ready to use. Start by:

1. **Adding your API keys** to `.env`
2. **Telling the AI** what you want to accomplish
3. **Let the system work** - the AI will handle the rest

Remember: This system learns and improves over time. The more you use it, the smarter it gets!

---

Need help? Just ask the AI agent! 🤖
