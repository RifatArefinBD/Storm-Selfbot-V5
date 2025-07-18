import discord
import aiohttp
from discord.ext import commands
from colorama import Fore

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"  
pink = "\033[38;2;255;192;203m"
white = "\033[37m"
blue = "\033[34m"
black = "\033[30m"
light_green = "\033[92m" 
light_yellow = "\033[93m" 
light_magenta = "\033[95m" 
light_cyan = "\033[96m"  
light_red = "\033[91m"  
light_blue = "\033[94m" 
www = Fore.WHITE
mkk = Fore.BLUE
b = Fore.BLACK
ggg = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX 
pps = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
qqq = Fore.MAGENTA
lbb = Fore.LIGHTBLUE_EX
mll = Fore.LIGHTBLUE_EX
mjj = Fore.RED
yyy = Fore.YELLOW

token = "lodadotcom"
class AntiSilentGCTrap(commands.Cog):
    def __init__(self, bot, token):
        self.bot = bot
        self.token = token
        self.enabled = False
        self.whitelist = self.load_whitelist()

    def load_whitelist(self):
        try:
            with open('sgcwl.txt', 'r') as file:
                return {int(line.strip()) for line in file if line.strip().isdigit()}
        except FileNotFoundError:
            return set()

    @commands.command()
    async def silentantigc(self, ctx, mode: str):
        """Enable or disable the Anti Group Chat Trap."""
        if mode.lower() == "on":
            self.enabled = True
            await ctx.send(f"```ansi\n Silent Anti Group Chat Trap is now {cyan}ON.```")
        elif mode.lower() == "off":
            self.enabled = False
            await ctx.send(f"```ansi\n Silent Anti Group Chat Trap is now {red} OFF.\n```")
        else:
            await ctx.send("Please use 'on' or 'off'.")
            
            
    @commands.Cog.listener()
    async def on_private_channel_create(self, channel):
        """Triggered when a new private channel (DM or group chat) is created."""
        if not isinstance(channel, discord.GroupChannel):
            return  # Ignore non-group channels

        print(f"New group chat created: {channel.id}")
        
        if self.enabled:
            # Leave the group chat if enabled
            await self.silent_leave(channel.id)
            print(f"Left the group chat {channel.id} automatically.")


    @commands.Cog.listener()
    async def on_message(self, message):
        """Detect when the bot is mentioned in a group chat and take action."""
        if not self.enabled:
            return

        # Check if the message is in a GroupChannel (group chat)
        if isinstance(message.channel, discord.GroupChannel):
            # Check if the bot is mentioned in the message
            if self.bot.user in message.mentions:
                # Check if it's a system message containing "added" (i.e., bot being added to group chat)
                if "added" in message.system_content.lower():
                    if message.author.id not in self.whitelist:
                        # Leave the group chat
                        await self.silent_leave(message.channel.id)
                        

                        # Block the unauthorized user
                        await self.getblockedlol(message.author.id)

    async def silent_leave(self, channel_id):
        """
        Leave the group chat silently using the Discord API.
        """
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{channel_id}?silent=true"
            headers = {
                "Authorization": self.token,
                "Content-Type": "application/json",
            }
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    print(f"Silently left group chat {channel_id}")
                else:
                    print(f"Failed to leave group chat {channel_id}: {response.status} - {await response.text()}")


    async def getblockedlol(self, user_id):
        """Block the user who added the bot to the group chat."""
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/users/@me/relationships/{user_id}"
            headers = {
                "Authorization": self.token,  # Use the bot's token for authorization
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
            }
            async with session.put(url, headers=headers, json={"type": 2}) as response:
                if response.status == 204:
                    print(f"Blocked user {user_id}")
                else:
                    print(f"Failed to block {user_id}: {response.status} - {await response.text()}")

    @commands.command()
    async def sgcwl(self, ctx, user_id: int):
        """Add a user to the whitelist."""
        self.whitelist.add(user_id)
        with open('gcwl.txt', 'a') as file:
            file.write(f"{user_id}\n")  # Append user ID to whitelist.txt
        await ctx.send(f"User {user_id} has been added to the whitelist.")
        
def setup(bot):
    bot.add_cog(AntiSilentGCTrap(bot, token))