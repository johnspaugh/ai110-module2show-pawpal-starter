# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

**Three core actions a user should be able to perform:**

1. **Add a pet** – enter basic owner and pet information (name, species, age) so the app knows who it is planning care for.
2. **Schedule a care task** – add a task such as a walk, feeding, medication, or grooming to a pet, with at least a duration and a priority.
3. **See today's plan** – generate a daily schedule that fits the owner's available time, puts the most important tasks first, and explains why it chose that plan.

**Initial UML design (four classes):**

- **Owner** – holds the owner's name, daily time available, and preferences, and owns a list of pets. It can add or remove pets and collect all tasks across its pets.
- **Pet** – holds the pet's name, species, and age, and owns a list of tasks. It can add or remove tasks and list the ones still pending.
- **Task** – a single care activity with a title, category, duration in minutes, priority, and completed status. It can mark itself complete.
- **Scheduler** – takes an owner and builds the daily plan by selecting and ordering tasks by priority within the available time, and explains its reasoning.

Relationships: an Owner has many Pets, a Pet has many Tasks, and the Scheduler plans for one Owner and works with the Tasks that owner's pets need. The diagram is saved in `diagrams/uml_draft.mmd`.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
