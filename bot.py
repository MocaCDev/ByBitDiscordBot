from bot_variables import BotVariables as BV
import asyncio # Needed for sleeping (without pausing the bot, as `time.sleep` would do).
import json
import sys 

BV.start()

sys.exit(0)

# Debug. Make sure connection happens.
@BV.BE
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# ------------ ADMIN ------------

# For all functions where `HTBP` is `False`, the channel does not need to be private,
# but the member invoking the command needs admin permissions.
# Usage: `!add_priv_channel [channel_id]`.
@BV.check_permissions(HTBP=False)
@BV.BE(name='add_priv_channel')
async def add_private_channel(ctx, priv_channel_id: int):
    BV.PRIVATE_CHANNELS.append(priv_channel_id)

# Usage: `!rem_priv_channel [channel_id]`.
@BV.check_permissions(HTBP=False)
@BV.BE(name='rem_priv_channel')
async def remove_private_channel(ctx, priv_channel_id: int):
    for i in range(len(BV.PRIVATE_CHANNELS)):
        if BV.PRIVATE_CHANNELS[i] == priv_channel_id:
            del BV.PRIVATE_CHANNELS[i]
            return

    # If we get here, we can assume the channel id was not found in `PRIVATE_CHANNELS`.    
    await ctx.send(f'{ctx.message.author.mention} {priv_channel_id} was not found in `PRIVATE_CHANNELS`.')

# Usage: `!add_pub_channel [channel_id]`.
@BV.check_permissions(HTBP=False)
@BV.BE(name='add_pub_channel')
async def add_public_channel(ctx, pub_channel_id: int):
    BV.PUBLIC_CHANNELS.append(pub_channel_id)

# Usage: `!rem_pub_channel [channel_id]`.
@BV.check_permissions(HTBP=False)
@BV.BE(name='rem_pub_channel')
async def remove_public_channel(ctx, pub_channel_id: int):
    for i in range(len(BV.PUBLIC_CHANNELS)):
        if BV.PUBLIC_CHANNELS[i] == pub_channel_id:
            del BV.PUBLIC_CHANNELS[i]
            return

    # If we get here, we can assume the channel id was not found in `PUBLIC_CHANNELS`.
    await ctx.send(f'{ctx.message.author.mention} {pub_channel_id} was not found in `PUBLIC_CHANNELS`.')

# Just in case.
# Usage: `!use_testnet`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='use_testnet')
async def use_testnet(ctx):
    BV.BBB.testnet = True

# Again, just in case.
# Usage: `!disable_testnet`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='disable_testnet')
async def disable_testnet(ctx):
    BV.BBB.testnet = False

# The below command is advised to be ran in a public channel.
# Usage: `!explain`.
@BV.check_permissions(HTBP=False)
@BV.BE(name='explain')
async def explain(ctx):
    await ctx.send(f'# Hello!\nWe assume you already have an account with ByBit. If you do not, please create one.\n\nBefore we can register you in our server, you are going to need to get a Read-Only API key. Follow the steps below:\n1. Head over to https://www.bybit.com/\n2. Log in to your account, if you are not already logged in.\n3. Click on your profile & select **API**\n4. Click on **API Management**, then click on **Create New Key**\n5. Select **System-generated API Keys**\n6. Select **API transaction**\n7. Apply a name to your API key. Name it however you would like.\n8. Set the permission to **Read-Only**\n9. Select **No IP restriction**\n10. Based on your account, click either **Standard Account** or **Unified Trading**.\n11. Submit your 2FA code (if need be).\n\nAfter all is said and done you should see a popup with your API keys.\n\n**Copy your API keys and store them in a file on your device. Do not lose them!**\n\nWhen you are ready to be registerd in the server, type `!ready`. You will get pinged in a private thread with further instructions.')

# Usage: `!enable_logs`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='enable_logs')
async def enable_logs(ctx):
    BV.LOGS = True

    await ctx.send(f'{ctx.message.author.mention} If you haven\'t already, don\'t forget to run `!set_log_channel [channel_id]`, where `[channel_id]` is the ID of the channel where you will want all logs relating to this bot to go.\nMake sure this channel is private!')

# Usage `!disable_logs`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='disable_logs')
async def disable_logs(ctx):
    BV.LOGS = False

# Usage: `!set_log_channel [channel_id]`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='set_log_channel')
async def set_log_channel(ctx, log_channel_id: int):
    BV.LOG_CHANNEL = log_channel_id

