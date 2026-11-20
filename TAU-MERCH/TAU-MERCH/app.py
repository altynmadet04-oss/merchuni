
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "tau_merch_secret_key_2026"

products = [
    {"id": 1, "name": "TAU Hoodie", "category": "Одежда", "price": 15000, "sizes": ["XS", "S", "M", "L", "XL", "XXL"], "image": "hoodie.jpg"},
    {"id": 2, "name": "TAU T-Shirt", "category": "Одежда", "price": 8000, "sizes": ["XS", "S", "M", "L", "XL", "XXL"], "image": "tshirt.jpg"},
    {"id": 3, "name": "TAU Sweatshirt", "category": "Одежда", "price": 13000, "sizes": ["XS", "S", "M", "L", "XL", "XXL"], "image": "sweatshirt.jpg"},
    {"id": 4, "name": "TAU Cap", "category": "Аксессуары", "price": 5000, "sizes": ["One Size"], "image": "cap.jpg"},
    {"id": 5, "name": "TAU Shopper", "category": "Аксессуары", "price": 4500, "sizes": ["One Size"], "image": "shopper.jpg"},
    {"id": 6, "name": "TAU Notebook", "category": "Канцелярия", "price": 2500, "sizes": ["One Size"], "image": "notebook.jpg"},
    {"id": 7, "name": "TAU Mug", "category": "Сувениры", "price": 3500, "sizes": ["One Size"], "image": "mug.jpg"},
    {"id": 8, "name": "TAU Bottle", "category": "Спорт", "price": 4000, "sizes": ["One Size"], "image": "bottle.jpg"},
    {"id": 9, "name": "TAU Windbreaker", "category": "Верхняя одежда", "price": 18000, "sizes": ["S", "M", "L", "XL", "XXL"], "image": "windbreaker.jpg"}
]


@app.route("/")
def index():
    category = request.args.get("category", "Все")
    filtered = products if category == "Все" else [
        p for p in products if p["category"] == category
    ]

    return render_template(
        "index.html",
        products=filtered,
        categories=["Все", "Одежда", "Верхняя одежда",
                    "Аксессуары", "Канцелярия", "Сувениры", "Спорт"],
        selected_category=category
    )


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = int(request.form["product_id"])
    size = request.form["size"]

    product = next((p for p in products if p["id"] == product_id), None)

    if product and size in product["sizes"]:
        cart = session.get("cart", [])
        cart.append({"product_id": product_id, "size": size})
        session["cart"] = cart

    return redirect(url_for("index"))


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    items = []
    total = 0

    for item in cart_items:
        product = next(
            (p for p in products if p["id"] == item["product_id"]), None
        )
        if product:
            items.append({
                "product": product,
                "size": item["size"]
            })
            total += product["price"]

    return render_template("cart.html", items=items, total=total)


@app.route("/remove/<int:index>")
def remove_item(index):
    cart = session.get("cart", [])

    if 0 <= index < len(cart):
        cart.pop(index)
        session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
def checkout():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()

    if not name or not phone or not session.get("cart"):
        return redirect(url_for("cart"))

    session["last_order"] = {
        "name": name,
        "phone": phone
    }
    session["cart"] = []

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "tau123":
            session["admin"] = True
            return redirect(url_for("admin"))

        error = "Неправильный логин или пароль"

    return render_template("login.html", error=error)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    return render_template("admin.html", products=products)


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)