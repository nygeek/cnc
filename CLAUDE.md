
You are an AI assistant that helps users develop software features using the responsible-vibe-mcp server.

IMPORTANT: Call whats_next() after each user message to get phase-specific instructions and maintain the development workflow.

Each tool call returns a JSON response with an "instructions" field. Follow these instructions immediately after you receive them.

Use the development plan which you will retrieve via whats_next() to record important insights and decisions as per the structure of the plan.

Do not use your own task management tools.

## Project Execution Rules

### Always Use Make Targets
- NEVER run Python scripts directly (e.g., `python cnc_gui.py`)
- ALWAYS use Makefile targets (e.g., `make gui`, `make screenshot`, `make compare`)
- This ensures consistent execution environment and dependencies

### Always Use Virtual Environment
- ALL Python commands must run through `.venv/bin/python`
- If running Python directly (when no make target exists), use `.venv/bin/python script.py`
- Never use system Python or bare `python` command

### Common Make Targets
- `make build` - Set up venv and install dependencies
- `make gui` - Launch the GUI calculator
- `make screenshot` - Capture GUI screenshot
- `make compare` - Compare screenshot with reference image
- `make test-gui` - Full automated testing workflow
- `make test` - Run calculator tests
- `make clean` - Clean build artifacts