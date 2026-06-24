from pawpal_system import Pet, Task


def test_task_completion():
    task = Task("Morning walk", "08:00", "daily")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Mochi", "dog", 3)
    task = Task("Breakfast feeding", "09:00", "daily")

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].description == "Breakfast feeding"