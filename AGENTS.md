# Repository Guidelines

## Project Structure & Module Organization

This repository provides an ESPHome external component for a Tuya RF433 bridge using a CBU/BK7231N and CMT2300A radio. The implementation lives in `components/tuya_rf/`: `__init__.py` defines ESPHome configuration validation and code generation, `tuya_rf*.cpp` and `tuya_rf.h` integrate with ESPHome, and the `cmt2300a*`, `cmt_spi3*`, and `radio*` files contain the lower-level radio driver. `automation.*` implements receiver on/off actions. `tuya.yaml` is the example device configuration, while `gencodes.py` converts captured TinyTuya RF data into ESPHome raw-transmit YAML. User-facing configuration belongs in `README.md`.

## Build, Test, and Development Commands

- `esphome config tuya.yaml` validates the example configuration and component schema. Provide a local `secrets.yaml` with `wifi_ssid`, `wifi_password`, and `ota_password`; never commit it.
- `esphome compile tuya.yaml` generates and compiles firmware for the configured CBU board without flashing hardware.
- `esphome run tuya.yaml` compiles, uploads, and tails logs; use only with the intended device connected or reachable.
- `python3 gencodes.py` regenerates YAML snippets from captured codes and requires `tinytuya`.

There is no standalone unit-test suite. At minimum, run configuration validation and compilation after changing Python schemas, C/C++ interfaces, pins, or the example YAML.

## Coding Style & Naming Conventions

Follow surrounding ESPHome conventions: four spaces in Python, two spaces in C/C++, braces on the same line, and `snake_case` configuration keys. C++ members use a trailing underscore (for example, `receiver_disabled_`), constants use uppercase names, and component APIs remain under `esphome::tuya_rf`. Keep C driver naming consistent with the existing vendor-style files. Avoid broad formatting-only changes to imported radio code.

## Testing Guidelines

For RF behavior changes, supplement compilation with device testing. Verify receive filtering, TX-to-RX restoration, and both `tuya_rf.turn_on_receiver` and `tuya_rf.turn_off_receiver`. Record the board, relevant pins, remote tested, and representative logs in the pull request. Do not assume timings captured from one remote suit every protocol.

## Commit & Pull Request Guidelines

History favors short, imperative, narrowly scoped subjects such as `reverse polarity of rf carrier`. Keep each commit focused and mention issue numbers when applicable. Pull requests should explain the behavioral change, list validation commands, identify hardware testing performed, and update `README.md` or `tuya.yaml` when configuration changes. Include logs or screenshots when they clarify ESPHome or web-server behavior.
