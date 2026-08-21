import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

# NOTE: path is relative to THIS file (tests/py1/)
scenarios("../../features/py1/ccp_tc_4.feature")


@pytest.fixture
def access_context() -> dict:
    return {}


@given("the user has no active session on demo.qmagic.ai")
def user_has_no_active_session(page: Page, base_url: str, access_context: dict) -> None:
    page.context.clear_cookies()
    page.context.clear_permissions()

    login_page = LoginPage(page, base_url)
    login_page.open()

    access_context["login_url"] = page.url


@when("the user attempts to navigate directly to a protected page URL")
def user_attempts_to_navigate_directly_to_protected_page_url(
    page: Page, base_url: str, access_context: dict
) -> None:
    # Protected route observed during exploration.
    protected_path = "/user-stories"
    access_context["protected_path"] = protected_path

    page.goto(f"{base_url.rstrip('/')}{protected_path}", wait_until="domcontentloaded")


@then("the user is redirected to the login page")
def user_is_redirected_to_the_login_page(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login/?$"))


@then("the protected page content is not displayed")
def the_protected_page_content_is_not_displayed(
    page: Page, access_context: dict
) -> None:
    protected_path = access_context.get("protected_path", "/user-stories")

    # Not on protected URL.
    expect(page).not_to_have_url(re.compile(rf".*{re.escape(protected_path)}.*"))

    # Login UI is visible.
    expect(page.get_by_role("heading", name="QMagic")).to_be_visible()
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()
