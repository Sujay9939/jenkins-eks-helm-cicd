from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

products = [
    {
        "id": 1,
        "name": "Premium Wireless Headphones",
        "price": 2999,
        "rating": 4.8,
        "category": "Electronics",
        "emoji": "🎧",
        "description": "Immersive sound with active noise cancellation."
    },
    {
        "id": 2,
        "name": "Smart Watch Pro",
        "price": 4999,
        "rating": 4.7,
        "category": "Electronics",
        "emoji": "⌚",
        "description": "Fitness tracking, notifications and modern design."
    },
    {
        "id": 3,
        "name": "Urban Running Shoes",
        "price": 2499,
        "rating": 4.6,
        "category": "Fashion",
        "emoji": "👟",
        "description": "Comfortable lightweight shoes for everyday running."
    },
    {
        "id": 4,
        "name": "Classic Denim Jacket",
        "price": 1999,
        "rating": 4.5,
        "category": "Fashion",
        "emoji": "🧥",
        "description": "Classic denim style for casual everyday wear."
    },
    {
        "id": 5,
        "name": "Premium Coffee Maker",
        "price": 3499,
        "rating": 4.8,
        "category": "Home",
        "emoji": "☕",
        "description": "Brew rich and delicious coffee at home."
    },
    {
        "id": 6,
        "name": "Minimal Desk Lamp",
        "price": 1299,
        "rating": 4.4,
        "category": "Home",
        "emoji": "💡",
        "description": "Modern LED desk lamp for your workspace."
    },
    {
        "id": 7,
        "name": "Travel Backpack",
        "price": 1799,
        "rating": 4.6,
        "category": "Travel",
        "emoji": "🎒",
        "description": "Spacious and durable backpack for travel."
    },
    {
        "id": 8,
        "name": "Smart Bluetooth Speaker",
        "price": 2299,
        "rating": 4.7,
        "category": "Electronics",
        "emoji": "🔊",
        "description": "Powerful wireless audio with deep bass."
    }
]

cart = {}


HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>NovaCart - Modern E-Commerce</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #1f2937;
        }

        header {
            background: #111827;
            color: white;
            padding: 18px 6%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 28px;
            font-weight: bold;
        }

        .logo span {
            color: #60a5fa;
        }

        .cart-button {
            border: none;
            background: #2563eb;
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 15px;
        }

        .hero {
            padding: 70px 6%;
            background: linear-gradient(135deg, #111827, #2563eb);
            color: white;
            text-align: center;
        }

        .hero h1 {
            font-size: 48px;
            margin-bottom: 15px;
        }

        .hero p {
            font-size: 18px;
            opacity: 0.9;
        }

        .search-container {
            max-width: 700px;
            margin: 30px auto 0;
        }

        #search {
            width: 100%;
            padding: 16px 20px;
            border-radius: 30px;
            border: none;
            font-size: 16px;
            outline: none;
        }

        .categories {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            padding: 30px 6%;
        }

        .category-btn {
            padding: 10px 20px;
            border-radius: 25px;
            border: 1px solid #d1d5db;
            background: white;
            cursor: pointer;
        }

        .category-btn:hover {
            background: #2563eb;
            color: white;
        }

        .products {
            padding: 10px 6% 60px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 25px;
        }

        .card {
            background: white;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            transition: 0.3s;
        }

        .card:hover {
            transform: translateY(-6px);
        }

        .product-image {
            height: 170px;
            border-radius: 15px;
            background: #eef2ff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 75px;
            margin-bottom: 18px;
        }

        .category {
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 8px;
        }

        .card h3 {
            margin-bottom: 8px;
        }

        .description {
            color: #6b7280;
            font-size: 14px;
            min-height: 42px;
        }

        .rating {
            margin: 12px 0;
        }

        .price {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .add-button {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            cursor: pointer;
            font-size: 15px;
        }

        .add-button:hover {
            background: #1d4ed8;
        }

        .cart-panel {
            position: fixed;
            right: -420px;
            top: 0;
            width: 400px;
            max-width: 95%;
            height: 100%;
            background: white;
            box-shadow: -5px 0 25px rgba(0,0,0,0.2);
            z-index: 200;
            padding: 25px;
            transition: 0.3s;
            overflow-y: auto;
        }

        .cart-panel.open {
            right: 0;
        }

        .cart-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 25px;
        }

        .close {
            border: none;
            background: none;
            font-size: 25px;
            cursor: pointer;
        }

        .cart-item {
            border-bottom: 1px solid #e5e7eb;
            padding: 15px 0;
        }

        .cart-item strong {
            display: block;
            margin-bottom: 8px;
        }

        .quantity {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .quantity button {
            width: 30px;
            height: 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .total {
            font-size: 22px;
            font-weight: bold;
            margin: 25px 0;
        }

        .checkout {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: #16a34a;
            color: white;
            cursor: pointer;
            font-size: 16px;
        }

        footer {
            background: #111827;
            color: white;
            text-align: center;
            padding: 25px;
        }

        @media(max-width: 600px) {

            .hero h1 {
                font-size: 34px;
            }

            .cart-panel {
                width: 100%;
            }

        }

    </style>
</head>

<body>

<header>

    <div class="logo">
        Nova<span>Cart</span>
    </div>

    <button class="cart-button" onclick="openCart()">
        🛒 Cart
        <span id="cart-count">0</span>
    </button>

</header>


<section class="hero">

    <h1>Shop Smarter with NovaCart</h1>

    <p>
        Discover premium products at amazing prices.
    </p>

    <div class="search-container">

        <input
            id="search"
            type="text"
            placeholder="Search products..."
            onkeyup="searchProducts()">

    </div>

</section>


<div class="categories">

    <button
        class="category-btn"
        onclick="filterCategory('All')">
        All
    </button>

    <button
        class="category-btn"
        onclick="filterCategory('Electronics')">
        Electronics
    </button>

    <button
        class="category-btn"
        onclick="filterCategory('Fashion')">
        Fashion
    </button>

    <button
        class="category-btn"
        onclick="filterCategory('Home')">
        Home
    </button>

    <button
        class="category-btn"
        onclick="filterCategory('Travel')">
        Travel
    </button>

</div>


<section class="products">

{% for product in products %}

<div
    class="card"
    data-name="{{ product.name }}"
    data-category="{{ product.category }}">

    <div class="product-image">
        {{ product.emoji }}
    </div>

    <div class="category">
        {{ product.category }}
    </div>

    <h3>
        {{ product.name }}
    </h3>

    <p class="description">
        {{ product.description }}
    </p>

    <div class="rating">
        ⭐ {{ product.rating }}
    </div>

    <div class="price">
        ₹{{ product.price }}
    </div>

    <button
        class="add-button"
        onclick="addToCart({{ product.id }})">

        Add to Cart

    </button>

</div>

{% endfor %}

</section>


<div id="cartPanel" class="cart-panel">

    <div class="cart-header">

        <h2>Your Cart</h2>

        <button
            class="close"
            onclick="closeCart()">
            ×
        </button>

    </div>

    <div id="cartItems"></div>

    <div class="total">
        Total: ₹<span id="cartTotal">0</span>
    </div>

    <button
        class="checkout"
        onclick="checkout()">

        Proceed to Checkout

    </button>

</div>


<footer>

    <p>
        © 2026 NovaCart | Jenkins CI/CD | Docker | Helm | Amazon EKS
    </p>

</footer>


<script>

let currentCategory = "All";


function addToCart(id) {

    fetch("/api/cart/add", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            product_id: id
        })

    })
    .then(response => response.json())
    .then(data => {

        updateCart();

        alert(data.message);

    });

}


