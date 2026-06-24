from pawpal_system import Owner, Pet, Task, Scheduler


owner = Owner("Jordan")

dog = Pet("Mochi", "dog", 3)
cat = Pet("Luna", "cat", 2)

dog.add_task(Task("Morning walk", "08:00", "daily"))
dog.add_task(Task("Breakfast feeding", "09:00", "daily"))
cat.add_task(Task("Clean litter box", "10:30", "daily"))
cat.add_task(Task("Evening play time", "18:00", "daily"))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)
scheduler.print_schedule()