from playwright.sync_api import Page, expect

from src.main.ui.pages.base_page import BasePage


class BasketPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart = page.locator(".shopping_cart_link")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.item_cards = page.locator(".cart_item")
        self.error_message = page.locator('[data-test="error"]')

    # --- Навигация ---
    def open_cart(self):
        self.cart.click()

    def checkout(self):
        self.checkout_button.click()

    # --- Добавление и удаление ---
    def remove_item(self, item_name: str):
        card = self.item_cards.filter(has_text=item_name)
        button = card.locator("button")
        button.click()

    # --- Проверки ---
    def expect_item_in_cart(self, product_name: str):
        card = self.item_cards.filter(has_text=product_name)
        expect(card).to_be_visible()

    def expect_item_not_in_cart(self, product_name: str):
        card = self.item_cards.filter(has_text=product_name)
        expect(card).not_to_be_visible()

    def get_item_names(self):
        return self.item_cards.locator(".inventory_item_name").all_text_contents()

    def get_item_prices(self):
        prices_text = self.item_cards.locator(".inventory_item_price").all_text_contents()
        prices = [float(el.replace("$","")) for el in prices_text]
        return prices

    def get_item_total_price(self):
        prices_text = self.item_cards.locator(".inventory_item_price").all_text_contents()
        prices = [float(el.replace("$", "")) for el in prices_text]
        return sum(prices)