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
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            category = st.selectbox("Category", ["exercise", "feeding", "meds", "grooming", "other"])
        with col3:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col4:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        if st.form_submit_button("Add task"):
            pet = next(p for p in owner.pets if p.name == target_name)
            pet.add_task(Task(title=task_title, category=category,
                              duration_minutes=int(duration), priority=priority))
            st.success(f"Added '{task_title}' to {target_name}.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([{"pet": t.pet_name, "title": t.title, "category": t.category,
                   "minutes": t.duration_minutes, "priority": t.priority}
                  for t in all_tasks])
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
        st.table([{"#": i, "pet": t.pet_name, "task": t.title,
                   "minutes": t.duration_minutes, "priority": t.priority}
                  for i, t in enumerate(plan, start=1)])
    else:
        st.warning("Nothing to schedule. Add pets and tasks first.")
    st.text(scheduler.explain_plan())
