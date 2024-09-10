from mytelegrammodules.commandhandlers.start import *
from mytelegrammodules.commandhandlers.help import *
from mytelegrammodules.commandhandlers.inlinedict import *
from mytelegrammodules.commandhandlers.nepcal import *
from mytelegrammodules.commandhandlers.nepse import *
from mytelegrammodules.commandhandlers.vidauddl import *
from mytelegrammodules.commandhandlers.insta_igdlp import *
from mytelegrammodules.commandhandlers.tweet_dl import *
from mytelegrammodules.commandhandlers.facebook_dl import *
from mytelegrammodules.commandhandlers.general_downloader import *
from mytelegrammodules.commandhandlers.others import *


API_HASH = TG_BOT = os.getenv('TG_BOT_TOKEN')



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_HASH).read_timeout(100).write_timeout(500).get_updates_read_timeout(100).connect_timeout(100).build()
    print("Application is running!")
    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("send", send))
    application.add_handler(CommandHandler("echo", send))
    application.add_handler(CommandHandler("pin", pin))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("unpin", unpin))
    application.add_handler(CommandHandler("unzip", unzip))


    # application.add_handler(MessageHandler(filters.Regex(r'^\/send'),send)) 
    application.add_handler(MessageHandler(filters.Caption(), check_if_caption_contains_send))
    application.add_handler(MessageHandler(filters.Caption(), check_if_caption_contains_send))

    
    # application.add_handler(MessageHandler(filters.Regex(r'^\/send ') & ~filters.COMMAND, send, block=False))

    #Calendar variants
    application.add_handler(CommandHandler("ad", ad))
    application.add_handler(CommandHandler("toad", ad))
    application.add_handler(CommandHandler("bs", bs))
    application.add_handler(CommandHandler("tobs", bs))
    application.add_handler(CommandHandler("now", now))
    application.add_handler(CommandHandler("time", now))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("date", today))
    application.add_handler(CommandHandler("patro", patro))
    application.add_handler(CommandHandler("calendar", patro))
    application.add_handler(CommandHandler("calender", patro))
    application.add_handler(CommandHandler("month", patro))

    
    #rasifal variants
    application.add_handler(CommandHandler("rasifal", rasifal))
    application.add_handler(CommandHandler("rashi", rasifal))
    application.add_handler(CommandHandler("rasi", rasifal))
    application.add_handler(CommandHandler("rasifal", rasifal))
    application.add_handler(CommandHandler("rasiphal", rasifal))
    application.add_handler(CommandHandler("horoscope", rasifal))
    application.add_handler(CommandHandler("zodiac", rasifal))

    
    #NEPSE
    application.add_handler(CommandHandler("nepse", nepse,block=False))

    #YTDLP
    application.add_handler(CommandHandler("video", video, block=False))
    application.add_handler(CommandHandler("audio", audio, block=False))
    
    #cobalt
    application.add_handler(CommandHandler("ig", instagram_dl, block=False))
    application.add_handler(CommandHandler("instagram", instagram_dl, block=False))
    
    #rapid_api
    application.add_handler(CommandHandler("igstory", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("ig2", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("igbackup", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("rapidapi", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("rapidig", rapid_ig_dl, block=False))
    
    application.add_handler(InlineQueryHandler(inline_query))
    
    #twitter
    application.add_handler(CommandHandler("twitter", tweet_dl, block=False))
    application.add_handler(CommandHandler("tweet", tweet_dl, block=False))
    application.add_handler(CommandHandler("x", tweet_dl, block=False))

    # #facebook
    application.add_handler(CommandHandler("fb", fbviddl, block=False))
    application.add_handler(CommandHandler("facebook", fbviddl, block=False))
    application.add_handler(CommandHandler("fbdl", fbviddl, block=False))
    application.add_handler(CommandHandler("fbvid", fbviddl, block=False))

    #Downloader
    application.add_handler(CommandHandler("download", file_dl, block=False))
    application.add_handler(CommandHandler("dwnld", file_dl, block=False))
    application.add_handler(CommandHandler("dwld", file_dl, block=False))
    application.add_handler(CommandHandler("file", file_dl, block=False))
    application.add_handler(CommandHandler("fdm", file_dl, block=False))
    application.add_handler(CommandHandler("dl", file_dl, block=False))
    application.add_handler(CommandHandler("direct_dl", file_dl, block=False))


    
    #For Short Video Links in Messages
    application.add_handler(MessageHandler(filters.Regex('(?:https?://)?(?:(?:www|m)\.)?youtube\.com/shorts/[-a-zA-Z0-9]+|tiktok\.com/@[-a-zA-Z0-9_]+/video/\d+|vt\.tiktok\.com/[-a-zA-Z0-9]+') & ~filters.COMMAND, short_vid_download, block=False))
    application.add_handler(MessageHandler(filters.Regex('(https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel(s)?)\/([^/?#&\s]+))') & ~filters.COMMAND, instagram_dl, block=False))
    application.add_handler(MessageHandler(filters.Regex('(twitter|x|X)\.com\/\w+\/status\/\d+') & ~filters.COMMAND, tweet_dl, block=False))
    application.add_handler(MessageHandler(filters.Regex('((https:\/\/)?(fb|www)?\.(facebook\.com|watch)\/[\w\/\.\?=\&]+)') & ~filters.COMMAND, fbviddl, block=False))

    
    # application.add_handler(MessageHandler(filters.Regex('(facebook\.com)\/((photo\/[\S]+)|(groups\/([\w\.]+\/permalink\/[\d]+))|([\w\.]+)\/(posts)\/[\w]+)') & ~filters.COMMAND, facebook_dl, block=False))

#  insta+yt+tiktok = (?:https?://)?(?:(?:www|m)\.)?(?:instagram\.com/reels/[-a-zA-Z0-9_]+|youtu(?:be\.com/shorts/|\.be/)|tiktok\.com/@[-a-zA-Z0-9_]+/video/\d+|vt\.tiktok\.com/[-a-zA-Z0-9]+)'

    #For other links
    # application.add_handler(MessageHandler(filters.Regex('([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})') & ~filters.COMMAND, main_url_dl))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()