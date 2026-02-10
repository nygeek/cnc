# Development Plan: cnc (feature/quaternion-octonion-support branch)

*Generated on 2026-02-09 by Vibe Feature MCP*
*Workflow: [minor](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/minor)*

## Goal
Improve the Makefile to support "build", "install", and "clean" targets that automatically manage Python virtual environment creation and cleanup

## Explore
<!-- beads-phase-id: cnc-2.1 -->
### Tasks

*Tasks managed via `bd` CLI*

## Implement
<!-- beads-phase-id: cnc-2.2 -->

### Phase Entrance Criteria:
- [x] Current Makefile has been analyzed
- [x] Project structure and dependencies (requirements.txt, setup.py, etc.) are understood
- [x] Design decisions for venv management strategy are documented
- [x] Target behavior for build, install, and clean is clearly defined

### Tasks

*Tasks managed via `bd` CLI*

## Finalize
<!-- beads-phase-id: cnc-2.3 -->

### Phase Entrance Criteria:
- [x] New Makefile targets (build, install, clean) have been implemented
- [x] Venv creation and cleanup logic is working correctly
- [x] All targets have been manually tested
- [x] Code follows project conventions

### Tasks

*Tasks managed via `bd` CLI*

## Key Decisions

### Current State Analysis
- Project uses pyproject.toml (setuptools-based) with no requirements.txt
- Existing install target references `.venv/bin/python` but doesn't create the venv
- Current clean target only removes *.ps and *.pdf files
- Install creates wrapper scripts (cnc and cnc10) in ~/bin

### Design Decisions
- **Build target**: Create venv if not exists, install project dependencies using `pip install -e .`
- **Install target**: Depend on build, create wrapper scripts in ~/bin (keep existing behavior)
- **Clean target**: Remove venv directory, generated files (*.ps, *.pdf), and wrapper scripts
- Use `python3 -m venv .venv` for venv creation (consistent with existing reference)
- Install project in editable mode (`-e`) for development convenience

## Notes

### Testing Results
- Build target successfully creates venv and installs project in editable mode
- Build is idempotent (can be run multiple times safely)
- Install target correctly depends on build and creates wrapper scripts in ~/bin
- Clean target removes venv, wrapper scripts, and generated files without errors
- All targets tested and working correctly

---
*This plan is maintained by the LLM and uses beads CLI for task management. Tool responses provide guidance on which bd commands to use for task management.*
