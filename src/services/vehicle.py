import re
from functools import lru_cache
from typing import Optional

from databases import Database
from fastapi import Depends

from db.postgre import get_database
from models.vehicle import Vehicle
from schemas.vehicle import vehicles
from services.decoder import get_vin_decoder_service, BaseVinDecoder


class VehicleService:
    """Service for interacting with vehicle data using a database and a VIN (Vehicle Identification Number) service."""

    def __init__(self, db: Database, vin_service: BaseVinDecoder) -> None:
        """Initializes a VehicleService instance.

        :param db: The SQLAlchemy database session used to store and retrieve vehicle information.
        """

        self.db = db
        self.vin_service = vin_service

    async def get_vehicle_data(self, vin: str) -> Optional[Vehicle]:
        """Fetches vehicle data by VIN. If the data is not in the database, it fetches it from the VIN service,
         stores it in the database, and returns the vehicle data.

        :param vin: The Vehicle Identification Number (VIN) of the vehicle.
        :return: A Vehicle instance containing the vehicle data, or None if the data is not found.
        """

        if not await self.validate_vin(vin):
            return None

        vehicle = await self._vehicle_from_db(vin)
        if not vehicle:
            vehicle = await self._load_vehicle_data(vin)
            await self._vehicle_to_db(vehicle, vin)
            return vehicle

        return vehicle

    async def validate_vin(self, vin: str) -> bool:
        """Validates a Vehicle Identification Number (VIN) to ensure it conforms to the expected format.

        :param vin: The Vehicle Identification Number (VIN) of the vehicle.
        :return: True if the VIN is valid; otherwise, False.
        """

        pattern = '(?=.*\d|=.*[A-Z])(?=.*[A-Z])[A-Z0-9]{17}$'
        result = re.match(pattern, vin)
        return bool(result)

    async def _load_vehicle_data(self, vin: str) -> Optional[Vehicle]:
        """Private method to fetch vehicle data from the VIN service by VIN.

        :param vin: The Vehicle Identification Number (VIN) of the vehicle.
        :return: A Vehicle instance containing the fetched vehicle data, or None if data is not available.
        """

        data = await self.vin_service.load_data(vin)
        if not data:
            return None
        return Vehicle.model_validate(data)

    async def _vehicle_from_db(self, vin: str) -> Optional[Vehicle]:
        """Private method to retrieve vehicle data from the database by VIN.

        :param vin: The Vehicle Identification Number (VIN) of the vehicle.
        :return: A Vehicle instance containing the vehicle data, or None if the data is not found.
        """

        query = vehicles.select().where(vehicles.c.vin == vin)
        row = await self.db.fetch_one(query=query)
        if row is None:
            return None
        return Vehicle.model_validate(row)

    async def _vehicle_to_db(self, vehicle: Vehicle, vin: str) -> dict:
        """Private method to store vehicle data in the database.

        :param vin: The Vehicle Identification Number (VIN) of the vehicle.
        :return: A dictionary containing the stored vehicle data with the 'id' key representing the database record ID.
        """

        query = vehicles.insert(values={'vin': vin, 'year': vehicle.year, 'make': vehicle.make, 'type': vehicle.type,
                                        'color': vehicle.color, 'weight': vehicle.weight, 'model': vehicle.model})
        last_record_id = await self.db.execute(query=query)
        return {**vehicle.model_dump(), 'id': last_record_id}


@lru_cache()
def get_vehicle_service(database: Database = Depends(get_database),
                        vin_service: BaseVinDecoder = Depends(get_vin_decoder_service)) -> VehicleService:
    """Factory function to create and cache a VehicleService instance.

    :param database: The SQLAlchemy database session used to create a VehicleService instance.
    :param vin_service: VIN service.
    :return: A cached instance of the VehicleService class with the provided database session.
    """

    return VehicleService(database, vin_service)
