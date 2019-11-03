"""Tests for HomematicIP Cloud switch."""
from homeassistant.components.homematicip_cloud import DOMAIN as HMIPC_DOMAIN
from homeassistant.components.homematicip_cloud.device import (
    ATTR_GROUP_MEMBER_UNREACHABLE,
)
from homeassistant.components.switch import (
    ATTR_CURRENT_POWER_W,
    ATTR_TODAY_ENERGY_KWH,
    DOMAIN as SWITCH_DOMAIN,
)
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.setup import async_setup_component

from .helper import async_manipulate_test_data, get_and_check_entity_basics


async def test_manually_configured_platform(hass):
    """Test that we do not set up an access point."""
    assert (
        await async_setup_component(
            hass, SWITCH_DOMAIN, {SWITCH_DOMAIN: {"platform": HMIPC_DOMAIN}}
        )
        is True
    )
    assert not hass.data.get(HMIPC_DOMAIN)


async def test_hmip_switch(hass, default_mock_hap):
    """Test HomematicipSwitch."""
    entity_id = "switch.schrank"
    entity_name = "Schrank"
    device_model = "HMIP-PS"

    ha_state, hmip_device = get_and_check_entity_basics(
        hass, default_mock_hap, entity_id, entity_name, device_model
    )

    assert ha_state.state == STATE_ON
    service_call_counter = len(hmip_device.mock_calls)

    await hass.services.async_call(
        "switch", "turn_off", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 1
    assert hmip_device.mock_calls[-1][0] == "turn_off"
    assert hmip_device.mock_calls[-1][1] == ()
    await async_manipulate_test_data(hass, hmip_device, "on", False)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_OFF

    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 3
    assert hmip_device.mock_calls[-1][0] == "turn_on"
    assert hmip_device.mock_calls[-1][1] == ()
    await async_manipulate_test_data(hass, hmip_device, "on", True)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_ON


async def test_hmip_switch_measuring(hass, default_mock_hap):
    """Test HomematicipSwitchMeasuring."""
    entity_id = "switch.pc"
    entity_name = "Pc"
    device_model = "HMIP-PSM"

    ha_state, hmip_device = get_and_check_entity_basics(
        hass, default_mock_hap, entity_id, entity_name, device_model
    )

    assert ha_state.state == STATE_ON
    service_call_counter = len(hmip_device.mock_calls)

    await hass.services.async_call(
        "switch", "turn_off", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 1
    assert hmip_device.mock_calls[-1][0] == "turn_off"
    assert hmip_device.mock_calls[-1][1] == ()
    await async_manipulate_test_data(hass, hmip_device, "on", False)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_OFF

    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 3
    assert hmip_device.mock_calls[-1][0] == "turn_on"
    assert hmip_device.mock_calls[-1][1] == ()
    await async_manipulate_test_data(hass, hmip_device, "on", True)
    await async_manipulate_test_data(hass, hmip_device, "currentPowerConsumption", 50)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_ON
    assert ha_state.attributes[ATTR_CURRENT_POWER_W] == 50
    assert ha_state.attributes[ATTR_TODAY_ENERGY_KWH] == 36

    await async_manipulate_test_data(hass, hmip_device, "energyCounter", None)
    ha_state = hass.states.get(entity_id)
    assert not ha_state.attributes.get(ATTR_TODAY_ENERGY_KWH)


async def test_hmip_group_switch(hass, default_mock_hap):
    """Test HomematicipGroupSwitch."""
    entity_id = "switch.strom_group"
    entity_name = "Strom Group"
    device_model = None

    ha_state, hmip_device = get_and_check_entity_basics(
        hass, default_mock_hap, entity_id, entity_name, device_model
    )

    assert ha_state.state == STATE_ON
    service_call_counter = len(hmip_device.mock_calls)

    await hass.services.async_call(
        "switch", "turn_off", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 1
    assert hmip_device.mock_calls[-1][0] == "turn_off"
    assert hmip_device.mock_calls[-1][1] == ()
    await async_manipulate_test_data(hass, hmip_device, "on", False)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_OFF

    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 3
    assert hmip_device.mock_calls[-1][0] == "turn_on"
    assert hmip_device.mock_calls[-1][1] == ()
    await async_manipulate_test_data(hass, hmip_device, "on", True)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_ON

    assert not ha_state.attributes.get(ATTR_GROUP_MEMBER_UNREACHABLE)
    await async_manipulate_test_data(hass, hmip_device, "unreach", True)
    ha_state = hass.states.get(entity_id)
    assert ha_state.attributes[ATTR_GROUP_MEMBER_UNREACHABLE] is True


async def test_hmip_multi_switch(hass, default_mock_hap):
    """Test HomematicipMultiSwitch."""
    entity_id = "switch.jalousien_1_kizi_2_schlazi_channel1"
    entity_name = "Jalousien - 1 KiZi, 2 SchlaZi Channel1"
    device_model = "HmIP-PCBS2"

    ha_state, hmip_device = get_and_check_entity_basics(
        hass, default_mock_hap, entity_id, entity_name, device_model
    )

    assert ha_state.state == STATE_OFF
    service_call_counter = len(hmip_device.mock_calls)

    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 1
    assert hmip_device.mock_calls[-1][0] == "turn_on"
    assert hmip_device.mock_calls[-1][1] == (1,)
    await async_manipulate_test_data(hass, hmip_device, "on", True)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_ON

    await hass.services.async_call(
        "switch", "turn_off", {"entity_id": entity_id}, blocking=True
    )
    assert len(hmip_device.mock_calls) == service_call_counter + 3
    assert hmip_device.mock_calls[-1][0] == "turn_off"
    assert hmip_device.mock_calls[-1][1] == (1,)
    await async_manipulate_test_data(hass, hmip_device, "on", False)
    ha_state = hass.states.get(entity_id)
    assert ha_state.state == STATE_OFF
