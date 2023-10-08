import abc
import logging
from typing import Optional

from core.config import settings

logger = logging.getLogger()


class BaseVinDecoder:
    """Base service for fetching vehicle data from by VIN."""

    @abc.abstractmethod
    async def load_data(self, vin: str) -> Optional[dict]:
        """Fetch vehicle data from the VIN service by VIN."""
        pass


class VinDecoderService(BaseVinDecoder):
    """Service for fetching vehicle data from by VIN."""

    def __init__(self) -> None:
        self.service_url = settings.VIN_SERVICE_URL

    async def load_data(self, vin: str) -> Optional[dict]:
        """Fetch vehicle data from the VIN service by VIN.

        :param vin: The Vehicle Identification Number (VIN) of the vehicle
        :return: A Vehicle data, or None if the data is not found.
        """

        # async with aiohttp.ClientSession() as session:
            # async with session.get(self.vin_service_url.format(vin=vin)) as resp:
                # data = await resp.json()
                # logging.info(f'Vehicle by vin {vin} data: {data}')
        # The http://18.202.200.86:9099/private/vin/decodes/{vin}/ service not working

        data = {'id': 1, 'year': 1997, 'make': 'PLYMOUTH', 'model': 'Prowler', 'type': 'PASSENGER CAR',
                'color': 'black', 'weight': 1270}

        if not data:
            logging.info(f'Vehicle by vin {vin} not found')
            return None
        return data


def get_vin_decoder_service() -> BaseVinDecoder:
    """Factory function to create and cache a VinDecoderService instance.

    :return: A cached instance of the VinDecoderService class.
    """

    return VinDecoderService()
