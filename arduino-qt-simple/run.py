

from lantz.ino import INODriver, QuantityFeat
from lantz.qt import Backend, Frontend, InstrumentSlot

# The driver would normally go into a different file.
# This is just for demonstration purposes.

class TemperatureSensor(INODriver):

    # We create a read only property for the arduino
    temperature = QuantityFeat('TEMP', units='degC', setter=False)


class Temperature(Backend):

    # Here we define that this backend requires an instrument assigned to
    # a variable named board.
    # This line could be just board = InstrumentSlot
    # By adding the TemperatureSensor after the semicolon
    # allows PyCharm and other IDE to provide autocompletion
    board: TemperatureSensor = InstrumentSlot

    _last_temperature = None

    def update_temperature(self):
        self.log_debug('Updating temperature')

        # Just by reading the temperature, any element in the frontend connected
        # to the temperature feat will be updated.
        # We store it just for fun
        self._last_temperature = self.board.temperature


class TemperatureUi(Frontend):

    # This line is completely unnecesary to run the program
    # (backend is already defined in the Frontend parent class)
    # But adding it allows PyCharm and other IDE to provide autocompletion
    backend: Temperature

    # Instead of drawing the gui programatically, we use QtDesigner and just load it.
    # The resulting gui will be inside an attribute named widget
    gui = 'temperature_simple.ui'


    def connect_backend(self):

        # This method is executed after the backend is assigned to the frontend

        # First we call the parent method
        super().connect_backend()

        # Then we connect
        #  the temperature widget
        #  to the board instrument in the backend,
        #  and specifically to the feat named temperature (Notice that is a string)
        self.connect_feat(self.widget.temperature, self.backend.board, 'temperature')

        # we also connect the button to a method in the backend.
        self.widget.btn_update.clicked.connect(self.backend.update_temperature)


if __name__ == '__main__':

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
        app = Temperature(board=board)

        # Then we use the start_gui_app. Notice that we provide the class for the Ui, not an instance
        start_gui_app(app, TemperatureUi)




