
class Seat:

    def __init__(self, seat):
        self.code = seat.get('code', None)
        self.status = seat.get('status', None)
        self.gender = seat.get('gender', None)

    def is_booked(self):
        return False if self.status=='0' else True