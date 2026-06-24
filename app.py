import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a pet owner track care tasks, organize them by time,
detect schedule conflicts, and handle recurring daily or weekly tasks.
"""
)

# Create owner once and keep it in Streamlit memory
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")


st.divider()

st.subheader("Owner Info")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

if st.button("Save owner"):
    st.session_state.owner.name = owner_name
    st.success(f"Owner saved: {st.session_state.owner.name}")


st.divider()

st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=1)

    submitted_pet = st.form_submit_button("Add pet")

    if submitted_pet:
        if pet_name.strip():
            new_pet = Pet(pet_name.strip(), species, int(age))
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added pet: {pet_name}")
        else:
            st.error("Please enter a pet name.")


if st.session_state.owner.pets:
    st.markdown("### Current Pets")

    pet_rows = []
    for pet in st.session_state.owner.pets:
        pet_rows.append(
            {
                "Name": pet.name,
                "Species": pet.species,
                "Age": pet.age,
                "Task Count": len(pet.tasks),
            }
        )

    st.table(pet_rows)
else:
    st.info("No pets added yet.")


st.divider()

st.subheader("Add a Task")

if st.session_state.owner.pets:
    pet_options = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Choose pet", pet_options)

    with st.form("add_task_form"):
        task_description = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Time", value="08:00")
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])

        submitted_task = st.form_submit_button("Add task")

        if submitted_task:
            selected_pet = None

            for pet in st.session_state.owner.pets:
                if pet.name == selected_pet_name:
                    selected_pet = pet

            if selected_pet and task_description.strip():
                new_task = Task(task_description.strip(), task_time.strip(), frequency)
                selected_pet.add_task(new_task)
                st.success(f"Added task for {selected_pet.name}: {task_description}")
            else:
                st.error("Please enter a task description.")
else:
    st.warning("Add a pet before adding tasks.")


st.divider()

st.subheader("Today's Schedule")

scheduler = Scheduler(st.session_state.owner)
schedule = scheduler.get_schedule()

if schedule:
    schedule_rows = []

    for pet, task in schedule:
        schedule_rows.append(
            {
                "Time": task.time,
                "Pet": pet.name,
                "Task": task.description,
                "Frequency": task.frequency,
                "Due Date": str(task.due_date),
                "Status": "Done" if task.completed else "Not done",
            }
        )

    st.table(schedule_rows)
else:
    st.info("No tasks scheduled yet.")


st.divider()

st.subheader("Conflict Warnings")

conflicts = scheduler.detect_conflicts()

if conflicts:
    for conflict in conflicts:
        st.warning(conflict)
else:
    st.success("No schedule conflicts found.")


st.divider()

st.subheader("Filter Tasks")

filter_choice = st.selectbox(
    "Show tasks by status",
    ["all", "incomplete", "completed"],
)

if filter_choice == "completed":
    filtered_tasks = scheduler.filter_tasks(completed=True)
elif filter_choice == "incomplete":
    filtered_tasks = scheduler.filter_tasks(completed=False)
else:
    filtered_tasks = scheduler.get_schedule()

if filtered_tasks:
    filtered_rows = []

    for pet, task in filtered_tasks:
        filtered_rows.append(
            {
                "Time": task.time,
                "Pet": pet.name,
                "Task": task.description,
                "Frequency": task.frequency,
                "Due Date": str(task.due_date),
                "Status": "Done" if task.completed else "Not done",
            }
        )

    st.table(filtered_rows)
else:
    st.info("No tasks match this filter.")


st.divider()

st.subheader("Mark Task Complete")

if schedule:
    incomplete_tasks = [
        (pet, task)
        for pet, task in schedule
        if not task.completed
    ]

    if incomplete_tasks:
        task_labels = [
            f"{pet.name} - {task.description} at {task.time}"
            for pet, task in incomplete_tasks
        ]

        selected_task_label = st.selectbox("Choose task to complete", task_labels)

        if st.button("Mark selected task complete"):
            selected_index = task_labels.index(selected_task_label)
            selected_pet, selected_task = incomplete_tasks[selected_index]

            scheduler.mark_task_complete(selected_pet.name, selected_task.description)

            st.success(
                f"Completed {selected_task.description}. "
                "If it is recurring, the next task was added."
            )

            st.rerun()
    else:
        st.success("All tasks are complete.")
else:
    st.info("Add tasks before marking anything complete.")