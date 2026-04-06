from itertools import combinations
from dataclasses import dataclass, field
from datetime import date, timedelta
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
    preferred_time: Optional[str] = None   # "morning", "afternoon", or "evening"
    is_planned: bool = False                # set to True when scheduler includes this task
    is_completed: bool = False              # set to True when task is marked done
    frequency: Optional[str] = None        # "daily" or "weekly"
    due_date: Optional[date] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a copy of this task with due_date advanced by its frequency interval.

        Returns None if frequency or due_date is not set.
        """
        intervals = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        if self.frequency not in intervals or self.due_date is None:
            return None
        return Task(
            title=self.title,
            duration=self.duration,
            priority=self.priority,
            pet_name=self.pet_name,
            preferred_time=self.preferred_time,
            frequency=self.frequency,
            due_date=self.due_date + intervals[self.frequency],
        )

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
    def __init__(self, name: str, available_time: int) -> None:
        self.name: str = name
        self.available_time: int = available_time
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

    def complete_task(self, task: Task, owner: Optional[Owner] = None) -> Optional[Task]:
        """Mark a task complete and, if recurring, add the next occurrence to the matching pet."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task:
            active_owner = owner or self.owner
            for pet in active_owner.get_pets():
                if pet.name == task.pet_name:
                    pet.add_task(next_task)
                    break
        return next_task

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """Return tasks from self.plan matching the given pet_name and/or completed status."""
        return [
            t for t in self.plan
            if (pet_name is None or t.pet_name == pet_name)
            and (completed is None or t.is_completed == completed)
        ]

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks that share the same preferred_time."""
        warnings = []
        by_time: dict[str, list[Task]] = {}

        for task in self.plan:
            if task.preferred_time is None:
                continue
            by_time.setdefault(task.preferred_time, []).append(task)

        for time, tasks in by_time.items():
            for a, b in combinations(tasks, 2):
                warnings.append(f"Conflict at '{time}': '{a.title}' and '{b.title}' overlap")

        return warnings

    def sort_by_time(self) -> list[Task]:
        """Return a new list of planned tasks sorted by preferred_time (morning → afternoon → evening)."""
        time_order = {"morning": 0, "afternoon": 1, "evening": 2}
        return sorted(self.plan, key=lambda t: time_order.get(t.preferred_time, 3))
