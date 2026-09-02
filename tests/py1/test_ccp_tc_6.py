import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when, parsers

from pages.login_page import LoginPage

scenarios("../../features/py1/ccp_tc_6.feature")


@pytest.fixture
def auth_context() -> dict:
    return {}


@given("the user navigates to the login page at demo.qmagic.ai")
def user_navigates_to_login_page(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.open()
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@given("no authenticated session is active")
def no_authenticated_session_is_active(page: Page, base_url: str) -> None:
    # Ensure a clean state (cookies + storage) before attempting login.
    page.context.clear_cookies()
    page.goto(f"{base_url.rstrip('/')}/login", wait_until="domcontentloaded")
    page.evaluate("() => { window.localStorage.clear(); window.sessionStorage.clear(); }")
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@when(parsers.parse('the user enters "{username}" in the username field'))
def user_enters_username(page: Page, base_url: str, username: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Email Input", username)


@when(parsers.parse('the user enters "{password}" in the password field'))
def user_enters_password(page: Page, base_url: str, password: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Password Input", password)


@when("the user submits the login form")
def user_submits_login_form(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.click("Sign In Button")


@then("the login attempt is rejected")
def login_attempt_is_rejected(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Invalid Credentials Notification")


@then("a field validation error or warning is displayed")
def field_validation_error_or_warning_is_displayed(page: Page, base_url: str) -> None:
    # Observed behavior: app shows a notification "Invalid credentials".
    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Invalid Credentials Notification")


@then("the user remains on the login page")
def user_remains_on_login_page(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@then("no authenticated session is established")
def no_authenticated_session_is_established(page: Page) -> None:
    storage_state = page.evaluate(
        """
        () => ({
            localStorageKeys: Object.keys(window.localStorage),
            sessionStorageKeys: Object.keys(window.sessionStorage),
        })
        """
    )
    assert storage_state["localStorageKeys"] == []
    assert storage_state["sessionStorageKeys"] == []
