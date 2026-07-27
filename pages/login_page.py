"""LoginPage — POM for the QMagic login page."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from framework.ui.base_page import BasePage
from framework.ui.page_factory import PageFactory

if TYPE_CHECKING:
    from playwright.sync_api import Page

log = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page actions and assertions."""

    PAGE_PATH = "/login"

    def __init__(self, page: "Page", base_url: str) -> None:
        super().__init__(page, base_url)

        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.invalid_credentials_notification = page.get_by_text(
            "Invalid credentials", exact=True
        )

        self.element_name_mapping.update(
            {
                "Email Input": self.email_input,
                "Password Input": self.password_input,
                "Sign In Button": self.sign_in_button,
                "Invalid Credentials Notification": self.invalid_credentials_notification,
            }
        )

    def navigate(self) -> "LoginPage":
        """Navigate to the login page and wait for it to be ready."""
        super().navigate(self.PAGE_PATH)
        self.email_input.wait_for(state="visible", timeout=30_000)
        return self

    def open(self) -> "LoginPage":
        """Backward-compatible alias for navigate()."""
        return self.navigate()


PageFactory.register("Login Page", LoginPage)
