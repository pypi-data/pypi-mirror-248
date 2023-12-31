from .seat import Seat

class Ticket:

    #Key = attribute name in class, value = attribute name in json response
    _JOURNEY_TICKET_KEY_ATTR_PAIRS = {
        'bus_code': 'busCode', 'trip_number': 'tripNumber', 'route_code': 'routeCode', 
        'route_name': 'routeName', 'via': 'via', 'depot_id': 'depotId', 'depot_name': 'depotName', 'available_seats': 'availableSeatCount', 'total_seats': 'totalSeatCount'
    }
    
    def __init__(self, ticket):
        if not ticket:
            raise Exception("No data")
        else:
            self.data = ticket
        self._initialize_class_attributes()
        
    def _initialize_class_attributes(self):
        if not self.data:
            raise Exception("No data")

        for key, value in self._JOURNEY_TICKET_KEY_ATTR_PAIRS.items():
                setattr(self, key, self.data.get(value, None))
        # Intialize Seats
        self.seats = []
        for seat in self.data.get('seats', []):
            self.seats.append( Seat(seat) )
        # TODO: Initialize Fare