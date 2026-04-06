"""PawPal+ Streamlit App - Smart Pet Care Management UI."""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Session State ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Parent")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling for happy, healthy pets.")

# --- Sidebar: Add Pet ---
with st.sidebar:
    st.header("➕ Add a Pet")
    with st.form("add_pet"):
        pet_name = st.text_input("Name")
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Fish", "Other"])
        age = st.number_input("Age", min_value=0, max_value=30, value=1)
        if st.form_submit_button("Add Pet"):
            if pet_name:
                owner.add_pet(Pet(name=pet_name, species=species, age=age))
                st.success(f"Added {pet_name}!")
            else:
                st.warning("Please enter a name.")

    if owner.pets:
        st.divider()
        st.header("📋 Schedule a Task")
        with st.form("add_task"):
            target_pet = st.selectbox("Pet", [p.name for p in owner.pets])
            desc = st.text_input("Task description")
            time_val = st.time_input("Time")
            freq = st.selectbox("Frequency", ["once", "daily", "weekly"])
            if st.form_submit_button("Add Task"):
                pet = owner.get_pet(target_pet)
                if pet and desc:
                    pet.add_task(Task(
                        description=desc,
                        time=time_val.strftime("%H:%M"),
                        frequency=freq,
                    ))
                    st.success(f"Task added for {target_pet}!")

# --- Main Area ---
if not owner.pets:
    st.info("Add a pet in the sidebar to get started!")
else:
    # Conflict warnings
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for c in conflicts:
            st.warning(c)

    # Today's schedule
    st.subheader("📅 Today's Schedule")
    todays = scheduler.get_todays_schedule()
    if todays:
        for task in todays:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(str(task))
            with col2:
                if not task.completed:
                    if st.button("Done", key=f"done-{id(task)}"):
                        pet = owner.get_pet(task.pet_name)
                        scheduler.mark_task_complete(task, pet)
                        st.rerun()
    else:
        st.write("No tasks scheduled for today.")

    # Pet overview
    st.subheader("🐾 Your Pets")
    for pet in owner.pets:
        with st.expander(str(pet)):
            pending = pet.get_pending_tasks()
            if pending:
                for t in pending:
                    st.write(str(t))
            else:
                st.write("All caught up! 🎉")
