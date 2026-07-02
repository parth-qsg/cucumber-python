from __future__ import annotations

from playwright.sync_api import Page

from framework.ui.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.element_name_mapping.update(
            {
                "Email Input": page.locator("#email"),
                "Password Input": page.locator("#password"),
                "Sign In Button": page.get_by_role("button", name="Sign In"),
                "Invalid Credentials Notification": page.get_by_text(
                    "Invalid credentials", exact=True
                ),
                "Login Heading": page.get_by_role("heading", name="QMagic"),
            }
        )

    def goto_login(self) -> "LoginPage":
        self.navigate("/login")
        return self
