from mytelegrammodules.commandhandlers.commonimports import *
from mytelegrammodules.user_bot import TelethonModuleByME
from utils.vid_aud_metadata import *
from downloader.facebookvids import main_fb_dl

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


async def fbviddl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)

    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Video Command")
    #Filter only URLS
    string = update.message.text
    texter = update.message.from_user.full_name
    print(str(texter)+" sent a Facebook video link" + str(string))
    pattern = '([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        check, CAPTION, fielist = main_fb_dl(url)
        try:
            filename = fielist[0]
        except Exception as e:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            break
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
        if check == True:
            CAPTION = f'<a href="{url}">{CAPTION}</a>'
            if is_file_size_less_than_50mb(filename):
                with Loader("Uploading Facebook Short Video : ","Facebook Short Video Upload Success"):
                    try:
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                        video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                        await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, caption=CAPTION,allow_sending_without_reply=True, disable_notification=True, width=video_dimensions['width'], height=video_dimensions['height'],thumb=open(video_thumbnail_path,'rb'), parse_mode='HTML', supports_streaming=True)
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                    except Exception as e:
                        print(e)
            else :
                try:
                    resp = await TelethonModuleByME.send_video_to_chat(filename, update, context, CAPTION)
                    fromchatid= int(os.environ.get('TG_APP_CHAT_ID'))
                    frommesid = resp.id
                    await update.message.reply_copy(from_chat_id=fromchatid, message_id=frommesid, caption=CAPTION,parse_mode='HTML', allow_sending_without_reply=True)
                except Exception as e:
                    print(e)
            os.remove(filename)
    print("%50s"%"Done\n")


