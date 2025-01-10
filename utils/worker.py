
from curl_cffi.requests import AsyncSession

from .core import *


class Worker():
    def __init__(self, client: Client):
        super().__init__()
        self.client: Client = client

    async def claim(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Bearer {self.client.token}',
            'origin': 'https://testnet.openledger.xyz',
            'referer': 'https://testnet.openledger.xyz/',
            'user-agent': self.client.get_user_agent(),
        }
        async with AsyncSession() as session:
            try:
                response = await session.get(
                    url='https://rewardstn.openledger.xyz/api/v1/claim_reward', headers=headers,
                    proxy=self.client.proxy_init
                )
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")

                    if status == 'SUCCESS':
                        logger.success(f'{self.client.name} Successfully branded the points')
                    else:
                        logger.debug(f'{self.client.name} Response: {data}')

                elif response.status_code == 420:
                    logger.warning(f'{self.client.name} The tokens have already been claimed today')

                else:
                    logger.error(f'{self.client.name} Code: {response.status_code} | Failed to send request for claim points')
    
            except Exception as error:
                logger.error(f'{self.client.name} Request error: {error}')

    async def check_points(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Bearer {self.client.token}',
            'origin': 'https://testnet.openledger.xyz',
            'referer': 'https://testnet.openledger.xyz/',
            'user-agent': self.client.get_user_agent(),
        }
        async with AsyncSession() as session:
            try:
                response = await session.get(
                    url='https://rewardstn.openledger.xyz/api/v1/reward', headers=headers,
                    proxy=self.client.proxy_init
                )
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")

                    if status == 'SUCCESS':
                        verified_pts = float(data["data"]["totalPoint"])
                    else:
                        logger.debug(f'{self.client.name} Response: {data}')
                        verified_pts = 0
                else:
                    logger.error(f'{self.client.name} Code: {response.status_code} | Failed to request the number of points')
                    verified_pts = 0

            except Exception as error:
                logger.error(f'{self.client.name} Request error: {error}')

        async with AsyncSession() as session:
            try:
                response = await session.get(
                    url='https://rewardstn.openledger.xyz/api/v1/reward_realtime', headers=headers,
                    proxy=self.client.proxy_init
                )
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")

                    if status == 'SUCCESS':
                        if data.get('data') and len(data['data']) > 0:
                            pending_pts = float(data['data'][0]['total_heartbeats'])
                        else:
                            pending_pts = 0
                    else:
                        logger.debug(f'{self.client.name} Response: {data}')
                        pending_pts = 0
                else:
                    logger.error(f'{self.client.name} Code: {response.status_code} | Failed to request the number of points')
                    pending_pts = 0

            except Exception as error:
                logger.error(f'{self.client.name} Request error: {error}')
                pending_pts = 0

            
        logger.success(f'{self.client.name} \nPTS Pending confirmation: {pending_pts} \nPTS Verified: {verified_pts} \nAll PTS {verified_pts+pending_pts}')


                