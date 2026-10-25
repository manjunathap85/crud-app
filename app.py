import os

import psycopg
import streamlit as st
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "crud_learning_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        row_factory=dict_row,
    )


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )


def get_items() -> list[dict]:
    with get_connection() as connection:
        return connection.execute(
            "SELECT id, name, description, created_at FROM items ORDER BY id DESC"
        ).fetchall()


def create_item(name: str, description: str) -> None:
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s)",
            (name, description),
        )


def update_item(item_id: int, name: str, description: str) -> bool:
    with get_connection() as connection:
        item = connection.execute(
            """
            UPDATE items
            SET name = %s, description = %s
            WHERE id = %s
            RETURNING id
            """,
            (name, description, item_id),
        ).fetchone()
    return item is not None


def delete_item(item_id: int) -> bool:
    with get_connection() as connection:
        item = connection.execute(
            "DELETE FROM items WHERE id = %s RETURNING id",
            (item_id,),
        ).fetchone()
    return item is not None


def main() -> None:
    st.set_page_config(page_title="Items CRUD", page_icon="🗂️")
    st.title("Items CRUD")
    st.caption("A beginner-friendly CRUD app using Streamlit and PostgreSQL.")

    if not st.session_state.get("database_initialized"):
        initialize_database()
        st.session_state.database_initialized = True

    with st.form("create_item_form", clear_on_submit=True):
        st.subheader("Create an item")
        name = st.text_input("Name", max_chars=120)
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create item")

    if submitted:
        name = name.strip()
        if not name:
            st.error("Name is required.")
        else:
            create_item(name, description.strip())
            st.success("Item created.")
            st.rerun()

    st.subheader("Your items")
    items = get_items()
    st.caption(f"{len(items)} total")

    if not items:
        st.info("No items yet. Create one above to get started.")

    for item in items:
        item_id = item["id"]
        is_editing = st.session_state.get("editing_item_id") == item_id
        with st.container(border=True):
            columns = st.columns([5, 1, 1])
            with columns[0]:
                st.markdown(f"**{item['name']}**")
                st.write(item["description"] or "_No description_")
                st.caption(f"Created {item['created_at']:%Y-%m-%d %H:%M}")
            with columns[1]:
                if st.button("Edit", key=f"edit_{item_id}"):
                    st.session_state.editing_item_id = item_id
                    st.session_state.pending_delete_id = None
                    st.rerun()
            with columns[2]:
                if st.button("Delete", key=f"delete_{item_id}"):
                    st.session_state.pending_delete_id = item_id
                    st.session_state.editing_item_id = None
                    st.rerun()

            if is_editing:
                with st.form(f"edit_item_form_{item_id}"):
                    edited_name = st.text_input(
                        "Name", value=item["name"], max_chars=120
                    )
                    edited_description = st.text_area(
                        "Description", value=item["description"]
                    )
                    save = st.form_submit_button("Save changes")
                if save:
                    edited_name = edited_name.strip()
                    if not edited_name:
                        st.error("Name is required.")
                    elif update_item(item_id, edited_name, edited_description.strip()):
                        st.session_state.editing_item_id = None
                        st.success("Item updated.")
                        st.rerun()
                    else:
                        st.error("This item no longer exists.")
                if st.button("Cancel edit", key=f"cancel_edit_{item_id}"):
                    st.session_state.editing_item_id = None
                    st.rerun()

            if st.session_state.get("pending_delete_id") == item_id:
                st.warning(f"Delete **{item['name']}**? This cannot be undone.")
                confirm_column, cancel_column = st.columns(2)
                with confirm_column:
                    if st.button(
                        "Confirm delete",
                        key=f"confirm_delete_{item_id}",
                        type="primary",
                    ):
                        if delete_item(item_id):
                            st.session_state.pending_delete_id = None
                            st.success("Item deleted.")
                            st.rerun()
                        else:
                            st.error("This item no longer exists.")
                with cancel_column:
                    if st.button("Cancel", key=f"cancel_delete_{item_id}"):
                        st.session_state.pending_delete_id = None
                        st.rerun()


if __name__ == "__main__":
    main()
