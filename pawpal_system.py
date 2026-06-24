import json
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


@dataclass
class Task:
    """Represents one pet care activity."""
    description: str
    time: str
    frequency: str
    priority: str = "Medium"
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
            priority=self.priority,
            completed=False,
            due_date=next_date,
        )

    def to_dict(self):
        """Convert a task into a dictionary for JSON saving."""
        return {
            "description": self.description,
            "time": self.time,
            "frequency": self.frequency,
            "priority": self.priority,
            "completed": self.completed,
            "due_date": self.due_date.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        """Create a Task object from saved dictionary data."""
        return Task(
            description=data["description"],
            time=data["time"],
            frequency=data["frequency"],
            priority=data.get("priority", "Medium"),
            completed=data.get("completed", False),
            due_date=date.fromisoformat(data["due_date"]),
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

    def to_dict(self):
        """Convert a pet into a dictionary for JSON saving."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @staticmethod
    def from_dict(data):
        """Create a Pet object from saved dictionary data."""
        pet = Pet(
            name=data["name"],
            species=data["species"],
            age=data["age"],
        )

        for task_data in data.get("tasks", []):
            pet.add_task(Task.from_dict(task_data))

        return pet


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

    def to_dict(self):
        """Convert an owner into a dictionary for JSON saving."""
        return {
            "name": self.name,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @staticmethod
    def from_dict(data):
        """Create an Owner object from saved dictionary data."""
        owner = Owner(name=data["name"])

        for pet_data in data.get("pets", []):
            owner.add_pet(Pet.from_dict(pet_data))

        return owner

    def save_to_json(self, filename="data.json"):
        """Save owner, pet, and task data to a JSON file."""
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    @staticmethod
    def load_from_json(filename="data.json"):
        """Load owner, pet, and task data from a JSON file."""
        with open(filename, "r") as file:
            data = json.load(file)

        return Owner.from_dict(data)


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

    def sort_by_priority(self, tasks=None):
        """Sort tasks by priority first, then time."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()

        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3,
            "high": 1,
            "medium": 2,
            "low": 3,
        }

        return sorted(
            tasks,
            key=lambda item: (
                priority_order.get(item[1].priority, 2),
                item[1].time,
            ),
        )

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
        """Get all pet tasks sorted by priority and time."""
        return self.sort_by_priority()

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
        schedule = self.sort_by_time()
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
                    suggested_slot = self.next_available_slot(
                        start_time=task_one.time,
                        due_date=task_one.due_date,
                    )

                    warning = (
                        f"Conflict at {task_one.time} on {task_one.due_date}: "
                        f"{pet_one.name} has '{task_one.description}' and "
                        f"{pet_two.name} has '{task_two.description}'. "
                        f"Suggested next available slot: {suggested_slot}."
                    )
                    conflicts.append(warning)

        return conflicts

    def next_available_slot(self, start_time="08:00", due_date=None, interval_minutes=30):
        """Find the next open time slot after a conflict."""
        if due_date is None:
            due_date = date.today()

        used_times = set()

        for pet, task in self.owner.get_all_tasks():
            if not task.completed and task.due_date == due_date:
                used_times.add(task.time)

        current_time = datetime.strptime(start_time, "%H:%M")

        for _ in range(48):
            current_time += timedelta(minutes=interval_minutes)
            candidate = current_time.strftime("%H:%M")

            if candidate not in used_times:
                return candidate

        return "No available slot found"

    def print_schedule(self):
        """Print today's schedule in a readable format."""
        schedule = self.get_schedule()

        print("Today's Priority Schedule")
        print("-------------------------")

        if not schedule:
            print("No tasks scheduled.")
            return

        for pet, task in schedule:
            status = "Done" if task.completed else "Not done"
            print(
                f"{task.time} - {pet.name} ({pet.species}): "
                f"{task.description} [{task.frequency}] "
                f"priority {task.priority} due {task.due_date} - {status}"
            )