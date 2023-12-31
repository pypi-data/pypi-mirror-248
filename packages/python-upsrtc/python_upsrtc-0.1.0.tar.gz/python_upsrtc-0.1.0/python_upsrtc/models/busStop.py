
class BusStop:

    #Key = attribute name in class, value = attribute name in json response
    _BUS_STOP_KEY_ATTR_PAIRS = {
        'name': 'name', 'code': 'code', 
        'latitude': 'latitude', 'longitude': 'longitude',
        'address': 'address', 'id': 'id', 'direction': 'direction',
        'abbreviation': 'abbreviation'
    }
    
    def __init__(self,data):
        if not data:
            raise Exception("No data")
        else:
            self.data = data
        self._initialize_class_attributes()

    def _initialize_class_attributes(self):
        if not self.data:
            raise Exception("No data")

        for key, value in self._BUS_STOP_KEY_ATTR_PAIRS.items():
                setattr(self, key, self.data.get(value, None))