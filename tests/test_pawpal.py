from pawpal_system import Pet, Task


def test_task_mark_complete():
    task = Task(title="Morning Walk", duration=30, priority=3, pet_name="Buddy")
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=4)
    task = Task(title="Feeding", duration=10, priority=2, pet_name="Buddy")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1
