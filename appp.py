
import streamlit as st
import json
import os

st.set_page_config(
    page_title="My To-Do List",
    page_icon="📝",
    layout="centered"
)

FILE = "tasks.json"

# Load saved tasks
def load_tasks():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []

# Save tasks to JSON file
def save_tasks():
    with open(FILE, "w") as f:
        json.dump(st.session_state.tasks, f, indent=4)

# Initialize tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("📝 My To-Do List")
st.write("Manage your daily tasks easily!")

# Add new task
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Enter a new task")
    add_button = st.form_submit_button("➕ Add Task")

    if add_button:
        if new_task.strip():
            st.session_state.tasks.append({
                "task": new_task.strip(),
                "done": False
            })
            save_tasks()
            st.success("Task saved successfully!")
        else:
            st.warning("Please enter a task.")

st.divider()
st.subheader("📋 Your Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add your first task!")

# Display tasks
for i, item in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([5, 1])

    with col1:
        checked = st.checkbox(
            item["task"],
            value=item["done"],
            key=f"task_{i}"
        )

        if checked != item["done"]:
            st.session_state.tasks[i]["done"] = checked
            save_tasks()

    with col2:
        if st.button("🗑️", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            save_tasks()
            st.rerun()

# Progress tracker
total = len(st.session_state.tasks)
completed = sum(task["done"] for task in st.session_state.tasks)

if total > 0:
    st.divider()
    st.subheader("📊 Your Progress")
    st.progress(completed / total)
    st.write(f"{completed} out of {total} tasks completed.")
