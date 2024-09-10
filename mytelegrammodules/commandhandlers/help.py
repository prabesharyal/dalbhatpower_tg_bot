from mytelegrammodules.commandhandlers.commonimports import *


sample_text = '''
**A lot of help commands available.**\n \n
    \t`/start` - _Check whether bot is working or not._ 
    \t`/help` - _This menu is displayed._
    \t`/clean` - _Resets the bot server to the deployment time._\n \n 
**Any Sort of Public Video Links** 
    \t- _Sends you video upto 50MB using that link._\n
    \t`/ytaudio` your\_youtube\_link - _Sends audio from link._ \n\n 
**Some OpenAI tools :**\n 
    \t•`/dalle` Write Something to generate Image from. - _Sends pictures from text._
    \t•`/gpt` Write Something to generate Text from. - _Completes Your Text._ \n\n
**Isn't this help enough ???**'''


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Help Command")
    
    helptext = ''' ‎ ‎ ‎ ‎ ‎ ‎ ‎***@DalBhatPowerBot*** \n‎ ‎ ‎ ‎ ‎ ‎ ‎__(v1.0 Beta release)__
    \n\t***Few help commands available.***\n \n
    \t`/start` - _Check whether bot is working or not._ 
    \t`/help` - _This menu is displayed._
    
    \t`/echo something` - _Copies message sent with or replied to_
    \t`/info something` - _General information of you_
    \t`/pin` - _Pins the message replied to_
    \t`/unpin` - _Unpins the message replied to_
    \t`/delete` - _Deletes the message replied to_

    \t`any message with tiktok, instagram, facebook videos or youtube short links ` - _Sends you videos/photos._ 
    \t`@dalbhatpowerbot nepaliword` - _Can be Used to Search Nepali word._ 

    \t`/rashi Makar` - _Get Your Nepali Horoscope._
    \t`/nepse` - _Get Index Info._
    \t`/nepse SYM` - _Get Scrip Info._

    \t`/ad 2072-10-18` - _Convert BS To AD (Beta)._
    \t`/bs 2000/10/08` - _Convert BS To AD._
    \t`/now` - _Display's current Nepali Time and Date._
    \t`/today` - _Displays todays Nepali Date_
    \t`/patro` - _Displays this Nepali Month_
\n  
    \t`/video link` - _Downloads and send videos(1080p) upto 2 GB_
    \t`/audio link` - _Downloads and send audios(mp3) upto 2 GB_
\n
    \t`/ig link` - _Downloads and send instagram posts/reels/stories_
    \t`/X link` - _Downloads and sends tweets and videos_
    \t`/fb link` - _Downloads and send facebook videos_

\t\t**Isn't this help enough ???**
'''
# Downloads and send Facebook posts/videos (alpha)


    # await context.bot.send_message(chat_id=update.message.chat.id, text=helptext,parse_mode='MARKDOWN')
    await update.message.reply_markdown(
    helptext, reply_markup=ReplyKeyboardRemove(selective=True))
    # print("Help Module 1 completed successfully")



async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /info is issued."""
    message = update.message

    # Check if it's a personal chat
    if message.chat.type == 'private':
        user = message.from_user
        if user.username:
            infotext = f"Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
        else:
            infotext = f"First Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"

    # Check if it's a group chat
    elif message.chat.type == 'group':
        chat = message.chat
        infotext = f"Group Name: {chat.title}\nID: `-100{chat.id}`"

    # Check if the command mentions a user
    elif context.args:
        username = context.args[0]

        # Try to retrieve the user's information
        try:
            user = await context.bot.get_chat(username)
            if user:
                if user.username:
                    infotext = f"Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
                else:
                    infotext = f"First Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
        except Exception as e:
            infotext = f"User not found: {e}"

    # If none of the above, default to group info in groups, user info in private messages
    else:
        if message.chat.type == 'group':
            chat = message.chat
            infotext = f"Group Name: {chat.title}\nID: `{chat.id}`"
        else:
            user = message.from_user
            if user.username:
                infotext = f"Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
            else:
                infotext = f"First Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"

    await message.reply_markdown(infotext, reply_markup=ReplyKeyboardRemove(selective=True))
