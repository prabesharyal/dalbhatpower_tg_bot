from mytelegrammodules.commandhandlers.commonimports import *
from downloader.instagram import ig_dlp
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


async def instagram_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # fullurlregex = r'(https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel)\/([^/?#&\s]+))'
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) + ' ' + str(json['last_name'])+' : ' +
          str(json['id']))+" - Sent Insta Link : " + update.message.text)
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    try:
        if re.match(r'(instagram\.com\/(stories)\/([\w\-\.]+)\/([\d]+)\/)', str(update.message.text)) == None:
            toreply = '*Sorry for Inconvenience*, Stories are not supported for now.'
            await update.message.reply_text(toreply, reply_markup=ReplyKeyboardRemove(selective=True), parse_mode='Markdown')
            print("Story Link, So Sent Sorry message.")
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
                check, caption, filelist = ig_dlp(url).download()
                if check != False:
                    cap = convert_html(caption)
                    CAPTION = '<a href="'+url+'">'+cap+'</a>'
                    if len(filelist) == 1:
                        filename = filelist[0]
                        if filename.endswith(('mp4', 'webm')):
                            with Loader("Uploading Instagram Video", "Instagram Video Upload Success"):
                                await update.message.reply_video(video=open(filename, 'rb'), caption=CAPTION, disable_notification=True, parse_mode='HTML', supports_streaming=True)
                        if filename.endswith(('jpg', 'webp')):
                            with Loader("Uploading Instagram Photo", "Instagram Photo Upload Success"):
                                await update.message.reply_photo(photo=open(filename, 'rb'), caption=CAPTION, disable_notification=True, parse_mode='HTML')
                        os.remove(filename)
                    else:
                        media_group = []
                        for filename in filelist:
                            if filename.endswith(('mp4', 'webm')):
                                media_group.append(InputMediaVideo(open(filename, 'rb'), caption=CAPTION if len(
                                    media_group) == 0 else '', parse_mode='HTML'))
                            if filename.endswith(('jpg', 'webp')):
                                media_group.append(InputMediaPhoto(open(filename, 'rb'), caption=CAPTION if len(
                                    media_group) == 0 else '', parse_mode='HTML'))
                        with Loader("Uploading Instagram Media Group", "Instagram Media Group Upload Success"):
                            for media_chunks in media_group_splitter(media_group):
                                await update.message.reply_media_group(media=media_chunks, write_timeout=1000, connect_timeout=1000, read_timeout=1000)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    except Exception as e:
        print(e)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    print('%50s' % "Done")
