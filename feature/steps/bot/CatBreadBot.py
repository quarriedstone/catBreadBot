import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import os
from clarifai.rest import ClarifaiApp, Concept


class CatBreadBot:
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    QUESTION1, QUESTION2, PHOTO = range(3)

    def __init__(self, dispatcher, bot):
        self.yes_words = ["да", "конечно", "ага", "пожалуй"]
        self.no_words = ["нет", "нет, конечно", "ноуп", "найн"]
        self.dispatcher = dispatcher
        self.bot = bot
        self.__process_handlers()

    def start(self, update, context):
        update.message.reply_text("Привет! Я помогу отличить кота от хлеба! Обьект перед тобой квадратный?")

        return self.QUESTION1

    def photo(self, update, context):
        update.message.reply_text("Привет, я помогу отличить кота от хлеба. Пришли мне фотографию обьекта. Я "
                                  "определю, что находится перед вами.")

        return self.PHOTO

    def classify_image(self, filename):
        cat_score, bread_score = 0, 0
        app = ClarifaiApp(api_key='d91a3c5af2234d1589e8f4ae7a98be08')
        model = app.public_models.general_model
        select_concept_list = [Concept(concept_name='bread'), Concept(concept_name='cat')]
        response = model.predict_by_filename(filename, select_concepts=select_concept_list)

        list_val = response['outputs'][0]['data']['concepts']
        for concept in list_val:
            if concept['name'] == 'cat':
                cat_score = float(concept['value'])
            if concept['name'] == 'bread':
                bread_score = float(concept['value'])

        return cat_score, bread_score

    def process_photo(self, update, context):
        user = update.message.from_user
        update.message.reply_text("Обрабатываю фото")
        photo = self.bot.getFile(update.message.photo[-1].file_id)
        self.logger.info(f"Message of {user.first_name}: photo")

        filename = os.path.join('./', f'{photo.file_id}.jpg')
        photo.download(filename)
        cat_score, bread_score = self.classify_image(filename)

        if bread_score > cat_score:
            update.message.reply_text("C %.2f вероятность это хлеб! Ешь его!" % bread_score)
        else:
            update.message.reply_text("С %.2f вероятность это кот! Не ешь его!" % cat_score)

        os.remove(filename)

        return ConversationHandler.END

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
            entry_points=[CommandHandler('start', self.start), CommandHandler('photo', self.photo)],

            states={
                self.QUESTION1: [MessageHandler(Filters.text, self.question_cube)],
                self.QUESTION2: [MessageHandler(Filters.text, self.question_ears)],
                self.PHOTO:[MessageHandler(Filters.photo, self.process_photo)]
            },

            fallbacks=[],
            allow_reentry=True
        )
        self.dispatcher.add_handler(conv_handler)
        self.dispatcher.add_error_handler(self.error)

def main():
    updater = Updater("982112851:AAHfZlRWnSsCdm58-uUfnjS9HtlMbO72l_M", use_context=True)

    dp = updater.dispatcher
    bot = updater.bot
    # Added conversation for QUESTION1 and QUESTION2
    cat_bread_bot = CatBreadBot(dp, bot)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()