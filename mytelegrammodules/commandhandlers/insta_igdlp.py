from mytelegrammodules.commandhandlers.commonimports import *
from downloader.instagram import ig_dlp
from downloader.insta_story import rapid_ig

from utils.loader import Loader


def convert_html(string):
    string = string.replace('<', '&lt')
    string = string.replace('>', '&gt')
    return string


def media_group_splitter(input_list):
    if len(input_list) <= 10:
        return [input_list]

    num_parts = len(input_list) // 10
    remainder = len(input_list) % 10

    parts = []
    start = 0
    for _ in range(num_parts):
        end = start + 10
        parts.append(input_list[start:end])
        start = end

    if remainder > 0:
        parts.append(input_list[-remainder:])

    return parts

async def send_and_all(update, context, check, caption, filelist, url):
    if check != False:
        cap = convert_html(caption)
        CAPTION = '<a href="'+url+'">'+cap+'</a>'
        if len(filelist) == 1:
            filename = filelist[0]
            if filename.endswith(('mp4','webm','mkv','hevc','avc')):
                video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                video_thumbnail_path = video_thumbnail_path if os.path.exists(video_thumbnail_path) else None
                with Loader("Uploading Instagram Video", "Instagram Video Upload Success"):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                    try:
                        await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, write_timeout=1000, connect_timeout=1000, read_timeout=1000, caption=CAPTION, disable_notification=True, width=video_dimensions['width'], height=video_dimensions['height'], thumbnail=open(video_thumbnail_path,'rb') if video_thumbnail_path else None, parse_mode='HTML', supports_streaming=True)
                    except Exception as e:
                        await context.bot.send_video(chat_id=update.effective_chat.id,
                            video=open(filename, "rb"),
                            duration=video_duration,
                            write_timeout=1000,
                            connect_timeout=1000,
                            read_timeout=1000,
                            caption=CAPTION,
                            disable_notification=True,
                            width=video_dimensions["width"],
                            height=video_dimensions["height"],
                            thumbnail=open(video_thumbnail_path, "rb"),
                            parse_mode="HTML",
                            supports_streaming=True,
                        )
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            if filename.endswith(('jpg','jpeg', 'webp','heic')):
                with Loader("Uploading Instagram Photo", "Instagram Photo Upload Success"):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                    try:
                        await update.message.reply_photo(photo=open(filename, 'rb'),caption=CAPTION, write_timeout=1000, connect_timeout=1000, read_timeout=1000,disable_notification=True, parse_mode='HTML')
                    except Exception as e:
                        context.bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open(filename, "rb"),
                            caption=CAPTION,
                            write_timeout=1000,
                            connect_timeout=1000,
                            read_timeout=1000,
                            disable_notification=True,
                            parse_mode="HTML",
                        )
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")

            os.remove(filename)
        else:
            media_group = []
            for filename in filelist:
                if filename.endswith(('mp4', 'webm','mkv','hevc','avc')):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                    media_group.append(InputMediaVideo(open(filename, 'rb'), caption=CAPTION if (len(media_group)%10==0) else '', parse_mode='HTML'))
                    time.sleep(0.4)
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                if filename.endswith(('jpg', 'jpeg','webp','heic')):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                    media_group.append(InputMediaPhoto(open(filename, 'rb'), caption=CAPTION if (len(media_group)%10==0) else '', parse_mode='HTML'))
                    time.sleep(0.2)
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            with Loader("Uploading Instagram Media Group", "Instagram Media Group Upload Success"):
                for index, media_chunks in enumerate(media_group_splitter(media_group)):
                    if index == 0:
                        try:
                            await update.message.reply_media_group(media=media_chunks, write_timeout=1000, connect_timeout=1000, read_timeout=1000)
                        except Exception as e:
                            await context.bot.send_media_group(
                                chat_id=update.effective_chat.id,
                                media=media_chunks,
                                write_timeout=1000,
                                connect_timeout=1000,
                                read_timeout=1000,
                            )
                    else:
                        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_chunks, write_timeout=1000, connect_timeout=1000, read_timeout=1000)
                    time.sleep(2)

async def rapid_ig_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # fullurlregex = r'(https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel)\/([^/?#&\s]+))' 
    print("This is RapidAPI Mode")
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Sent Insta Link : " + update.message.text)
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    try:
        # only_necesssary_regex = r'((instagram\.com\/(p|reel|reels)\/([\w\-]+))|(instagram\.com\/(stories)\/([\w\-\.]+)\/([\d]+)\/))'
        only_necesssary_regex = r'(instagram\.com\/(p|reel|reels|stories)\/([\w\-]+)(\/[\d]+)?)'
        links= re.findall(only_necesssary_regex,update.message.text)
        if len(links) == 0:
            toreply = 'Please send a Proper Instagram Post Or Reels Link\n\tNote : Profiles and Highlights are not yet Supported_'
            await update.message.reply_markdown(toreply, reply_markup=ReplyKeyboardRemove(selective=True))
            return 'Done'
        else :
            for link in links:
                url = "https://"+link[0]
                check,caption,filelist  = rapid_ig(url).download()
                await send_and_all(update, context, check, caption, filelist, url)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    except Exception as e:
        print(e)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    print('%50s'%"Done")


async def instagram_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # fullurlregex = r'(https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel)\/([^/?#&\s]+))'
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) + ' ' + str(json['last_name'])+' : ' +
          str(json['id']))+" - Sent Insta Link : " + update.message.text)
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    try:
        if re.search(r'instagram\.com\/(stories)\/([\w\.\_\-]+)\/([\d]+)(\/)?(\?)?.*',update.message.text):
            # toreply = '*Sorry for Inconvenience*, Stories are not supported for now.'
            # await update.message.reply_text(toreply, reply_markup=ReplyKeyboardRemove(selective=True), parse_mode='Markdown')
            # print("Story Link, So Sent Sorry message.")
            await rapid_ig_dl(update, context)
            return 'Done'

            
        only_necesssary_regex = r'(instagram\.com\/(p|reel|reels)\/([\w\-]+))'
        links = re.findall(only_necesssary_regex, update.message.text)

        if len(links) == 0:
            toreply = 'Please send a Proper Instagram Post Or Reels Link\n\tNote : Profiles and Highlights are not yet Supported_'
            await update.message.reply_markdown(toreply, reply_markup=ReplyKeyboardRemove(selective=True))
            return 'Done'
        else:
            for link in links:
                url = "https://"+link[0]
                # print(url)
                check, caption, filelist = await ig_dlp(url).download()
                # check, caption, filelist = ig_dlp(url).download()
                # print(filelist)
                time.sleep(5)
                # print(caption)

                # if os.path.exists(filelist[0]):
                #     print("File exists")
                # else:
                #     print("File doesn't exist")
                await send_and_all(update, context, check, caption, filelist, url)
                time.sleep(2)
                # os.remove(s for s in filelist)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    except Exception as e:
        print(e)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    print('%50s' % "Done")


