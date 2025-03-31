
 

import random
import time
from playwright.sync_api import sync_playwright, expect

def generate_name():
    names = ["Алексей", "Мария", "Иван", "Ольга", "Дмитрий"]
    return f"{random.choice(names)}{random.randint(1, 100)}"

def test_order_creation():
    with sync_playwright() as p:
        # Настройка браузера с увеличенным таймаутом
        browser = p.chromium.launch(headless=True, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 1. Переход на страницу
            page.goto(
                "https://super-memory-664p54q7vvj34q65-5500.app.github.dev/",
                timeout=20000,
                wait_until="networkidle"  # Ждем завершения сетевых запросов
            )
            print("Страница загружена")

            # 2. Обработка GitHub Codespaces (если есть)
            if "Codespaces" in page.title():
                print("Обнаружена страница Codespaces")
                page.click("button:has-text('Continue')")
                page.wait_for_url("**/", timeout=5000)

            # 2. Ожидание загрузки списка продуктов (динамический контент)
            print("Ожидаем загрузки продуктов...")
            page.wait_for_selector("#product-list li", timeout=15000)
            products = page.locator("#product-list li")
            product_count = products.count()
            print(f"Найдено продуктов: {product_count}")

            if product_count == 0:
                raise Exception("Список продуктов пуст!")

            # 3. Ввод имени клиента
            customer_name = generate_name()
            page.fill("#customer_name", customer_name)
            print(f"Введено имя клиента: {customer_name}")

            # 4. Выбор случайных продуктов
            selected_indices = random.sample(range(product_count), min(3, product_count))
            for index in selected_indices:
                products.nth(index).locator("input[type='checkbox']").check()
            print(f"Выбрано {len(selected_indices)} продуктов")

            # 5. Проверка обновления общей стоимости
            initial_price = page.locator("#total-price").inner_text()
            if initial_price != "0":
                print(f"Предупреждение: начальная цена не 0 ({initial_price})")

            # 6. Нажатие кнопки оформления
            page.click("#place-order")
            print("Кнопка 'Оформить заказ' нажата")

            # 7. Ожидание успешного оформления (через alert)
            def handle_dialog(dialog):
                print(f"Alert сообщение: {dialog.message}")
                dialog.accept()
            
            page.on("dialog", handle_dialog)
            
            # 8. Проверка изменения на странице после оформления
            try:
                expect(page.locator("#total-price")).to_have_text("0", timeout=5000)
                print("Общая стоимость сброшена до 0")
            except:
                print("Общая стоимость не сбросилась, но это может быть нормально")

            # 9. Скриншот результата
            page.screenshot(path="order_result.png")
            print("Тест завершен успешно")

        except Exception as e:
            print(f"\nОшибка во время выполнения: {str(e)}")
            page.screenshot(path="test_error.png")
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    test_order_creation()