"""PawPal+ System - Core logic layer for smart pet care management."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str  # "HH:MM" format
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False
    pet_name: str = ""
    date: Optional[str] = None  # "YYYY-MM-DD"

    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now().strftime("%Y-%m-%d")

    def mark_complete(self) -> Optional["Task"]:
        """Mark task complete. Returns a new Task if recurring."""
        self.completed = True
        if self.frequency == "daily":
            next_date = datetime.strptime(self.date, "%Y-%m-%d") + timedelta(days=1)
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                pet_name=self.pet_name,
                date=next_date.strftime("%Y-%m-%d"),
            )
        elif self.frequency == "weekly":
            next_date = datetime.strptime(self.date, "%Y-%m-%d") + timedelta(weeks=1)
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                pet_name=self.pet_name,
                date=next_date.strftime("%Y-%m-%d"),
            )
        return None

    def __str__(self):
        status = "✅" if self.completed else "⬜"
        freq = f" ({self.frequency})" if self.frequency != "once" else ""
        return f"{status} [{self.time}] {self.description} - {self.pet_name}{freq}"


@dataclass
class Pet:
    """Stores pet details and associated tasks."""
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task for this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_pending_tasks(self) -> list[Task]:
        """Return incomplete tasks."""
        return [t for t in self.tasks if not t.completed]

    def __str__(self):
        return f"{self.name} ({self.species}, {self.age}y) - {len(self.tasks)} tasks"


@dataclass
class Owner:
    """Manages multiple pets and provides access to all tasks."""
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Register a new pet."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Collect all tasks across all pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """The 'brain' — retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner

    def get_todays_schedule(self) -> list[Task]:
        """Get all tasks for today, sorted by time."""
        today = datetime.now().strftime("%Y-%m-%d")
        tasks = [t for t in self.owner.get_all_tasks() if t.date == today]
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks: list[Task] = None) -> list[Task]:
        """Sort tasks chronologically by their HH:MM time."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Filter tasks for a specific pet."""
        return [t for t in self.owner.get_all_tasks() if t.pet_name.lower() == pet_name.lower()]

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Filter tasks by completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self) -> list[str]:
        """Detect tasks scheduled at the same time on the same date."""
        warnings = []
        tasks = self.owner.get_all_tasks()
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time and tasks[i].date == tasks[j].date:
                    warnings.append(
                        f"⚠️ Conflict: '{tasks[i].description}' ({tasks[i].pet_name}) "
                        f"and '{tasks[j].description}' ({tasks[j].pet_name}) "
                        f"at {tasks[i].time} on {tasks[i].date}"
                    )
        return warnings

    def mark_task_complete(self, task: Task, pet: Pet):
        """Mark a task complete and handle recurrence."""
        new_task = task.mark_complete()
        if new_task:
            pet.add_task(new_task)
            return new_task
        return None
