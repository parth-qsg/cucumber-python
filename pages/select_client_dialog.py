"""SelectClientDialog — modal shown after successful credential submission."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from framework.ui.base_component import BaseComponent

if TYPE_CHECKING:
    from playwright.sync_api import Page

log = logging.getLogger(__name__)


class SelectClientDialog(BaseComponent):
    """Client selection dialog that appears immediately after login."""

    def __init__(self, page: "Page") -> None:
        super().__init__(page)

        self.dialog = page.get_by_role("dialog")
        self.select_client_combobox = page.get_by_role("combobox")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.confirm_button = page.get_by_role("button", name="Confirm")

        self.element_name_mapping.update(
            {
                "Select Client Dialog": self.dialog,
                "Select Client Combobox": self.select_client_combobox,
                "Cancel Button": self.cancel_button,
                "Confirm Button": self.confirm_button,
            }
        )

    def wait_until_visible(self) -> "SelectClientDialog":
        """Wait for the dialog to appear."""
        self.dialog.wait_for(state="visible", timeout=30_000)
        return self

    def select_client_and_confirm(self, client_value: str) -> None:
        """Select a client by option value and confirm."""
        self.select_option("Select Client Combobox", client_value)
        self.click("Confirm Button")
