import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../../features/sdf/oaa_tc_2.feature")


@pytest.fixture
def login_context() -> dict:
    return {}


@given("the user is on the application login page")
def user_is_on_the_application_login_page(
    page: Page, base_url: str, login_context: dict
) -> None:
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_context["login_url"] = page.url


@when('the user enters "invalidUser" as the username')
def user_enters_invalid_user_as_the_username(
    page: Page, base_url: str, login_context: dict
) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Email Input", "invalidUser")


@when('the user enters "wrongPassword" as the password')
def user_enters_wrong_password_as_the_password(
    page: Page, base_url: str, login_context: dict
) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Password Input", "wrongPassword")


@when("the user clicks the Login button")
def the_user_clicks_the_login_button(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.click("Sign In Button")


@then("an error message is displayed indicating invalid credentials")
def an_error_message_is_displayed_indicating_invalid_credentials(
    page: Page, base_url: str
) -> None:
    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Invalid Credentials Notification")


@then("the user remains on the login page")
def the_user_remains_on_the_login_page(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))
