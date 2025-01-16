SensorBridge FTDI Driver installation
======================================

The SensorBridge is a USB FTDI device and has a custom PID.
Special setup is needed such that the SensorBridge is detected by your operating system.

Windows
-------

Install the custom FTDI Driver for the SensorBridge.
You can download it from  https://control-center.sensirion.com/sensor-bridge/sensirion_sensor_bridge_ftdi_driver.zip

Note: this driver is also included in the ControlCenter installation.

MacOS
-----

No setup needed, the SensorBridge PID is registered in the system.

Linux
-----

To load the FTDI driver and activate it on the new PID one needs to run the following as root:

.. sourcecode:: bash

    modprobe ftdi_sio
    echo 0403 7168 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id

The above command will only add the Sensor Bridge dynamically until reboot.
To automate it on startup, one may create a custom udev rule:

.. sourcecode:: bash

    SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="7168", RUN+="/sbin/modprobe ftdi_sio", RUN+="/bin/sh -c 'echo 0403 7168 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id'"

Now one may reload the created rules and trigger them as super user:

.. sourcecode:: bash

    udevadm control --reload-rules
    udevadm trigger

