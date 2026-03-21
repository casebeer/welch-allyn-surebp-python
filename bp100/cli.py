
import bleak
from bleak import (
    BleakScanner,
)

import logging
bleak_logger = logging.getLogger("bleak")
#bleak_logger.setLevel(logging.DEBUG)
bleak_logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


import asyncio
import sys
import pprint

from .TranstekController import TranstekController
from .TranstekBleDriver import TranstekBleDriver

from .bleUuids import (
    GattServices,
)

async def main():
    logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.DEBUG)

    # optional device address – connect directly to device without waiting for advertisements
    deviceAddress = sys.argv[1] if len(sys.argv) > 1 else None

    if deviceAddress is None:
        # Normalized service UUIDs since Bleak will not match on a short/16 bit UUID
        serviceUuids = [bleak.uuids.normalize_uuid_str(u) for u in [GattServices.TRANSTEK_BP.value]]
        async with BleakScanner(
            service_uuids=serviceUuids,
            ) as scanner:
            logger.info(f"Scanning for service UUIDs {serviceUuids}...")

            async for bleDevice, advertisementData in scanner.advertisement_data():
                if advertisementData.service_uuids:
                    logger.info(f"Got matching UUID: {advertisementData.service_uuids}")
                    # return the first matching device seen
                    device = bleDevice
                    break
            logger.debug("Broken out of scanning loop...")
    else:
        logger.info(f"Connecting to specified BLE device with address {deviceAddress}")
        device = deviceAddress

    logger.info(f"Connecting to BP monitor {device}...")

    transtekController = TranstekController(TranstekBleDriver(device))

    # Once the controller is initialized, it will respond asynchronously
    # to BLE indications from the BP device.
    await transtekController.initialize()

    # wait until the client is disconnected before printing, etc.
    await transtekController.join()

    logger.info("BLE connection done!")

    pprint.pprint(transtekController.deviceInfo)
    async for bpData in transtekController.bpData():
        pprint.pprint(bpData)

    return 0

def run():
    return asyncio.run(main())

if __name__ == '__main__':
    sys.exit(run())
