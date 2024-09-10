from mytelegrammodules.commandhandlers.commonimports import *
from downloader.twitter import twiiter_dl
from utils.loader import Loader
from mytelegrammodules.commandhandlers.vidauddl import is_file_size_less_than_50mb
from mytelegrammodules.user_bot import TelethonModuleByME


def convert_html(string):
    string = string.replace('<', '&lt')
    string = string.replace('>', '&gt')
    return string

async def tweet_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) + ' ' + str(json['last_name'])+' : ' +
          str(json['id']))+" - Sent Twitter Link : " + update.message.text)
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    try:
        only_necesssary_regex = r'((twitter|x|X)\.(com)\/([\w]+)\/(status)\/[\d]+)'
        links = re.findall(only_necesssary_regex, update.message.text)

        if len(links) == 0:
            toreply = 'Please send a Proper Twitter Post Link\n\tNote : Private accounts are not yet Supported_'
            await update.message.reply_markdown(toreply,allow_sending_without_reply=True, reply_markup=ReplyKeyboardRemove(selective=True))
            return 'Done'    
        else:
            for link in links:
                url = "https://"+link[0]
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
                check, caption, filelist = twiiter_dl().scrape_download_tweet(url)
                os.system("pkill -f chrome")
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                if check != False:
                    cap = convert_html(caption)
                    CAPTION = '<a href="'+url+'">'+cap+'</a>'
                    if filelist==None and check=='empty':
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
                        username = re.search(r'https://twitter\.com/([^/]+)/status/\d+', url).group(1)
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                        CAPTION = f"<b>X`ed by @{username} on X:</b> \n\n" + CAPTION
                        await update.message.reply_html(CAPTION,allow_sending_without_reply=True, reply_markup=ReplyKeyboardRemove(selective=True), disable_web_page_preview=True)
                    elif len(filelist) == 1:
                        filename = filelist[0]
                        if filename.endswith(('mp4', 'webm')):
                            if is_file_size_less_than_50mb(filename):
                                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                                with Loader("Uploading Tweet Short Video : ","Tweeet Short Video Upload Success"):
                                    try:
                                        video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                                        await update.message.reply_video(video=open(filename, 'rb'),allow_sending_without_reply=True,duration=video_duration, caption=CAPTION, disable_notification=True, width=video_dimensions.get('width', 0), height=video_dimensions.get('height', 0),thumbnail=open(video_thumbnail_path,'rb'), parse_mode='HTML', supports_streaming=True)
                                    except Exception as e:
                                        print(e)
                                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                            else :
                                try:
                                    resp = await TelethonModuleByME.send_video_to_chat(filename, update, context, cap[:25]+"...")
                                    fromchatid= int(os.environ.get('TG_APP_CHAT_ID'))
                                    frommesid = resp.id
                                    await context.bot.copy_message(chat_id=update.effective_chat.id, from_chat_id=fromchatid, message_id=frommesid, caption=CAPTION,parse_mode='HTML')
                                except Exception as e:
                                    print(e)
                        if filename.endswith(('jpg', 'webp','heic')):
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                            with Loader("Uploading Twitter Photo", "Twitter Photo Upload Success"):
                                await update.message.reply_photo(photo=open(filename, 'rb'),allow_sending_without_reply=True, caption=CAPTION, disable_notification=True, parse_mode='HTML')
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                        os.remove(filename)
                    else:
                        media_group = []
                        for filename in filelist:
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                            media_group.append(InputMediaPhoto(open(filename, 'rb'), caption=CAPTION if len(
                                media_group) == 0 else '', parse_mode='HTML'))
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                        with Loader("Uploading Twitter Media Group", "Twitter Media Group Upload Success"):
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                            await update.message.reply_media_group(media=media_group, write_timeout=1000, allow_sending_without_reply=True,connect_timeout=1000, read_timeout=1000)
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")

        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    except Exception as e:
        print(e)
        os.system("pkill -f chrome")
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    print('%50s' % "Done")



#Upto 
#Here 
# Is
# Correct