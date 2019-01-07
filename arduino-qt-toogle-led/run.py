from lantz.ino import INODriver, BoolFeat
from lantz.qt import Backend, Frontend, InstrumentSlot

class LEDDriver(INODriver):
    led = BoolFeat('LED')

class LEDBackend(Backend):
    board: LEDDriver = InstrumentSlot

    def turn_on_LED_method(self):
        self.board.led = True
    
    def turn_off_LED_method(self):
        self.board.led = False

class LEDUserInterfase(Frontend):
    gui = 'LED.ui'

    def connect_backend(self):
        super().connect_backend()
        self.widget.turn_on_led_button.clicked.connect(self.backend.turn_on_LED_method)
        self.widget.turn_off_led_button.clicked.connect(self.backend.turn_off_LED_method)
        

if __name__ == '__main__':
    from lantz.core.log import log_to_screen, log_to_socket, DEBUG
    from lantz.qt import start_gui_app, wrap_driver_cls
    
    # ~ log_to_socket(DEBUG) # Uncommment this line to log to socket
    log_to_screen(DEBUG) # or comment this line to stop logging

    QLED = wrap_driver_cls(LEDDriver)
    with QLED.via_packfile('LEDDriver.pack.yaml', check_update=True) as board:
        app = LEDBackend(board=board)
        start_gui_app(app, LEDUserInterfase)




