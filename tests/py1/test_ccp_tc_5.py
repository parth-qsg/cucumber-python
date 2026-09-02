import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.login_page import LoginPage

scenarios("../../features/py1/ccp_tc_5.feature")


@pytest.fixture
def protected_path() -> str:
    # Discovered via browser exploration: authenticated navigation lands on /user-stories.
    # This route redirects to /login when unauthenticated.
    return "/user-stories"


@given("no authenticated session exists in the browser")
def no_authenticated_session_exists(page: Page) -> None:
    page.context.clear_cookies()
    page.goto("about:blank")
    page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")


@when(
    "the user attempts to navigate directly to a protected page URL on demo.qmagic.ai"
)
def user_navigates_directly_to_protected_page(
    page: Page, base_url: str, protected_path: str
) -> None:
    page.goto(f"{base_url}{protected_path}", wait_until="domcontentloaded")


@then("the application denies access to the protected content")
def application_denies_access(page: Page) -> None:
    expect(page).to_have_url(re.compile(r".*/login(?:\?.*)?$"))


@then("the user is redirected to the login page")
def user_redirected_to_login_page(page: Page, base_url: str) -> None:
    expect(page).to_have_url(re.compile(r".*/login(?:\?.*)?$"))

    login_page = LoginPage(page, base_url)
    login_page.expect_visible("Email Input")
    login_page.expect_visible("Password Input")
    login_page.expect_visible("Sign In Button")


@then("no protected page content is rendered or exposed")
def no_protected_content_rendered(page: Page) -> None:
    expect(page.get_by_role("link", name="Dashboard")).not_to_be_visible()
    expect(page.get_by_role("link", name="User Stories")).not_to_be_visible()
    expect(page.get_by_role("link", name="Execution")).not_to_be_visible()

    # Authenticated /user-stories page shows a "Products" heading; ensure it is not present.
    expect(page.get_by_role("heading", name="Products")).not_to_be_visible()
