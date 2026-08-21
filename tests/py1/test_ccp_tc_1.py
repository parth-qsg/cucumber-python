import os
import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../../features/py1/ccp_tc_1.feature")


@pytest.fixture
def login_state() -> dict:
    return {}


@given("the user navigates to the login page at demo.qmagic.ai")
def user_navigates_to_login_page(page: Page, base_url: str, login_state: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.open()
    expect(page).to_have_url(re.compile(r".*/login/?$"))
    login_state["login_url"] = page.url


@given("the user is not authenticated")
def user_is_not_authenticated(page: Page, login_state: dict) -> None:
    # On this app, unauthenticated users remain on /login and do not see the
    # authenticated navigation (e.g., "Dashboard").
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()
    expect(page.get_by_role("link", name="Dashboard")).not_to_be_visible()
    login_state["was_authenticated"] = False


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

    # Post-login, the app shows a "Select Client" dialog. Choose "QMagic" and confirm.
    # Locators are derived from live exploration snapshots.
    page.get_by_role("combobox").select_option("QMagic")
    page.get_by_role("button", name="Confirm").click()

    login_state["post_login_url"] = page.url


@then("the user is redirected to the authenticated dashboard or home page")
def user_redirected_to_authenticated_home(page: Page) -> None:
    # Observed landing page after successful login: /user-stories?... (authenticated area)
    expect(page).to_have_url(re.compile(r".*/(user-stories|execution|/)(\?.*)?$"))
    expect(page.get_by_role("link", name="Dashboard")).to_be_visible()


@then("no error message is displayed")
def no_error_message_displayed(page: Page, base_url: str) -> None:
    login_page = LoginPage(page, base_url)
    expect(login_page.element_name_mapping["Invalid Credentials Notification"]).not_to_be_visible()


@then("the user session is active")
def user_session_is_active(page: Page) -> None:
    # Authenticated UI shows an account menu with the user's name.
    expect(page.get_by_role("button", name=re.compile(r"Account menu for .+"))).to_be_visible()
