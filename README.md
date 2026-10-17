# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🛠️ Implementation Summary

The logic lives in `pawpal_system.py` as four classes that work together:

- **`Task`** (dataclass): one care activity with a title, category, duration in minutes, priority (`low`/`medium`/`high`), frequency, completion status, and the name of the pet it belongs to. `mark_complete()` marks it done.
- **`Pet`** (dataclass): a pet's name, species, age, and its list of tasks. `add_task()` attaches a task and tags it with the pet's name; `get_pending_tasks()` returns the ones not yet done.
- **`Owner`** (dataclass): the owner's name, daily time budget in minutes, and a list of pets. `get_all_tasks()` returns every pet's tasks in one list.
- **`Scheduler`**: the "brain". It reads tasks from `Owner.get_all_tasks()` (so it covers all pets, not one), keeps the pending ones, sorts them by priority (shortest first within a priority), and adds each task that still fits in the owner's time budget. Tasks that don't fit are recorded in `skipped`, and `explain_plan()` describes the result.

Flow: `Owner` -> `Pet`s -> `Task`s are the data; `Scheduler(owner).generate_daily_plan()` turns that data into a plan. `main.py` is a terminal demo, and `tests/test_pawpal.py` holds the tests. The UML is in `diagrams/uml_draft.mmd`.

## 🖥️ Sample Output

Output of `python main.py`, which builds an owner with two pets and seven tasks, prints the plan, then demos sorting, filtering, recurrence and conflict warnings:

```
====================================================
  Today's Schedule for Sally
  Pets: Robert, Mochi
  Time used: 75 of 90 min
====================================================
#  Pet      Task               Min  Priority Repeats
----------------------------------------------------
1  Robert   Heartworm pill       5  high     daily
2  Mochi    Flea medication      5  high     monthly
3  Mochi    Feeding             10  high     daily
4  Robert   Morning walk        30  high     daily
5  Mochi    Playtime            20  medium   daily
6  Mochi    Brushing             5  low      daily
----------------------------------------------------
Skipped (not enough time):
  - Robert: Grooming (45 min, low)

Conflict check:
  Conflict (same pet): Robert's Morning walk (08:00-08:30) overlaps Robert's Heartworm pill (08:00-08:05)
  Conflict (different pets): Robert's Morning walk (08:00-08:30) overlaps Mochi's Feeding (08:15-08:25)
  Conflict (different pets): Robert's Morning walk (08:00-08:30) overlaps Mochi's Brushing (08:15-08:20)
  Conflict (same pet): Mochi's Feeding (08:15-08:25) overlaps Mochi's Brushing (08:15-08:20)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest
```

(`pytest --cov` needs the extra `pytest-cov` package, which is not installed.)

Sample test output:

```
======================== test session starts =========================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
collected 10 items

tests\test_pawpal.py ..........                                 [100%]

========================= 10 passed in 0.04s =========================
```

The tests check that `Task.mark_complete()` changes a task's status, that adding a task to a `Pet` increases its task count, sorting by time, filtering by pet and status, daily and weekly recurrence (and that `once` tasks don't repeat), and conflict detection (overlaps, same start time, and back-to-back tasks that don't conflict).

## 📐 Smarter Scheduling

Tasks now have an optional `start_time` (`"HH:MM"`, 24-hour) and `due_date`, which the features below use.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Plan ordering | `Scheduler.generate_daily_plan()` | Highest priority first, shortest first within a priority, added while it fits the time budget. |
| Sorting by time | `Scheduler.sort_by_time()` | Orders tasks by start time, earliest first. Tasks with no start time go last. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Keeps tasks for one pet, only done or only pending tasks, or both filters together. |
| Conflict detection | `Scheduler.detect_conflicts()` | Returns warning strings for overlapping tasks, same pet or different pets. |
| Recurring tasks | `Task.mark_complete()`, `Pet.complete_task()` | Completing a daily, weekly or monthly task creates the next one. |

### Sorting
`sort_by_time()` sorts on the `"HH:MM"` text, which orders correctly because the times are zero-padded. It sorts all of the owner's tasks unless you pass it a list.

### Filtering
`filter_tasks(pet_name="Mochi", completed=False)` returns Mochi's pending tasks. Any filter left out is ignored, so `filter_tasks()` returns every task.

### Conflict detection
`detect_conflicts()` sorts the pending timed tasks by start time and compares each one with the tasks that start before it ends. Two tasks conflict when one starts before the other ends, so partial overlaps are caught as well as identical start times. A task that starts exactly when another ends is fine. The method returns messages and never raises, so the app can show a warning and carry on.

Tradeoff: `generate_daily_plan()` does not use start times, so a generated plan can still contain overlapping tasks. The conflict check only warns; it does not rearrange anything. Times are also assumed to be on the same day.

### Recurring tasks
`Task.mark_complete()` marks the task done. For `daily`, `weekly` and `monthly` tasks it returns a copy that is not completed and is due `date.today() + timedelta(days=1 / 7 / 30)`; a `once` task returns `None`. `Pet.complete_task()` calls it and adds the new task to the pet. A monthly task repeats every 30 days, not on the same calendar date.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
