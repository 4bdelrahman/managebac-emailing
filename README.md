# ManageBac Classifier Email System

This project uses a 3-layer architecture to separate concerns and maximize reliability.

## Architecture Overview

### Layer 1: Directives (`directives/`)
Natural language SOPs that define:
- Goals and objectives
- Required inputs
- Tools/scripts to use
- Expected outputs
- Edge cases and error handling

### Layer 2: Orchestration (AI Agent)
The AI agent (you're reading its work!) handles:
- Reading directives
- Intelligent routing and decision making
- Calling execution tools in the right order
- Error handling and recovery
- Updating directives with learnings

### Layer 3: Execution (`execution/`)
Deterministic Python scripts that:
- Handle API calls
- Process data
- Manage file operations
- Interface with databases
- Provide reliable, testable functionality

## Directory Structure

```
.
├── Agent.md              # AI agent instructions (mirrored as CLAUDE.md, AGENTS.md, GEMINI.md)
├── README.md            # This file
├── .env                 # Environment variables and API keys (not committed)
├── .gitignore           # Git ignore rules
├── directives/          # SOPs and instructions
├── execution/           # Python scripts (deterministic tools)
├── .tmp/                # Intermediate files (never committed, always regenerated)
├── credentials.json     # Google OAuth credentials (not committed)
└── token.json          # Google OAuth token (not committed)
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env` (if available)
   - Add your API keys and credentials to `.env`

3. **Set up Google OAuth (if needed):**
   - Place `credentials.json` in the root directory
   - Run a script that requires Google auth to generate `token.json`

## Key Principles

- **Deliverables** live in the cloud (Google Sheets, Slides, etc.)
- **Intermediates** are temporary files in `.tmp/` that can be regenerated
- **Scripts are deterministic** - the AI orchestrates, but doesn't execute business logic directly
- **Self-annealing** - when errors occur, fix the code, test, and update directives

## Usage

Interact with the AI agent and reference directives in the `directives/` folder. The agent will:
1. Read the relevant directive
2. Determine the right execution script to call
3. Handle errors and edge cases
4. Update directives as it learns

## Contributing

When adding new functionality:
1. Create a directive in `directives/` describing the process
2. Build deterministic scripts in `execution/`
3. Test thoroughly
4. Update directives with learnings and edge cases
