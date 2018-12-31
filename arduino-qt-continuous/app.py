
import time

from lantz.core import ureg

from lantz.qt import Backend, Frontend, InstrumentSlot, QtCore

from lantz.qt.blocks import ChartUi, VerticalUi

from drivers import TemperatureSensor


class TemperatureMonitor(Backend):

    # Here we define that this backend requires an instrument assigned to
    # a variable named board.
    # This line could be just board = InstrumentSlot
    # By adding the TemperatureSensor after the semicolon
    # allows PyCharm and other IDE to provide autocompletion
    board: TemperatureSensor = InstrumentSlot

    # We create a Signal that will be emitted every time the timer ticks
    new_data = QtCore.pyqtSignal(object, object)

    # We also create signals every time the Timer is started or stopped.
    started = QtCore.pyqtSignal()
    stopped = QtCore.pyqtSignal()

    def __init__(self, interval, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If the user is smart, she will provide a Pint Quantity.
        try:
            interval = interval.to('ms').magnitude
        except:
            pass

        # This timer will run periodically and call update temperature.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval) # ms
        self.timer.timeout.connect(self.update_temperature)

    def update_temperature(self):
        self.log_debug('Updating temperature')

        now = time.monotonic() * ureg.ms
        temp = self.board.temperature
        self.new_data.emit(now, temp)
        self.log_debug('The temperature is {} at {}'.format(temp, now))

    def start_stop(self, value):
        if value:
            self.timer.start()
            self.started.emit()
            self.log_debug('Timer started')
        else:
            self.timer.stop()
            self.stopped.emit()
            self.log_debug('Timer stopped')


# This is a very simple interface containing:
# - a check box to start/stop the timer
# - spin box to display the temperature

class TemperatureMonitorUi(Frontend):

    # This line is completely unnecesary to run the program
    # (backend is already defined in the Frontend parent class)
    # But adding it allows PyCharm and other IDE to provide autocompletion
    backend: TemperatureMonitor

    # Instead of drawing the gui programatically, we use QtDesigner and just load it.
    # The resulting gui will be inside an attribute named widget
    gui = 'temperature_continuous.ui'

    def connect_backend(self):

        # This method is executed after the backend is assigned to the frontend

        # First we call the parent method
        super().connect_backend()

        # Then we connect
        #  the temperature widget
        #  to the board instrument in the backend,
        #  and specifically to the feat named temperature (Notice that is a string)
        self.connect_feat(self.widget.temperature, self.backend.board, 'temperature')

        # We also connect the check box
        # Check boxes in Qt are annoying because they have 3 states: Unchecked(0)/PartiallyChecked(1)/Checked(2)
        # We go through the lambda function so that the Backend receives a boolean value.
        self.widget.chk_update.stateChanged.connect(lambda new_value: self.backend.start_stop(new_value == 2))


# This interface combines the previous one with a chart

class TemperaturePlotterUi(VerticalUi):
    """ """

    # We embed two existing Frontends.
    # We reuse first the temperature monitor! and we provide the same backend
    monitorui = TemperatureMonitorUi.using_parent_backend()

    # The ChartUi, which plot a dataset point-by-point using pyqtgraph
    # Notice we do not use a backend for this.
    chartui = ChartUi

    # Here we tell HorizonalUi how we want to organize the widgets
    # Notice that we need to put the names of the attributes as strings.

    parts = ('monitorui',  # The TemperatureMonitorUi will be in the first colum
             'chartui')   # The ChartUI will be in the second column.

    def connect_backend(self):
        """ """

        # This method is called after gui has been loaded (referenced in self.widget)
        # and the backend is connected to the frontend (referenced in self.backend).
        # In this case, we use it to connect the new_data signal of the backend
        # with the plot function in ChartUi
        self.backend.new_data.connect(self.chartui.plot)

        # To clear the chart every time we start a series
        # we connect the request start signal of the user interface
        # to the clear method of the chart ui
        self.backend.started.connect(self.chartui.clear)

        super().connect_backend()

        # We define the labels and the units to use.
        # ChartUi will automatically convert.
        self.chartui.ylabel = 'temperature'
        self.chartui.yunits = 'degC'

        self.chartui.xlabel = 'time'
        self.chartui.xunits = 's'

        # Notice that the units is not just a change to the label,
        # it rescales the values that are shown in the plot.







