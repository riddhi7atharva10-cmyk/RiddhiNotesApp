from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to Neon PostgreSQL
conn = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
""")
conn.commit()


@app.route("/")
def index():
    cursor.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]

    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s)",
        (title, content)
    )
    conn.commit()

    return redirect("/")


@app.route("/edit/<int:id>")
def edit(id):
    cursor.execute("SELECT * FROM notes WHERE id = %s", (id,))
    note = cursor.fetchone()
    return render_template("edit.html", note=note)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    title = request.form["title"]
    content = request.form["content"]

    cursor.execute(
        "UPDATE notes SET title = %s, content = %s WHERE id = %s",
        (title, content, id)
    )
    conn.commit()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM notes WHERE id = %s", (id,))
    conn.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
