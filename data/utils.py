import sys, logging, os

from pystyle import *


class Util:
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    @staticmethod
    async def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    async def logo_flash(self=None):
        await Util.cls()
        logging.info(
            Colorate.Horizontal(Colors.purple_to_blue,('''
\t             ██▒   █▓ ▒█████   ██▓▓█████▄    ▒██   ██▒ 
\t             ▓██░   █▒▒██▒  ██▒▓██▒▒██▀ ██▌   ▒▒ █ █ ▒░ 
 \t             ▓██  █▒░▒██░  ██▒▒██▒░██   █▌   ░░  █   ░ 
  \t             ▒██ █░░▒██   ██░░██░░▓█▄   ▌    ░ █ █ ▒  
   \t             ▒▀█░  ░ ████▓▒░░██░░▒████▓    ▒██▒ ▒██▒ 
   \t             ░ ▐░  ░ ▒░▒░▒░ ░▓   ▒▒▓  ▒    ▒▒ ░ ░▓ ░ 
   \t             ░ ░░    ░ ▒ ▒░  ▒ ░ ░ ▒  ▒    ░░   ░▒ ░ 
     \t             ░░  ░ ░ ░ ▒   ▒ ░ ░ ░  ░     ░    ░   
      \t             ░      ░ ░   ░     ░        ░    ░   
     \t             ░                 ░                 

╔═══════════════════════╦═══════════════════════╦═══════════════════════╗
║ [1] MassRole          ║ [5] MassDeleteRole    ║ [9] SupportServer     ║
║ [2] MassChannel       ║ [6] MassDeleteChannel ║ [0] UpdateChecker     ║
║ [3] MassBan           ║ [7] MassBanMembers    ║ [M] Menu              ║
║ [4] RoleEveryone      ║ [8] SpamPingEveryone  ║ [X] Exit              ║
╚═══════════════════════╩═══════════════════════╩═══════════════════════╝'''
        )))


