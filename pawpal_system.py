"""
PawPal+ logic layer.

Backend classes for the pet care planner, matching diagrams/uml_draft.mmd:
Task, Pet, Owner and Scheduler.
"""

from dataclasses import dataclass, field
from typing import List


# Lets the scheduler sort priority strings; higher number = more important.
PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}


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

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


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
