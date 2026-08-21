import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../../features/py1/ccp_tc_2.feature")


@pytest.fixture
def login_context() -> dict:
    return {}


@given("the user navigates to the login page at demo.qmagic.ai")
def user_navigates_to_login_page(page: Page, base_url: str, login_context: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_context["login_url"] = page.url


@given("the user is not authenticated")
def user_is_not_authenticated(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@when(parsers.parse('the user enters "{username}" as the username'))
def user_enters_username(page: Page, base_url: str, username: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Email Input", username)


@when(parsers.parse('the user enters "{password}" as the password'))
def user_enters_password(page: Page, base_url: str, password: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Password Input", password)


@when("the user clicks the Login button")
def user_clicks_login_button(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.click("Sign In Button")


@then("the login attempt fails")
def login_attempt_fails(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@then("an error message indicating invalid credentials is displayed")
def invalid_credentials_error_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Invalid Credentials Notification")


@then("the user remains on the login page")
def user_remains_on_login_page(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))
