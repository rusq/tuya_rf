import importlib.util
from pathlib import Path

import pytest


pytest.importorskip("tinytuya")
spec = importlib.util.spec_from_file_location(
    "gencodes", Path(__file__).parents[1] / "gencodes.py"
)
gencodes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gencodes)


def test_generator_uses_structured_decoder(monkeypatch, capsys):
    class FakeRF:
        @staticmethod
        def rf_decode_button(value):
            assert value == "encoded"
            return {"data0": "pulses"}

        @staticmethod
        def base64_to_pulses(value):
            assert value == "pulses"
            return [1, 2]

    monkeypatch.setattr(gencodes, "rf", FakeRF)
    monkeypatch.setattr(gencodes, "buttons", {"test": "encoded"})
    gencodes.generate_codes()
    output = capsys.readouterr().out
    assert "code: [1,-2]" in output
