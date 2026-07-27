"""UserStoriesPage — POM for the authenticated landing page (/user-stories)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from framework.ui.base_page import BasePage
from framework.ui.page_factory import PageFactory

if TYPE_CHECKING:
    from playwright.sync_api import Page

log = logging.getLogger(__name__)


class UserStoriesPage(BasePage):
    """Authenticated landing page after login and client confirmation."""

    PAGE_PATH = "/user-stories"

    def __init__(self, page: "Page", base_url: str) -> None:
        super().__init__(page, base_url)

        self.user_stories_link = page.get_by_role("link", name="User Stories")
        self.execution_link = page.get_by_role("link", name="Execution")
        self.account_menu_button = page.get_by_role(
            "button", name="Account menu for Jane Smith"
        )

        self.element_name_mapping.update(
            {
                "User Stories Link": self.user_stories_link,
                "Execution Link": self.execution_link,
                "Account Menu Button": self.account_menu_button,
            }
        )

    def wait_until_loaded(self) -> "UserStoriesPage":
        """Wait for a landmark authenticated element to be visible."""
        self.user_stories_link.wait_for(state="visible", timeout=30_000)
        return self


PageFactory.register("User Stories Page", UserStoriesPage)
