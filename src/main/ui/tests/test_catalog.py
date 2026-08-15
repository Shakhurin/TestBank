from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_count_catalog(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")
    assert steps_catalog.get_products_count() == 6, "Товаров больше 6"


def test_sorted_by_name(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    steps_catalog.sort_items('az')
    assert steps_catalog.get_product_names() == sorted(
        steps_catalog.get_product_names()), "Отсортировано не в алфавитном порядке"

    steps_catalog.sort_items("za")
    assert steps_catalog.get_product_names() == sorted(steps_catalog.get_product_names(),
                                                       reverse=True), "Отсортировано не от в обратном алфавитном порядке"


def test_sort_by_price(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    steps_catalog.sort_items("lohi")
    assert steps_catalog.get_product_prices() == sorted(
        steps_catalog.get_product_prices()), "Отсортировано не от меньшего к большему"

    steps_catalog.sort_items("hilo")
    assert steps_catalog.get_product_prices() == sorted(steps_catalog.get_product_prices(),
                                                        reverse=True), "Отсортировано не от большего к меньшему"


def test_add_to_card(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    button = steps_catalog.add_to_cart("Sauce Labs Bike Light")
    assert steps_catalog.get_cart_count() == 1, "В корзине не 1 товар"


def test_add_sauce_labs_onesie_to_cart(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    steps_catalog.add_to_cart("Sauce Labs Onesie")
    assert steps_catalog.get_cart_count() == 1, "В корзине не 1 товар"

    steps_catalog.remove_from_cart("Sauce Labs Onesie")
    assert steps_catalog.get_cart_count() == 0, "В корзине что-то есть"


def test_product_details_onesie(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    name, price, detailed_name, detailed_price = steps_catalog.open_product_details("Sauce Labs Onesie")

    assert name == detailed_name, "Название карточек не совпадает"
    assert price == detailed_price, "Цена карточек не совпадает"


def test_product_details_fleece_jacket(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    name, price, detailed_name, detailed_price = steps_catalog.open_product_details("Sauce Labs Fleece Jacket")

    assert name == detailed_name, "Название карточек не совпадает"
    assert price == detailed_price, "Цена карточек не совпадает"


def test_remove_item_from_catalog(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    steps_catalog.remove_from_cart("Test.allTheThings() T-Shirt (Red)")


def test_remove_onesie_from_catalog(page):
    steps_login = LoginSteps(page)
    steps_catalog = CatalogSteps(page)

    steps_login.open_login_page().login("standard_user", "secret_sauce")

    steps_catalog.remove_from_cart("Sauce Labs Onesie")