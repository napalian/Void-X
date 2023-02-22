import aiohttp
import asyncio

class Proxy:
    def __init__(self) -> None:
        self.proxies = []

    async def proxy_gen(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=50&country=all") as resp:
                proxies = await resp.text()
                proxies = proxies.split()

                with open("proxies.txt", "w") as f:
                    for proxy in proxies:
                        f.write("http://{}\n".format(proxy))

    async def proxy_check(self) -> str:
        with open("proxies.txt", "r") as proxies_file, open("working_proxies.txt", "w+") as working_file:
            proxies = proxies_file.read().split()

            for proxy in proxies:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.head("https://www.google.com", proxy=proxy) as resp:
                            self.proxies.append(proxy)
                            working_file.write(f"{proxy}\n")
                except:
                    working_file.write(f"{proxy}\n")

async def main():
    proxy = Proxy()
    await asyncio.gather(proxy.proxy_gen(), proxy.proxy_check())
