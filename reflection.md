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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
