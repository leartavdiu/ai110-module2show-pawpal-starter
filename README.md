# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

* Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
* Consider constraints (time available, priority, owner preferences)
* Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

* Let a user enter basic owner + pet info
* Let a user add/edit tasks with frequency and priority
* Generate a daily schedule/plan based on constraints and priorities
* Display the plan clearly and explain important scheduling behavior
* Include tests for the most important scheduling behaviors
* Include optional extensions such as persistence, priority scheduling, conflict warnings, and next available slot suggestions

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Streamlit app

```bash
streamlit run app.py
```

### Run the CLI demo

```bash
python main.py
```

### Run the tests

```bash
python -m pytest
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram with classes, attributes, methods, and relationships.
3. Convert UML into Python class stubs.
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect the logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches the final implementation.

## 🖥️ Sample Output

Here is sample CLI output from running `python main.py`:

```text
Today's Priority Schedule
-------------------------
08:00 - Luna (cat): Morning medicine [daily] priority High due 2026-06-23 - Not done
09:00 - Mochi (dog): Breakfast feeding [daily] priority High due 2026-06-23 - Not done
08:00 - Mochi (dog): Morning walk [daily] priority Medium due 2026-06-23 - Not done
10:30 - Luna (cat): Clean litter box [daily] priority Low due 2026-06-23 - Not done
18:00 - Luna (cat): Evening play time [daily] priority Low due 2026-06-23 - Not done

Schedule Sorted Only By Time
----------------------------
08:00 - Mochi: Morning walk priority Medium
08:00 - Luna: Morning medicine priority High
09:00 - Mochi: Breakfast feeding priority High
10:30 - Luna: Clean litter box priority Low
18:00 - Luna: Evening play time priority Low

Incomplete Tasks
----------------
Mochi: Breakfast feeding at 09:00
Mochi: Morning walk at 08:00
Luna: Clean litter box at 10:30
Luna: Evening play time at 18:00
Luna: Morning medicine at 08:00

Mochi's Tasks
----------------
Mochi: Breakfast feeding at 09:00
Mochi: Morning walk at 08:00

Conflict Warnings Before Completing Task
---------------------------------------
Conflict at 08:00 on 2026-06-23: Mochi has 'Morning walk' and Luna has 'Morning medicine'. Suggested next available slot: 08:30.

Next Available Slot After 08:00
-------------------------------
08:30

Saving data to data.json...

Loading data from data.json...

Loaded Schedule
---------------
08:00 - Luna: Morning medicine priority High
09:00 - Mochi: Breakfast feeding priority High
08:00 - Mochi: Morning walk priority Medium
10:30 - Luna: Clean litter box priority Low
18:00 - Luna: Evening play time priority Low

Completing Morning walk...

Updated Priority Schedule
-------------------------
08:00 - Luna (cat): Morning medicine [daily] priority High due 2026-06-23 - Not done
09:00 - Mochi (dog): Breakfast feeding [daily] priority High due 2026-06-23 - Not done
08:00 - Mochi (dog): Morning walk [daily] priority Medium due 2026-06-23 - Done
08:00 - Mochi (dog): Morning walk [daily] priority Medium due 2026-06-24 - Not done
10:30 - Luna (cat): Clean litter box [daily] priority Low due 2026-06-23 - Not done
18:00 - Luna (cat): Evening play time [daily] priority Low due 2026-06-23 - Not done

Conflict Warnings After Completing Task
--------------------------------------
No conflicts found.
```

## 🧪 Testing PawPal+

To run the automated test suite:

```bash
python -m pytest
```

The tests verify the most important backend behaviors:

* Marking a task complete
* Adding a task to a pet
* Sorting tasks in chronological order
* Creating the next daily recurring task
* Detecting scheduling conflicts
* Handling a pet with no tasks
* Sorting tasks by priority
* Finding the next available time slot
* Saving and loading data with JSON persistence

Sample successful test output:

```text
==================================================================== test session starts =====================================================================
platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
rootdir: /Users/leartavdiu/Downloads/ai110-module2show-pawpal-starter-main
plugins: anyio-4.10.0
collected 9 items                                                                                                                                            

tests/test_pawpal.py .........                                                                                                                         [100%]

