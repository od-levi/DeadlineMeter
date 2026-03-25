import streamlit as st
from datetime import date, datetime
from utils.task_manager import add_task, delete_task, mark_task_done, restore_task
from utils.layout import style_task_card, style_done_task
from utils.data_storage import load_data, add_task_db, delete_task_db, update_task_db

# Initialize session state attributes
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

if "done_tasks" not in st.session_state:
    st.session_state["done_tasks"] = []

# Your existing code continues...
user = st.text_input("Enter your name")

# Load from Supabase
if user:
    tasks = load_data(user)

    for t in tasks:
        t["deadline"] = datetime.fromisoformat(t["deadline"]).date()

    st.session_state['tasks'] = tasks
else:
    st.stop()


st.title("⏳ Deadline Meter")

# Input section
col1, col2 = st.columns(2)
with col1:
    task_name = st.text_input("Task name", placeholder="e.g. Math assignment")
with col2:
    deadline = st.date_input("Deadline date", min_value=date.today())

# Add task
if st.button("Add Task"):
    if task_name:
        # create task locally first (reuse your logic)
        add_task(st.session_state, task_name, deadline)

        # get the LAST added task
        new_task = st.session_state.tasks[-1]

        # save to DB
        add_task_db(user, new_task)

        st.rerun()

# Warning for panic tasks
panic_tasks = [t for t in st.session_state.tasks if t["status"] == "Panic"]
if len(panic_tasks) > 0:
    st.warning(f"⚠ You have {len(panic_tasks)} task(s) in Panic mode! Time to focus!")

# Sort tasks by days_left
st.session_state.tasks.sort(key=lambda x: x['days_left'])

# Display Tasks in columns
num_columns = 3
for i in range(0, len(st.session_state.tasks), num_columns):
    cols = st.columns(num_columns)
    for j, t in enumerate(st.session_state.tasks[i:i+num_columns]):
        with cols[j]:
            # Use layout styles
            style = style_task_card()

            # Top row with task name and buttons
            col_task, col_delete, col_done = st.columns([4, 1, 1])

            with col_task:
                st.write(f"**{t['name']}**")

            with col_delete:
                if st.button("🗑", key=f"delete_{t['id']}", help="Delete task"):
                    delete_task_db(t["id"])
                    st.rerun()

            with col_done:
                if st.button("✔", key=f"done_{t['id']}", help="Mark task as done"):
                    mark_task_done(st.session_state, t)
                    update_task_db(t["id"], {
                        "status": "Done"
                    })

                    st.rerun()

            # Restore from done if applicable
            if "done" in st.session_state and t.get("restorable", True):
                if st.button("🔄 Restore", key=f"restore_{t['id']}"):
                    restore_task(st.session_state, t)
                    update_task_db(t["id"], {
                        "status": t["status"]
                    })

                    st.rerun()

            # Display task details
            st.markdown(
                f"""
                <div style="
                    background-color:{style['background_color']};
                    padding:{style['padding']};
                    border-radius:{style['border_radius']};
                    margin-bottom:{style['margin_bottom']};
                ">
                    <p style="margin:5px 0">Days left: {t['days_left']}</p>
                    <p style="margin:5px 0">Deadline: {t['deadline'].strftime('%B %d, %Y')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Status indicator
            if t["status"] == "Chill":
                st.success("Chill")
            elif t["status"] == "Start Planning":
                st.warning("Start Planning")
            elif t["status"] == "Panic":
                st.error("Panic")
            else:
                st.error("Missed deadline")


# Show completed tasks
if st.session_state.done_tasks:
    st.markdown("## Completed Tasks")
    for t in reversed(st.session_state.done_tasks):
        style = style_done_task()
        st.markdown(
            f"""
            <div style="
                background-color:{style['background_color']};
                color:{style['color']};
                padding:{style['padding']};
                border-radius:{style['border_radius']};
                margin-bottom:{style['margin_bottom']};
            ">
                <h4 style="margin:0; text-decoration: line-through;">{t['name']}</h4>
                <p style="margin:5px 0">Deadline: {t['deadline'].strftime('%B %d, %Y')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Button to restore from done
        if st.button(f"Restore '{t['name']}'", key=f"restore_done_{t['id']}"):
            restore_task(st.session_state, t)
            update_task_db(t["id"], {
                "status": t["status"]
            })

            st.rerun()