from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

products = [
    {
        "id": 1,
        "name": "Premium Wireless Headphones",
        "category": "Electronics",
        "price": 2499,
        "old_price": 3999,
        "rating": 4.8,
        "emoji": "🎧",
        "description": "Immersive sound with active noise cancellation."
    },
    {
        "id": 2,
        "name": "Smart Watch Pro",
        "category": "Electronics",
        "price": 3299,
        "old_price": 4999,
        "rating": 4.7,
        "emoji": "⌚",
        "description": "Fitness tracking, notifications and premium design."
    },
    {
        "id": 3,
        "name": "Urban Running Shoes",
        "category": "Fashion",
        "price": 1899,
        "old_price": 2999,
        "rating": 4.6,
        "emoji": "👟",
        "description": "Lightweight running shoes designed for everyday comfort."
    },
    {
        "id": 4,
        "name": "Classic Denim Jacket",
        "category": "Fashion",
        "price": 1599,
        "old_price": 2499,
        "rating": 4.5,
        "emoji": "🧥",
        "description": "Classic denim jacket with a modern relaxed fit."
    },
    {
        "id": 5,
        "name": "Premium Coffee Maker",
        "category": "Home",
        "price": 2799,
        "old_price": 3999,
        "rating": 4.9,
        "emoji": "☕",
        "description": "Brew rich coffee at home with one-touch controls."
    },
    {
        "id": 6,
        "name": "Minimal Desk Lamp",
        "category": "Home",
        "price": 899,
        "old_price": 1499,
        "rating": 4.4,
        "emoji": "💡",
        "description": "Modern LED desk lamp with adjustable brightness."
    },
    {
        "id": 7,
        "name": "Travel Backpack",
        "category": "Accessories",
        "price": 1299,
        "old_price": 1999,
        "rating": 4.7,
        "emoji": "🎒",
        "description": "Spacious waterproof backpack for work and travel."
    },
    {
        "id": 8,
        "name": "Smart Bluetooth Speaker",
        "category": "Electronics",
        "price": 1499,
        "old_price": 2299,
        "rating": 4.6,
        "emoji": "🔊",
        "description": "Portable speaker with powerful bass and Bluetooth 5.0."
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

<title>NovaCart - Online Store</title>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    background: #f6f7fb;
    color: #1f2937;
}

header {
    background: #111827;
    color: white;
    padding: 18px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo {
    font-size: 27px;
    font-weight: bold;
}

.logo span {
    color: #60a5fa;
}

nav {
    display: flex;
    gap: 25px;
    align-items: center;
}

nav a {
    color: white;
    text-decoration: none;
    font-size: 15px;
}

.cart-button {
    background: #2563eb;
    border: none;
    color: white;
    padding: 11px 18px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
}

.hero {
    padding: 75px 7%;
    background: linear-gradient(135deg, #111827, #2563eb);
    color: white;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 40px;
    align-items: center;
}

.hero h1 {
    font-size: 50px;
    line-height: 1.1;
    margin-bottom: 20px;
}

.hero p {
    font-size: 18px;
    color: #dbeafe;
    max-width: 600px;
    margin-bottom: 30px;
}

.shop-button {
    display: inline-block;
    background: white;
    color: #1d4ed8;
    padding: 14px 25px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: bold;
}

.hero-card {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 45px;
    border-radius: 25px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.hero-card .big-icon {
    font-size: 100px;
}

.hero-card h2 {
    margin-top: 15px;
}

.container {
    width: 86%;
    margin: 45px auto;
}

.section-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.section-title h2 {
    font-size: 30px;
}

.search-area {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
    flex-wrap: wrap;
}

.search {
    flex: 1;
    min-width: 240px;
    padding: 14px 18px;
    border: 1px solid #d1d5db;
    border-radius: 30px;
    font-size: 15px;
    outline: none;
}

.categories {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.category {
    padding: 11px 18px;
    border-radius: 25px;
    border: 1px solid #d1d5db;
    background: white;
    cursor: pointer;
}

.category:hover {
    background: #2563eb;
    color: white;
}

.products {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 25px;
}

.product {
    background: white;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0,0,0,0.07);
    transition: 0.25s;
}

.product:hover {
    transform: translateY(-7px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}

.product-image {
    height: 190px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #eef2ff;
    font-size: 80px;
}

.product-info {
    padding: 20px;
}

.badge {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    padding: 5px 9px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: bold;
    margin-bottom: 10px;
}

.product h3 {
    font-size: 17px;
    margin-bottom: 8px;
}

.description {
    color: #6b7280;
    font-size: 13px;
    min-height: 38px;
    margin-bottom: 12px;
}

.rating {
    color: #f59e0b;
    font-size: 14px;
    margin-bottom: 10px;
}

.price {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 15px;
}

.current {
    font-size: 21px;
    font-weight: bold;
}

.old {
    color: #9ca3af;
    text-decoration: line-through;
    font-size: 13px;
}

.add {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 10px;
    background: #2563eb;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

.add:hover {
    background: #1d4ed8;
}

.cart-panel {
    position: fixed;
    right: -420px;
    top: 0;
    width: 400px;
    height: 100%;
    background: white;
    z-index: 200;
    box-shadow: -5px 0 30px rgba(0,0,0,0.2);
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
    cursor: pointer;
    font-size: 25px;
}

.cart-item {
    display: flex;
    gap: 15px;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
}

.cart-icon {
    font-size: 40px;
}

.cart-item-info {
    flex: 1;
}

.quantity {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-top: 8px;
}

.quantity button {
    border: none;
    background: #e5e7eb;
    width: 25px;
    height: 25px;
    border-radius: 5px;
    cursor: pointer;
}

.cart-total {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 2px solid #eee;
}

.total-row {
    display: flex;
    justify-content: space-between;
    font-size: 20px;
    font-weight: bold;
}

.checkout {
    width: 100%;
    padding: 15px;
    margin-top: 20px;
    border: none;
    border-radius: 10px;
    background: #16a34a;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

.empty {
    text-align: center;
    color: #777;
    padding: 50px 10px;
}

footer {
    margin-top: 60px;
    background: #111827;
    color: #9ca3af;
    text-align: center;
    padding: 30px;
}

@media (max-width: 1000px) {

    .products {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero {
        grid-template-columns: 1fr;
    }

}

@media (max-width: 600px) {

    .products {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 38px;
    }

    nav a {
        display: none;
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

<nav>

<a href="#products">Products</a>
<a href="#deals">Deals</a>

<button class="cart-button"
        onclick="openCart()">

🛒 Cart
<span id="cartCount">0</span>

</button>

</nav>

</header>


<section class="hero">

<div>

<h1>
Shop smarter.<br>
Live better.
</h1>

<p>
Discover premium electronics, fashion, accessories
and home essentials at prices you'll love.
</p>

<a href="#products" class="shop-button">
Start Shopping →
</a>

</div>


<div class="hero-card">

<div class="big-icon">
🛍️
</div>

<h2>
Big Deals Are Here
</h2>

<p>
Up to 40% OFF
</p>

</div>

</section>


<div class="container" id="products">


<div class="section-title">

<h2>
Featured Products
</h2>

<span>
{{ products|length }} products
</span>

</div>


<div class="search-area">

<input
    class="search"
    id="search"
    placeholder="🔎 Search products..."
    onkeyup="filterProducts()"
>


<div class="categories">

<button class="category"
        onclick="filterCategory('All')">
All
</button>

<button class="category"
        onclick="filterCategory('Electronics')">
Electronics
</button>

<button class="category"
        onclick="filterCategory('Fashion')">
Fashion
</button>

<button class="category"
        onclick="filterCategory('Home')">
Home
</button>

<button class="category"
        onclick="filterCategory('Accessories')">
Accessories
</button>

</div>

</div>


<div class="products" id="productGrid">


{% for product in products %}

<div class="product"
     data-name="{{ product.name|lower }}"
     data-category="{{ product.category }}">

<div class="product-image">
{{ product.emoji }}
</div>


<div class="product-info">

<span class="badge">
{{ product.category }}
</span>

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

<span class="current">
₹{{ "{:,}".format(product.price) }}
</span>

<span class="old">
₹{{ "{:,}".format(product.old_price) }}
</span>

</div>


<button class="add"
        onclick="addToCart({{ product.id }})">

🛒 Add to Cart

</button>

</div>

</div>

{% endfor %}

</div>

</div>


<div class="cart-panel" id="cartPanel">

<div class="cart-header">

<h2>
Your Cart 🛒
</h2>

<span class="close"
      onclick="closeCart()">
×
</span>

</div>


<div id="cartItems">

<div class="empty">
Your cart is empty.
</div>

</div>


<div class="cart-total">

<div class="total-row">

<span>
Total
</span>

<span id="cartTotal">
₹0
</span>

</div>


<button class="checkout"
        onclick="checkout()">

Proceed to Checkout →

</button>

</div>

</div>


<footer>

<p>
© 2026 NovaCart
</p>

<p>
Built with Python Flask • Docker • Jenkins • Helm • Amazon EKS
</p>

</footer>


<script>

let selectedCategory = "All";


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

});

}


function updateQuantity(id, change) {

fetch("/api/cart/update", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
product_id: id,
change: change
})

})
.then(response => response.json())
.then(data => {

updateCart();

});

}


function updateCart() {

fetch("/api/cart")

.then(response => response.json())

.then(data => {

document.getElementById("cartCount").innerText =
data.count;


document.getElementById("cartTotal").innerText =
"₹" + data.total.toLocaleString("en-IN");


let container =
document.getElementById("cartItems");


if (data.items.length === 0) {

container.innerHTML =
'<div class="empty">Your cart is empty.</div>';

return;

}


container.innerHTML = data.items.map(item => `

<div class="cart-item">

<div class="cart-icon">
${item.emoji}
</div>

<div class="cart-item-info">

<strong>
${item.name}
</strong>

<div>
₹${item.price.toLocaleString("en-IN")}
</div>

<div class="quantity">

<button onclick="updateQuantity(${item.id}, -1)">
−
</button>

<span>
${item.quantity}
</span>

<button onclick="updateQuantity(${item.id}, 1)">
+
</button>

</div>

</div>

</div>

`).join("");

});

}


function openCart() {

document.getElementById("cartPanel")
.classList.add("open");

updateCart();

}


function closeCart() {

document.getElementById("cartPanel")
.classList.remove("open");

}


function checkout() {

fetch("/api/checkout", {
method: "POST"
})

.then(response => response.json())

.then(data => {

alert(
"🎉 " +
data.message +
"\\nOrder Total: ₹" +
data.total.toLocaleString("en-IN")
);

updateCart();

});

}


function filterCategory(category) {

selectedCategory = category;

filterProducts();

}


function filterProducts() {

let search =
document.getElementById("search")
.value
.toLowerCase();


let cards =
document.querySelectorAll(".product");


cards.forEach(card => {

let name =
card.dataset.name;

let category =
card.dataset.category;


let matchesSearch =
name.includes(search);


let matchesCategory =
selectedCategory === "All" ||
category === selectedCategory;


if (matchesSearch && matchesCategory) {

card.style.display = "block";

} else {

card.style.display = "none";

}

});

}


updateCart();

</script>


</body>

</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        products=products
    )


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

            total += item_total
            count += quantity

            items.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "emoji": product["emoji"],
                "quantity": quantity
            })

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
        "success": True
    })


@app.route("/api/cart/update", methods=["POST"])
def update_cart():

    data = request.get_json()

    product_id = int(data["product_id"])
    change = int(data["change"])

    if product_id in cart:

        cart[product_id] += change

        if cart[product_id] <= 0:
            del cart[product_id]

    return jsonify({
        "success": True
    })


@app.route("/api/checkout", methods=["POST"])
def checkout():

    total = sum(
        next(
            p["price"]
            for p in products
            if p["id"] == product_id
        ) * quantity
        for product_id, quantity in cart.items()
    )

    cart.clear()

    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "total": total
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
