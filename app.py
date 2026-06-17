import os
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "demo"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password")
    )

@app.route("/", methods=["GET", "POST"])
def home():

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]

        cur.execute(
            "INSERT INTO visitors(name) VALUES(%s)",
            (name,)
        )

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/")

    cur.execute(
        "SELECT * FROM visitors ORDER BY id DESC"
    )

    visitors = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        visitors=visitors
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    echo "# test" >> app.py