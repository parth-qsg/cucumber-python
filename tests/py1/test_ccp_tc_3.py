import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../../features/py1/ccp_tc_3.feature")


@pytest.fixture
def auth_context() -> dict:
    return {}


@given("the user navigates to the login page at demo.qmagic.ai")
def user_navigates_to_login_page(page: Page, base_url: str, auth_context: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.open()
    auth_context["login_url"] = page.url


@given("the user is not authenticated")
def user_is_not_authenticated(page: Page, base_url: str) -> None:
    # Ensure we are on the login page and not already in an authenticated area.
    login_page = LoginPage(page, base_url)
    login_page.open()
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@when("the user leaves the username field empty")
def user_leaves_username_empty(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Email Input", "")


@when("the user leaves the password field empty")
def user_leaves_password_empty(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Password Input", "")


@when("the user clicks the Login button")
def user_clicks_login_button(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    # App uses "Sign In" as the visible button label.
    login_page.click("Sign In Button")


@then("a validation error message is displayed")
def validation_error_message_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Invalid Credentials Notification")


@then("the user is not logged in")
def user_is_not_logged_in(page: Page) -> None:
    # Still on login page (not redirected to an authenticated route).
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@then("the user remains on the login page")
def user_remains_on_login_page(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))
