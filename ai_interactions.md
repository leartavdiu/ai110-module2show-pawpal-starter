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

I manually verified the code by running `python main.py` and `python -m pytest`.

I checked that the CLI output clearly showed priority scheduling, conflict detection, next available slot suggestions, and JSON persistence. I also confirmed that the full test suite passed with 9 tests.

I had to keep the design simpler than some AI suggestions. Some suggestions made the project more complex by adding extra classes or more advanced scheduling models. I decided to keep the final version focused on the four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. I also chose custom dictionary conversion for JSON persistence instead of adding a larger serialization library because it was easier to understand and test.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | ChatGPT | GitHub Copilot in VS Code |
| **Prompt** | Add all optional extensions for PawPal+: next available slot, JSON persistence, priority scheduling, professional UI formatting, and tests. | How would you implement next available slot logic for a pet scheduler that stores tasks with HH:MM time strings? |
| **Response summary** | ChatGPT gave a full multi-file plan. It suggested updates for `pawpal_system.py`, `main.py`, `app.py`, `tests/test_pawpal.py`, `README.md`, and `ai_interactions.md`. | Copilot focused more narrowly on the next available slot idea. It suggested checking existing times and moving forward until an unused time is found. |
| **What was useful** | The response was useful because it connected all the stretch features together and showed how the classes, UI, CLI demo, and tests should work as one system. | The response was useful because it gave a simple way to think about the algorithm: collect the used times, then check later time slots until one is open. |
| **Problems noticed** | Some suggestions were large and needed careful review before pasting, especially because changing the `Task` constructor could break existing tests or UI code. | Copilot’s suggestion was more limited and did not fully connect the algorithm to conflict warnings, tests, or the Streamlit UI. |
| **Decision** | I used ChatGPT’s full structure as the main implementation guide. | I used the Copilot-style idea of checking used times and searching forward in simple time intervals. |

**Which approach did you use in your final implementation and why?**

I used a combined approach. I followed ChatGPT’s broader plan because it helped update the whole project consistently across the backend, CLI demo, Streamlit UI, tests, README, and AI log. For the next available slot algorithm, I kept the simpler idea of checking used times and moving forward in 30-minute intervals. This was easier to understand, easier to test, and matched the project requirements without making the system too complicated.