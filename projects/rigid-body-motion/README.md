# Rigid Body Motion

Rigid Body Motion is a project for the Pico that aims to accurately describe the motion of a rigid body in space. It's currently in the heavy experimentation phase, and will require a lot more work before this project reaches MVP.

As of 4/28/2023, it collects data that's to be processed later. It's a data collection tool. In reality, it'll probably stay this way, as the Pico isn't suitable for the kinds of extensive computations that I'd like to do.

## Usage
---
It's expected that a microSD card will be connected to the Pico and used for storing data. When the Pico is run, it creates a folder on the microSD which will contain run details. A "run" is just a single instance of the Pico collecting data. Global configuration settings can be found in `config.json`. Run-level settings are set via the `metadata` object defined in `main.py`. The configuration used in a particular run will be saved in the run's directory as `metadata.json`.

When the Pico runs, it'll read from the MPU6050 and create an entry for the CSV `run_id.csv`.

## Pin Mapping
---

|Device|DevPin|PicoGP|PicoPin|
|---|---|---|---|
| MicroSD | `CS` | `GP1` | 2 |
|| `SCK` | `GP2` | 4 |
|| `MOSI` | `GP3` | 5 |
|| `MISO` | `GP0` | 1 |
|| `VCC` | `5V` |-|
|| `GND` | `GND` |-|
| MPU6050 | `VCC` | `3.3` |-|
|| `GND` | `GND` |-|
|| `SCL` | `GP5` | 7 |
|| `SDA` | `GP4` | 6 |
