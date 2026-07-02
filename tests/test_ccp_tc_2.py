import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

scenarios("../features/ccp_tc_2.feature")


@pytest.fixture
def login_state() -> dict:
    return {}


@given("the user navigates to the login page at demo.qmagic.ai")
def user_navigates_to_login_page(page: Page, base_url: str, login_state: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.goto_login()
    login_page.wait_for_load()
    login_page.expect_visible("Login Heading")
    login_state["login_url"] = page.url


@given("the user is not authenticated")
def user_is_not_authenticated(page: Page) -> None:
    # On this app, unauthenticated users are served the /login page.
    # Playwright's to_have_url expects a string or regex (not a callable).
    expect(page).to_have_url(r".*/login.*")


@when(parsers.parse('the user enters "{username}" as the username'))
def user_enters_username(
    page: Page, base_url: str, username: str, login_state: dict
) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Email Input", username)
    login_state["username"] = username


@when(parsers.parse('the user enters "{password}" as the password'))
def user_enters_password(
    page: Page, base_url: str, password: str, login_state: dict
) -> None:
    login_page = LoginPage(page, base_url)
    login_page.fill("Password Input", password)
    login_state["password"] = password


@when("the user clicks the Login button")
def user_clicks_login_button(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.click("Sign In Button")


@then("the login attempt fails")
def login_attempt_fails(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Invalid Credentials Notification")


@then("an error message indicating invalid credentials is displayed")
def invalid_credentials_error_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    login_page.expect_text("Invalid Credentials Notification", "Invalid credentials")


@then("the user remains on the login page")
def user_remains_on_login_page(page: Page) -> None:
    expect(page).to_have_url(r".*/login.*")
