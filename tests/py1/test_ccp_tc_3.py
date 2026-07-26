import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../../features/py1/ccp_tc_3.feature")


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
    # Observed unauthenticated state: user is on /login and the Sign In button is visible.
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()


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
    # On the actual page, the button label is "Sign In".
    login_page.click("Sign In Button")


@then("a validation error message is displayed")
def validation_error_message_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.wait_for_visible("Invalid Credentials Notification")
    expect(login_page.element_name_mapping["Invalid Credentials Notification"]).to_be_visible()


@then("the user is not logged in")
def user_is_not_logged_in(page: Page) -> None:
    # Observed not-logged-in state: still on login page and Sign In button remains visible.
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()


@then("the user remains on the login page")
def user_remains_on_login_page(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login.*"))
