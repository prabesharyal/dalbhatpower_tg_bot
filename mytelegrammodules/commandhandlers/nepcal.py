from mytelegrammodules.commandhandlers.commonimports import *



async def rasifal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Rasifal Command")
    receivedstring = update.message.text
    splitted = receivedstring.split(' ')
    if len(splitted) == 1:
        rashi=NepaliRashiFal.get_all_horoscope()
    else:
        rashi=NepaliRashiFal.get_horoscope(splitted[1])   
    await update.message.reply_markdown(rashi, reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")
    
async def ad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued AD Command")
    string = ' '.join(update.message.text.split()[1:])
    await update.message.reply_markdown(nepalSpecialTimes.convert_to_ad(string), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")

async def bs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued BS Command")
    string = ' '.join(update.message.text.split()[1:])
    await update.message.reply_markdown(nepalSpecialTimes.convert_to_bs(string), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued NOW Command")
    await update.message.reply_markdown(nepalSpecialTimes.nepali_now(), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")



async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Today Command")
    await update.message.reply_markdown(nepalSpecialTimes.nepali_today(), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")



async def patro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Patro Command")
    await update.message.reply_markdown(nepalSpecialTimes.patro(), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")


