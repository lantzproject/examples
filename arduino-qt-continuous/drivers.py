

from lantz.ino import INODriver, QuantityFeat

class TemperatureSensor(INODriver):

    # We create a read only property for the arduino
    temperature = QuantityFeat('TEMP', units='degC', setter=False)