# Usage: `!remove_user [from] [user_id]`
#   `[from=database]` -> `[user_id]` needs to be the users username.
#   `[from=RCUB]` -> `[user_id]` needs to be the ID of the user.
@BV.check_permissions(HTBP=True)
@BV.BE(name='remove_user')
async def remove_user(ctx, remove_from: str, user_id):
    if remove_from == 'database':
        # `user_id` will have to be a string.
        if not type(user_id) == str:
            await ctx.send(f'{ctx.message.author.mention} `[user_id]` needs to be the users display name (the name you see displayed in the server, not the username of the user).')
            return

        good = BV.db.remove_user(user_id)

        if not good:
            await ctx.send(f'{ctx.message.author.mention} An error has occurred. Please contact the developer.')

        return
    
    if remove_from == 'RCUB': # `RCUB` = Ready Command Used By
        # `user_id` will have to be a integer.
        if not type(user_id) == int:
            await ctx.send(f'{ctx.message.author.mention} `[user_id]` needs to be the users ID (integer).')
            return

        for i in range(len(BV.READY_COMMAND_USED_BY)):
            if BV.READY_COMMAND_USED_BY[i] == user_id:
                del BV.READY_COMMAND_USED_BY[i]
                return

        await ctx.send(f'{ctx.message.author.mention} {user_id} was not found in `READY_COMMAND_USED_BY`.')
        return

    await ctx.send(f'{ctx.message.author.mention} {remove_from} not recognized.\nRecognized values are `database` or `RCUB` (Ready Command Used By array. Read `readme.pdf` for more information).')

# Usage: `!calc [based_on] [user_id] OPTIONAL[interval]`.
#   `[based_on]` needs to be `bs` for buy/sell data, or `s` for stock data.
#       If `[based_on]` is `bs`, it will calculate the users new balance based off their
#       buy/sell data.
#       If `[based_on]` is `s`, it will calculate the daily balance the user has all together.
#           With this, the data will be based purely off stocks that have been bought. The balance
#           will be added by how all the stocks are doing + any sell data.
#           If `[based_on]` is `s`, `[interval]` will be needed.
#               `[interval]` can be:
#                   1, 3, 5, 15, 30, 60, 120, 240, 360, 720 (minutes)
#                   D - Stock based on the day
#                   W - Stock based on the week
#                   M - Stock based on the month
#               Default is D.
#   `[user_id]` needs to be the users ID.
@BV.check_permissions(HTBP=True)
@BV.BE(name='calc')
async def calculate_gain_or_loss(ctx, based_on: str, user_id: int, O_interval: str = 'D'):
    user_balance = BV.db.get_users_balance(user_id)

    if user_balance is None:
        await ctx.send(f'{ctx.message.author.mention} An error occurred getting users balance from the database.')
        return

    if based_on == 'bs': # `bs` = Buy Sell.
        total = BV.BBB.get_total_bs_data_from_session(user_id)

        # This should honestly never happen. Better safe than sorry though.
        if total[0] == '' or total[1] == '':
            ctx.send(f'{ctx.message.author.mention} An internal error has occurred on behalf of ByBit. Try again later.\nIf the problem persists, please get in contact with Fire🔥Kurama🃏.')
            return

        user_balance -= total[0]
        user_balance += total[1]

        await ctx.send(f'{ctx.message.author.mention}\nBuy: {total[0]}\nSell: {total[1]}\nEnding Balance: {user_balance}')
        return

    if based_on == 's':
        stock_info, needs_warnings = BV.BBB.get_total_stock_data_from_session(user_id, O_interval)

        if needs_warnings:
            ctx.send(f'{ctx.message.author.mention} While getting market data, an error response was returned by ByBit. Some market data was unable to be obtained, which might make the calculations inaccurate.')

        if stock_info[0] == '' or stock_info[1] == '' or stock_info[2] == '':
            ctx.send(f'{ctx.message.author.mention} An internal error has occurred on behalf of ByBit. Try again later.\nIf the problem persists, please get in contact with Fire🔥Kurama🃏.')
            return

        await ctx.send(f'{ctx.message.author.mention}\nStock gain/loss: {stock_info[0]}\nTotal Sell: {stock_info[1]}\nTotal Buy: {stock_info[2]}\nBalance: {(user-balance - stock_info[2]) + stock_info[1]}')

        user_balance += stock_info[0]
        user_balance += stock_info[1]

        await ctx.send(f'Balance with loss/gain + total sell: {user_balance}')

    await ctx.send(f'{ctx.message.author.mention} {based_on} is not recognized. Recognized `[based_on]` arguments are `s` (stock data) or `bs` (buy/sell data).')

