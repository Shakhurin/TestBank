from playwright.sync_api import Page

from src.main.ui.pages.base_page import BasePage


class CatalogPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_cards = page.locator(".inventory_item")
        self.sort_select = page.locator(".product_sort_container")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.locator("#login-button")

    # ---Навигация и логин---
    def logout(self):
        self.menu_button.click()
        self.logout_link.click()

    # ---Соритровка---
    def sort(self, option: str):
        # Варианты: "az", "za", "lohi", "hilo"
        self.sort_select.select_option(option)

    # ---Работа с корзиной---
    def add_to_cart(self, product_name: str):
        card = self.page.locator(".inventory_item", has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Add to cart":
            button.click()
        return button

    def remove_from_cart(self, product_name: str):
        card = self.page.locator(".inventory_item", has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Remove":
            button.click()
        return button

    # ---Работа с карточкой товара---
    def get_product_count(self):
        return self.product_cards.count()

    def get_product_names(self) -> list[str]:
        return self.product_cards.locator(".inventory_item_name").all_text_contents()

    def get_product_prices(self):
        prices_text = self.product_cards.locator(".inventory_item_price").all_text_contents()
        return [float(el.replace("$", "")) for el in prices_text]

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return self.cart_badge.count()
        return 0

    def open_product_details(self, product_name: str):
        card = self.page.locator(".inventory_item", has_text=product_name)
        name = card.locator(".inventory_item_name").inner_text()
        price_text = card.locator(".inventory_item_price").inner_text()
        price = float(price_text.replace("$", ""))

        card.locator(".inventory_item_name").click()

        detailed_name = self.page.locator(".inventory_details_name").inner_text()
        detailed_price_text = self.page.locator(".inventory_details_price").inner_text()
        detailed_price = float(detailed_price_text.replace("$",""))

        self.page.go_back()
        return name, price, detailed_name, detailed_price