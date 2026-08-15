import allure
from playwright.sync_api import Page

from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.checkout = CheckoutPage(page)

    @allure.step("Заполнение реквизитов {first_name}, {last_name}, {zip_code}")
    def start_checkout(self, first_name: str, last_name: str, zip_code: str):
        self.checkout.start_checkout(first_name, last_name, zip_code)
        return self

    @allure.step("Подтверждение заполнения реквизитов")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step("Ошибка при заполнении реквизитов")
    def get_error_text(self) -> str:
        return self.checkout.get_error_text()

    @allure.step("Сообщение об успешном оформлении заказа")
    def get_success_text(self) -> str:
        return self.checkout.get_success_text()

    @allure.step("Получаем общую сумму товаров после налогов")
    def get_item_total_after_continue(self) -> float:
        return self.checkout.get_item_total_after_continue()