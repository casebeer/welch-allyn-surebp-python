import logging
logging.basicConfig(level=logging.DEBUG)

import asyncio
import pytest

from surebp.TranstekController import TranstekController
from surebp.bleUuids import DeviceInfoCharacteristics
from . import MockTranstekBleDriver

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def testTranstekController():
    transtekController = TranstekController(MockTranstekBleDriver.MockTranstekBleDriver())
    await transtekController.initialize()

    assert transtekController.deviceInfo[DeviceInfoCharacteristics.SERIAL_NUMBER.name] ==\
            MockTranstekBleDriver.MOCK_SERIAL_NUMBER

    # this should block until all data is done and the Mock object disconnects
    await transtekController.join()

    count = 0
    async for data in transtekController.bpData():
        count += 1
    assert count == 3

async def main():
    await testTranstekController()

if __name__ == '__main__':
    asyncio.run(main())
