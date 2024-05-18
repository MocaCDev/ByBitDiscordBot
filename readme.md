# This file contains key information over the bot and the database.

<hr>

### Quick Disclaimer
The bot is going to need admin-level privileges as it will be creating private threads for the user to send their private/public API key.
This is the only way to keep all information confidential to the user.
The channel in which the thread is created **must** be a public text channel.
Private threads, by default, are allowed to be seen by mods and admins.

## Bot 
As requested, the bot comes equipped with commands that enable admins of the discord server to interact with it, obtain user-data and perform various other tasks.

The bot will need some initial configuration before being able to be used to its full potential.
The bot will work in any private channel. So, there is no configuration to be done in regards to private channels.

By default, all public channels are off limits to the bot; with that, you are going to have to configure the bot to accustom itself to a specific channel of choice in which it can display the how-to guide for generating Read-Only API private/public keys alongside create private threads where users supply the bot with their private/public key.

`!add_pub_channel [channel_id]` will add a public channel to a list that the bot holds. This list will hold all public channels in which the how-to guide can be displayed and private-threads can be created.
Inversely, to remove a public channel run `!rem_pub_channel [channel_id]`

With the above said, you can always explicitly edit the source code and add the channel IDs directly into the list. The above commands have been added for ease of use.

The commands consist of, but are not limited to:

1. `!calc [user]`
    * Gathers trading history, performs calculation to calculate loss/gain.
2. `!view_users`
    * Fetches all users from database and displays their informatoin in a private channel.
3. `!view_user [user]`
    * Fetches a specific user from the database and displays their information in a private channel.
4. `!get_user_pub [user]`
    * Fetches a users public key from the database.
5. `!get_user_priv [user]`
    * Fetches a users private key from the database.
6. `!get_user_keys [user]`
    * Fetches both private/public keys from the database.
7. `!manually_add [user] [public_key] [private_key]`
    * Enables owners, admins (and mods) to explicitly add a user to the database.
8. `!manually_del [user]`
    * Enables owners, admins (and mods) to explicitly remove a user from the database.

### Upon Joining & How users can secretly give the bot their API keys
Upon joining, it will be up to you to invoke `!explain` in the channel of choice. This command will result in a thorough explanation on how the user can get a Read-Only API key.

**Don't forget to run `!add_pub_channel [channel_id]`, where `[channel_id]` is the channel where `!explain` is being invoked.**

Once the user is done following the instructions, they can run the `!ready` command which will notify the bot they are ready to give it their private/public API key. This command will prompt the bot to create a private thread with the user. In this thread, the user will run `!submit [public_key] [private_key]`. **The public key needs to be first, followed by the private.**

This will prompt the bot to save their key in the database. The bot will take the users discord username as a value to store for the username in the database.

## Database 
The code comes equipped with a database template.

There are two files that comes with the source code:
1. `database_connection.yaml`
    * This file is where you can specify the host, username and password to your sql instance
2. `table_layout.yaml`
    * This file is where you can specify the table layout you want for your database.

An advised table layout (which is shipped with the source code):

`user, varchar(15)`
* 15 characters will give enough room for a username. Frankly, discord usernames don't exceed 10 characters but 15 is a safe number.

`private, varchar(50)`
* 50 characters will give enough padding for a value that will be rather volatile from user to user in regards to length of the private key.

`public, varchar(25)`
* 25 characters will give enough padding for a value that, again, will be rather volatile from user to user in regards to the length of the public key.
