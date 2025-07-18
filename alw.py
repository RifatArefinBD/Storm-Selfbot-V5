import discord
import aiohttp
import requests
import random
TOKEN = "lodadotcom"
lwmessages = [
    "LOL FAILED LAST Word",
    "last word for apophis",
    "nice failed last word, last word for me",
    "nigga failed a last word LOL"
]
class ALWHandler:
    def __init__(self, bot):
        self.bot = bot
        self.alw_enabled = False
        self.uid = None
        self.token = bot.http.token
        self.whitelist = self.load_whitelist()  # Load the whitelist from a file

    def load_whitelist(self):
        try:
            with open('wl.txt', 'r') as f:
                return {line.strip() for line in f if line.strip()}  # Set for quick lookups
        except FileNotFoundError:
            return set()  # Return empty set if file doesn't exist

    def save_whitelist(self):
        with open('wl.txt', 'w') as f:
            f.writelines(f"{uid}\n" for uid in self.whitelist)

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def leave_gc(self, channel_id):
        """Leave the group chat with the given channel ID."""
        url = f"https://discord.com/api/v9/channels/{channel_id}"
        headers = self.get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    print(f"Left group channel {channel_id} successfully")
                else:
                    print(f"Failed to leave group channel {channel_id}: {response.status} - {await response.text()}")

    async def get_blocked(self, user_id):
        """Block the user with the given user ID."""
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/users/@me/relationships/{user_id}"
            headers = {
                "Authorization": self.token,
                "Content-Type": "application/json",
                "Accept": "*/*",
            }
            async with session.put(url, headers=headers, json={"type": 2}) as response:
                if response.status == 204:
                    print(f"Blocked user {user_id}")
                else:
                    print(f"Failed to block {user_id}: {response.status} - {await response.text()}")

    async def on_message(self, message):
        random_message = random.choice(lwmessages)  # Assume lwmessages is defined elsewhere
        if not self.alw_enabled:
            return

        if message.author.id != int(self.uid):
            # Check if the user is in the whitelist
            if str(message.author.id) in self.whitelist:
                return  # User is whitelisted; do nothing

            # Check for "last word" in DM messages
            if isinstance(message.channel, discord.DMChannel):
                if any(term in message.content.lower() for term in ["last word", "lastword", "last", "lw", "lst", "lst word"]):
                    await message.reply(random_message)
                    await self.get_blocked(message.author.id)

            # Check for "last word" in GroupChannel messages
            elif isinstance(message.channel, discord.GroupChannel):
                if any(term in message.content.lower() for term in ["last word", "lastword", "last", "lw"]):
                    await message.reply(random_message)
                    await self.get_blocked(message.author.id)
                    await self.leave_gc(message.channel.id)  # Leave the group chat

    async def wl(self, user_id: int):
        """Add a user ID to the whitelist."""
        self.whitelist.add(str(user_id))  # Add to the in-memory set
        self.save_whitelist()  # Save to file
        print(f"User ID {user_id} has been added to the whitelist.")