import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler



st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=0)

if "pets" not in st.session_state:
    st.session_state.pets = []

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, age=pet_age)
    st.session_state.owner.add_pet(new_pet)
    st.session_state.pets = st.session_state.owner.get_pets()
    st.success(f"Added {new_pet.get_info()} to {owner.name}'s pets!")

current_pets = st.session_state.owner.get_pets()
if current_pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in current_pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

if st.button("Add task"):
    new_task = Task(
        title=task_title,
        duration=int(duration),
        priority=PRIORITY_MAP[priority],
        pet_name=pet_name,
    )
    matched_pet = next((p for p in current_pets if p.name == pet_name), None)
    if matched_pet:
        matched_pet.add_task(new_task)
    st.session_state.tasks.append(new_task)

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table([{"pet": t.pet_name, "title": t.title, "duration (min)": t.duration, "priority": t.priority} for t in st.session_state.tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
