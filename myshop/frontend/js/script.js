// script.js

// Базовая функция для отправки запросов
async function fetchData(endpoint, method = 'GET', data = null) {
    const response = await fetch(`https://super-memory-664p54q7vvj34q65-8000.app.github.dev/api/${endpoint}`, {
    method: method,
    headers: {
    'Content-Type': 'application/json'
    },
    body: data ? JSON.stringify(data) : null
    });
   
    if (!response.ok) {
    throw new Error(`Ошибка ${response.status}: ${response.statusText}`);
    }
   
    return await response.json();
   }
   

// Функция для загрузки списка товаров
async function loadProducts() {
    try {
        const products = await fetchData('products');
        const productsSelect = document.getElementById('products-select');

        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.id;
            option.dataset.price = product.price;
            option.text = `${product.name} (${product.price} руб.)`;
            productsSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Ошибка загрузки товаров:', error);
    }
}

// Функция для подсчета общей суммы
function calculateTotalPrice() {
    const selectedOptions = document.getElementById('products-select').selectedOptions;
    let total = 0;

    for (let i = 0; i < selectedOptions.length; i++) {
        total += parseFloat(selectedOptions[i].dataset.price);
    }

    document.getElementById('total-price').textContent = total.toFixed(2);
}

// Функция для создания заказа
async function createOrder() {
    const customerName = document.getElementById('customer-name').value;
    const selectedProducts = Array.from(document.getElementById('products-select').selectedOptions)
        .map(option => ({
            product_id: option.value,
            price: parseFloat(option.dataset.price)
        }));

    const totalPrice = calculateTotalPrice();

    try {
        await fetchData('orders', 'POST', {
            customer_name: customerName,
            products: selectedProducts,
            total_price: totalPrice
        });

        alert('Заказ успешно создан!');
        document.getElementById('order-form').reset();
        document.getElementById('total-price').textContent = '0';
    } catch (error) {
        console.error('Ошибка создания заказа:', error);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();

    document.getElementById('products-select').addEventListener('change', calculateTotalPrice);
    document.getElementById('create-order-btn').addEventListener('click', createOrder);
});
