import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters, ConversationHandler)


class CatBreadBot:
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    QUESTION1, QUESTION2 = range(2)

    def __init__(self, dispatcher):
        self.yes_words = ["да", "конечно", "ага", "пожалуй"]
        self.no_words = ["нет", "нет, конечно", "ноуп", "найн"]
        self.dispatcher = dispatcher
        self.__process_handlers()

    def start(self, update, context):
        update.message.reply_text("Привет! Я помогу отличить кота от хлеба! Обьект перед тобой квадратный?")

        return self.QUESTION1

    def understand(self, msg):
        return any(x in msg.lower() for x in self.yes_words) or any(x in msg.lower() for x in self.no_words)

    def question_cube(self, update, context):
        user = update.message.from_user
        msg = update.message.text
        self.logger.info(f"Message of {user.first_name}: {msg}")

        if not self.understand(msg):
            update.message.reply_text("Не понимаю(\nДа или нет?")
            return self.QUESTION1
        if any(x in msg.lower() for x in self.no_words):
            update.message.reply_text("Это кот, а не хлеб! Не ешь его!")
            return ConversationHandler.END
        else:
            update.message.reply_text("У него есть уши?")
            return self.QUESTION2

    def question_ears(self, update, context):
        user = update.message.from_user
        msg = update.message.text
        self.logger.info(f"Message of {user.first_name}: {msg}")

        if not self.understand(msg):
            update.message.reply_text("Не понимаю(\n Да или нет?")
            return self.QUESTION2
        if any(x in msg.lower() for x in self.no_words):
            update.message.reply_text("Это хлеб, а не кот! Ешь его!")
        else:
            update.message.reply_text("Это кот, а не хлеб! Не ешь его!")
        return ConversationHandler.END

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning(f'Update "{update}" caused error "{context.error}"')

    def __process_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                self.QUESTION1: [MessageHandler(Filters.text, self.question_cube)],
                self.QUESTION2: [MessageHandler(Filters.text, self.question_ears)]
            },

            fallbacks=[]
        )
        self.dispatcher.add_handler(conv_handler)
        self.dispatcher.add_error_handler(self.error)