# Usage: `!stop_session [user_id]`
@BV.check_permissions(HTBP=True)
@BV.BE(name='stop_session')
async def stop_users_session(ctx, user_id: int):
    BV.BBB.close_session(user_id)

    await ctx.send(f'{ctx.message.author.mention} Session for {user_id} has been closed.')

# Usage: `!start_session [user_id]`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='start_session')
async def start_users_session(ctx, user_id: int):
    good = BV.BBB.init_session(
        user_id,
        BV.db.get_user_public_key(user_id),
        BV.db.get_user_private_key(user_id)
    )

    if not good:
        await ctx.send(f'{ctx.message.author.mention} An error occurred while initializing a session for {user_id}. This is most likely due to `get_user_public_key` or `get_user_private_key` returning `None` (meaning an error occurred whilst getting the users public/private keys from the database).')
        return

    await ctx.send(f'{ctx.message.author.mention} Session for {user_id} has been added.')

@BV.check_permissions(HTBP=True)
@BV.BE(name='show_sessions')
async def show_sessions(ctx):
    await ctx.send(f'{ctx.message.author.mention}\n{json.dumps(BV.BBB.sessions, indent=2)}')

# Usage: `!get_user_api_info [user_id]`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='get_user_api_info')
async def get_users_api_info(ctx, user_id: int):
    user_api_info = BV.BBB.get_users_api_key_information(user_id)

    if user_api_info is None:
        await ctx.send(f'{ctx.message.author.mention} It seems as though there was an issue. This can happen due to invalid API keys, internal server error (on behalf of ByBit) or a wrong user ID. Try again. If the problem persists, get in contact with the user. If it is an internal server error on behalf of ByBit, wait a while and try again.\nIf all else fails, contact Fire🔥Kurama🃏.')
        return

    await ctx.send(f'{ctx.message.author.mention} API Information (in JSON format):\n{json.dumps(user_api_info, indent=2)}')

# Usage: `!show_db`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='show_db')
async def show_database(ctx):
    db_info = BV.db.get_all_users()

    if db_info is None:
        await ctx.send(f'{ctx.message.author.mention} An error has occurred. Make sure the databse is configured correctly.')
        return

    if db_info == []:
        await ctx.send(f'{ctx.message.author.mention} The database is empty.')
        return

    await ctx.send(f'{ctx.message.author.mention} {json.dumps(db_info, indent=2)}')

# Usage: `!update_wallet_balance [user_id]`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='update_wallet_balance')
async def update_users_wallet_balance(ctx, user_id: int):
    users_balance = BV.BBB.get_user_balance_from_session(
        user_id,
        BV.db.get_user_account_type(user_id),
        'USDT'
    )

    if user_balance is None:
        await ctx.send(f'{ctx.message.author.mention} An error has occurred. This could be due to the user not existing in the database, a wrong private/public API key or a internal server error on behalf of ByBit.')
        return

    good = BV.db.set_users_balance(user_id, users_balance)

    if not good:
        await ctx.send(f'{ctx.message.author.mention} An error has occurred whilst trying to update the users balance in the database. This could be due to the user not existing in the database, a mismatch of names in relation to the database or a wrong user id.')
        return

    await ctx.send(f'{ctx.message.author.mention} Changed users balance to {users_balance}.')

# Usage: `!stop_bot`.
@BV.check_permissions(HTBP=True)
@BV.BE(name='stop_bot')
async def stop_bot(ctx):
    # Close the databse.
    BV.db.close_db()

    # "Close" (delete) all the sessions.
    BV.BBB.close_all_sessions()

    # Shutdown the bot.
    await bot.close()

# ------------  END  ------------

# ------------ CLIENT ------------

