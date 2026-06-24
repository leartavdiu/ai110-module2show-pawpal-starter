from pawpal_system import Owner, Pet, Task, Scheduler


owner = Owner("Jordan")

dog = Pet("Mochi", "dog", 3)
cat = Pet("Luna", "cat", 2)

owner.add_pet(dog)
owner.add_pet(cat)

# Tasks are added out of order on purpose to test sorting.
dog.add_task(Task("Breakfast feeding", "09:00", "daily"))
dog.add_task(Task("Morning walk", "08:00", "daily"))
cat.add_task(Task("Clean litter box", "10:30", "daily"))
cat.add_task(Task("Evening play time", "18:00", "daily"))

# Conflict test: this happens at the same time as Morning walk.
cat.add_task(Task("Morning medicine", "08:00", "daily"))

scheduler = Scheduler(owner)

print("Today's Schedule")
print("----------------")
for pet, task in scheduler.get_schedule():
    status = "Done" if task.completed else "Not done"
    print(
        f"{task.time} - {pet.name} ({pet.species}): "
        f"{task.description} [{task.frequency}] due {task.due_date} - {status}"
    )

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

print("\nCompleting Morning walk...")
scheduler.mark_task_complete("Mochi", "Morning walk")

print("\nUpdated Schedule")
print("----------------")
for pet, task in scheduler.get_schedule():
    status = "Done" if task.completed else "Not done"
    print(
        f"{task.time} - {pet.name} ({pet.species}): "
        f"{task.description} [{task.frequency}] due {task.due_date} - {status}"
    )

print("\nConflict Warnings After Completing Task")
print("--------------------------------------")
conflicts = scheduler.detect_conflicts()

if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts found.")