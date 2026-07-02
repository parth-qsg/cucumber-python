import os
import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../features/ccp_tc_1.feature")


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
    # On this app, unauthenticated users land on /login.
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@when("the user enters a valid username")
def user_enters_valid_username(page: Page, base_url: str, credentials: dict) -> None:
    login_page = LoginPage(page, base_url)

    username = (
        credentials.get("username")
        if isinstance(credentials, dict)
        else os.environ.get("TEST_USERNAME")
    )
    if not username:
        username = os.environ.get("TEST_USERNAME") or os.environ.get("APP_USERNAME", "")

    login_page.fill("Email Input", username)


@when("the user enters the correct password")
def user_enters_correct_password(page: Page, base_url: str, credentials: dict) -> None:
    login_page = LoginPage(page, base_url)

    password = (
        credentials.get("password")
        if isinstance(credentials, dict)
        else os.environ.get("TEST_PASSWORD")
    )
    if not password:
        password = os.environ.get("TEST_PASSWORD") or os.environ.get("APP_PASSWORD", "")

    login_page.fill("Password Input", password)


@when("the user clicks the Login button")
def user_clicks_login_button(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    # App uses a "Sign In" button on the login page.
    login_page.click("Sign In Button")

    # Post-login, the app shows a "Select Client" dialog that must be confirmed.
    # Select a known client option from the observed list and confirm.
    page.get_by_role("combobox").select_option("TEST")
    page.get_by_role("button", name="Confirm").click()


@then("the user is redirected to the authenticated dashboard or home page")
def user_redirected_to_authenticated_page(page: Page) -> None:
    # Observed authenticated landing page after confirming client selection.
    expect(page).to_have_url(re.compile(r".*/user-stories.*"))

    # Authenticated navigation is visible.
    expect(page.get_by_role("link", name="User Stories")).to_be_visible()
    expect(page.get_by_role("link", name="Execution")).to_be_visible()


@then("no error message is displayed")
def no_error_message_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    # BaseComponent provides expect_hidden(), not expect_not_visible().
    login_page.expect_hidden("Invalid Credentials Notification")


@then("the user session is active")
def user_session_is_active(page: Page) -> None:
    # Session is considered active if we are not on /login and the app shell is present.
    expect(page).not_to_have_url(re.compile(r".*/login/?$"))
    expect(page.get_by_role("navigation")).to_be_visible()
