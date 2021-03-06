import re
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from settings import TOKEN, phrases, stickers

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здарова поехавшие!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Где помощь? По чему нет помощи?')


def echo(update, context):
    text_lover = update.message.text.lower()

    for phrase, msg in phrases.items():
        reg = re.compile(phrase)
        if reg.search(text_lover):
            update.message.reply_text(msg)
            break

    for phrase, sticker_id in stickers.items():
        reg = re.compile(phrase)
        if reg.search(text_lover):
            update.message.reply_sticker(sticker_id)
            break


# def sticker(update, context):  # для поиска file_id стикера
#     update.message.reply_sticker("Make error")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # updater = Updater(TOKEN, use_context=True)
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_handler(MessageHandler(Filters.sticker, sticker))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
