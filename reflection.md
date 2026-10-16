# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

**Three core actions a user should be able to perform:**

1. **Add a pet** – enter basic owner and pet information (name, species, age) so the app knows who it is planning care for.
2. **Schedule a care task** – add a task such as a walk, feeding, medication, or grooming to a pet, with at least a duration and a priority.
3. **See today's plan** – generate a daily schedule that fits the owner's available time, puts the most important tasks first, and explains why it chose that plan.

**Initial UML design (four classes):**

- **Owner** – holds the owner's name, available_minutes_per_day, and preferences, pets. And the methods add_pet(), remove_pet(), and get_all_tasks()
- **Pet** – holds the pet's name, species, and age, and owns a list of tasks. And the methods add_task() , remove_task() and get_pending_tasks()
- **Task** – a single care activity with a title, category, duration in minutes, priority, and completed status. And method mark_complete()
- **Scheduler** – And methods __init__(), generate_daily_plan(), explain_plan()

Relationships: an Owner has many Pets, a Pet has many Tasks, and the Scheduler plans for one Owner and works with the Tasks that owner's pets need. The diagram is saved in `diagrams/uml_draft.mmd`.

**b. Design changes**

After writing the skeleton in `pawpal_system.py`, I asked my AI assistant to review it for missing relationships and logic bottlenecks. I made these changes based on its feedback:

- **Tasks now know their pet (`Task.pet_name`).** `Owner.get_all_tasks()` returns a flat list of tasks, so the scheduler had no way to say which pet a task was for, and the plan could only say "Walk" instead of "Walk Biscuit". `Pet.add_task` will fill this field in.
- **Added `PRIORITY_ORDER`.** Priority is a string ("low", "medium", "high"), which can't be sorted meaningfully on its own. A small mapping to numbers gives the scheduler something to sort by.
- **Scheduler now stores `plan` and `skipped`.** `explain_plan()` needs to say what was chosen and what didn't fit, but it had no access to that after `generate_daily_plan()` returned. Keeping both lists on the scheduler solves that without changing the method signatures.

I also updated `diagrams/uml_draft.mmd` to match.

Review points I noted but did **not** change yet:

- Choosing tasks to fit a time limit is a packing problem. A simple "highest priority first, skip what doesn't fit" approach is easy to explain but may leave time unused. I'll treat this as a tradeoff in section 2b.
- Tasks have no start time, so the plan is an ordered list, not a real schedule with clock times.
- `Pet.remove_task` will compare dataclass equality, so two identical tasks (e.g., two "Feeding" tasks) could be confused. Fix when implementing it.
- `Owner.preferences` is an unstructured list of strings, so the scheduler can't act on it yet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The priority since I created a dictionary for it

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
the scheduler is greedy. A big high-priority task can crowd out several smaller ones,
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I attempted or did follow the instructions correctly 
and process the code to do the task, then I would copy
the instructions into the AI assistent, which would confirm 
or improve bugs found in my code.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
when it earsed all my code in the scheduler class
because it was very off, and every time I did a while
loop, was replaced with a for loop.
funcitionally did the same, but the code provided was
cleaner, so kept it after verify the same results by
running the code.
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
