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

Relationships: an Owner has many Pets, a Pet has many Tasks, and the Scheduler plans for one Owner and works with the Tasks that owner's pets need. The diagram is saved in `diagrams/uml_draft.mmd`. The final version, with the methods and fields added later (sorting, filtering, conflict detection, recurrence, start times), is in `diagrams/uml_final.mmd`.

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
ut this is reasonable because it's easy to explain to a pet owner and high-priority care like medication should never be dropped for convenience."
also the conflict tradeoff: "detect_conflicts only warns and doesn't change the plan, and generate_daily_plan ignores start times. That keeps the logic simple and never blocks the owner, but the generated plan can still contain overlapping tasks."
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

**c. AI strategy**

*Which AI features were most effective for building the scheduler?*

- **Design review of my own skeleton.** Asking the assistant to look for missing relationships and bottlenecks gave me concrete fixes (`Task.pet_name`, `PRIORITY_ORDER`, storing `plan` and `skipped`) before I wrote any scheduling logic.
- **Working from the real file.** Attaching `pawpal_system.py` and asking for test cases and UML updates produced answers tied to my actual code. For example, the review of the code noticed that `mark_complete()` counts from today's date rather than the task's due date, and that `detect_conflicts` ignores zero-duration tasks.
- **Running the code, not just writing it.** The assistant ran the tests and `main.py` and showed the real output, so the README output and the "12 passed" result come from actual runs.

*One suggestion I rejected or modified:*

At one point the assistant rewrote my whole `Scheduler` class. It was off from what I intended, and it had swapped every `while` loop for a `for` loop. I did not accept it as-is. I compared the result with my version and ran the code to confirm the output was identical. Only then did I keep the cleaner loops, and I discarded the rest of the rewrite so the design stayed the one I had drawn in the UML.

*How separate chat sessions for different phases helped:*

Each phase (design and UML, scheduling logic, testing, UI, documentation) had its own goal and its own files. Starting a fresh session for each one meant the assistant was not carrying old assumptions about the code. For testing, a clean session treated my code as a stranger would, which is closer to how a reviewer will read it. It also kept each conversation short enough that I could trace which decision came from where.

*What I learned about being the lead architect:*

The assistant is fast at producing code, but it does not know what I intend. My job was to decide the design (four classes, greedy planning, warn-only conflicts), then judge each suggestion against it. A suggestion can be correct and still wrong for the design. Being lead architect means writing the UML first, giving the assistant narrow tasks, asking for options instead of letting it change files unprompted, and verifying every change by running tests.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
test that the code and run and the expect output is displayed for owner, pet ant task
the more important tasks generated in the schedular are tested for real suite checks sorting, recurrence and conflict detection,

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
that a schedular will display no conflict schedule with alot time best can be, but if I had more time, I would try to incorperate more task flagged out for having conflict of time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The UI displaying the add pet and add task and schedule displayed

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
how a owner is created or more owner to choose from the code, and similar redesign on how a pet is initiallized to create more on the UI side.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The AI was able to stream line debugging my intial work, but some times when giving the prompts, AI would create thing different or other things not intended. However, when reviewing it, it was good, so kept. For example in this relection.md AI assistent gave 3.c and after reviewing I kept it, but this not building my self is not good, so need to verify everything to ensure security and it is still good code. As a good principle I think I will need to use more since AI assistent are likely to be used more. Thus, at least will always ask for permission to do anything first and provide options that I as software developer can evaluate to move in the direction I intend.
