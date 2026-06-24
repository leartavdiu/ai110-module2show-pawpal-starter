from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: str = "general"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task for this pet."""
        pass

    def remove_task(self, task_title: str):
        """Remove a task by title."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        pass

    def add_preference(self, preference: str):
        """Add an owner preference."""
        pass


@dataclass
class DailyPlan:
    owner: Owner
    pet: Pet
    scheduled_tasks: list[Task] = field(default_factory=list)

    def generate_plan(self, tasks: list[Task]):
        """
        Generate a daily care plan based on task priority,
        task duration, and owner availability.
        """
        pass

    def explain_plan(self):
        """Explain why tasks were included in the schedule."""
        pass