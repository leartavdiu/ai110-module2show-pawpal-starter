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
    schedule = scheduler.sort_by_time()

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
    assert "Suggested next available slot" in conflicts[0]


def test_pet_with_no_tasks_returns_empty_schedule():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_schedule()

    assert schedule == []


def test_priority_sorting():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)

    pet.add_task(Task("Low priority grooming", "08:00", "daily", "Low"))
    pet.add_task(Task("High priority medicine", "12:00", "daily", "High"))
    pet.add_task(Task("Medium priority walk", "09:00", "daily", "Medium"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_schedule()

    descriptions = [task.description for pet, task in schedule]

    assert descriptions == [
        "High priority medicine",
        "Medium priority walk",
        "Low priority grooming",
    ]


def test_next_available_slot():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)

    pet.add_task(Task("Morning walk", "08:00", "daily"))
    pet.add_task(Task("Breakfast feeding", "08:30", "daily"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    next_slot = scheduler.next_available_slot("08:00")

    assert next_slot == "09:00"


def test_owner_save_and_load_json(tmp_path):
    file_path = tmp_path / "data.json"

    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    task = Task("Morning walk", "08:00", "daily", "High")

    pet.add_task(task)
    owner.add_pet(pet)

    owner.save_to_json(file_path)

    loaded_owner = Owner.load_from_json(file_path)

    assert loaded_owner.name == "Jordan"
    assert len(loaded_owner.pets) == 1
    assert loaded_owner.pets[0].name == "Mochi"
    assert loaded_owner.pets[0].tasks[0].description == "Morning walk"
    assert loaded_owner.pets[0].tasks[0].priority == "High"