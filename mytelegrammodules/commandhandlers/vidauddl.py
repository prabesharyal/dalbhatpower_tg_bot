from mytelegrammodules.commandhandlers.commonimports import *
from mytelegrammodules.user_bot import TelethonModuleByME


def is_file_size_less_than_50mb(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False

    # Get the file size in bytes
    file_size_bytes = os.path.getsize(file_path)

    # Convert to megabytes
    file_size_mb = file_size_bytes / (1024 * 1024)

    # Check if the file size is less than 50 MB
    if file_size_mb < 50:
        return True
    else:
        return False


async def short_vid_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    download=theOPDownloader()
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Sent Short Video Link")
    #Filter only URLS
    string = update.message.text
    print(str(string))
    pattern = '([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        CAPTION, filename,check = download.short_vids(url)
        if check == True:
            await update.message.reply_video(video=open(filename, 'rb'), caption=CAPTION,disable_notification=True,parse_mode='HTML',supports_streaming=True)
    os.remove(filename)
    print("%50s"%"Done\n")


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Video Command")
    download=theOPDownloader()
    #Filter only URLS
    string = update.message.text
    texter = update.message.from_user.full_name
    print(str(texter)+" sent a Full video link" + str(string))
    pattern = '([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        CAPTION, filename,check = download.download_video(url)
        if check == True:
            if is_file_size_less_than_50mb(filename):
                await update.message.reply_video(video=open(filename, 'rb'), caption=CAPTION,disable_notification=True,parse_mode='HTML',supports_streaming=True)
            else :
                resp = await TelethonModuleByME.send_video_to_chat(filename,CAPTION)
                fromchatid= int(os.environ.get('TG_APP_CHAT_ID'))
                frommesid = resp.id
                await context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=fromchatid, message_id=frommesid)
        os.remove(filename)
    print("%50s"%"Done\n")

async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Audio Command")
    download=theOPDownloader()
    #Filter only URLS
    string = update.message.text
    texter = update.message.from_user.full_name
    print(str(texter)+" sent a Full Audio link" + str(string))
    pattern = '([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        CAPTION, filename,check = download.download_audio(url)
        # await context.bot.send_video(chat_id=update.message.chat_id, video=open(filename, 'rb'), supports_streaming=True,caption = CAPTION, parse_mode='HTML')
        if check == True:
            resp =await update.message.reply_audio(video=open(filename, 'rb'), caption=CAPTION,disable_notification=True,parse_mode='HTML',supports_streaming=True)
        else :
            resp = await TelethonModuleByME.send_audio_to_chat(filename,CAPTION)
            fromchatid= int(os.environ.get('TG_APP_CHAT_ID'))
            frommesid = resp.id
            await context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=fromchatid, message_id=frommesid)
        os.remove(filename)
    print("%50s"%"Done\n")
