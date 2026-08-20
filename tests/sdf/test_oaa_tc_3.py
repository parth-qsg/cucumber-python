import os
import re
import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

scenarios("../../features/sdf/oaa_tc_3.feature")


@pytest.fixture
def ui_context() -> dict:
    return {}


@given("the user is authenticated and on the main website")
def user_is_authenticated_and_on_main_website(
    page: Page, base_url: str, ui_context: dict
) -> None:
    login_page = LoginPage(page, base_url).open()

    username = os.environ.get("TEST_USERNAME") or os.environ.get("APP_USERNAME") or ""
    password = os.environ.get("TEST_PASSWORD") or os.environ.get("APP_PASSWORD") or ""

    page.locator("#email").fill(username)
    page.locator("#password").fill(password)
    page.get_by_role("button", name="Sign In").click()

    # Client selection modal appears after login; select a client and confirm.
    page.get_by_role("combobox").select_option(label="QMagic")
    page.get_by_role("button", name="Confirm").click()

    # Record the main website URL after successful authentication.
    page.wait_for_load_state("domcontentloaded")
    ui_context["main_url"] = page.url


@when("the user clicks the Logout button or option")
def user_clicks_logout(page: Page) -> None:
    page.get_by_role("button", name=re.compile(r"Account menu for", re.I)).click()
    page.get_by_role("button", name="Logout").click()


@then("the user is redirected to the login page")
def user_redirected_to_login(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login.*"))
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()


@then("the user session is terminated")
def user_session_terminated(page: Page) -> None:
    # Assert that authenticated navigation elements are not present on the login page.
    expect(page.get_by_role("button", name=re.compile(r"Account menu for", re.I))).not_to_be_visible()


@when("the user attempts to navigate directly to the main website URL")
def user_navigates_directly_to_main_url(
    page: Page, ui_context: dict, base_url: str
) -> None:
    target_url = ui_context.get("main_url") or base_url
    page.goto(target_url, wait_until="domcontentloaded")


@then("the user is redirected to the login page again")
def user_redirected_to_login_again(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login.*"))
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
