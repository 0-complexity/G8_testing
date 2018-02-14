from telegram.ext import Updater, CommandHandler


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(str(update.message.chat.__dict__)))

updater = Updater('452340132:AAGIRY6YPKo1TMCsWgU-jP_FVwmCm2t3xgg')
dp = updater.dispatcher
dp.add_handler(CommandHandler('hi', hello))

updater.start_polling()
updater.idle()
