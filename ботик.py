from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


TOKEN = '5219235474:AAG4SluLc6f44WVFK8KlOnZlRkgXsEK8IJI'


class Menu:
    def __init__(self):
        reply_keyboard = [['/Time_to_end', '/Timetable'],
                          ['/Redact', '/Homework'],
                          ['/Subject', '/Repetition', '/Help']]
        self.markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        updater = Updater(TOKEN)
        dp = updater.dispatcher
        text_handler = MessageHandler(Filters.text & ~Filters.command, self.echo)
        dp.add_handler(text_handler)
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("Time_to_end", self.Time_to_end_def))
        dp.add_handler(CommandHandler("Timetable", self.Timetable_def))
        dp.add_handler(CommandHandler("Redact", self.Redact_def))
        dp.add_handler(CommandHandler("Homework", self.Homework_def))
        dp.add_handler(CommandHandler("Subject", self.Subject_def))
        dp.add_handler(CommandHandler("Repetition", self.Repetition_def))
        dp.add_handler(CommandHandler("Help", self.help))
        dp.add_handler(CommandHandler("close", self.close_keyboard))
        updater.start_polling()
        updater.idle()

    def echo(self, update, context):
        update.message.reply_text("Пожалуйста, введите команду\n:((")

    def start(self, update, context):
        update.message.reply_text(
            "Ля ля ля большой текст о способностях",
            reply_markup=self.markup
        )

    def close_keyboard(self, update, context):
        update.message.reply_text(
            "Ok",
            reply_markup=ReplyKeyboardRemove()
        )

    def help(self, update, context):
        update.message.reply_text(
            "Ля ля ля ещё большой текст как в старте")

    def Timetable_def(self, update, context):
        update.message.reply_text(
            "Выдаёт расписание: всё, по дню недели, числу"
            "Проверить наличие дз на число")

    def Time_to_end_def(self, update, context):
        update.message.reply_text("Предлагает выбрать: до конца года(установленное значение), до введённой даты "
                                  "АЙПИ ссылка на официальный сайт МИНобразования")

    def Redact_def(self, update, context):
        update.message.reply_text(
            "Даёт возможность добавить/удалить предмет, изменить/добавить расписание, изменить класс")

    def Homework_def(self, update, context):
        update.message.reply_text(
            "Спрашивает число предмет, если в тот день нет данного предмета"
            " предупреждает и предлагает перенести на ближайшее число ")

    def Repetition_def(self, update, context):
        update.message.reply_text(
            "Предлагает записать вопросы в виде вопрос-ответ, или же повторить формулы"
            " (берет из БД в зависимости от класса человека)"
            "Далее выдаёт по одному вопросы и считает результат в процентах")

    def Subject_def(self, update, context):
        update.message.reply_text(
            "Список предметов в виде кнопок, там же ссылки на Якласс теорию)")


if __name__ == '__main__':
    Menu()