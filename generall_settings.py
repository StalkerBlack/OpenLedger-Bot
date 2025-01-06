SLEEP_MODE = True                                     # True or False | Enables sleep after each account is used up

STREAM = True                                        # True or False | Enables parallel mode

ACCOUNTS_IN_STREAM = 10                               # Number of accounts in the stream

SLEEP_TIME_ACCOUNTS = (30, 120)                       # (minimum, maximum) seconds | Sleep time between accounts

SLEEP_TIME_TASKS = (30, 120)                          # (minimum, maximum) seconds | Sleep time between tasks

SHUFFLE_ACCOUNTS = True                               # To mix accounts or not
 
SHUFFLE_TASKS = True                                 # Shuffle the assignments or not


ACCOUNTS_TO_WORK: int | tuple | list = [1, 10]              # 0 - all accounts
                                                      # 1 - account No. 1
                                                      # 1, 7 - accounts 1 and 7
                                                      # [5, 25] - accounts 5 through 25 inclusive


TITLE = """\033[33m
  /$$$$$$                                /$$                       /$$                                      /$$$$$$             /$$$$$$   /$$    
 /$$__  $$                              | $$                      | $$                                     /$$__  $$           /$$__  $$ | $$    
| $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$ | $$        /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$       | $$  \__/  /$$$$$$ | $$  \__//$$$$$$  
| $$  | $$ /$$__  $$ /$$__  $$| $$__  $$| $$       /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$      |  $$$$$$  /$$__  $$| $$$$   |_  $$_/  
| $$  | $$| $$  \ $$| $$$$$$$$| $$  \ $$| $$      | $$$$$$$$| $$  | $$| $$  \ $$| $$$$$$$$| $$  \__/       \____  $$| $$  \ $$| $$_/     | $$    
| $$  | $$| $$  | $$| $$_____/| $$  | $$| $$      | $$_____/| $$  | $$| $$  | $$| $$_____/| $$             /$$  \ $$| $$  | $$| $$       | $$ /$$
|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$  | $$| $$$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$            |  $$$$$$/|  $$$$$$/| $$       |  $$$$/
 \______/ | $$____/  \_______/|__/  |__/|________/ \_______/ \_______/ \____  $$ \_______/|__/             \______/  \______/ |__/        \___/  
          | $$                                                         /$$  \ $$                                                                 
          | $$                                                        |  $$$$$$/                                                                 
          |__/                                                         \______/                       
\033[0m                                                                                                                                 \033[32m@divinus.xyz\033[0m 
"""