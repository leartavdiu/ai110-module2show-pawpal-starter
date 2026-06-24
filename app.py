import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This app helps a pet owner keep track of pet care tasks and generate a simple daily schedule.
"""
)

# Session state setup
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
            new_pet = Pet(pet_name, species, int(age))
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added pet: {pet_name}")
        else:
            st.error("Please enter a pet name.")


if st.session_state.owner.pets:
    st.markdown("### Current Pets")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
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
                new_task = Task(task_description, task_time, frequency)
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
    for pet, task in schedule:
        status = "Done" if task.completed else "Not done"
        st.write(
            f"**{task.time}** - {pet.name} ({pet.species}): "
            f"{task.description} [{task.frequency}] - {status}"
        )
else:
    st.info("No tasks scheduled yet.")