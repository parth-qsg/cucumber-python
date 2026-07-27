import os

import pytest

from framework.contexts.ui_context import UIContext
from pages.select_client_dialog import SelectClientDialog


@pytest.mark.ui
@pytest.mark.smoke
def test_ite_tc_1_successful_login_with_valid_credentials(
    ui_context: UIContext, base_url: str, credentials: dict
) -> None:
    """Verify a registered user can log in with valid credentials and reach an authenticated page."""

    # Arrange
    username = (
        os.environ.get("TEST_USERNAME")
        or os.environ.get("APP_USERNAME")
        or credentials.get("admin", {}).get("username", "")
    )
    password = (
        os.environ.get("TEST_PASSWORD")
        or os.environ.get("APP_PASSWORD")
        or credentials.get("admin", {}).get("password", "")
    )

    login_page = ui_context.page_factory("Login Page")
    login_page.navigate()

    # Verify login page is displayed
    login_page.wait_for_visible("Email Input", timeout=30_000)
    login_page.expect_visible("Password Input")
    login_page.expect_visible("Sign In Button")

    # Act
    login_page.fill("Email Input", username)
    login_page.expect_value("Email Input", username)

    login_page.fill("Password Input", password)
    login_page.click("Sign In Button")

    select_client = SelectClientDialog(ui_context.page)
    select_client.wait_until_visible()
    select_client.select_client_and_confirm("TEST")

    # Assert
    assert "/login" not in ui_context.page.url

    user_stories_page = ui_context.page_factory("User Stories Page")
    user_stories_page.wait_until_loaded()
    user_stories_page.expect_visible("User Stories Link")
    user_stories_page.expect_visible("Execution Link")


KEY_RECONCILIATION_AUDIT = """
KEY RECONCILIATION AUDIT:
✅ "Email Input"                     → found in LoginPage.element_name_mapping
✅ "Password Input"                  → found in LoginPage.element_name_mapping
✅ "Sign In Button"                  → found in LoginPage.element_name_mapping
✅ "User Stories Link"               → found in UserStoriesPage.element_name_mapping
✅ "Execution Link"                  → found in UserStoriesPage.element_name_mapping
✅ "Select Client Dialog"            → found in SelectClientDialog.element_name_mapping
✅ "Select Client Combobox"          → found in SelectClientDialog.element_name_mapping
✅ "Confirm Button"                  → found in SelectClientDialog.element_name_mapping
"""
