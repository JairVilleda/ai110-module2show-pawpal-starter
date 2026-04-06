# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
I included the 4 classes: Owner, Per, Task, Scheduler
The Owner class stores owner info, available time, preferences, and their pets. It manages adding and listing pets. The Pet class holds basic pet info like the name, species, and age. The Task class represents a care task with a title, duration, priority, pet assignment, and preferred time. The Scheduler manages tasks, generates a daily plan based on priorities and constraints, and provides an explanation for scheduling decisions. 
An Owner owns multiple pets
A Pet has multiple tasks
The Scheduler schedules Tasks to create the daily plan

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design changed slightly during implementation. One key change was that the Scheduler class originally had no reference to the owner, which made it harder to acces the owner's available time and preferences when generating a plan. I updated Scheduler to optionally store an Owner and also allow passing an Owner as a parameter to generate_plan(). This ensures that the Scheduler can always consider constraints and priorities correctly when creating the daily schedule.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler considers:
    Available time: tasks only fit within the owner's remaining minutes
    Priority: tasks with higher priority are scheduled first
    Preferred time blocks: morning, afternoon, and evening preferences slightly boost priority
    Recurring tasks: daily or weekly tasks automatically generate the next occurence when completed
I prioritized constraints based on what impacts the owner's ability to carte for pets most directly. Time was the hard limit while priority and preferred time were soft constraints to guide the ordering

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff in my scheduler is in the conflict detection algorithm. I replaced a nested loop approach with itertools.combinations, which generates pairs of tasks more cleanly and makes the code easier to understand. However, this approach introduces a dependency on the itertools module and may be less intuitive for someone unfamiliar with it. Both approaches have the same performance but I chose combinations because it improves readability

---

## Smarter Scheduling

New algorithmic improvements to make scheduling more intelligent

- Sorting by Time: Tasks are ordered by preferred time blocks (morning, afternoon, evening) for better organization
- Filtering Tasks: Tasks can be filtered by pet or completion status for easier viewing
- Recurring Tasks: Daily and weekly tasks automatically generate their next occurrence when completed.
- Conflict Detection: The system detects tasks scheduled in the same time block and returns warnings instead of failing

---

## Testing PawPal+

The automated tests for PawPal+ to verify core behaviors:

- Sorting correctness: Tasks are correctly ordered by preferred_time (morning → afternoon → evening)  
- Recurrence logic: Completing a daily task automatically creates the next occurrence for the following day  
- Conflict detection: Scheduler flags tasks that share the same preferred_time

Confidence Level: 4/5 stars
All automated tests pass and the system handles typical edge cases like overlapping tasks and recurring tasks. However, more complex scenarios like overlapping durations or multiple pets with simultaneous tasks could be tested further

Run Tests
```bash
python -m pytest

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used Claude to brainstorm, draft, and refactor methods for the Scheduler, Pet, and Task classes. The inline code suggests were very useful for implementing algorithms like sorting by time, detecting conflicts, and generating recurring tasks. The chat sessions helped me understand the project and plan before any coding.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One moment where I did not accept Claude's suggestion was when it recommended adding recurring tasks directly to the Scheduler.plan instead of the pet’s task list. I realized that doing so would cause the task to disappear from the pet’s permanent record. To verify this, I reviewed the code and ran a small test marking a daily task complete to see if the next occurrence appeared with the pet. I then modified the implementation so that the next occurrence is correctly added to the pet’s task list.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested completing tasks and making sure daily and weekly tasks generate the next occurrence correctly. I also tested that tasks are sorted by time and can be filtered by pet or completion status. I verified that the scheduler detects conflicts when tasks share the same time block. These tests ensured the core scheduling logic works as intended and that pets’ tasks are not lost.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
Considering this is my first time designing a management system with algorithmic logic, I am fairly confident that the scheduler works correctly for typical use. If I had more time, I would test cases with multiple pets, overlapping tasks, and recurring tasks completed more than once in a day. I would test more extreme cases that would probably come up after multiple uses.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with how the integrates all the mutliple features smoothly. For example. the tasks are correctly prioritized and conflicts are clearly flagged. The system works consistently and the interface makes it easy to see the schedule. Overall I am proud because in the beginning I was not sure on how I was going to start and implement all of these features.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteraton, I would improve the layout of the generated schedule. As of now, the generated plan follows a simple structure of morning, afternoon, and evening sections with the tasks ordered. I would redesign it closer to a real schedule with time slots. For example, the owner would identify all the time slots they have available for their pets and then the tasks would fill those time slots while also considering the duration of each. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that being a lead architect means making thoughtful decisions about AI suggestions, verifying them, and integrating them in a way that keeps the system reliable. AI is a very useful tool to brainstorm and plan before any implemenation, which could save a lot of error and time.