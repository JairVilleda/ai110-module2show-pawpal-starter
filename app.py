import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state initialization ---
# owners: list of {"owner": Owner, "scheduler": Scheduler, "tasks": list[Task]}
if "owners" not in st.session_state:
    st.session_state.owners = []

st.title("🐾 PawPal+")

st.divider()

# ─── Add Owner ───────────────────────────────────────────────────────────────
st.subheader("Owners")

col1, col2 = st.columns(2)
with col1:
    new_owner_name = st.text_input("Owner name")
with col2:
    available_time = st.number_input("Available time (minutes)", min_value=1, max_value=1440, value=120)

if st.button("Add Owner"):
    if not new_owner_name.strip():
        st.error("Owner name is required.")
    elif any(e["owner"].name == new_owner_name.strip() for e in st.session_state.owners):
        st.error(f"An owner named '{new_owner_name.strip()}' already exists.")
    else:
        owner_obj = Owner(name=new_owner_name.strip(), available_time=int(available_time))
        st.session_state.owners.append({
            "owner": owner_obj,
            "scheduler": Scheduler(owner=owner_obj),
            "tasks": [],
        })
        st.success(f"Added owner '{owner_obj.name}'.")

if st.session_state.owners:
    st.write("Current owners:")
    st.table([
        {"name": e["owner"].name, "available time (min)": e["owner"].available_time}
        for e in st.session_state.owners
    ])

    # --- Update available time ---
    st.markdown("**Update available time**")
    edit_owner_name = st.selectbox("Select owner to update", options=[e["owner"].name for e in st.session_state.owners], key="edit_time_owner")
    new_time = st.number_input("New available time (minutes)", min_value=1, max_value=1440, value=120, key="new_available_time")
    if st.button("Update Available Time"):
        entry = next(e for e in st.session_state.owners if e["owner"].name == edit_owner_name)
        entry["owner"].update_available_time(int(new_time))
        st.success(f"Updated {edit_owner_name}'s available time to {new_time} min.")

else:
    st.info("No owners yet. Add one above.")

st.divider()

# ─── Add Pet ─────────────────────────────────────────────────────────────────
st.subheader("Pets")

owner_names = [e["owner"].name for e in st.session_state.owners]

if not owner_names:
    st.info("Add an owner first before adding pets.")
else:
    selected_owner_for_pet = st.selectbox("Select owner", options=owner_names, key="pet_owner_select")
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=0)

    if st.button("Add Pet"):
        if not pet_name.strip():
            st.error("Pet name is required.")
        else:
            entry = next(e for e in st.session_state.owners if e["owner"].name == selected_owner_for_pet)
            owner_obj = entry["owner"]
            new_pet = Pet(name=pet_name.strip(), species=species, age=pet_age)
            owner_obj.add_pet(new_pet)
            st.success(f"Added {new_pet.get_info()} to {owner_obj.name}'s pets.")

    # Show all owners' pets with remove option
    for entry in st.session_state.owners:
        pets = entry["owner"].get_pets()
        if pets:
            st.write(f"**{entry['owner'].name}'s pets:**")
            for pet in list(pets):
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.write(pet.get_info())
                with col_btn:
                    if st.button("Remove", key=f"remove_pet_{entry['owner'].name}_{pet.name}"):
                        entry["owner"].remove_pet(pet)
                        entry["tasks"] = [t for t in entry["tasks"] if t.pet_name != pet.name]
                        st.success(f"Removed {pet.name} from {entry['owner'].name}'s pets.")
                        st.rerun()

st.divider()

# ─── Add Task ────────────────────────────────────────────────────────────────
st.subheader("Tasks")

all_pets = [(e["owner"].name, p) for e in st.session_state.owners for p in e["owner"].get_pets()]

