"""The Entity Broadcaster integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_ENTITIES, CONF_UDP_PORT, CONF_NAME
from .broadcaster import EntityBroadcaster

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = []


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Entity Broadcaster from a config entry."""
    _LOGGER.debug("Setting up Entity Broadcaster with config: %s", entry.data)

    # Extract configuration
    entities = entry.data.get(CONF_ENTITIES, [])
    udp_port = entry.data.get(CONF_UDP_PORT)
    name = entry.data.get(CONF_NAME, "Entity Broadcaster")

    # Create and setup the broadcaster
    broadcaster = EntityBroadcaster(hass, entities, udp_port, name)

    if not await broadcaster.async_setup():
        _LOGGER.error("Failed to setup Entity Broadcaster")
        return False

    # Store the broadcaster instance
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "broadcaster": broadcaster,
        "config": entry.data,
    }

    # Set up update listener for config changes
    entry.async_on_unload(entry.add_update_listener(async_update_listener))

    # Forward the setup to the platforms if any
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener for config entry options."""
    data = hass.data[DOMAIN][entry.entry_id]
    broadcaster = data["broadcaster"]

    # Get updated configuration from options or data
    entities = entry.options.get(CONF_ENTITIES) or entry.data.get(CONF_ENTITIES, [])
    udp_port = entry.options.get(CONF_UDP_PORT) or entry.data.get(CONF_UDP_PORT)

    # Update broadcaster with new configuration
    await broadcaster.async_update_entities(entities)
    await broadcaster.async_update_port(udp_port)

    _LOGGER.info("Updated Entity Broadcaster configuration")


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Entity Broadcaster config entry: %s", entry.entry_id)

    # Shutdown the broadcaster
    data = hass.data[DOMAIN].get(entry.entry_id)
    if data and "broadcaster" in data:
        await data["broadcaster"].async_shutdown()

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
