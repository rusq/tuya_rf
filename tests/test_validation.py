import importlib.util
from pathlib import Path

import pytest


esphome = pytest.importorskip("esphome")
spec = importlib.util.spec_from_file_location(
    "tuya_rf_config", Path(__file__).parents[1] / "components/tuya_rf/__init__.py"
)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


def test_receiver_is_disabled_by_default():
    assert config.DEFAULT_RECEIVER_DISABLED is True


@pytest.mark.parametrize("value", ["0b", "39b", "17kb", "16385b"])
def test_buffer_size_rejects_unsafe_values(value):
    with pytest.raises(config.cv.Invalid):
        config.validate_buffer_size(value)


@pytest.mark.parametrize("value", ["40b", "41b", "16kb", "16383b"])
def test_buffer_size_accepts_safe_values(value):
    assert config.validate_buffer_size(value) >= config.MIN_BUFFER_SIZE


def test_equal_pulse_thresholds_are_rejected():
    values = {
        config.CONF_START_PULSE_MIN: 6000,
        config.CONF_START_PULSE_MAX: 6000,
        config.CONF_END_PULSE: 50000,
    }
    with pytest.raises(config.cv.Invalid):
        config.validate_pulses(values)


def test_end_threshold_must_exceed_start_maximum():
    values = {
        config.CONF_START_PULSE_MIN: 6000,
        config.CONF_START_PULSE_MAX: 10000,
        config.CONF_END_PULSE: 10000,
    }
    with pytest.raises(config.cv.Invalid):
        config.validate_pulses(values)
