from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import time


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
        update.message.reply_text("Пожалуйста, введите команду\n:(( \n Чтобы начать сначала введите /start")

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
            "Список предметов в виде кнопок, там же ссылки на Якласс теорию)")   #, reply_markup=ReplyKeyboardRemove())
        # self.close_keyboard(self, update, context)
        self.Predmets(update, context)


    def Predmets(self, update, context):
        subjects_keyboard = [['/Math', '/Russian'],
                             ['/Biology', '/Chemistry'],
                             ['/Geography', '/History']]
        self.markup_subj = ReplyKeyboardMarkup(subjects_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            "Список предметов на кнопках", reply_markup=self.markup_subj)
        print(1)
        updater = Updater(TOKEN)
        print(2)
        dp = updater.dispatcher
        print(3)
        text_handler = MessageHandler(Filters.text & ~Filters.command, self.echo)
        print(4)
        dp.add_handler(text_handler)
        print(5)
        dp.add_handler(CommandHandler("Math", self.Math))
        dp.add_handler(CommandHandler("Russian", self.Russian))
        dp.add_handler(CommandHandler("Chemistry", self.Chemistry))
        dp.add_handler(CommandHandler("Biology", self.Biology))
        dp.add_handler(CommandHandler("Geography", self.Geography))
        dp.add_handler(CommandHandler("History", self.History))


        print(6)
        # dp.add_handler(CommandHandler("help", help))
        updater.start_polling()
        print(7)
        #updater.idle()


    def Math(self, update, context):
        update.message.reply_text(
            "Ваш учебник по алгебре: https://school-textbook.com/algebra/2935-algebra-9-klass-merzljak-ag-polonskij-vb-jakir-ms.html")

        update.message.reply_text(
            "Ваш учебник по геометрии: https://ege-ok.ru/wp-content/uploads/2014/01/59_2-Geometriya.-7-9-kl.-Uchebnik_Atanasyan-L.S.-i-dr_2010-384s.pdf")

        self.Predmets(update, context)

    def Russian(self, update, context):
        update.message.reply_text(
            "Ваш учебник по русскому: https://school-textbook.com/himiya/9-klass-himiya/39992-russkij-jazyk-9-klass-uchebnik-v-2-chastjah-lvova-si-lvov-vv.html")
        self.Predmets(update, context)

    def Chemistry(self, update, context):
        update.message.reply_text(
            "Ваш учебник по химии: https://uchebnik-i-tetrad.com/1890_Chitat_onlajn_uchebnik_po_himii_za_9_klass_Rudzitis_Feldman/index.html#prettyPhoto")
        self.Predmets(update, context)

    def Biology(self, update, context):
        update.message.reply_text(
            "Ваш учебник по биологии: https://school-textbook.com/biologija/39750-biologija-vvedenie-v-obschuju-biologiju-9-klass-pasechnik-vv-kamenskij-aa-kriksunov-ea-shvecov-gg.html")
        self.Predmets(update, context)

    def Geography(self, update, context):
        update.message.reply_text(
            "Ваш атлас: https://school-textbook.com/himiya/9-klass-himiya/39918-atlas-istorija-rossii-xx-nachalo-xix-veka-9-klass.html")
        update.message.reply_text(
            "Ваш учебник по географии: https://school-textbook.com/geografiya/12505-geografija-rossii-naselenie-i-hozjajstvo-9-klass-dronov-vp-rom-vja.html"
        )
        self.Predmets(update, context)

    def History(self, update, context):
        update.message.reply_text(
            "Ваш учебник по всеобщей истории: https://school-textbook.com/vsemirnaya-istoriya/12083-vseobschaya-istoriya-xx-nachalo-xxi-veka-9-klass-aleksashkina-ln.html")
        self.Predmets(update, context)









if __name__ == '__main__':
    Menu()
    #try:
    #    Menu()
    #except Exception as e:
    #    print(e)  # или import traceback; traceback.print_exc() для печати полной инфы
    #    time.sleep(15)