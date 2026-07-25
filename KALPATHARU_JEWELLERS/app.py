from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "kalpatharu_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/gold")
def gold():
    connection = sqlite3.connect("jewellery.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE category='Gold'")
    products = cursor.fetchall()

    connection.close()

    return render_template("gold.html", products=products)


@app.route("/silver")
def silver():
    connection = sqlite3.connect("jewellery.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE category='Silver'")
    products = cursor.fetchall()

    connection.close()

    return render_template("silver.html", products=products)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")

    connection = sqlite3.connect("jewellery.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        ('%' + query + '%',)
    )

    products = cursor.fetchall()

    connection.close()

    return render_template("search.html", products=products, query=query)
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "Kalpatharu@123" and password == "9490087011":
            session["admin"] = True
            return redirect("/admin")

        return "Invalid Username or Password"

    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        weight = request.form["weight"]
        price = request.form["price"]

        image = request.files["image"]

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join("static", "uploads", filename))
            image_path = filename
        else:
            image_path = ""

        connection = sqlite3.connect("jewellery.db")
        cursor = connection.cursor()

        cursor.execute(
    "INSERT INTO products (name, category, weight, price, image) VALUES (?, ?, ?, ?, ?)",
    (name, category, weight, price, image_path)
)

        connection.commit()
        connection.close()

        return redirect("/admin")

    connection = sqlite3.connect("jewellery.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    return render_template("admin.html", products=products)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("jewellery.db")
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        product_type = request.form["type"]
        weight = request.form["weight"]
        price = request.form["price"]
        image = request.files["image"]

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join("static", "uploads", filename))

            cursor.execute(
                "UPDATE products SET name=?, category=?, weight=?, price=?, image=? WHERE id=?",
                (name, category, weight, price, filename, id)
            )
        else:
            cursor.execute(
                "UPDATE products SET name=?, category=?, weight=?, price=? WHERE id=?",
                (name, category, weight, price, id)
            )

        connection.commit()
        connection.close()
        return redirect("/admin")

    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cursor.fetchone()

    connection.close()

    return render_template("edit.html", product=product)

@app.route("/delete/<int:id>")
def delete(id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("jewellery.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (id,))

    connection.commit()
    connection.close()

    return redirect("/admin")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)