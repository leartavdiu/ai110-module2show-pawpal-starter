from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


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


def test_sorting_correctness():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)

    pet.add_task(Task("Evening walk", "18:00", "daily"))
    pet.add_task(Task("Morning feeding", "08:00", "daily"))
    pet.add_task(Task("Medicine", "12:00", "daily"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_schedule()

    times = [task.time for pet, task in schedule]

    assert times == ["08:00", "12:00", "18:00"]


def test_daily_recurrence_creates_next_day_task():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)

    today = date.today()
    task = Task("Morning walk", "08:00", "daily", due_date=today)

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Mochi", "Morning walk")

    assert result is True
    assert pet.tasks[0].completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].description == "Morning walk"
    assert pet.tasks[1].due_date == today + timedelta(days=1)
    assert pet.tasks[1].completed is False


def test_conflict_detection_flags_duplicate_times():
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog", 3)
    cat = Pet("Luna", "cat", 2)

    dog.add_task(Task("Morning walk", "08:00", "daily"))
    cat.add_task(Task("Morning medicine", "08:00", "daily"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Conflict at 08:00" in conflicts[0]
    assert "Morning walk" in conflicts[0]
    assert "Morning medicine" in conflicts[0]


def test_pet_with_no_tasks_returns_empty_schedule():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_schedule()

    assert schedule == []