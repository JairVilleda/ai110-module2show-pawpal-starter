from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list["Task"] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a readable string with the pet's name, species, and age."""
        return f"{self.name} ({self.species}, {self.age} yrs)"

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task from this pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list["Task"]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class Task:
    title: str
    duration: int          # minutes
    priority: int          # e.g. 1 (low) to 3 (high)
    pet_name: str
    preferred_time: Optional[str] = None  # "morning", "afternoon", or "evening"
    is_planned: bool = False               # set to True when scheduler includes this task
    is_completed: bool = False             # set to True when task is marked done

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def get_priority_score(self, current_time_block: Optional[str] = None) -> int:
        """Return the task's priority score, boosted by 1 if the time block matches preferred_time."""
        score = self.priority
        if current_time_block and current_time_block == self.preferred_time:
            score += 1
        return score

    def __str__(self) -> str:
        """Return a readable string showing the task's pet, title, duration, and priority."""
        return f"[{self.pet_name}] {self.title} — {self.duration} min (priority: {self.priority})"


class Owner:
    def __init__(self, name: str, available_time: int, preferences: Optional[dict] = None) -> None:
        self.name: str = name
        self.available_time: int = available_time
        self.preferences: dict = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's pet list if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Return a combined list of all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def update_available_time(self, time: int) -> None:
        """Update the owner's available time in minutes."""
        self.available_time = time

    def update_preferences(self, prefs: dict) -> None:
        """Replace the owner's preferences with the given dictionary."""
        self.preferences = prefs


class Scheduler:
    def __init__(self, owner: Optional[Owner] = None) -> None:
        self.owner: Optional[Owner] = owner
        self.plan: list[Task] = []
        self.explanation: list[str] = []

    def generate_plan(
        self,
        owner: Optional[Owner] = None,
        current_time_block: Optional[str] = None,
    ) -> None:
        """Build a daily plan by greedily selecting the highest-priority tasks that fit within available time."""
        active_owner = owner or self.owner
        tasks = active_owner.get_all_tasks()
        sorted_tasks = sorted(tasks, key=lambda t: t.get_priority_score(current_time_block), reverse=True)

        self.plan = []
        self.explanation = []
        time_used = 0

        for task in sorted_tasks:
            if time_used + task.duration <= active_owner.available_time:
                task.is_planned = True
                self.plan.append(task)
                time_used += task.duration
                self.explanation.append(f"Added '{task.title}' for {task.pet_name} ({task.duration} min, priority {task.get_priority_score(current_time_block)})")
            else:
                self.explanation.append(f"Skipped '{task.title}' for {task.pet_name} — not enough time remaining ({task.duration} min needed)")

    def get_plan(self) -> list[Task]:
        """Return the list of planned tasks."""
        return self.plan

    def explain_plan(self) -> list[str]:
        """Return the list of explanation messages for scheduling decisions."""
        return self.explanation
