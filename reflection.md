# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I chose four main classes for my initial design: Owner, Pet, Task, and DailyPlan.

The Owner class represents the person using the app. It stores the owner’s name, available time, preferences, and pets.

The Pet class represents the animal being cared for. It stores basic information like the pet’s name, species, and age. It also stores the tasks connected to that pet.

The Task class represents one pet care activity, such as feeding, walking, medicine, grooming, or enrichment. Each task stores a title, duration, priority, category, and completion status.

The DailyPlan class is responsible for building the daily schedule. It uses the owner’s available time, the pet’s tasks, and the task priorities to decide what should be included in the plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design changed during implementation because I replaced the DailyPlan class with a Scheduler class. Scheduler made more sense because it acts as the brain of the system. It sorts tasks, filters tasks, handles recurring tasks, and detects conflicts. This change made the design clearer because the schedule logic is now separated from the basic data classes like Owner, Pet, and Task.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler mainly considers task time, completion status, pet name, frequency, and basic conflicts. Time matters because the schedule should appear in the correct order for the day. Completion status matters because the app needs to know which tasks are already done and which tasks still need attention. Pet name matters because an owner may have multiple pets, so the scheduler needs to filter tasks for a specific pet. Frequency matters because daily and weekly tasks should continue after they are completed. I decided time and completion status mattered most because the main goal of the app is to help the owner clearly see what needs to be done and when.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is that conflict detection only checks for exact time matches. For example, if two tasks are both scheduled at 08:00, the scheduler gives a warning. However, it does not check for overlapping task durations, such as one task from 08:00 to 08:30 and another from 08:15 to 08:45. This is reasonable for this version because the app is still simple, and exact time conflicts are easier to understand and test. A future version could add duration-based conflict detection.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools for design brainstorming, code generation, debugging, and refactoring. In the beginning, AI helped me turn the PawPal+ scenario into a small class design with Owner, Pet, Task, and Scheduler. Later, I used AI to help add scheduling features like sorting by time, filtering tasks, recurring task creation, and conflict detection. The most helpful prompts were specific questions, such as asking how the Scheduler should get tasks from the Owner’s pets or how to test recurring daily tasks.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion as-is was when the design started to become more complicated than needed. I kept the system focused on four main classes instead of adding extra classes too early. I also verified the AI suggestions by running python main.py and python -m pytest. If the output or tests did not match the project requirements, I adjusted the code instead of blindly accepting it.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the main behaviors of the backend system. I tested that a task can be marked complete, that a task can be added to a pet, that the scheduler sorts tasks in chronological order, that a daily recurring task creates a new task for the next day, and that the scheduler detects conflicts when two tasks happen at the same time. I also tested the edge case where a pet has no tasks, because the scheduler should return an empty schedule instead of crashing.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that the scheduler works correctly for the main features because the automated tests passed and the CLI demo shows the schedule output clearly. I would rate my confidence as 4 out of 5 stars. If I had more time, I would test more edge cases, such as weekly recurring tasks, invalid time formats, duplicate pet names, and overlapping task durations.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part I am most satisfied with is how the backend logic became connected to both the CLI demo and the Streamlit UI. The Scheduler can sort tasks, filter tasks, detect conflicts, and create recurring tasks, and those behaviors are visible in the app instead of only existing in the code.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the conflict detection system. Right now, it only checks if two tasks have the exact same time. A better version would also use task duration to detect overlapping tasks, such as one task from 08:00 to 08:30 and another task from 08:15 to 08:45. I would also add stronger validation for time input so users cannot enter invalid times.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned is that AI can help write code quickly, but the human still has to act as the lead architect. I had to decide which classes made sense, which suggestions were too complicated, and whether the final system matched the project requirements. Using separate phases helped keep the work organized because I could focus on design, implementation, testing, and polish one step at a time.