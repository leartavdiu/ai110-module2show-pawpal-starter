from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """Represents one pet care activity."""
    description: str
    time: str
    frequency: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as not completed."""
        self.completed = False

    def create_next_occurrence(self):
        """Create the next recurring copy of this task."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=next_date,
        )


@dataclass
class Pet:
    """Stores pet details and the pet's tasks."""
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Stores owner details and manages multiple pets."""
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks from all of the owner's pets."""
        all_tasks = []

        for pet in self.pets:
            for task in pet.get_tasks():
                all_tasks.append((pet, task))

        return all_tasks


class Scheduler:
    """Organizes, filters, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        """Create a scheduler for one owner."""
        self.owner = owner

    def sort_by_time(self, tasks=None):
        """Sort tasks by their HH:MM time value."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()

        return sorted(tasks, key=lambda item: item[1].time)

    def filter_tasks(self, pet_name=None, completed=None):
        """Filter tasks by pet name or completion status."""
        tasks = self.owner.get_all_tasks()
        filtered_tasks = []

        for pet, task in tasks:
            matches_pet = pet_name is None or pet.name == pet_name
            matches_status = completed is None or task.completed == completed

            if matches_pet and matches_status:
                filtered_tasks.append((pet, task))

        return filtered_tasks

    def get_schedule(self):
        """Get all pet tasks sorted by time."""
        return self.sort_by_time()

    def mark_task_complete(self, pet_name, task_description):
        """Mark a task complete and create the next recurring task if needed."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                for task in pet.tasks:
                    if task.description == task_description and not task.completed:
                        task.mark_complete()

                        next_task = task.create_next_occurrence()
                        if next_task:
                            pet.add_task(next_task)

                        return True

        return False

    def detect_conflicts(self):
        """Return warning messages for incomplete tasks scheduled at the same time on the same due date."""
        schedule = self.get_schedule()
        conflicts = []

        for i in range(len(schedule)):
            pet_one, task_one = schedule[i]

            if task_one.completed:
                continue

            for j in range(i + 1, len(schedule)):
                pet_two, task_two = schedule[j]

                if task_two.completed:
                    continue

                same_time = task_one.time == task_two.time
                same_date = task_one.due_date == task_two.due_date

                if same_time and same_date:
                    warning = (
                        f"Conflict at {task_one.time} on {task_one.due_date}: "
                        f"{pet_one.name} has '{task_one.description}' and "
                        f"{pet_two.name} has '{task_two.description}'."
                    )
                    conflicts.append(warning)

        return conflicts

    def print_schedule(self):
        """Print today's schedule in a readable format."""
        schedule = self.get_schedule()

        print("Today's Schedule")
        print("----------------")

        if not schedule:
            print("No tasks scheduled.")
            return

        for pet, task in schedule:
            status = "Done" if task.completed else "Not done"
            print(
                f"{task.time} - {pet.name} ({pet.species}): "
                f"{task.description} [{task.frequency}] "
                f"due {task.due_date} - {status}"
            )