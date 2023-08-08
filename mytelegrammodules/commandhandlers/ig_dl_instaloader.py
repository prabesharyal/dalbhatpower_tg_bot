from mytelegrammodules.commandhandlers.commonimports import *
 



async def instagram_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # fullurlregex = r'(https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel)\/([^/?#&\s]+))'
    
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Instagram Command")
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)

    only_necesssary_regex = r'(instagram\.com\/(p|reel)\/([\w-]+))'
    links= re.findall(only_necesssary_regex,update.message.text)
    if len(links) == 0:
        toreply = 'Please send a Proper Instagram Post Or Reels Link\n\tNote : _Stories, Profiles and Highlights are not yet Supported_'
        await update.message.reply_markdown(toreply, reply_markup=ReplyKeyboardRemove(selective=True))
        return 'Done'
    else :
        for link in links:
            shortcode = link[2]
            CAPTION, filelist,check  = download_from_shortcode(shortcode)
            CAPTION = f'<a href="https://{link[0]}">{CAPTION}</a>'
            if check == True:
                if len(filelist) == 1:
                    filename = filelist[0]
                    if filename.endswith('mp4'):
                        await update.message.reply_video(video=open(filename, 'rb'), caption=CAPTION,disable_notification=True,parse_mode='HTML',supports_streaming=True)
                    if filename.endswith('jpg'):
                        await update.message.reply_photo(photo=open(filename, 'rb'), caption=CAPTION,disable_notification=True,parse_mode='HTML')
                    os.remove(filename)
                else:
                    media_group = []
                    for filename in filelist:
                        if filename.endswith('mp4'):
                            media_group.append(InputMediaVideo(open(filename, 'rb'),caption = CAPTION if len(media_group) == 0 else '',parse_mode='HTML'))
                        if filename.endswith('jpg'):
                            media_group.append(InputMediaPhoto(open(filename, 'rb'),caption = CAPTION if len(media_group) == 0 else '',parse_mode='HTML'))
                    await update.message.reply_media_group(media=media_group,write_timeout=60)
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    print('%50s'%"Done")





    
    
    
    