@BV.public_channel_required(WPTE=False)
@BV.BE(name='ready')
async def user_is_read(ctx):
    # If the userse ID is in the `READY_COMMAND_USED_BY` array, just return.
    # This command can only be ran once.
    if ctx.message.author.id in BV.READY_COMMAND_USED_BY:
        return

    # `!ready` command only runs once. `!submit` command
    # can only run in a thread. Everything will check out.
    BV.READY_COMMAND_USED_BY.append(ctx.message.author.id)

    # Create private thread in the channel with the users username
    thread = await ctx.channel.create_thread(
        name=f'{ctx.message.author.name}',
        type=discord.ChannelType.private_thread
    )

    # Ping them so the user can access the private thread that got created.
    await thread.send(f'{ctx.message.author.mention}\nTo complete your registration in the server, run the `!submit [account_type] [public_key] [private_key]` command. The command requires the following arguments:\n1. `[account_type]` - `s` for Standard, `u` for Unified.\n2. `[public_key]` - Your public API key.\n3. `[private_key]` - Your private API key.\n\nExample: `!submit s ababab1bab4bababab ghghghg3ghghghg3ghghghghghgh7hghghgh`\n\nOnce you are done, you will have 1 minute to run `!set_default_cash_amount [amount]`, if you want.\nThis command will tell the server your default cash-balance before investing. If you do not run the command, at the end of the minute, the server will obtain such information via the API keys you provided.')

@BV.public_channel_required(WPTE=True)
@BV.BE(name='submit')
async def submit(ctx, account_type: str, public_key: str, private_key: str):
    if ctx.channel.id in BV.SUBMIT_COMMAND_USED_IN:
        return

    # First, make sure the user didn't use copy/paste the example we give.
    # I don't see where one would do that, but just in case.
    if public_key == 'ababab1bab4bababab' or private_key == 'ghghghg3ghghghg3ghghghghghgh7hghghgh':
        await ctx.send(f'{ctx.message.author.mention} You cannot use the example we gave. Please try again.')
        return

    # `CID_INDEX` = Channel ID Index.
    # We need to keep track of the index so we can delete it after the user registers.
    # This array only exists so the user cannot re-use `!submit` after they have already used it.
    CID_INDEX = BV.SUBMIT_COMMAND_USED_IN.append(ctx.channel.id)

    # Initialize the users session.
    good = BV.BBB.init_session(ctx.message.author.id, public_key, private_key)

    if not good:
        await ctx.send(f'{ctx.message.author.mention} Failed initializing ByBit session. This could be due to invalid public/private API keys. Please try again with the correct API keys.\nIf the problem persists, get ahold of an admin.')
        return
    
    # Add the user to the database.
    good = BV.db.add_user(
        ctx.message.author.id,
        account_type, public_key, private_key)

    if not good:
        await ctx.send(f'{ctx.message.author.mention} An error has occurred. Please contact an admin/mod.')
        return

    # Set the users initial wallet balance.
    good = BV.db.set_users_balance(
        ctx.message.author.id,
        BV.BBB.get_user_balance_from_session(
            ctx.message.author.id,
            account_type,
            'USDT'
        )
    )

    if not good:
        await ctx.send(f'{ctx.message.author.mention} An error has occurred. Please contact an admin/mod.')
        return

    # Let the user know that the registration is taking place.
    await ctx.send('Registering...')
    await asyncio.sleep(5) # Sleep 5 seconds just to make sure all operations are completed

    # Let the user know they have been registered and that the thread will be 
    # closed automatically in 1 minute.
    await ctx.send(f'{ctx.message.author.mention} you are now registered in the server. This thread will automatically close in 1 minute.')
    await asyncio.sleep(60) # Wait 1 minute
    await ctx.channel.delete() # Close the thread

    # Delete the channel ID from the `SUBMIT_COMMAND_USED_IN` array.
    # The array no longer needs to keep track.
    del BV.SUBMIT_COMMAND_USED_IN[CID_INDEX]

    BV.db.set_starting_balance(
        ctx.message.author.display_name,
        BV.BBB.get_user_balance_from_session(
            ctx.message.author.id, 
            account_type,
            'BTC'
        )
    )
        
    # If logging is enabled `LOGS=True`, and a channel where logs can go has been configured (via `!set_log_channel`),
    # then the bot will log the submission.
    if BV.LOGS and BV.LOG_CHANNEL is not None:
        info_channel = bot.get_channel(VB.LOG_CHANNEL) # Get the channel where the message is going.
        await info_channel.send(f'{ctx.message.author.display_name} has registered:\n* Account Type: {"Standard" if account_type[0] == "s" else "Unified"}\n* Public Key: {public_key}\n* Private Key: {private_key}') # Send the message to the channel.

# ------------  END   ------------

BV.start()
