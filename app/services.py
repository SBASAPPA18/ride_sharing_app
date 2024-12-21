class RideService:
    def get_ride(self, ride_id: int):
        return {"ride_id": ride_id, "status": "active"}