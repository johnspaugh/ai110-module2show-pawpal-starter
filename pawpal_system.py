"""
PawPal+ logic layer.

Backend classes for the pet care planner. This is a skeleton: attributes and
method signatures only, matching diagrams/uml_draft.mmd. Logic comes later.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, grooming, ...)."""

    title: str
    category: str
    duration_minutes: int
    priority: str  # e.g. "low", "medium", "high"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Return the tasks that are not yet completed."""
        pass


@dataclass
class Owner:
    """A pet owner with limited daily time and a list of pets."""

    name: str
    available_minutes_per_day: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        pass


class Scheduler:
    """Builds and explains a daily plan for an owner."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_daily_plan(self) -> List[Task]:
        """Select and order tasks by priority within the owner's available time."""
        pass

    def explain_plan(self) -> str:
        """Return a human readable explanation of why the plan looks the way it does."""
        pass
