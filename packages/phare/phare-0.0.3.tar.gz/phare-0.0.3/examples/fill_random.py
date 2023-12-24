import asyncio
import numpy as np
import os

from phare.auth import Auth
from phare.lighthouse import Lighthouse
from phare.constants import LIGHTHOUSE_FRAME_SHAPE, LIGHTHOUSE_URL

async def main():
    user = os.environ['LIGHTHOUSE_USER']
    token = os.environ['LIGHTHOUSE_TOKEN']
    url = os.environ.get('LIGHTHOUSE_URL', LIGHTHOUSE_URL)

    async with await Lighthouse.connect(Auth(user, token), url) as lh:
        frame = np.random.randint(0, 255, size=LIGHTHOUSE_FRAME_SHAPE, dtype=np.uint8)
        await lh.put_model(frame)

asyncio.run(main())