function updateQuantity(id, quantity) {

    fetch("/api/cart/update", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            product_id: id,
            quantity: quantity
        })

    })
    .then(response => response.json())
    .then(() => {

        updateCart();

    });

}


function updateCart() {

    fetch("/api/cart")

    .then(response => response.json())

    .then(data => {

        document.getElementById("cart-count").innerText =
            data.count;

        document.getElementById("cartTotal").innerText =
            data.total;

        const container =
            document.getElementById("cartItems");

        container.innerHTML = "";

        if (data.items.length === 0) {

            container.innerHTML =
                "<p>Your cart is empty.</p>";

            return;

        }


        data.items.forEach(item => {

            const div =
                document.createElement("div");

            div.className = "cart-item";

            div.innerHTML = `

                <strong>${item.name}</strong>

                <div>
                    ₹${item.price} × ${item.quantity}
                </div>

                <div class="quantity">

                    <button
                        onclick="updateQuantity(
                            ${item.id},
                            ${item.quantity - 1}
                        )">
                        -
                    </button>

                    <span>${item.quantity}</span>

                    <button
                        onclick="updateQuantity(
                            ${item.id},
                            ${item.quantity + 1}
                        )">
                        +
                    </button>

                </div>

            `;

            container.appendChild(div);

        });

    });

}


function openCart() {

    document
        .getElementById("cartPanel")
        .classList.add("open");

    updateCart();

}


function closeCart() {

    document
        .getElementById("cartPanel")
        .classList.remove("open");

}


function checkout() {

    fetch("/api/checkout", {
        method: "POST"
    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        updateCart();

    });

}


function searchProducts() {

    const search =
        document
            .getElementById("search")
            .value
            .toLowerCase();

    document
        .querySelectorAll(".card")
        .forEach(card => {

            const name =
                card
                .dataset
                .name
                .toLowerCase();

            const category =
                card
                .dataset
                .category;

            const matchesSearch =
                name.includes(search);

            const matchesCategory =
                currentCategory === "All" ||
                category === currentCategory;

            card.style.display =
                matchesSearch && matchesCategory
                    ? "block"
                    : "none";

        });

}


function filterCategory(category) {

    currentCategory = category;

    searchProducts();

}


updateCart();

</script>

</body>

</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, products=products)


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "application": "novacart-ecommerce",
        "version": "1.0"
    })


@app.route("/api/cart")
def get_cart():

    items = []
    total = 0
    count = 0

    for product_id, quantity in cart.items():

        product = next(
            (p for p in products if p["id"] == product_id),
            None
        )

        if product:

            item_total = product["price"] * quantity

            items.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            })

            total += item_total
            count += quantity

    return jsonify({
        "items": items,
        "total": total,
        "count": count
    })


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():

    data = request.get_json()

    product_id = int(data["product_id"])

    cart[product_id] = cart.get(product_id, 0) + 1

    return jsonify({
        "message": "Product added to cart"
    })


@app.route("/api/cart/update", methods=["POST"])
def update_cart():

    data = request.get_json()

    product_id = int(data["product_id"])
    quantity = int(data["quantity"])

    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity

    return jsonify({
        "message": "Cart updated"
    })


@app.route("/api/checkout", methods=["POST"])
def checkout():

    cart.clear()

    return jsonify({
        "message": "Checkout successful! Thank you for shopping with NovaCart."
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
