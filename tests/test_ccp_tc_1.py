import os
import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

scenarios("../features/ccp_tc_1.feature")


@pytest.fixture
def login_context() -> dict:
    return {}


@given("the user navigates to the login page at demo.qmagic.ai")
def user_navigates_to_login_page(page: Page, base_url: str, login_context: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.goto_login()
    login_page.expect_visible("Login Heading")
    login_context["login_url"] = page.url


@given("the user is not authenticated")
def user_is_not_authenticated(page: Page, login_context: dict) -> None:
    # On this app, unauthenticated users are redirected to /login.
    assert "/login" in page.url


@when("the user enters a valid username")
def user_enters_valid_username(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    username = os.environ.get("TEST_USERNAME") or os.environ.get("APP_USERNAME") or ""
    login_page.fill("Email Input", username)


@when("the user enters the correct password")
def user_enters_correct_password(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    password = os.environ.get("TEST_PASSWORD") or os.environ.get("APP_PASSWORD") or ""
    login_page.fill("Password Input", password)


@when("the user clicks the Login button")
def user_clicks_login_button(page: Page, base_url: str, login_context: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.click("Sign In Button")

    # Observed post-login behavior: a "Select Client" dialog appears on /login.
    # We treat this as an authenticated post-login state.
    select_client_dialog = page.get_by_role("dialog")
    expect(select_client_dialog).to_be_visible()
    # Avoid strict-mode ambiguity: "Select Client" appears in multiple elements.
    expect(page.get_by_role("group", name="Select Client")).to_be_visible()

    login_context["post_login_url"] = page.url


@then("the user is redirected to the authenticated dashboard or home page")
def user_redirected_to_authenticated_area(page: Page, login_context: dict) -> None:
    # From exploration, successful sign-in shows a post-login modal (Select Client)
    # while still on /login.
    assert "/login" in page.url
    expect(page.get_by_role("dialog")).to_be_visible()
    # Avoid strict-mode ambiguity: "Select Client" appears in multiple elements.
    expect(page.get_by_role("group", name="Select Client")).to_be_visible()


@then("no error message is displayed")
def no_error_message_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    expect(login_page.element_name_mapping["Invalid Credentials Notification"]).not_to_be_visible()


@then("the user session is active")
def user_session_is_active(page: Page) -> None:
    # Session activity is inferred from the authenticated-only "Select Client" dialog.
    expect(page.get_by_role("dialog")).to_be_visible()
    # Avoid strict-mode ambiguity: "Select Client" appears in multiple elements.
    expect(page.get_by_role("group", name="Select Client")).to_be_visible()
