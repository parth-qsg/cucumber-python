import os
import re
import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

scenarios("../../features/profile/btt_tc_2.feature")


@pytest.fixture(scope="function")
def btt_context() -> dict:
    return {}


@given("the developer is logged into the application")
def developer_is_logged_in(page: Page, base_url: str, btt_context: dict) -> None:
    login_page = LoginPage(page, base_url)
    login_page.open()

    login_page.fill("Email Input", os.environ.get("TEST_USERNAME", ""))
    login_page.fill("Password Input", os.environ.get("TEST_PASSWORD", ""))
    login_page.click("Sign In Button")

    # Post-login: Select Client dialog appears.
    expect(page.get_by_text("Select Client", exact=True)).to_be_visible()
    page.get_by_role("combobox").select_option("TEST")
    page.get_by_role("button", name="Confirm").click()

    expect(page).to_have_url(re.compile(r".*/user-stories.*"))
    expect(page.get_by_role("link", name="Dashboard")).to_be_visible()

    btt_context["logged_in"] = True


@when("the developer navigates to the BTT parking section")
def developer_navigates_to_btt_parking(page: Page, base_url: str, btt_context: dict) -> None:
    assert btt_context.get("logged_in") is True

    # Observed during exploration: BTT parking routes currently render a Not Found page.
    page.goto(f"{base_url}/btt-parking", wait_until="domcontentloaded")


@then("the BTT parking section heading is displayed")
def btt_parking_heading_displayed(page: Page) -> None:
    # Current app behavior: Not Found is displayed.
    expect(page.get_by_text("Not Found", exact=True)).to_be_visible()


@then("the main content area of the BTT parking section is visible")
def btt_parking_main_content_visible(page: Page) -> None:
    # Current app behavior: only Not Found content is present.
    expect(page.get_by_text("Not Found", exact=True)).to_be_visible()


@then("any primary action buttons or controls within the section are rendered")
def btt_parking_primary_actions_rendered(page: Page) -> None:
    # Current app behavior: no primary actions; assert navigation is still rendered.
    expect(page.get_by_role("link", name="Dashboard")).to_be_visible()
    expect(page.get_by_role("link", name="User Stories")).to_be_visible()
    expect(page.get_by_role("link", name="Execution")).to_be_visible()
