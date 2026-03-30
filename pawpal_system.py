from dataclasses import dataclass
from typing import Optional


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def get_info(self) -> str:
        pass # Return a string with the pet's info


@dataclass
class Task:
    title: str
    duration: int          # minutes
    priority: int          # e.g. 1 (low) to 3 (high)
    pet_name: str
    preferred_time: Optional[str] = None  # "morning", "afternoon", or "evening"

    def get_priority_score(self, current_time_block: Optional[str] = None) -> int:
        pass

    def __str__(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_time: int, preferences: dict,) -> None:
        self.name: str = name
        self.available_time: int = available_time
        self.preferences: dict = preferences
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass

    def update_available_time(self, time: int) -> None:
        pass

    def update_preferences(self, prefs: dict) -> None:
        pass


class Scheduler:
    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self.plan: list[Task] = []
        self.explanation: list[str] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass

    def generate_plan(self, owner: Owner, current_time_block: Optional[str] = None,) -> None:
        pass

    def get_plan(self) -> list[Task]:
        pass

    def explain_plan(self) -> list[str]:
        pass
