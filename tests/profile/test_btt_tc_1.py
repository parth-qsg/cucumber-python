import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../../features/profile/btt_tc_1.feature")


@pytest.fixture
def btt_context() -> dict:
    return {}


@given("the user is not logged into the application")
def user_not_logged_in(page: Page, base_url: str, btt_context: dict) -> None:
    # Ensure no active session exists.
    page.context.clear_cookies()

    # Navigate to login page (observed unauthenticated landing page).
    login_page = LoginPage(page, base_url)
    login_page.open()

    btt_context["login_url"] = page.url


@when("the user attempts to navigate directly to the BTT parking section URL")
def user_navigates_directly_to_btt_parking(page: Page, base_url: str, btt_context: dict) -> None:
    # Observed direct URL attempt for BTT parking section.
    btt_context["btt_parking_url"] = f"{base_url.rstrip('/')}" + "/btt/parking"
    page.goto(btt_context["btt_parking_url"], wait_until="domcontentloaded")


@then("the user is redirected to the login page")
def user_redirected_to_login(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@then("the BTT parking section content is not displayed")
def btt_parking_content_not_displayed(page: Page, base_url: str) -> None:
    # Login form is visible, indicating protected content is not shown.
    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Email Input")
    login_page.expect_visible("Password Input")
    login_page.expect_visible("Sign In Button")

    # Additionally, ensure we are not on the BTT parking URL.
    expect(page).not_to_have_url(re.compile(r".*/btt/parking/?$"))
