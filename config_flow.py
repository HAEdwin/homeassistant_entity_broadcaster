"""Config flow for Entity Broadcaster integration."""

from __future__ import annotations

import logging
import socket
from typing import Any
import voluptuous as vol


from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "entity_broadcaster"

# Default values
DEFAULT_UDP_PORT = 8888
MIN_UDP_PORT = 1024
MAX_UDP_PORT = 65535

# Configuration keys
CONF_ENTITIES = "entities"
CONF_UDP_PORT = "udp_port"
CONF_NAME = "name"


class EntityBroadcasterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Entity Broadcaster."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._entities: list[str] = []
        self._udp_port: int = DEFAULT_UDP_PORT
        self._name: str = ""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate the name is unique
            await self.async_set_unique_id(user_input[CONF_NAME])
            self._abort_if_unique_id_configured()

            self._name = user_input[CONF_NAME]
            return await self.async_step_entities()

        # Schema for the initial step (name configuration)
        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Entity Broadcaster"): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_entities(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle entity selection step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            entities = user_input.get(CONF_ENTITIES, [])

            if not entities:
                errors[CONF_ENTITIES] = "no_entities_selected"
            else:
                self._entities = entities
                return await self.async_step_network()

        # Get all entities for selection
        entity_registry = async_get_entity_registry(self.hass)
        entity_options = []

        for entity in entity_registry.entities.values():
            if entity.entity_id and not entity.disabled:
                entity_options.append(
                    {
                        "value": entity.entity_id,
                        "label": f"{entity.entity_id} ({entity.name or entity.entity_id})",
                    }
                )

        # Sort entities alphabetically
        entity_options.sort(key=lambda x: x["label"])

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ENTITIES): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=entity_options,
                        multiple=True,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="entities",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "name": self._name,
            },
        )

    async def async_step_network(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle network configuration step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            udp_port = user_input[CONF_UDP_PORT]

            # Validate UDP port
            if not self._is_port_available(udp_port):
                errors[CONF_UDP_PORT] = "port_in_use"
            else:
                self._udp_port = udp_port

                # Create the config entry
                return self.async_create_entry(
                    title=self._name,
                    data={
                        CONF_NAME: self._name,
                        CONF_ENTITIES: self._entities,
                        CONF_UDP_PORT: self._udp_port,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_UDP_PORT, default=DEFAULT_UDP_PORT): vol.All(
                    vol.Coerce(int), vol.Range(min=MIN_UDP_PORT, max=MAX_UDP_PORT)
                ),
            }
        )

        return self.async_show_form(
            step_id="network",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "name": self._name,
                "entity_count": len(self._entities),
                "min_port": MIN_UDP_PORT,
                "max_port": MAX_UDP_PORT,
            },
        )

    def _is_port_available(self, port: int) -> bool:
        """Check if the UDP port is available."""

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(("", port))
                return True
        except OSError:
            return False

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> EntityBroadcasterOptionsFlow:
        """Get the options flow for this handler."""
        return EntityBroadcasterOptionsFlow(config_entry)


class EntityBroadcasterOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Entity Broadcaster."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self._entities: list[str] = config_entry.data.get(CONF_ENTITIES, [])
        self._udp_port: int = config_entry.data.get(CONF_UDP_PORT, DEFAULT_UDP_PORT)

    async def async_step_init(self) -> FlowResult:
        """Manage the options."""
        return await self.async_step_entities()

    async def async_step_entities(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle entity selection in options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            entities = user_input.get(CONF_ENTITIES, [])

            if not entities:
                errors[CONF_ENTITIES] = "no_entities_selected"
            else:
                self._entities = entities
                return await self.async_step_network()

        # Get all entities for selection
        entity_registry = async_get_entity_registry(self.hass)
        entity_options = []

        for entity in entity_registry.entities.values():
            if entity.entity_id and not entity.disabled:
                entity_options.append(
                    {
                        "value": entity.entity_id,
                        "label": f"{entity.entity_id} ({entity.name or entity.entity_id})",
                    }
                )

        # Sort entities alphabetically
        entity_options.sort(key=lambda x: x["label"])

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_ENTITIES, default=self._entities
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=entity_options,
                        multiple=True,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="entities",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_network(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle network configuration in options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            udp_port = user_input[CONF_UDP_PORT]

            # Only validate port if it's different from current
            if udp_port != self._udp_port and not self._is_port_available(udp_port):
                errors[CONF_UDP_PORT] = "port_in_use"
            else:
                self._udp_port = udp_port

                # Update the config entry
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_ENTITIES: self._entities,
                        CONF_UDP_PORT: self._udp_port,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_UDP_PORT, default=self._udp_port): vol.All(
                    vol.Coerce(int), vol.Range(min=MIN_UDP_PORT, max=MAX_UDP_PORT)
                ),
            }
        )

        return self.async_show_form(
            step_id="network",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "entity_count": len(self._entities),
                "min_port": MIN_UDP_PORT,
                "max_port": MAX_UDP_PORT,
            },
        )

    def _is_port_available(self, port: int) -> bool:
        """Check if the UDP port is available."""

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(("", port))
                return True
        except OSError:
            return False
