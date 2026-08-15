from playwright.sync_api import Page

from src.main.ui.pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("#finish")
        self.total_without_taxes = page.locator("[data-test='subtotal-label']")
        self.taxes = page.locator("[data-test='tax-label']")
        self.total_with_taxes = page.locator(".summary_total_label")
        self.error_message = page.locator('[data-test="error"]')
        self.success_message = page.locator(".complete-header")

    # --- Действия ---
    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        self.finish_button.click()

    # --- Методы для получения данных ---
    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def get_success_text(self) -> str:
        return self.success_message.inner_text()

    def get_item_total_after_continue(self) -> float:
        total_text = self.total_without_taxes.inner_text()
        return float(total_text.split("$")[1])