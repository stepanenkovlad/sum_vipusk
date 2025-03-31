const apiUrl = 'http://localhost:8000/api/';

async function getData(endpoint) {
    const response = await fetch(apiUrl + endpoint);
    return await response.json();
}

async function displayProducts() {
    const products = await getData('products/');
    const productsDiv = document.getElementById('products');
    productsDiv.innerHTML = products.map(product => `
        <div>
            <p>Name: ${product.name}</p>
            <p>Price: ${product.price}</p>
        </div>
    `).join('');
}

async function displayOrders() {
    const orders = await getData('orders/');
    const ordersDiv = document.getElementById('orders');
    ordersDiv.innerHTML = orders.map(order => `
        <div>
            <p>Customer Name: ${order.customer_name}</p>
            <p>Total Price: ${order.total_price}</p>
            <p>Products: ${order.products.map(p => p.name).join(', ')}</p>
        </div>
    `).join('');
}

displayProducts();
displayOrders();
