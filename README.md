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

Output of `python main.py`, which builds an owner with two pets and five tasks and prints the generated plan:

```
====================================================
  Today's Schedule for Sally
  Pets: Robert, Mochi
  Time used: 65 of 90 min
====================================================
#  Pet      Task               Min  Priority Repeats
----------------------------------------------------
1  Mochi    Flea medication      5  high     monthly
2  Mochi    Feeding             10  high     daily
3  Robert   Morning walk        30  high     daily
4  Mochi    Playtime            20  medium   daily
----------------------------------------------------
Skipped (not enough time):
  - Robert: Grooming (45 min, low)

Plan for Sally: 65 of 90 minutes used.
Tasks are ordered by priority (high first), then shortest first, and added while they still fit.
  1. Flea medication for Mochi (5 min, high priority)
  2. Feeding for Mochi (10 min, high priority)
  3. Morning walk for Robert (30 min, high priority)
  4. Playtime for Mochi (20 min, medium priority)
Skipped (not enough time left):
  - Grooming for Robert (45 min, low priority)
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
collected 2 items

tests\test_pawpal.py ..                                         [100%]

========================= 2 passed in 0.02s ==========================
```

The two tests check that `Task.mark_complete()` changes a task's status, and that adding a task to a `Pet` increases its task count.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
