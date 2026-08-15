from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_add_item_and_check_in_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Backpack")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")


def test_add_items_and_check_in_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()

    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")


def test_remove_item_from_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")

    basket.remove_from_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_items_from_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    basket.remove_from_cart("Sauce Labs Fleece Jacket")
    basket.remove_from_cart("Test.allTheThings() T-Shirt (Red)")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")


def test_checkout_multiple_items(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")
    basket_total = basket.get_item_total_price()

    basket.checkout()
    checkout.start_checkout(first_name="Test", last_name="User", zip_code="12345")
    checkout_total = checkout.get_item_total_after_continue()
    assert checkout_total == basket_total, "Сумма товаров в Checkout не совпадает с корзиной"


def test_checkout_without_items(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")

    basket.checkout()
    checkout.start_checkout(first_name="Test", last_name="User", zip_code="")

    error_text = checkout.get_error_text()
    assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"