import discord
from discord.ext import commands
import requests
import asyncio  # Import asyncio for async sleep

# Replace with your actual user token
USER_TOKEN = 'lodadotcom'  # User token to perform actions
auto_adder_enabled = False  # Flag to control the auto adder

class GCFill(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = False
        self.gc_id = None  # Store the group chat ID
        self.user_ids = []  # Store user IDs to track

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
                    self.gc_id = message.channel.id
                    await self.add_users_to_gc()

    async def add_users_to_gc(self):
        """Add users from gcfill.txt to the group chat."""
        global auto_adder_enabled
        auto_adder_enabled = True  # Enable auto adder

        try:
            with open('gcfill.txt', 'r') as file:
                self.user_ids = [line.strip() for line in file if line.strip()]  # Read and strip whitespace

            while auto_adder_enabled:
                await asyncio.sleep(0.1)  # Use async sleep to avoid blocking the event loop
                try:
                    r = requests.get(
                        f'https://discord.com/api/v9/channels/{self.gc_id}',
                        headers={'Authorization': USER_TOKEN}
                    )

                    if r.status_code == 200:
                        data = r.json()

                        if 'recipients' in data:
                            recipients = data['recipients']

                            for user_id in self.user_ids:
                                if not any(recipient['id'] == user_id for recipient in recipients):
                                    # User not found in the group chat; attempt to add them
                                    add_response = requests.put(
                                        f'https://discord.com/api/v9/channels/{self.gc_id}/recipients/{user_id}',
                                        headers={'Authorization': USER_TOKEN}
                                    )

                                    if add_response.status_code == 204:
                                        print(f"User {user_id} added to the group chat.")
                                    else:
                                        print(f"Failed to add user {user_id}: {add_response.status_code}")

                    # Check for users removed or left
                    current_recipients = [recipient['id'] for recipient in data['recipients']]
                    for user_id in self.user_ids:
                        if user_id not in current_recipients:
                            # User is no longer in the group chat; add them back
                            add_response = requests.put(
                                f'https://discord.com/api/v9/channels/{self.gc_id}/recipients/{user_id}',
                                headers={'Authorization': USER_TOKEN}
                            )
                            if add_response.status_code == 204:
                                print(f"User {user_id} added back to the group chat.")

                except Exception as e:
                    auto_adder_enabled = False  # Stop on error
                    print(f"Error occurred: {e}")

        except FileNotFoundError:
            print("The file gcfill.txt was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @commands.command()
    async def gcfill(self, ctx):
        """Manually add users from gcfill.txt to the current group chat."""
        self.gc_id = ctx.channel.id  # Set the current group chat ID
        await self.add_users_to_gc()

    def start_auto_adder(self):
        """Start the auto adder if not already running."""
        global auto_adder_enabled
        auto_adder_enabled = True
        self.bot.loop.create_task(self.add_users_to_gc())

    def stop_auto_adder(self):
        """Stop the auto adder."""
        global auto_adder_enabled
        auto_adder_enabled = False

