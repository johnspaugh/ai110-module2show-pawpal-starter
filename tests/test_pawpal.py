"""Automated tests for the PawPal+ logic layer (pawpal_system.py)."""

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

# Let `import pawpal_system` work when pytest is run from any directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Owner, Pet, Scheduler, Task  # noqa: E402


def make_task(title="Walk", start_time="", duration=30, priority="medium",
              frequency="daily"):
    return Task(
        title=title,
        category="general",
        duration_minutes=duration,
        priority=priority,
        frequency=frequency,
        start_time=start_time,
    )


@pytest.fixture
def owner():
    """An owner with two pets and no tasks yet."""
    o = Owner(name="Sam", available_minutes_per_day=120)
    o.add_pet(Pet(name="Biscuit", species="dog", age=3))
    o.add_pet(Pet(name="Mochi", species="cat", age=5))
    return o


# --- Sorting correctness ---------------------------------------------------

def test_sort_by_time_returns_chronological_order(owner):
    biscuit, mochi = owner.pets
    biscuit.add_task(make_task("Evening walk", "18:00"))
    biscuit.add_task(make_task("Breakfast", "07:30"))
    mochi.add_task(make_task("Lunch", "12:15"))

    result = Scheduler(owner).sort_by_time()

    assert [t.start_time for t in result] == ["07:30", "12:15", "18:00"]


def test_sort_by_time_puts_unscheduled_tasks_last(owner):
    pet = owner.pets[0]
    pet.add_task(make_task("Anytime", ""))
    pet.add_task(make_task("Morning", "08:00"))

    result = Scheduler(owner).sort_by_time()

    assert [t.title for t in result] == ["Morning", "Anytime"]


def test_sort_by_time_does_not_modify_input_list(owner):
    tasks = [make_task("B", "10:00"), make_task("A", "09:00")]

    Scheduler(owner).sort_by_time(tasks)

    assert [t.title for t in tasks] == ["B", "A"]


def test_sort_by_time_with_no_tasks_returns_empty_list(owner):
    assert Scheduler(owner).sort_by_time() == []


# --- Recurrence logic ------------------------------------------------------

def test_completing_daily_task_creates_task_for_next_day(owner):
    pet = owner.pets[0]
    task = make_task("Feed", "08:00", frequency="daily")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task in pet.tasks
    assert next_task.pet_name == "Biscuit"
    assert next_task.title == "Feed"


def test_completing_weekly_task_is_due_in_seven_days(owner):
    pet = owner.pets[0]
    task = make_task("Bath", frequency="weekly")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task.due_date == date.today() + timedelta(days=7)


def test_completing_once_task_creates_no_new_task(owner):
    pet = owner.pets[0]
    task = make_task("Vet visit", frequency="once")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is None
    assert task.completed is True
    assert len(pet.tasks) == 1


# --- Conflict detection ----------------------------------------------------

def test_detect_conflicts_flags_duplicate_times_same_pet(owner):
    pet = owner.pets[0]
    pet.add_task(make_task("Walk", "09:00"))
    pet.add_task(make_task("Groom", "09:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "same pet" in warnings[0]
    assert "Walk" in warnings[0] and "Groom" in warnings[0]


def test_detect_conflicts_flags_duplicate_times_different_pets(owner):
    biscuit, mochi = owner.pets
    biscuit.add_task(make_task("Walk", "09:00"))
    mochi.add_task(make_task("Feed", "09:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "different pets" in warnings[0]


def test_detect_conflicts_back_to_back_tasks_do_not_conflict(owner):
    pet = owner.pets[0]
    pet.add_task(make_task("Walk", "09:00", duration=30))  # ends 09:30
    pet.add_task(make_task("Feed", "09:30", duration=15))

    assert Scheduler(owner).detect_conflicts() == []


def test_detect_conflicts_ignores_completed_tasks(owner):
    pet = owner.pets[0]
    done = make_task("Walk", "09:00")
    done.completed = True
    pet.add_task(done)
    pet.add_task(make_task("Groom", "09:00"))

    assert Scheduler(owner).detect_conflicts() == []


def test_detect_conflicts_with_no_tasks_returns_empty_list(owner):
    assert Scheduler(owner).detect_conflicts() == []
