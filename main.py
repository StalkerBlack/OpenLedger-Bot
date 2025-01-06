import asyncio
import random
import sys
import subprocess

from typing import List, Dict, Optional
from questionary import select, Choice

from utils.worker import Worker
from utils.core import *
from generall_settings import *


class Runner:
    @staticmethod
    async def smart_sleep(up, to, msg: str = None):
        duration = random.randint(up, to)
        if msg is None:
            logger.info(f"💤 The next account will start in {duration:.2f} seconds")
        else:
            logger.info(f"💤 {msg} {duration:.2f} seconds")
        await asyncio.sleep(duration)

    @classmethod
    def get_selected_accounts(cls) -> List[Dict]:
        accounts = get_accounts_data()

        if ACCOUNTS_TO_WORK == 0:
            return accounts

        if isinstance(ACCOUNTS_TO_WORK, int):
            return [accounts[ACCOUNTS_TO_WORK - 1]]

        if isinstance(ACCOUNTS_TO_WORK, tuple):
            return [accounts[i - 1] for i in ACCOUNTS_TO_WORK]

        if isinstance(ACCOUNTS_TO_WORK, list):
            start, end = ACCOUNTS_TO_WORK
            return accounts[start-1:end]

        return []

    async def execute_action(self, account_data: Dict, action: int) -> None:
        account_name = account_data['account_name']

        client = Client(
            name=account_data['account_name'],
            proxy=account_data['proxies'],
            token=account_data['token']
        )

        try:
            worker = Worker(client=client)

            action_map = {
                1: worker.claim,
                2: worker.check_points,
            }

            task_func = action_map.get(action)
            if task_func:
                await task_func()
            else:
                logger.warning(f"{account_name} received an unknown action: {action}")

        except Exception as e:
            logger.error(f"Error when executing a {action} task for an account {account_name}: {e}")

    async def run_account_modules(
        self, 
        account_data: Dict, 
        parallel_mode: bool = STREAM, 
        actions_to_perform: Optional[List[int]] = None
    ) -> None:
        
        logger.info(f"Account startup: {account_data['account_name']} (parallel mode: {parallel_mode})")

        actions = actions_to_perform if isinstance(actions_to_perform, list) else [actions_to_perform]

        if SHUFFLE_TASKS:
            random.shuffle(actions)

        for action in actions:
            await self.execute_action(account_data, action)
            if len(actions) > 1:
                await self.smart_sleep(
                    SLEEP_TIME_TASKS[0], SLEEP_TIME_TASKS[1],
                    msg=f'The following task for {account_data["account_name"]} will be executed via '
                )
                
    async def run_parallel(self, actions_to_perform: Optional[List[int]] = None) -> None:
        selected_accounts = self.get_selected_accounts()

        if SHUFFLE_ACCOUNTS:
            random.shuffle(selected_accounts)

        tasks = []

        for idx, account_data in enumerate(selected_accounts):
            current_account = account_data.copy()
            
            async def account_task(account):
                await self.run_account_modules(account, actions_to_perform=actions_to_perform)

            if idx > 0:
                if SLEEP_MODE:
                    await self.smart_sleep(SLEEP_TIME_ACCOUNTS[0], SLEEP_TIME_ACCOUNTS[1])

            task = asyncio.create_task(account_task(current_account))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def run_sequential(self, actions_to_perform: Optional[List[int]] = None) -> None:
        selected_accounts = self.get_selected_accounts()

        if SHUFFLE_ACCOUNTS:
            random.shuffle(selected_accounts)

        for idx, account_data in enumerate(selected_accounts):
            await self.run_account_modules(account_data, actions_to_perform=actions_to_perform)
            
            if idx < len(selected_accounts) - 1 and SLEEP_MODE:
                await self.smart_sleep(SLEEP_TIME_ACCOUNTS[0], SLEEP_TIME_ACCOUNTS[1])  

    async def run(self, actions_to_perform: Optional[List[int]] = None, ignore_settings: bool = False) -> None:
        if ignore_settings:
            selected_accounts = self.get_selected_accounts()
            for account_data in selected_accounts:
                await self.run_account_modules(account_data, parallel_mode=False, actions_to_perform=actions_to_perform)
        else:
            if STREAM:
                await self.run_parallel(actions_to_perform=actions_to_perform)
            else:
                await self.run_sequential(actions_to_perform=actions_to_perform)

def main():
    print(TITLE)
    print('\033[32m💬 Updates and code support ➡️  https://t.me/divinus_xyz  🍀 Subscribe 🍀 \033[0m')
    print()
    try:
        while True:
            answer = select(
                'What do you want to do?',
                choices=[
                    Choice(" 🚀 Claim PTS", 'run_all'),
                    Choice(" 🚀 Requesting the number of points", 'check_points'),
                    Choice(' ❌ Exit', 'exit')
                ],
                qmark='🛠️',
                pointer='👉'
            ).ask()

            runner = Runner()
            if answer == 'run_all':
                actions_to_perform = [1]
                if SHUFFLE_TASKS:
                    random.shuffle(actions_to_perform)
                asyncio.run(runner.run(actions_to_perform=actions_to_perform))
            elif answer == 'check_points':
                actions = [2]
                asyncio.run(runner.run(actions_to_perform=actions, ignore_settings=True))
            elif answer == 'exit':
                sys.exit()
            else:
                print("Unknown action selected")
    except KeyboardInterrupt:
        print("\nExiting the program by signal <Ctrl+C>")
        sys.exit()

def install_requirements():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing requirements: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    install_requirements()
    asyncio.run(main())