from typing import List

import allure
from playwright.sync_api import Page

from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:
    def __init__(self, page: Page):
        self.basket = BasketPage(page)

    @allure.step("Открыть корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Переход к оформлению заказа")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Удаление товара из корзины {product_name}")
    def remove_from_cart(self, product_name: str):
        self.basket.remove_item(product_name)
        return self

    @allure.step("Проверка наличия {product_name} в корзине")
    def expect_item_in_cart(self, product_name: str):
        self.basket.expect_item_in_cart(product_name)

    @allure.step("Проверка отсутствия {product_name} в корзине")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket.expect_item_not_in_cart(product_name)

    @allure.step("Получение названий товаров в корзине")
    def get_item_names(self) -> List[str]:
        return self.basket.get_item_names()

    @allure.step("Получение стоимости товаров в корзине")
    def get_item_prices(self) -> List[str]:
        return self.basket.get_item_prices()

    @allure.step("Получение итоговой стоимости с налогом")
    def get_item_total_price(self):
        return self.basket.get_item_total_price()