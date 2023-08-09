from mytelegrammodules.commandhandlers.start import *
from mytelegrammodules.commandhandlers.help import *
from mytelegrammodules.commandhandlers.inlinedict import *
from mytelegrammodules.commandhandlers.nepcal import *
from mytelegrammodules.commandhandlers.nepse import *
from mytelegrammodules.commandhandlers.vidauddl import *
from mytelegrammodules.commandhandlers.insta_igdlp import *


API_HASH = TG_BOT = os.getenv('TG_BOT_TOKEN')



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_HASH).read_timeout(100).write_timeout(500).get_updates_read_timeout(100).connect_timeout(100).build()
    print("Application is running!")
    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    
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
    
    #instaloader
    application.add_handler(CommandHandler("ig", instagram_dl, block=False))
    application.add_handler(CommandHandler("instagram", instagram_dl, block=False))
    
    application.add_handler(InlineQueryHandler(inline_query))
    
    
    #For Short Video Links in Messages
    application.add_handler(MessageHandler(filters.Regex('(?:https?://)?(?:(?:www|m)\.)?youtube\.com/shorts/[-a-zA-Z0-9]+|tiktok\.com/@[-a-zA-Z0-9_]+/video/\d+|vt\.tiktok\.com/[-a-zA-Z0-9]+') & ~filters.COMMAND, short_vid_download, block=False))
    application.add_handler(MessageHandler(filters.Regex('(https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel(s)?)\/([^/?#&\s]+))') & ~filters.COMMAND, instagram_dl, block=False))

#  insta+yt+tiktok = (?:https?://)?(?:(?:www|m)\.)?(?:instagram\.com/reels/[-a-zA-Z0-9_]+|youtu(?:be\.com/shorts/|\.be/)|tiktok\.com/@[-a-zA-Z0-9_]+/video/\d+|vt\.tiktok\.com/[-a-zA-Z0-9]+)'

    #For other links
    # application.add_handler(MessageHandler(filters.Regex('([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})') & ~filters.COMMAND, main_url_dl))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()