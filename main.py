from pawpal_system import Owner, Pet, Task, Scheduler


owner = Owner("Jordan")

dog = Pet("Mochi", "dog", 3)
cat = Pet("Luna", "cat", 2)

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Breakfast feeding", "09:00", "daily", "High"))
dog.add_task(Task("Morning walk", "08:00", "daily", "Medium"))
cat.add_task(Task("Clean litter box", "10:30", "daily", "Low"))
cat.add_task(Task("Evening play time", "18:00", "daily", "Low"))

# Conflict test: this happens at the same time as Morning walk.
cat.add_task(Task("Morning medicine", "08:00", "daily", "High"))

scheduler = Scheduler(owner)

print("Today's Priority Schedule")
print("-------------------------")
for pet, task in scheduler.get_schedule():
    status = "Done" if task.completed else "Not done"
    print(
        f"{task.time} - {pet.name} ({pet.species}): "
        f"{task.description} [{task.frequency}] "
        f"priority {task.priority} due {task.due_date} - {status}"
    )

print("\nSchedule Sorted Only By Time")
print("----------------------------")
for pet, task in scheduler.sort_by_time():
    print(f"{task.time} - {pet.name}: {task.description} priority {task.priority}")

print("\nIncomplete Tasks")
print("----------------")
for pet, task in scheduler.filter_tasks(completed=False):
    print(f"{pet.name}: {task.description} at {task.time}")

print("\nMochi's Tasks")
print("----------------")
for pet, task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"{pet.name}: {task.description} at {task.time}")

print("\nConflict Warnings Before Completing Task")
print("---------------------------------------")
conflicts = scheduler.detect_conflicts()

if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts found.")

print("\nNext Available Slot After 08:00")
print("-------------------------------")
print(scheduler.next_available_slot("08:00"))

print("\nSaving data to data.json...")
owner.save_to_json("data.json")

print("\nLoading data from data.json...")
loaded_owner = Owner.load_from_json("data.json")
loaded_scheduler = Scheduler(loaded_owner)

print("\nLoaded Schedule")
print("---------------")
for pet, task in loaded_scheduler.get_schedule():
    print(f"{task.time} - {pet.name}: {task.description} priority {task.priority}")

print("\nCompleting Morning walk...")
scheduler.mark_task_complete("Mochi", "Morning walk")

print("\nUpdated Priority Schedule")
print("-------------------------")
for pet, task in scheduler.get_schedule():
    status = "Done" if task.completed else "Not done"
    print(
        f"{task.time} - {pet.name} ({pet.species}): "
        f"{task.description} [{task.frequency}] "
        f"priority {task.priority} due {task.due_date} - {status}"
    )

print("\nConflict Warnings After Completing Task")
print("--------------------------------------")
conflicts = scheduler.detect_conflicts()

if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts found.")