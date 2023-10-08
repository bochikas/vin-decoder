from fastapi import APIRouter, Depends, HTTPException, status

from models.vehicle import Vehicle
from services.vehicle import VehicleService, get_vehicle_service

router = APIRouter()


@router.get('/decode/{vin}/', response_model=Vehicle)
async def get_vehicle_data_by_vin(vin: str, vehicle_service: VehicleService = Depends(get_vehicle_service)) -> Vehicle:
    """Get vehicle information by VIN number."""

    vehicle = await vehicle_service.get_vehicle_data(vin)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return Vehicle(id=vehicle.id, model=vehicle.model, year=vehicle.year, make=vehicle.make, type=vehicle.type,
                   color=vehicle.color, weight=vehicle.weight)
