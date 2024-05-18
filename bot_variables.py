from database import DB
from by_bit import ByBitBackend
from discord.ext import commands
import discord.errors
from functools import wraps
import yaml

# All variables used throughout the bot.
# Put into a class to "group" them all together.
class BotVariables:
    
    # `!add_pub_channel [channel_id]` will add the channel ID to `PUBLIC_CHANNELS`.
    PUBLIC_CHANNELS = []

    # `!add_priv_channel [channel_id]` will add the channel ID to `PRIVATE_CHANNELS`.
    PRIVATE_CHANNELS = []

    # `!enable_logs` will set this value to True, `!disable_logs` will set this value to False.
    LOGS = False

    # The channel where all logs will go, if enabled.
    # `!set_log_channel [channel_id]` command will set the below variable.
    LOG_CHANNEL = None

    # This array keeps track of all the threads where `!submit` has been used.
    # This makes sure the user cannot re-run the command and screw things up.
    SUBMIT_COMMAND_USED_IN = []

    # `SCUI` = Submit Command Used In (`SUBMIT_COMMAND_USED_IN` array).
    def add_to_SCUI(channel_id: int) -> int:
        BotVariables.SUBMIT_COMMAND_USED_IN.append(channel_id)

        # Return the length of the array. This will return the index in which
        # this channel ID is at.
        return len(BotVariables.SUBMIT_COMMAND_USED_IN)

    # This array keeps track of the users who invoke `!ready`. Once they exist in this array they cannot use the `!ready`
    # command again.
    READY_COMMAND_USED_BY = []

    # The bot. The variable that makes it all happen :)
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

    # Bot-related variables (make the overall code easier).
    # `BE` = Bot Event.
    BE = bot.event

    # Run the bot.
    def start():
        with open('dt.yaml', 'r') as file:
            discord_token_data = yaml.safe_load(file)
            file.close()
            
            BotVariables.bot.run(discord_token_data['discord_token'])

    # Used on commands that require the member to have admin permissions, as well as on 
    # commands that need to be in a private channel.
    def check_permissions(*args, **kwargs):
        async def check_permissions_inner(ctx):
            if not ctx.author.top_role.permissions.administrator:
                return False

            # `HTBP` = Has To Be Private.
            #   True if the channel in which the command is invoked in has to be private.
            #   False if the channel in which the command is invoked in does not have to be private.
            if kwargs['HTBP']:
                if BotVariables.PRIVATE_CHANNELS == []:
                    return False

                if not ctx.channel.id in BotVariables.PRIVATE_CHANNELS:
                    return False

            return True
        
        return commands.check(check_permissions_inner)

    # Used on commands that are to be invoked in public channels only
    def public_channel_required(*args, **kwargs):
        async def public_channel_required_inner(ctx):
            # `WPTE` = With Private Thread Exception.
            # If this is True, we will check to see if the command was invoked in a private thread.
            # If it was not, we will return False else we will return True.
            if kwargs['WPTE']:
                if not ctx.channel.type == 'private_thread':
                    return False
                return True

            # If `WPTE` is `False`, then we can only assume that the command is not to be used in any
            # thread (public or private).
            if ctx.channel.type == 'private_thread' or ctx.channel.type == 'public_thread':
                return False

            if not ctx.channel.id in BotVariables.PUBLIC_CHANNELS:
                return False
                
            return True

        return commands.check(public_channel_required_inner)
        
    # The above functions will raise an exception if `False` gets returned.
    # The below function makes sure nothing gets printed. We don't care about any sort of
    # exception that gets raised.
    async def on_command_error(self, ctx: commands.Context):
        pass # Do nothing. We don't care about the error that gets raised.

    bot.on_command_error = on_command_error

    # Database.
    db = DB()

    # ByBit backend.
    BBB = ByBitBackend()
