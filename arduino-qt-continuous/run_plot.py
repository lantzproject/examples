from drivers import TemperatureSensor

from app import TemperatureMonitor, TemperaturePlotterUi

if __name__ == '__main__':

    from lantz.core import ureg

    from lantz.core.log import log_to_screen, log_to_socket, DEBUG

    from lantz.qt import start_gui_app, wrap_driver_cls

    # Uncommment this line to log to socket
    # log_to_socket(DEBUG)

    # or comment this line to stop logging
    log_to_screen(DEBUG)

    # Instead of using the TemperatureSensor driver, we automagically create
    # a Qt aware version of it. This allows
    QTemperatureSensor = wrap_driver_cls(TemperatureSensor)

    # We initialize the board via the packfile to autodetect it.
    # You can alternative use the COMPORT using the `via_serial`
    # However, notice that using the packfile is superior as it allows you:
    # - to check if the software on the arduino is up to date with the version on your computer.
    #   and update it if necessary.
    # - works even if the comport has changed
    # - you can specify the model and/or serialno of the board to use a particular one
    #   if you have many connected.

    # The `with` syntax as equivalent to:
    # - instantiate the driver
    # - initialize the driver
    # - finalize the driver (even if there was a bug and the software crashes!)

    with QTemperatureSensor.via_packfile('TemperatureSensor.pack.yaml', check_update=True) as board:
        # We then create the backend and provide the driver we have just created
        # This will be bound to the corresponding instrument slot
        app = TemperatureMonitor(interval=5 * ureg.second, board=board)

        # Then we use the start_gui_app. Notice that we provide the class for the Ui, not an instance
        start_gui_app(app, TemperaturePlotterUi)
