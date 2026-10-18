import re

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()


# --- Session "vault": create the Owner once, reuse it on every rerun ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=120)
owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes_per_day = int(
    st.number_input("Minutes available per day", min_value=1, max_value=1440,
                    value=owner.available_minutes_per_day)
)

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=40, value=1)
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name}!")

if owner.pets:
    st.write("Your pets:")
    st.table([{"name": p.name, "species": p.species, "age": p.age, "tasks": len(p.tasks)}
              for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")


st.markdown("### Tasks")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=False):
        target_name = st.selectbox("For which pet?", [p.name for p in owner.pets])
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            category = st.selectbox("Category", ["exercise", "feeding", "meds", "grooming", "other"])
        with col3:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        col5, col6, col7 = st.columns(3)
        with col5:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col6:
            frequency = st.selectbox("Repeats", ["daily", "weekly", "monthly", "once"])
        with col7:
            start_time = st.text_input("Start time (HH:MM, optional)", value="")
        if st.form_submit_button("Add task"):
            start_time = start_time.strip()
            if start_time and not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", start_time):
                st.error("Start time must look like 08:30 (24-hour HH:MM).")
            else:
                pet = next(p for p in owner.pets if p.name == target_name)
                pet.add_task(Task(title=task_title, category=category,
                                  duration_minutes=int(duration), priority=priority,
                                  frequency=frequency, start_time=start_time))
                st.success(f"Added '{task_title}' to {target_name}.")

    scheduler = Scheduler(owner)

    # --- Conflict warnings: shown first so the owner sees problems before the list ---
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning(
            f"{len(conflicts)} scheduling conflict(s) found. "
            "Change one task's start time or duration to fix each one."
        )
        for message in conflicts:
            st.warning(message, icon="⚠️")
    elif any(t.start_time for t in owner.get_all_tasks()):
        st.success("No time conflicts between your scheduled tasks.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Your tasks:")
        f1, f2 = st.columns(2)
        with f1:
            pet_filter = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
        with f2:
            status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

        shown = scheduler.filter_tasks(
            pet_name=None if pet_filter == "All" else pet_filter,
            completed={"All": None, "Pending": False, "Completed": True}[status_filter],
        )
        shown = scheduler.sort_by_time(shown)  # earliest first, unscheduled last

        if shown:
            st.table([{
                "time": f"{t.start_time}-{t.end_time}" if t.start_time else "unscheduled",
                "pet": t.pet_name,
                "title": t.title,
                "minutes": t.duration_minutes,
                "priority": t.priority,
                "repeats": t.frequency,
                "due": t.due_date.isoformat() if t.due_date else "",
                "done": "✅" if t.completed else "",
            } for t in shown])
        else:
            st.info("No tasks match these filters.")

        pending = scheduler.filter_tasks(completed=False)
        if pending:
            st.write("Mark a task complete:")
            labels = {id(t): f"{t.pet_name}: {t.title} ({t.start_time or 'unscheduled'})"
                      for t in pending}
            chosen = st.selectbox("Task", pending, format_func=lambda t: labels[id(t)])
            if st.button("Complete task"):
                pet = next(p for p in owner.pets if p.name == chosen.pet_name)
                next_task = pet.complete_task(chosen)
                if next_task:
                    st.success(f"Done! Next '{chosen.title}' is due {next_task.due_date}.")
                else:
                    st.success(f"Done! '{chosen.title}' won't repeat.")
                st.rerun()
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.caption("Add a pet first, then you can add tasks for it.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()
    if plan:
        used = sum(t.duration_minutes for t in plan)
        st.success(f"Planned {len(plan)} task(s): {used} of "
                   f"{owner.available_minutes_per_day} minutes used.")
        st.table([{"#": i, "pet": t.pet_name, "task": t.title,
                   "minutes": t.duration_minutes, "priority": t.priority}
                  for i, t in enumerate(plan, start=1)])
        if scheduler.skipped:
            st.warning("Not enough time for: " + ", ".join(
                f"{t.pet_name}'s {t.title} ({t.duration_minutes} min)"
                for t in scheduler.skipped))
    else:
        st.warning("Nothing to schedule. Add pets and tasks first.")
    with st.expander("Why this plan?"):
        st.text(scheduler.explain_plan())
