# Python Driver for Sensirion SEK-SensorBridge

This repository contains the SHDLC driver for the
[Sensirion SEK-SensorBridge](https://www.sensirion.com/sensorbridge/)
as a Python package. For details, please read the package description in
[README.rst](README.rst).

## Usage

See package description in [README.rst](README.rst) and user manual at
https://sensirion.github.io/python-shdlc-sensorbridge/.

## Development

We develop and test this driver using our company internal tools (version
control, continuous integration, code review etc.) and automatically
synchronize the `master` branch with GitHub. But this doesn't mean that we
don't respond to issues or don't accept pull requests on GitHub. In fact,
you're very welcome to open issues or create pull requests :)

### Check coding style

The coding style can be checked with [`flake8`](http://flake8.pycqa.org/):

```bash
pip install -e .[test]  # Install requirements
flake8                  # Run style check
```

In addition, we check the formatting of files with
[`editorconfig-checker`](https://editorconfig-checker.github.io/):

```bash
pip install editorconfig-checker==2.0.3   # Install requirements
editorconfig-checker                      # Run check
```

### Run tests

Unit tests can be run with [`pytest`](https://pytest.org/):

```bash
pip install -e .[test]          # Install requirements
pytest -m "not needs_device"    # Run tests without hardware
pytest                          # Run all tests
```

The tests with the marker `needs_device` have following requirements:

- A SensorBridge must be connected to the computer:
  - Firmware version must be 5.8
  - Default settings (baudrate 460800, address 0)
  - Port 0: SHTC3 connected
  - Port 1: No device connected
- Pass the serial port where the SensorBridge is connected with `--serial-port`,
  e.g. `pytest --serial-port=COM7`


### Build documentation

The documentation can be built with [Sphinx](http://www.sphinx-doc.org/):

```bash
python setup.py install                        # Install package
pip install -r docs/requirements.txt           # Install requirements
sphinx-versioning build docs docs/_build/html  # Build documentation
```

## License

See [LICENSE](LICENSE).
