from dataclasses import dataclass, field


@dataclass
class Task:
    """Represents one pet care activity."""
    description: str
    time: str
    frequency: str
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as not completed."""
        self.completed = False


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
    """Organizes and displays tasks across all pets."""

    def __init__(self, owner: Owner):
        """Create a scheduler for one owner."""
        self.owner = owner

    def get_schedule(self):
        """Get all pet tasks organized by time."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda item: item[1].time)

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
                f"{task.description} [{task.frequency}] - {status}"
            )