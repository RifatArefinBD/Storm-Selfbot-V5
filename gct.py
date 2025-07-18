import discord
import asyncio
import random
import signal
import sys

# Define the intents for the clients
intents = discord.Intents.default()
intents.guilds = True  # Adjust intents as needed

class CustomClient(discord.Client):
    def __init__(self, token, channel_id, name_placeholder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = channel_id
        self.name_placeholder = name_placeholder

    async def on_ready(self):
        print(f'Logged in as {self.user} using token {self.token[-4:]}.')
        channel = self.get_channel(self.channel_id)
        if channel:
            # Start the renaming task
            asyncio.create_task(self.rename_channel(channel))
        else:
            print(f"Channel ID {self.channel_id} not found.")
            await self.close()

    async def rename_channel(self, channel):
        # Load names from gcname.txt and replace "&" for lowercase and "@" for uppercase
        try:
            with open("gcname.txt", "r") as f:
                gc_names = [line.strip().replace("&", self.name_placeholder.lower()).replace("@", self.name_placeholder.upper()) for line in f]
        except FileNotFoundError:
            print("Error: gcname.txt not found.")
            await self.close()
            return

        while True:
            new_name = random.choice(gc_names)

            # Check if '&' or '@' is in the new_name and format accordingly
            if '@' in new_name:
                formatted_name = new_name.replace("@", self.name_placeholder.upper())
            elif '&' in new_name:
                formatted_name = new_name.replace("&", self.name_placeholder.lower())
            else:
                formatted_name = new_name  # No placeholder found, keep original

            try:
                await channel.edit(name=formatted_name)
                print(f"Changed group chat name to '{formatted_name}'")

            except discord.errors.Forbidden:
                print("Bot doesn't have permission to change the group chat name.")
                await self.close()
                return
            except discord.errors.HTTPException as e:
                if e.status == 429:  # Handling rate limit
                    retry_after = int(e.response.headers.get('Retry-After', 1))
                    print(f"Token {self.token[-4:]} is being rate limited. Waiting for {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                elif e.status == 401:  # Handling improper token
                    print(f"Token {self.token[-4:]} is invalid. Skipping...")
                    await self.close()
                    return
                else:
                    print(f"HTTP error occurred: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                await self.close()
                return
            
            await asyncio.sleep(1)  # Delay before next iteration

    async def close(self):
        await super().close()
        await self.http.close()

async def create_and_run_client(token, channel_id, name_placeholder):
    client = CustomClient(token, channel_id, name_placeholder, intents=intents)
    await client.start(token, bot=False)

def handle_termination_signal(signal, frame):
    print("Termination signal received. Shutting down...")
    asyncio.get_event_loop().stop()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_termination_signal)

    # Load tokens
    tokens_file_path = "tokens2.txt"
    tokens = open(tokens_file_path, "r").read().splitlines()

    # Get parameters from command line arguments
    if len(sys.argv) < 4:
        print("Usage: python gct.py <channel_id> <position> <name_placeholder>")
        sys.exit(1)

    channel_id = int(sys.argv[1])
    position = int(sys.argv[2]) - 1  # Convert to 0-based index
    name_placeholder = sys.argv[3]

    # Check if the position is valid
    if position < 0 or position >= len(tokens):
        print(f"Invalid position: {position + 1}")
        sys.exit(1)

    # Run the client for the specified token
    token = tokens[position]
    asyncio.run(create_and_run_client(token, channel_id, name_placeholder))