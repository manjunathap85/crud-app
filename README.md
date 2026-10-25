# Sample edit
# PostgreSQL CRUD Learning App

A small Streamlit app for learning Create, Read, Update, and Delete (CRUD) operations. It stores items in your local PostgreSQL database.

## 1. Create a PostgreSQL database

Make sure the PostgreSQL service on your desktop is running. In pgAdmin's Query Tool or `psql`, create the database:

```sql
CREATE DATABASE crud_learning_db;
```

The app creates its `items` table the first time it starts. The database user in `.env` needs permission to connect to `crud_learning_db` and create tables in its schema.

## 2. Configure your environment

Open PowerShell in this project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `DB_PASSWORD` to the password for your PostgreSQL user. Change `DB_USER` too if you do not use the `postgres` user. Keep `.env` private; it is excluded from Git. `.env.example` contains placeholders and is safe to commit.

The `.venv` directory is your Python virtual environment. The `.env` file stores the app's local database settings; they serve different purposes.

## 3. Start the app

With the virtual environment activated:

```powershell
streamlit run app.py
```

Streamlit will open the app in your browser.

If the connection fails, check that PostgreSQL is running, the database exists, and the host, port, database, user, and password in `.env` are correct. The terminal will show the database connection error.

## CRUD operations in this app

- **Create:** Submit the form on the home page.
- **Read:** The home page lists items from PostgreSQL.
- **Update:** Select **Edit**, change the fields, and save.
- **Delete:** Select **Delete** and confirm.

The SQL statements use parameters for user-entered values. The app and its database operations are in `app.py`.

## Start learning Git

Once the app is working, you can initialize a repository and inspect the files Git will track:

```powershell
git init
git status
```

`.gitignore` keeps `.env`, `.venv`, and Python cache files out of the repository.