if not all_pets:
    st.info("Add at least one pet before adding tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        preferred_time = st.selectbox("Preferred time", ["(none)", "morning", "afternoon", "evening"])
    with col5:
        pet_options = [f"{owner_name} — {p.name}" for owner_name, p in all_pets]
        task_pet_selection = st.selectbox("Assign to pet", options=pet_options)

    frequency = st.selectbox("Recurring", ["(none)", "daily", "weekly"])

    PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

    if st.button("Add task"):
        if not task_title.strip():
            st.error("Task title is required.")
        else:
            selected_owner_name, selected_pet_name = task_pet_selection.split(" — ", 1)
            entry = next(e for e in st.session_state.owners if e["owner"].name == selected_owner_name)
            matched_pet = next(p for p in entry["owner"].get_pets() if p.name == selected_pet_name)
            new_task = Task(
                title=task_title.strip(),
                duration=int(duration),
                priority=PRIORITY_MAP[priority],
                pet_name=selected_pet_name,
                preferred_time=preferred_time if preferred_time != "(none)" else None,
                frequency=frequency if frequency != "(none)" else None,
                due_date=date.today() if frequency != "(none)" else None,
            )
            matched_pet.add_task(new_task)
            entry["tasks"].append(new_task)
            st.success(f"Added task '{new_task.title}' for {selected_pet_name} ({selected_owner_name}).")

    # Show tasks grouped by owner with remove option
    for entry in st.session_state.owners:
        if entry["tasks"]:
            st.write(f"**{entry['owner'].name}'s tasks:**")
            for task in list(entry["tasks"]):
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.write(str(task) + (f" [{task.frequency}]" if task.frequency else ""))
                with col_btn:
                    if st.button("Remove", key=f"remove_task_{entry['owner'].name}_{task.pet_name}_{task.title}"):
                        matched_pet = next(
                            (p for p in entry["owner"].get_pets() if p.name == task.pet_name), None
                        )
                        if matched_pet:
                            matched_pet.remove_task(task)
                        entry["tasks"].remove(task)
                        st.success(f"Removed task '{task.title}'.")
                        st.rerun()

st.divider()

# ─── Build Schedule ───────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if not st.session_state.owners:
    st.info("Add an owner to generate a schedule.")
else:
    schedule_owner_name = st.selectbox("Select owner to schedule", options=owner_names, key="schedule_owner_select")
    schedule_entry = next(e for e in st.session_state.owners if e["owner"].name == schedule_owner_name)
    schedule_owner = schedule_entry["owner"]
    scheduler = schedule_entry["scheduler"]

    col_a, col_b = st.columns(2)
    with col_a:
        schedule_pet_names = [p.name for p in schedule_owner.get_pets()]
        filter_pet = st.selectbox(
            "Filter by pet",
            options=["All pets"] + schedule_pet_names,
        )
    with col_b:
        current_time_block = st.selectbox(
            "Current time of day",
            options=["(none)", "morning", "afternoon", "evening"],
            key="time_block_select",
        )

    filter_completed = st.radio(
        "Filter by completion",
        options=["All", "Pending", "Completed"],
        horizontal=True,
    )
    if st.button("Generate Schedule"):
        if not schedule_owner.get_pets():
            st.error(f"{schedule_owner_name} has no pets. Add a pet first.")
        elif not schedule_entry["tasks"]:
            st.error(f"{schedule_owner_name} has no tasks. Add a task first.")
        else:
            time_block = current_time_block if current_time_block != "(none)" else None
            scheduler.generate_plan(owner=schedule_owner, current_time_block=time_block)
            st.session_state["last_schedule_owner"] = schedule_owner_name

    # Show schedule if one has been generated for the selected owner
    if st.session_state.get("last_schedule_owner") == schedule_owner_name and scheduler.get_plan():
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.markdown("#### Conflicts Detected")
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No scheduling conflicts found.")

        pet_filter_value = None if filter_pet == "All pets" else filter_pet
        completed_filter_value = (
            None if filter_completed == "All"
            else filter_completed == "Completed"
        )
        filtered_tasks = scheduler.filter_tasks(
            pet_name=pet_filter_value,
            completed=completed_filter_value,
        )

        sorted_tasks = scheduler.sort_by_time()
        sorted_tasks = [t for t in sorted_tasks if t in filtered_tasks]

        st.markdown(f"#### {schedule_owner_name}'s Planned Tasks (chronological order)")
        if sorted_tasks:
            st.table([
                {
                    "Pet": t.pet_name,
                    "Task": t.title,
                    "Time": t.preferred_time or "anytime",
                    "Duration (min)": t.duration,
                    "Priority": t.priority,
                    "Completed": "✅" if t.is_completed else "Pending",
                }
                for t in sorted_tasks
            ])
        else:
            st.info("No tasks match the current filters.")

        with st.expander("Scheduling explanation"):
            for line in scheduler.explain_plan():
                st.write(line)

        # --- Mark Task Complete ---
        st.markdown("#### Mark Task Complete")
        pending_tasks = [t for t in scheduler.get_plan() if not t.is_completed]
        if not pending_tasks:
            st.info("All tasks are completed.")
        else:
            task_labels = [f"{t.pet_name} — {t.title}" for t in pending_tasks]
            selected_label = st.selectbox("Select a task to mark complete", options=task_labels, key="complete_select")
            if st.button("Mark Complete"):
                selected_task = pending_tasks[task_labels.index(selected_label)]
                next_task = scheduler.complete_task(selected_task, owner=schedule_owner)
                if next_task:
                    schedule_entry["tasks"].append(next_task)
                    st.success(f"'{selected_task.title}' marked complete. Next occurrence scheduled for {next_task.due_date}.")
                else:
                    st.success(f"'{selected_task.title}' marked complete.")
