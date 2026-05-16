let cart = [];

document.addEventListener("DOMContentLoaded", () => {
    fetchProducts();
    setupEventListeners();
});

async function fetchProducts() {
    try {
        const response = await fetch("/products");
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

function displayProducts(products) {
    const grid = document.getElementById("productGrid");
    grid.innerHTML = "";

    products.forEach(product => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <div class="product-name">${product.name}</div>
            <div class="product-price">${product.price.toLocaleString()} Ft</div>
            <button class="add-btn" onclick="addToCart('${product.name}', ${product.price})">Add to Cart</button>
        `;
        grid.appendChild(card);
    });
}

function addToCart(name, price) {
    const existingItem = cart.find(item => item.name === name);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ name, price, quantity: 1 });
    }
    updateCartUI();
}

function updateCartUI() {
    const cartCount = document.getElementById("cartCount");
    const cartItems = document.getElementById("cartItems");
    const cartTotal = document.getElementById("cartTotal");

    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.innerText = totalItems;

    cartItems.innerHTML = "";
    let totalMoney = 0;

    cart.forEach(item => {
        totalMoney += item.price * item.quantity;
        const itemEl = document.createElement("div");
        itemEl.className = "cart-item";
        itemEl.innerHTML = `
            <div>
                <div><strong>${item.name}</strong></div>
                <small>${item.price.toLocaleString()} Ft x ${item.quantity}</small>
            </div>
            <div>${(item.price * item.quantity).toLocaleString()} Ft</div>
        `;
        cartItems.appendChild(itemEl);
    });

    cartTotal.innerText = totalMoney.toLocaleString();
}

function setupEventListeners() {
    const cartBtn = document.getElementById("cartBtn");
    const closeCart = document.getElementById("closeCart");
    const cartSidebar = document.getElementById("cartSidebar");
    const checkoutBtn = document.getElementById("checkoutBtn");

    cartBtn.addEventListener("click", () => cartSidebar.classList.add("open"));
    closeCart.addEventListener("click", () => cartSidebar.classList.remove("open"));
    
    checkoutBtn.addEventListener("click", () => {
        if(cart.length === 0) {
            alert("Your cart is empty!");
            return;
        }
        alert("Order submitted successfully!");
        cart = [];
        updateCartUI();
        cartSidebar.classList.remove("open");
    });
}