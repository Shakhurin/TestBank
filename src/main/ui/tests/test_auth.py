from playwright.sync_api import expect

from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.login_steps import LoginSteps


def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_product_count() > 0, "Нет товаров на странице"


def test_auth_locked_out(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    assert "locked out" in steps.get_error_text()


def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogPage(page)

    login.open_login_page().login("standard_user", "secret_sauce")

    assert catalog.get_product_count() > 0, "Нет товаров на странице"

    catalog.logout()
    expect(page).to_have_url(login.LOGIN_URL)


def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogPage(page)

    login.open_login_page().login("standard_user", "secret_sauce")

    assert catalog.get_product_count() > 0, "Нет товаров на странице"

    catalog.logout()

    expect(page).to_have_url(login.LOGIN_URL)
