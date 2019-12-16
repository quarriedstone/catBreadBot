from telegram.ext import Updater
from bot.CatBreadBot import CatBreadBot


def main():
    updater = Updater("982112851:AAHfZlRWnSsCdm58-uUfnjS9HtlMbO72l_M", use_context=True)

    dp = updater.dispatcher
    # Added conversation for QUESTION1 and QUESTION2
    cat_bread_bot = CatBreadBot(dp, updater.bot)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
