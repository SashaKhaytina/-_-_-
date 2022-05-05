import logging

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import time
import sqlite3

TOKEN = '5219235474:AAG4SluLc6f44WVFK8KlOnZlRkgXsEK8IJI'


class Menu:
    def __init__(self):
        self.person_id = '1'
        self.db = sqlite3.connect("info1.db")
        self.sql = self.db.cursor()
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users_Repetition(
                    id TEXT,
                    question TEXT,
                    answer TEXT)""")
        self.db.commit()
        self.db_ras = sqlite3.connect("info1.db")
        self.sql_ras = self.db_ras.cursor()
        self.sql_ras.execute("""CREATE TABLE IF NOT EXISTS users_R(
                            id TEXT,
                            raspisanie TEXT)""")
        self.db_ras.commit()
        self.db_user = sqlite3.connect("info1.db")
        self.sql_user = self.db_user.cursor()
        self.sql_user.execute("""CREATE TABLE IF NOT EXISTS users(
                                    id TEXT)""")
        self.db_user.commit()
        self.result = self.sql.execute("""SELECT * FROM users WHERE id = ?""", (self.person_id,)).fetchall()
        self.db.close()
        self.raspisanie = ['0', '0', '0', '0', '0', '0', '0']
        start_keyboard = [['/Registration']]
        reg_end_keyboard = [['/Menu']]
        reply_keyboard = [['/Time_to_end', '/Timetable'],
                          ['/Redact', '/Homework'],
                          ['/Subject', '/Repetition', '/Help']]
        redact_keyboard = [['/Redact_Timetable'],
                           ['/Back']]
        subjects_keyboard = [['/Math', '/Russian'],
                             ['/Biology', '/Chemistry'],
                             ['/Geography', '/History'],
                             ['/Back']]
        predmet_add = [['/Update', '/Back']]
        add_question_answer = [['/Input', '/Repetition_start', '/Back']]
        self.markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        self.markup_start = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)
        self.markup_end_reg = ReplyKeyboardMarkup(reg_end_keyboard, one_time_keyboard=False)
        self.markup_subj = ReplyKeyboardMarkup(subjects_keyboard, one_time_keyboard=False)
        self.markup_reda = ReplyKeyboardMarkup(redact_keyboard, one_time_keyboard=False)
        self.markup_predmet_add = ReplyKeyboardMarkup(predmet_add, one_time_keyboard=False)
        self.markup_question = ReplyKeyboardMarkup(predmet_add, one_time_keyboard=False)
        self.markup_repet = ReplyKeyboardMarkup(add_question_answer, one_time_keyboard=False)
        self.updater = Updater(TOKEN)
        dp = self.updater.dispatcher
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
        dp.add_handler(CommandHandler("Math", self.Math))
        dp.add_handler(CommandHandler("Russian", self.Russian))
        dp.add_handler(CommandHandler("Chemistry", self.Chemistry))
        dp.add_handler(CommandHandler("Biology", self.Biology))
        dp.add_handler(CommandHandler("Geography", self.Geography))
        dp.add_handler(CommandHandler("History", self.History))
        dp.add_handler(CommandHandler("Back", self.Menu))
        dp.add_handler(CommandHandler("Menu", self.Menu))
        dp.add_handler(CommandHandler("Registration", self.Registration_def))
        dp.add_handler(CommandHandler("Update", self.update))
        dp.add_handler(CommandHandler("Redact_Timetable", self.add_timetable))
        dp.add_handler(CommandHandler("Input", self.Add_answer_quest))
        dp.add_handler(CommandHandler("Repetition_start", self.Repet_formules))
        self.updater.start_polling()
        self.flag_add_timetable_day = False
        self.flag_add_timetable_predmet = False
        self.flag_add_question = False
        self.flag_add_answer = False
        self.flag_person_ans = False
        self.flag_reg = False
        self.is_answer = False
        self.ras = []
        self.days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.day = ''
        self.q_a = []
        self.i = 0
        self.sum_b = 0
        self.updater.idle()

    def echo(self, update, context):
        if update.message.text in self.days and self.flag_add_timetable_day:
            self.day = update.message.text
            self.day_add(update, self.day)
            self.flag_add_timetable_day = False
        elif self.flag_add_timetable_predmet:
            self.predmet_add(update, update.message.text)
        elif self.flag_person_ans:
            self.is_answer = True
            self.Repet_formules(update, update.message.text)
        elif self.flag_add_question:
            self.Add_answer_quest(update, update.message.text)
        elif self.flag_add_answer:
            self.Add_answer_quest(update, update.message.text)
        elif self.flag_reg:
            self.Reg(update, update.message.text)
        else:
            update.message.reply_text("Пожалуйста, введите команду\n:((")

    def day_add(self, update, day):
        update.message.reply_text(
            f"Ля ля ля, вы выбрали день {day}.Напишите расписание уроков, начиная с первого(если есть окно или"
            f" уроки начинаются не с первого отправьте '-') в конце отправьте 'Update'. выход сбросит изменения",
            reply_markup=self.markup_predmet_add
        )
        self.flag_add_timetable_predmet = True

    def predmet_add(self, update, s):
        update.message.reply_text(
            f"Ля ля ля, вы выбрали предмет {s}. продолжайте",
            reply_markup=self.markup_predmet_add
        )
        self.ras.append(update.message.text)

    def update(self, update, context):
        update.message.reply_text(
            f" вы сохранили день {self.day} за текст в сообщенях отвечаю не я))",
            reply_markup=self.markup_reda
        )
        self.flag_add_timetable_predmet = False
        self.flag_add_timetable_day = False
        self.raspisanie[self.days.index(self.day)] = "/".join(self.ras)
        self.db_ras = sqlite3.connect("info1.db")
        self.sql_ras = self.db_ras.cursor()
        self.sql_ras.execute(f"""INSERT INTO users_R (id, raspisanie) VALUES 
                                    ('{self.person_id}', '{'razdel'.join(self.raspisanie)}')""")
        self.db_ras.commit()
        self.db_ras.close()
        self.ras = []
        self.day = ''

    def start(self, update, context):
        update.message.reply_text(
            "Ля ля ля большой ВСТУПИТЕЛЬНЫЙ текст и просьба зарегаться",
            reply_markup=self.markup_start
        )

    def Menu(self, update, context):
        update.message.reply_text(
            " Приветствие Ля ля ля большой текст о способностях",
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

    def Registration_def(self, update, context):
        update.message.reply_text(
            "Введите ник")
        self.flag_reg = True

    def Reg(self, update, text):
        con = sqlite3.connect("info1.db")
        cur = con.cursor()
        otvet = cur.execute('''SELECT id FROM users''').fetchall()
        if otvet != []:
            if text in otvet[0]:
                update.message.reply_text(
                    "Ник занят, введите другой")
            else:
                self.person_id = text
                db = sqlite3.connect("info1.db")
                sql = db.cursor()
                sql.execute(f"""INSERT INTO users (id) VALUES 
                                            ('{self.person_id}')""")
                db.commit()
                update.message.reply_text(
                    f"Вы зарегестрировались под ником {text}", reply_markup=self.markup_end_reg)
                self.flag_reg = False
        else:
            self.person_id = text
            db = sqlite3.connect("info1.db")
            sql = db.cursor()
            sql.execute(f"""INSERT INTO users (id) VALUES 
                                                        ('{self.person_id}')""")
            db.commit()
            update.message.reply_text(
                f"Вы зарегестрировались под ником {text}", reply_markup=self.markup_end_reg)
            self.flag_reg = False

    def Timetable_def(self, update, context):
        update.message.reply_text(
            "Выдаёт расписание: всё, по дню недели, числу"
            "Проверить наличие дз на число")
        con = sqlite3.connect("info1.db")
        cur = con.cursor()
        otvet = cur.execute('''SELECT raspisanie FROM users_R WHERE id IS (?)''', (self.person_id, )).fetchall()
        sms = otvet[0][0].split('razdel')
        for i in range(len(sms)):
            s = str(self.days[i]) + ': \n' + str("\n".join(sms[i].split('/')))
            update.message.reply_text(s)
        con.close()

    def Time_to_end_def(self, update, context):
        update.message.reply_text("Предлагает выбрать: до конца года(установленное значение), до введённой даты "
                                  "АЙПИ ссылка на официальный сайт МИНобразования")

    def Redact_def(self, update, context):
        update.message.reply_text(
            "Ля ля ля большой текст о способностях",
            reply_markup=self.markup_reda
        )

    def add_timetable(self, update, context):
        update.message.reply_text(
            "Напишите день недели")
        self.flag_add_timetable_day = True

    def Homework_def(self, update, context):
        update.message.reply_text(
            "Спрашивает число предмет, если в тот день нет данного предмета"
            " предупреждает и предлагает перенести на ближайшее число ")

    def Repetition_def(self, update, context):
        update.message.reply_text(
            "Предлагает записать вопросы в виде вопрос-ответ, или же повторить формулы"
            " (берет из БД в зависимости от класса человека)"
            "Далее выдаёт по одному вопросы и считает результат в процентах",
            reply_markup=self.markup_repet
        )

    def Add_answer_quest(self, update, text):
        if self.flag_add_question is False and self.flag_add_answer is False:
            update.message.reply_text(
                "Введите вопрос")
            self.flag_add_question = True
        elif self.flag_add_question:
            self.q_a.append(text)
            self.flag_add_question = False
            update.message.reply_text(
                "Введите ответ")
            self.flag_add_answer = True
        else:
            self.q_a.append(text)
            self.flag_add_answer = False
            self.db = sqlite3.connect("info1.db")
            self.sql = self.db.cursor()
            self.sql.execute(f"""INSERT INTO users_Repetition (id, question, answer) VALUES 
                            ('{self.person_id}', '{self.q_a[0]}', '{self.q_a[1]}')""")
            self.db.commit()
            self.result = self.sql.execute("""SELECT * FROM users_Repetition WHERE id = ?""", (self.person_id,)).fetchall()
            self.db.close()
            self.q_a = []

    def Repet_formules(self, update, context):
        if self.i < len(self.result):
            if self.flag_person_ans is False:
                update.message.reply_text(
                    str(self.result[self.i][1])
                )
                update.message.reply_text(
                    "Введите ответ"
                )
                self.flag_person_ans = True
            elif self.is_answer is True:
                if context.lower() == self.result[self.i][2].lower():
                    update.message.reply_text(
                        "Правильный ответ!")
                    if self.i + 1 < len(self.result):
                        update.message.reply_text(
                            "Продолжаем...")
                    else:
                        update.message.reply_text(
                            "Подсчет результатов...")
                    self.sum_b += 1
                else:
                    update.message.reply_text(
                        "Неравильный ответ!")
                    update.message.reply_text(
                        f"Ответ: {str(self.result[self.i][2])}")
                    if self.i + 1 < len(self.result):
                        update.message.reply_text(
                            "Продолжаем...")
                    else:
                        update.message.reply_text(
                            "Подсчет результатов...")
                self.i += 1
                self.flag_person_ans = False
                self.is_answer = False
                self.Repet_formules(update, context)
        else:
            update.message.reply_text(
                "Тест закончен!"
                f"Вы получили {str(self.sum_b)} из {str(len(self.result))}!")
            self.i = 0
            self.sum_b = 0

    def Subject_def(self, update, context):
        update.message.reply_text(
            "Ля",
            reply_markup=self.markup_subj
        )

    def Math(self, update, context):
        update.message.reply_text(
            "Ваш учебник по алгебре: https://school-textbook.com/algebra/2935-algebra-9-klass-merzljak-ag-polonskij-vb-jakir-ms.html")

        update.message.reply_text(
            "Ваш учебник по геометрии: https://ege-ok.ru/wp-content/uploads/2014/01/59_2-Geometriya.-7-9-kl.-Uchebnik_Atanasyan-L.S.-i-dr_2010-384s.pdf")

    def Russian(self, update, context):
        update.message.reply_text(
            "Ваш учебник по русскому: https://school-textbook.com/himiya/9-klass-himiya/39992-russkij-jazyk-9-klass-uchebnik-v-2-chastjah-lvova-si-lvov-vv.html")

    def Chemistry(self, update, context):
        update.message.reply_text(
            "Ваш учебник по химии: https://uchebnik-i-tetrad.com/1890_Chitat_onlajn_uchebnik_po_himii_za_9_klass_Rudzitis_Feldman/index.html#prettyPhoto")

    def Biology(self, update, context):
        update.message.reply_text(
            "Ваш учебник по биологии: https://school-textbook.com/biologija/39750-biologija-vvedenie-v-obschuju-biologiju-9-klass-pasechnik-vv-kamenskij-aa-kriksunov-ea-shvecov-gg.html")

    def Geography(self, update, context):
        update.message.reply_text(
            "Ваш атлас: https://school-textbook.com/himiya/9-klass-himiya/39918-atlas-istorija-rossii-xx-nachalo-xix-veka-9-klass.html")
        update.message.reply_text(
            "Ваш учебник по географии: https://school-textbook.com/geografiya/12505-geografija-rossii-naselenie-i-hozjajstvo-9-klass-dronov-vp-rom-vja.html"
        )

    def History(self, update, context):
        update.message.reply_text(
            "Ваш учебник по всеобщей истории: https://school-textbook.com/vsemirnaya-istoriya/12083-vseobschaya-istoriya-xx-nachalo-xxi-veka-9-klass-aleksashkina-ln.html")


if __name__ == '__main__':
    Menu()