===================================================================== 9 passed in 0.02s =====================================================================
```

Confidence Level: ⭐⭐⭐⭐☆

I am mostly confident that the system works for the main scheduling behaviors because the CLI demo runs correctly and all automated tests pass. I would still add more edge case tests in the future for invalid time formats, duplicate pet names, and overlapping task durations.

## 📐 Smarter Scheduling

| Feature             | Method(s)                                                            | Notes                                                                        |
| ------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Task sorting        | `Scheduler.sort_by_time()`                                           | Sorts tasks by their `time` value in HH:MM format.                           |
| Priority sorting    | `Scheduler.sort_by_priority()`                                       | Sorts tasks by priority first, then by time.                                 |
| Filtering           | `Scheduler.filter_tasks()`                                           | Filters tasks by pet name or completion status.                              |
| Conflict handling   | `Scheduler.detect_conflicts()`                                       | Checks for exact time matches and returns warning messages.                  |
| Next available slot | `Scheduler.next_available_slot()`                                    | Suggests the next open time slot after a conflict.                           |
| Recurring tasks     | `Task.create_next_occurrence()` and `Scheduler.mark_task_complete()` | Creates a new daily or weekly task when a recurring task is marked complete. |
| Data persistence    | `Owner.save_to_json()` and `Owner.load_from_json()`                  | Saves and loads owner, pet, and task data using `data.json`.                 |

## Optional Extensions

### Challenge 1: Advanced Algorithmic Capability

I added a next available slot algorithm. When two incomplete tasks are scheduled at the same time on the same due date, the Scheduler can suggest the next open time slot.

Method added:

* `Scheduler.next_available_slot()`

Example:

```text
Conflict at 08:00 on 2026-06-23: Mochi has 'Morning walk' and Luna has 'Morning medicine'. Suggested next available slot: 08:30.
```

### Challenge 2: Data Persistence

I added data persistence so PawPal+ can remember pets and tasks between app runs. The system saves owner, pet, and task data to a `data.json` file using custom dictionary conversion methods.

Methods added:

* `Task.to_dict()`
* `Task.from_dict()`
* `Pet.to_dict()`
* `Pet.from_dict()`
* `Owner.to_dict()`
* `Owner.from_dict()`
* `Owner.save_to_json()`
* `Owner.load_from_json()`

Persistence workflow:

1. When the app starts, it checks if `data.json` exists.
2. If the file exists, the app loads the saved owner, pets, and tasks.
3. If the file does not exist, the app creates a new default owner.
4. When the user adds a pet, adds a task, saves the owner, or marks a task complete, the app saves the updated data to `data.json`.

Files modified:

* `pawpal_system.py`
* `app.py`
* `tests/test_pawpal.py`
* `README.md`

### Challenge 3: Advanced Priority Scheduling

I added priority-based scheduling. Each task now has a priority level: High, Medium, or Low. The Scheduler uses `Scheduler.sort_by_priority()` to organize tasks by priority first and time second. This means important tasks, like medicine or feeding, appear before lower priority tasks, even if a lower priority task happens earlier in the day.

Methods added or updated:

* `Task.priority`
* `Scheduler.sort_by_priority()`
* `Scheduler.get_schedule()`

Example priority schedule:

```text
Today's Priority Schedule
-------------------------
08:00 - Luna (cat): Morning medicine [daily] priority High due 2026-06-23 - Not done
09:00 - Mochi (dog): Breakfast feeding [daily] priority High due 2026-06-23 - Not done
08:00 - Mochi (dog): Morning walk [daily] priority Medium due 2026-06-23 - Not done
10:30 - Luna (cat): Clean litter box [daily] priority Low due 2026-06-23 - Not done
18:00 - Luna (cat): Evening play time [daily] priority Low due 2026-06-23 - Not done
```

### Challenge 4: Professional UI and Output Formatting

I improved the Streamlit UI with clearer tables, emoji-based priority labels, completion status indicators, success messages, warning messages, and a next available slot tool.

Formatting features added:

* `st.table()` for structured pet and schedule displays
* `st.warning()` for conflict warnings
* `st.success()` for saved data, completed tasks, and no-conflict messages
* Priority labels like 🔴 High, 🟡 Medium, and 🟢 Low
* Status labels like ✅ Done and ⏳ Not done

### Challenge 5: Multi-Model Prompt Comparison

I compared AI suggestions for the scheduling logic. I used ChatGPT for the main implementation plan and GitHub Copilot in VS Code for an alternate idea on next available slot logic. I kept the final design simple by using a readable loop that checks 30-minute time intervals.

## 📸 Demo Walkthrough

1. The user opens the Streamlit app and enters the owner name.
2. The user adds one or more pets, such as Mochi the dog or Luna the cat.
3. The user adds care tasks for each pet, including the task description, time, frequency, and priority.
4. The app displays today’s schedule using the Scheduler class.
5. Tasks are organized by priority first and then by time.
6. If two incomplete tasks are scheduled at the same time on the same due date, the app shows a warning message with a suggested next available slot.
7. The user can search for the next available slot manually by entering a start time.
8. The user can filter tasks by completion status.
9. The user can mark a task complete.
10. If the completed task is daily or weekly, the system creates the next recurring task automatically.
11. The app saves owner, pet, and task data to `data.json`, so the information can persist between runs.
12. The user can also run `python main.py` to see the same scheduling logic demonstrated in the terminal.

**Screenshot or video** *(optional)*: A screenshot or video can be added here to show the Streamlit app running.

## Project Files

| File                     | Purpose                                                      |
| ------------------------ | ------------------------------------------------------------ |
| `app.py`                 | Streamlit user interface                                     |
| `pawpal_system.py`       | Backend classes and scheduling logic                         |
| `main.py`                | CLI demo script                                              |
| `tests/test_pawpal.py`   | Automated pytest test suite                                  |
| `data.json`              | Saved owner, pet, and task data                              |
| `diagrams/uml_draft.mmd` | Initial UML diagram                                          |
| `diagrams/uml_final.mmd` | Final UML diagram                                            |
| `reflection.md`          | Project reflection                                           |
| `ai_interactions.md`     | Notes about AI collaboration and optional extension workflow |
