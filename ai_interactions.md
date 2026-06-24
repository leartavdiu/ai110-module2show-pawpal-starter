# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI assistant to help extend PawPal+ with several stretch features. The goal was to add a next available slot algorithm, data persistence with JSON, priority-based scheduling, improved Streamlit UI formatting, and stronger tests for the new behavior.

**What did the agent do?**

The agent helped plan and generate updates across several files:

- `pawpal_system.py`
  - Added `priority` to the `Task` class.
  - Added JSON conversion methods like `to_dict()` and `from_dict()` for `Task`, `Pet`, and `Owner`.
  - Added `Owner.save_to_json()` and `Owner.load_from_json()` for persistence.
  - Added `Scheduler.sort_by_priority()` for priority-based scheduling.
  - Added `Scheduler.next_available_slot()` to suggest an open time after a conflict.
  - Updated conflict detection to include a suggested next available slot.

- `main.py`
  - Updated the CLI demo to show priority scheduling.
  - Added a conflict example.
  - Added output showing the next available slot.
  - Added save/load behavior using `data.json`.

- `app.py`
  - Updated the Streamlit UI to use the smart `Scheduler` methods.
  - Added priority selection when creating tasks.
  - Added schedule tables with clearer formatting.
  - Added warning messages for conflicts.
  - Added success messages for completed tasks and saved data.
  - Added a next available slot tool.
  - Added persistence so the app loads from and saves to `data.json`.

- `tests/test_pawpal.py`
  - Added tests for priority sorting.
  - Added tests for next available slot logic.
  - Added tests for JSON save/load persistence.
  - Kept existing tests for task completion, task addition, sorting, recurrence, and conflict detection.

- `README.md`
  - Added descriptions of the optional extensions.
  - Added testing instructions and sample passing test output.
  - Added CLI output examples.
  - Added a smarter scheduling table.
  - Added documentation for persistence and UI formatting features.

**What did you have to verify or fix manually?**

I manually verified the code by running:

```bash
python main.py
python -m pytest