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

## ✨ Features

- **Multiple pets, one owner:** every pet's tasks are pooled through `Owner.get_all_tasks()`, so the scheduler plans across all pets at once.
- **Priority-based daily plan:** pending tasks are sorted high to low priority, shortest first within a priority, then added greedily while they fit the owner's daily minutes. Tasks that don't fit are recorded as skipped.
- **Plan explanation:** `explain_plan()` reports minutes used, the order chosen and what was skipped.
- **Sorting by time:** tasks are ordered by `HH:MM` start time, earliest first, with unscheduled tasks last. The original list is never modified.
- **Filtering:** by pet, by completed or pending status, or both together.
- **Conflict warnings:** any two pending timed tasks that overlap, for the same pet or different pets, produce a readable warning. Back-to-back tasks are not flagged, and nothing is raised, so the UI can warn and carry on.
- **Recurring tasks:** completing a daily, weekly or monthly task creates the next occurrence (due in 1, 7 or 30 days). A `once` task does not repeat.
- **Computed end times:** each task with a start time knows when it finishes, which the conflict messages use.
- **Streamlit UI and CLI demo:** `app.py` exposes all of the above; `main.py` prints the same behaviours in the terminal.

## 🛠️ Implementation Summary

The logic lives in `pawpal_system.py` as four classes that work together:

- **`Task`** (dataclass): one care activity with a title, category, duration in minutes, priority (`low`/`medium`/`high`), frequency, completion status, and the name of the pet it belongs to. `mark_complete()` marks it done.
- **`Pet`** (dataclass): a pet's name, species, age, and its list of tasks. `add_task()` attaches a task and tags it with the pet's name; `get_pending_tasks()` returns the ones not yet done.
- **`Owner`** (dataclass): the owner's name, daily time budget in minutes, and a list of pets. `get_all_tasks()` returns every pet's tasks in one list.
- **`Scheduler`**: the "brain". It reads tasks from `Owner.get_all_tasks()` (so it covers all pets, not one), keeps the pending ones, sorts them by priority (shortest first within a priority), and adds each task that still fits in the owner's time budget. Tasks that don't fit are recorded in `skipped`, and `explain_plan()` describes the result.

Flow: `Owner` -> `Pet`s -> `Task`s are the data; `Scheduler(owner).generate_daily_plan()` turns that data into a plan. `main.py` is a terminal demo, and `tests/test_pawpal.py` holds the tests. The final UML is in `diagrams/uml_final.mmd` (the original design is in `diagrams/uml_draft.mmd`).

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

Run the suite from the project root (with the virtual environment active):

```bash
python -m pytest
```

Output of a successful run:

```
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\Lenovo PC\Documents\2026_Fall\AI_110_Foundations_of_AI_Engineering\codePratice\ai110-module2show-pawpal-starter
collected 12 items

tests\test_pawpal.py ............                                        [100%]

============================= 12 passed in 0.05s ==============================
```

**What the tests cover** (`tests/test_pawpal.py`):

- **Sorting:** tasks come back in chronological order, unscheduled tasks go last, the input list is not modified, and an empty list returns `[]`.
- **Recurrence:** completing a daily task creates a new incomplete task due tomorrow on the same pet; weekly tasks are due in 7 days; `once` tasks create nothing.
- **Conflict detection:** identical start times are flagged (same pet and different pets), back-to-back tasks are not, completed tasks are ignored, and no tasks gives no warnings.

**Not yet tested:** partial/nested overlaps, zero-duration tasks, `end_time` past midnight, recurrence based on a task's own due date (it currently uses today's date), `filter_tasks`, and `generate_daily_plan`.

**Confidence Level: ⭐⭐⭐⭐ (4 / 5)** All 12 tests pass, and they cover the three core behaviours (sorting, recurrence, conflicts) including key edge cases. I'm holding back one star because the daily plan, filtering and midnight-rollover cases have no tests yet. Also, some times would provide more than intended, but it was good. Thus, I kept it.

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

## 🎬 Demo Walkthrough

Start the app with `streamlit run app.py`, or see the terminal version with `python main.py`.

### What you can do in the app

- **Set up the owner:** edit the owner's name and how many minutes they have each day.
- **Add pets:** enter a name, species and age. A table lists each pet and its task count.
- **Add tasks:** pick a pet, then set the title, category, duration, priority, how often it repeats (daily, weekly, monthly or once) and an optional `HH:MM` start time.
- **Review tasks:** filter the task table by pet and by status (pending or completed). It is always sorted by start time, with unscheduled tasks last.
- **Complete tasks:** choose a task from the dropdown and press "Complete task". Repeating tasks get their next occurrence automatically.
- **Generate the schedule:** press "Generate schedule" to see today's plan, the minutes used, any skipped tasks and an explanation of why.

### Example workflow

1. The owner starts as "Jordan" with 120 minutes a day. Change the name or minutes if you like.
2. Add a pet, for example Mochi the cat.
3. Add two tasks for Mochi: "Feeding" at 08:15 for 10 minutes and "Brushing" at 08:15 for 5 minutes.
4. A yellow warning appears above the task list: Mochi's Feeding overlaps Mochi's Brushing. Change one start time and the warning turns into a green "No time conflicts" message.
5. Press "Generate schedule". High-priority tasks come first and the plan stops when the day's minutes run out.
6. Mark "Feeding" complete. Because it repeats daily, a new "Feeding" task appears, due tomorrow.

### Scheduler behaviours on show

- **Sorting by time:** the task table and the "Sorted by time" CLI section order tasks by start time.
- **Filtering:** the task table filters by pet and status; the CLI shows one pet's tasks.
- **Conflict warnings:** each overlap gets its own warning that names both tasks, both pets and both time ranges. Back-to-back tasks are not flagged.
- **Recurrence:** completing a daily, weekly or monthly task creates the next one and reports its due date.
- **Time budget:** tasks that don't fit are skipped and listed rather than dropped silently.

### Sample CLI output

Output of `python main.py`. The "Completed 'Grooming'" due date is today plus 7 days, so it changes with the day you run it.

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

Plan for Sally: 75 of 90 minutes used.
Tasks are ordered by priority (high first), then shortest first, and added while they still fit.
  1. Heartworm pill for Robert (5 min, high priority)
  2. Flea medication for Mochi (5 min, high priority)
  3. Feeding for Mochi (10 min, high priority)
  4. Morning walk for Robert (30 min, high priority)
  5. Playtime for Mochi (20 min, medium priority)
  6. Brushing for Mochi (5 min, low priority)
Skipped (not enough time left):
  - Grooming for Robert (45 min, low priority)

Sorted by time:
  07:30  Mochi: Playtime
  08:00  Robert: Morning walk
  08:00  Robert: Heartworm pill
  08:15  Mochi: Feeding
  08:15  Mochi: Brushing
  17:00  Robert: Grooming
  --:--  Mochi: Flea medication

Mochi's tasks only:
  Feeding
  Brushing
  Playtime
  Flea medication

Completed 'Grooming'; next one due 2026-10-24
Pending after completion: 7

Conflict check:
  Conflict (same pet): Robert's Morning walk (08:00-08:30) overlaps Robert's Heartworm pill (08:00-08:05)
  Conflict (different pets): Robert's Morning walk (08:00-08:30) overlaps Mochi's Feeding (08:15-08:25)
  Conflict (different pets): Robert's Morning walk (08:00-08:30) overlaps Mochi's Brushing (08:15-08:20)
  Conflict (same pet): Mochi's Feeding (08:15-08:25) overlaps Mochi's Brushing (08:15-08:20)
```

**Screenshot or video** *(optional)*: add one here for human reviewers.
