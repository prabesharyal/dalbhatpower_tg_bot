from mytelegrammodules.commandhandlers.commonimports import *

async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /send is issued."""
    json = update.message.from_user
    # # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    # print(update.message)
    print((str(json['first_name']) + ' ' + str(json['last_name']) + ' : ' + str(json['id'])) + " - Issued Send Command")
    
    if update.message.reply_to_message:
        messages_to_send = update.message.reply_to_message
        await context.bot.copy_message(chat_id=update.effective_chat.id, from_chat_id=messages_to_send.chat_id, message_id=messages_to_send.message_id)
    else:
        if update.message.caption:
            message_text = update.message.caption[len('/send'):]
            await context.bot.copy_message(chat_id=update.effective_chat.id, from_chat_id=update.effective_chat.id, message_id=update.message.message_id,caption=message_text if message_text else ' ', disable_notification=True,parse_mode='HTML')   
        else:
        # Remove /send from the message text
            message_text = update.message.text[len('/send '):]
            # Copy the modified message content
            if message_text:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text,disable_web_page_preview=True, disable_notification=True,parse_mode='HTML') 
        
   
    await update.message.delete()

async def check_if_caption_contains_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if re.search(r'^\/send',update.message.caption) or re.search(r'^\/echo',update.message.caption):
        await send(update,context)
        
async def unzip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # if update.message.reply_to_message:
    #     messages_to_get_zip_from = update.message.reply_to_message
    # else:
    #     messages_to_get_zip_from = update.message
    json = update.message.from_user
    print((str(json['first_name']) + ' ' + str(json['last_name']) + ' : ' + str(json['id'])) + " - Issued UNzip Command")
    await update.message.reply_text(text="Please Use any other bots, cause I can't handle everything on my own.")
    
    
# Define the pin function
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    print((str(json['first_name']) + ' ' + str(json['last_name']) + ' : ' + str(json['id'])) + " - Issued PIN Command")
    chat_id = update.message.chat_id

    if update.message.reply_to_message:
        message_to_pin = update.message.reply_to_message
        # Check if the bot has the necessary permissions to pin messages
        try: 
            await context.bot.pin_chat_message(chat_id, message_to_pin.message_id, disable_notification=True)
        except Exception:
            await update.message.reply_text("I don't have permission to pin messages in this chat.")
    else:
        await update.message.reply_text("Please reply to a message to pin it.")

# Define the unpin function
async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    print((str(json['first_name']) + ' ' + str(json['last_name']) + ' : ' + str(json['id'])) + " - Issued PIN Command")
    chat_id = update.message.chat_id

    if update.message.reply_to_message:
        message_to_pin = update.message.reply_to_message
        # Check if the bot has the necessary permissions to pin messages
        try: 
            await context.bot.unpin_chat_message(chat_id, message_to_pin.message_id, disable_notification=True)
        except Exception:
            await update.message.reply_text("I don't have permission to unpin messages in this chat.")
    else:
        await update.message.reply_text("Please reply to a message to unpin it.")

# Define the delete function
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    print((str(json['first_name']) + ' ' + str(json['last_name']) + ' : ' + str(json['id'])) + " - Issued Delete Command")
    chat_id = update.message.chat_id

    if update.message.reply_to_message:
        message_to_delete = update.message.reply_to_message
        # Delete the replied message
        try:
            await context.bot.delete_message(chat_id, message_to_delete.message_id)
        except Exception:
            await update.message.reply_text("Not enough permission to delete.")
    else:
        await update.message.reply_text("Please reply to a message to delete it.")
