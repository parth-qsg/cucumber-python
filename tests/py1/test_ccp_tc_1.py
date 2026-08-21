import os
import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

# NOTE: scenarios() resolves paths relative to the *tests root directory*.
# This test file lives in tests/py1, so we must go up TWO levels to reach repo root.
scenarios("../../features/py1/ccp_tc_1.feature")


@pytest.fixture
def login_state() -> dict:
    return {}


@given("the user navigates to the login page at demo.qmagic.ai")
def user_navigates_to_login_page(page: Page, base_url: str, login_state: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.open()
    expect(page).to_have_url(re.compile(r".*/login/?$"))
    login_state["started_url"] = page.url


@given("the user is not authenticated")
def user_is_not_authenticated(page: Page) -> None:
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()


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
def user_clicks_login_button(page: Page, base_url: str, login_state: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.click("Sign In Button")

    # Observed post-login modal: "Select Client".
    if page.get_by_text("Select Client", exact=True).is_visible():
        page.get_by_role("combobox").select_option(label="QMagic")
        page.get_by_role("button", name="Confirm").click()

    login_state["post_login_url"] = page.url


@then("the user is redirected to the authenticated dashboard or home page")
def user_redirected_to_authenticated_page(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/(user-stories|execution|dashboard)(\?.*)?$"))
    expect(page.get_by_role("link", name="Dashboard")).to_be_visible()


@then("no error message is displayed")
def no_error_message_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    expect(
        login_page.element_name_mapping["Invalid Credentials Notification"]
    ).not_to_be_visible()


@then("the user session is active")
def user_session_is_active(page: Page) -> None:
    expect(
        page.get_by_role("button", name=re.compile(r"Account menu for", re.I))
    ).to_be_visible()
