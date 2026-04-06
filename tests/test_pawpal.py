from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


def test_task_mark_complete():
    task = Task(title="Morning Walk", duration=30, priority=3, pet_name="Buddy")
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=4)
    task = Task(title="Feeding", duration=10, priority=2, pet_name="Buddy")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    pet = Pet(name="Buddy", species="Dog", age=4)
    evening_task = Task(title="Evening Walk", duration=20, priority=2, pet_name="Buddy", preferred_time="evening")
    morning_task = Task(title="Morning Feed", duration=10, priority=2, pet_name="Buddy", preferred_time="morning")
    afternoon_task = Task(title="Afternoon Play", duration=15, priority=2, pet_name="Buddy", preferred_time="afternoon")
    pet.add_task(evening_task)
    pet.add_task(morning_task)
    pet.add_task(afternoon_task)

    owner = Owner(name="Alex", available_time=60)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    sorted_tasks = scheduler.sort_by_time()

    time_blocks = [t.preferred_time for t in sorted_tasks]
    assert time_blocks == ["morning", "afternoon", "evening"]


def test_complete_daily_task_creates_next_occurrence():
    today = date(2026, 4, 5)
    pet = Pet(name="Mochi", species="Cat", age=2)
    task = Task(title="Medicine", duration=5, priority=3, pet_name="Mochi", frequency="daily", due_date=today)
    pet.add_task(task)

    owner = Owner(name="Alex", available_time=60)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task, owner)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.title == task.title
    assert next_task in pet.get_tasks()


def test_detect_conflicts_flags_same_preferred_time():
    pet = Pet(name="Rex", species="Dog", age=3)
    task_a = Task(title="Walk", duration=20, priority=2, pet_name="Rex", preferred_time="morning")
    task_b = Task(title="Feed", duration=10, priority=2, pet_name="Rex", preferred_time="morning")
    pet.add_task(task_a)
    pet.add_task(task_b)

    owner = Owner(name="Alex", available_time=60)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "morning" in conflicts[0]
