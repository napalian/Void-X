import aiohttp, asyncio

from pystyle import *
from data.utils import *


class Features:
    def __init__(self) -> None:
        pass

    async def fetch_guild_data(headers: dict, guild_id: int):
        async with aiohttp.ClientSession() as session:
            guild_url = f"https://discord.com/api/guilds/{guild_id}/members?limit=1000"
            async with session.get(guild_url, headers=headers) as response:
                json = await response.json()
                members = [json[i]['user']['id'] for i in range(len(json))]

                with open ('data/ids/members.txt', "w+") as m_id:
                    m_id.write('\n'.join(members))

        async with aiohttp.ClientSession() as session:
            role_url = f"https://discord.com/api/guilds/{guild_id}/roles"
            async with session.get(role_url, headers=headers) as response:
                json = await response.json()
                roles = [json[l]['id'] for l in range(len(json))]

                with open('data/ids/roles.txt', "w+") as r_id:
                    r_id.write('\n'.join(members))

    


    async def runner(guild_id:int,headers:dict):
        guild = guild_id
        bot_headers = headers

        await Util.logo_flash()
        while True:
            choice = Write.Input("\n\nChoice >> ", Colors.purple_to_blue, interval=0.000)

    async def checker():

        bot_token = 'tsting.'#Write.Input("\n\nToken >> ",Colors.purple_to_blue,interval=0.000)
        guild_id = 1077675203301224468#Write.Input("\n\nGuild ID >> ", Colors.purple_to_blue, interval=0.000)

        await Features.fetch_guild_data({"Authorization":"Bot {}".format(bot_token)},guild_id)

        await Features.runner(guild_id,{"Authorization":"Bot {}".format(bot_token)})


if __name__ == '__main__':
    os.system(f'cls & mode 85,20 & title Void X')
    os.system("mode con: cols=74 lines=25")
    asyncio.run(Features.checker())


