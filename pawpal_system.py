"""
PawPal+ logic layer.

Backend classes for the pet care planner, matching diagrams/uml_draft.mmd:
Task, Pet, Owner and Scheduler.
"""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List, Optional


# Lets the scheduler sort priority strings; higher number = more important.
PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}

# Days until the next occurrence of a recurring task; "once" never repeats.
RECURRENCE_DAYS = {"daily": 1, "weekly": 7, "monthly": 30}


def _to_minutes(hhmm: str) -> int:
    """Convert "HH:MM" to minutes since midnight."""
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, grooming, ...)."""

    title: str
    category: str
    duration_minutes: int
    priority: str  # one of PRIORITY_ORDER's keys
    frequency: str = "daily"  # e.g. "daily", "weekly", "once"
    completed: bool = False
    pet_name: str = ""  # filled in by Pet.add_task so a plan can say "Walk Biscuit"
    start_time: str = ""  # "HH:MM" (24h); empty means unscheduled
    due_date: Optional[date] = None

    @property
    def end_time(self) -> str:
        """Return "HH:MM" for when this task finishes, or "" if it has no start time."""
        if not self.start_time:
            return ""
        end = _to_minutes(self.start_time) + self.duration_minutes
        return f"{end // 60:02d}:{end % 60:02d}"

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as done and build its next occurrence if it recurs.

        "daily", "weekly" and "monthly" tasks get a copy that is not completed
        and is due today + 1, 7 or 30 days (computed with timedelta). Any other
        frequency, such as "once", returns None. The copy is only returned here;
        use Pet.complete_task() to also attach it to the pet.
        """
        self.completed = True
        days = RECURRENCE_DAYS.get(self.frequency)
        if days is None:
            return None
        next_due = date.today() + timedelta(days=days)
        return replace(self, completed=False, due_date=next_due)


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove this exact task object from the pet (not just an equal-looking copy)."""
        for i, existing in enumerate(self.tasks):
            if existing is task:
                del self.tasks[i]
                return

    def complete_task(self, task: Task) -> Optional[Task]:
        """Complete a task and, if it recurs, add the next occurrence to this pet.

        Returns the newly added task, or None if the task does not repeat.
        """
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task

    def get_pending_tasks(self) -> List[Task]:
        """Return the tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """A pet owner with limited daily time and a list of pets."""

    name: str
    available_minutes_per_day: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        for i, existing in enumerate(self.pets):
            if existing is pet:
                del self.pets[i]
                return

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Builds and explains a daily plan for an owner."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for one owner, with an empty plan and skipped list."""
        self.owner = owner
        # Results of the last generate_daily_plan() call, kept so explain_plan()
        # can say what was chosen and what was left out.
        self.plan: List[Task] = []
        self.skipped: List[Task] = []

    def generate_daily_plan(self) -> List[Task]:
        """Build today's plan from all pets' pending tasks, highest priority first, within the time budget."""
        # Reads tasks via Owner.get_all_tasks(), sorts by priority then duration,
        # adds each task that still fits, and puts the rest in self.skipped.
        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        pending.sort(
            key=lambda t: (-PRIORITY_ORDER.get(t.priority, 0), t.duration_minutes)
        )

        self.plan = []
        self.skipped = []
        minutes_left = self.owner.available_minutes_per_day

        for task in pending:
            if task.duration_minutes <= minutes_left:
                self.plan.append(task)
                minutes_left -= task.duration_minutes
            else:
                self.skipped.append(task)

        return self.plan

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks ordered by "HH:MM" start time, earliest first.

        Sorts the given tasks, or all of the owner's tasks if none are given.
        Tasks with no start time go last. The input list is not modified.
        """
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: (t.start_time == "", t.start_time))

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        """Return the owner's tasks that match every filter given.

        pet_name keeps only that pet's tasks; completed=True/False keeps only
        done/pending tasks. A filter left as None is ignored.
        """
        return [
            t
            for t in self.owner.get_all_tasks()
            if (pet_name is None or t.pet_name == pet_name)
            and (completed is None or t.completed == completed)
        ]

    def detect_conflicts(self) -> List[str]:
        """Return a warning message for each pair of overlapping pending tasks.

        Only tasks with a start_time are checked, for the same pet or different
        pets. Two tasks overlap when one starts before the other ends; a task
        that starts exactly when another ends is not a conflict. Never raises
        for overlaps, so the caller can just print the messages. An empty list
        means no conflicts.
        """
        timed = self.sort_by_time(
            [t for t in self.filter_tasks(completed=False) if t.start_time]
        )
        warnings: List[str] = []
        # Sorted by start, so a task can only overlap tasks that start before it ends.
        for i, a in enumerate(timed):
            a_end = _to_minutes(a.start_time) + a.duration_minutes
            for b in timed[i + 1:]:
                if _to_minutes(b.start_time) >= a_end:
                    break
                same = "same pet" if a.pet_name == b.pet_name else "different pets"
                warnings.append(
                    f"Conflict ({same}): {a.pet_name}'s {a.title} "
                    f"({a.start_time}-{a.end_time}) overlaps {b.pet_name}'s "
                    f"{b.title} ({b.start_time}-{b.end_time})"
                )
        return warnings

    def explain_plan(self) -> str:
        """Return a human readable explanation of why the plan looks the way it does."""
        budget = self.owner.available_minutes_per_day
        used = sum(t.duration_minutes for t in self.plan)
        lines = [
            f"Plan for {self.owner.name}: {used} of {budget} minutes used.",
            "Tasks are ordered by priority (high first), then shortest first, "
            "and added while they still fit.",
        ]

        for n, task in enumerate(self.plan, start=1):
            lines.append(
                f"  {n}. {task.title} for {task.pet_name} "
                f"({task.duration_minutes} min, {task.priority} priority)"
            )

        if self.skipped:
            lines.append("Skipped (not enough time left):")
            for task in self.skipped:
                lines.append(
                    f"  - {task.title} for {task.pet_name} "
                    f"({task.duration_minutes} min, {task.priority} priority)"
                )

        return "\n".join(lines)
