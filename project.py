from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import time
from random import shuffle
import sqlite3
import datetime as dt


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
        self.raspisanie = '0razdel0razdel0razdel0razdel0razdel0razdel0'
        if len(self.result) > 0:
            shuffle(self.result)
        self.db.close()
        self.raspisanie = [0, 0, 0, 0, 0, 0, 0]
        reply_keyboard = [['/Time_to_end', '/Timetable'],
                          ['/Redact', '/Subject'],
                          ['/Repetition', '/Help']]
        redact_keyboard = [['/Redact_Timetable'],
                           ['/Back']]
        subjects_keyboard = [['/Math', '/Russian'],
                             ['/Biology', '/Chemistry'],
                             ['/Geography', '/History'],
                             ['/Back']]
        timetable_keyboard = [['/To_Day'], ['/To_Week'],
                              ['/Back']]
        predmet_add = [['/Update', '/Back']]
        add_question_answer = [['/Input', '/Repetition_start', '/Delete_test', '/Back']]
        time_to_end = [['/End_of_the_Year', '/Your_data', '/Back']]

        self.markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        self.markup_subj = ReplyKeyboardMarkup(subjects_keyboard, one_time_keyboard=False)
        self.markup_reda = ReplyKeyboardMarkup(redact_keyboard, one_time_keyboard=False)
        self.markup_predmet_add = ReplyKeyboardMarkup(predmet_add, one_time_keyboard=False)
        self.markup_question = ReplyKeyboardMarkup(predmet_add, one_time_keyboard=False)
        self.markup_repet = ReplyKeyboardMarkup(add_question_answer, one_time_keyboard=False)
        self.markup_timetable = ReplyKeyboardMarkup(timetable_keyboard, one_time_keyboard=False)
        self.markup_time_to_end = ReplyKeyboardMarkup(time_to_end, one_time_keyboard=False)
        self.updater = Updater(TOKEN)
        dp = self.updater.dispatcher
        text_handler = MessageHandler(Filters.text & ~Filters.command, self.echo)
        dp.add_handler(text_handler)
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("Time_to_end", self.Time_to_end_def))
        dp.add_handler(CommandHandler("Your_data", self.Until_your_data))
        dp.add_handler(CommandHandler("End_of_the_Year", self.Until_end))
        dp.add_handler(CommandHandler("Timetable", self.Timetable_def))
        dp.add_handler(CommandHandler("Redact", self.Redact_def))
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
        dp.add_handler(CommandHandler("Back", self.start))
        dp.add_handler(CommandHandler("Update", self.update))
        dp.add_handler(CommandHandler("Redact_Timetable", self.add_timetable))
        dp.add_handler(CommandHandler("Input", self.Add_answer_quest))
        dp.add_handler(CommandHandler("Delete_test", self.Delete_test))
        dp.add_handler(CommandHandler("Repetition_start", self.Repet_formules))
        dp.add_handler(CommandHandler("To_Day", self.day_def))
        dp.add_handler(CommandHandler("To_Week", self.week_def))
        self.updater.start_polling()
        self.flag_add_timetable_day = False
        self.flag_add_timetable_predmet = False
        self.flag_add_question = False
        self.flag_add_answer = False
        self.flag_person_ans = False
        self.is_answer = False
        self.ask_for_homework = False
        self.ask_for_homework2 = False
        self.flag_day = False
        self.flag_agree_to_delete = False
        self.flag_until_your_data = False
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
        elif self.flag_day and update.message.text in self.days:
            self.flag_day = False
            self.day_info(update, update.message.text)
        elif self.flag_agree_to_delete:
            self.is_answer = True
            self.Delete_test(update, update.message.text)
        elif self.flag_until_your_data:
            self.is_answer = True
            self.Until_your_data(update, update.message.text)
        else:
            update.message.reply_text("Пожалуйста, введите команду\n:((")

    def day_add(self, update, day):
        update.message.reply_text(
            f"Ля ля ля, вы выбрали день {day}.Напишите расписание уроков, начиная с первого(если есть окно или"
            f" уроки начинаются не с первого отправьте '-') в конце отправьте 'Update'. выход сбросит изменения",
            reply_markup=self.markup_predmet_add
        )
        self.flag_add_timetable_predmet = True

    def day_info(self, update, day):
        con = sqlite3.connect("info1.db")
        cur = con.cursor()
        otvet = cur.execute('''SELECT raspisanie FROM users_R WHERE id IS (?)''', (self.person_id,)).fetchall()
        print(self.person_id, otvet)
        sms = otvet[0][0].split('razdel')
        i = self.days.index(day)
        s = str(self.days[i]) + ': \n' + str("\n".join(sms[i].split('/')))
        update.message.reply_text(s, reply_markup=self.markup_timetable)
        con.close()

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
        self.raspisanie[self.days.index(self.day)] = self.ras
        self.ras = []
        self.day = ''

    def week_def(self, update, context):
        con = sqlite3.connect("info1.db")
        cur = con.cursor()
        otvet = cur.execute('''SELECT raspisanie FROM users_R WHERE id IS (?)''', (self.person_id,)).fetchall()
        print(self.person_id, otvet)
        sms = otvet[0][0].split('razdel')
        for i in range(len(sms)):
            s = str(self.days[i]) + ': \n' + str("\n".join(sms[i].split('/')))
            update.message.reply_text(s, reply_markup=self.markup_timetable)
        con.close()

    def day_def(self, update, context):
        update.message.reply_text("Введите день недели", reply_markup=self.markup_timetable)
        self.flag_day = True

    def start(self, update, context):
        update.message.reply_text(
            "Добро пожаловать в телеграмм-бот 'Школьный помощник'! "
            "Наш бот создан для того чтобы помогать детям учиться и "
            "организовывать домашнее задание, материалы и учебники."
            "Здесь вы сможете не только весело провести время, посмотреть количество оставшихся учебных дней, "
            "быстро найти все свои учебники и домашнее задание, "
            "но и сможете потренироваться создавая собственные тесты и потом проверяя по ним знания!"
            "Надеемся, что наш бот будт вам полезным!"
        )
        update.message.reply_text(
            "Правила бота:"
            "Внимательно читайте все, что пишет вам бот, это поможет не допускать ошибки."
            "Если у вас возникли проблемы, то нажмите на кнопку '/Help', "
            "там вы сможете найти более подробное описание всех кнопок и функций."
            "'/Back' будет возвращать вас назад, поэтому если вы хотите вернуться в предыдущее окно, то нажмите на нее."
            "Большинство кнопок имеют названия, связанные с функциями бота, за которые они отвечают."
            "Не волнуйтесь, даже если случайно нажали не туда, "
            "чаще всего бот будет запрашивать повторное согласие на удаление "
            "или изменение какой-либо информации или данных."
            "Удачи!",
            reply_markup=self.markup
        )

    def close_keyboard(self, update, context):
        update.message.reply_text(
            "Ok",
            reply_markup=ReplyKeyboardRemove()
        )

    def help(self, update, context):
        update.message.reply_text(
            "Если вам нужна помощь по работе с ботом, "
            "то прочитайте последующую инструкцию, возможна она сможет помочь вам решить вашу проблему.\n"
            ""
            "1. Если внизу экрана появились кнопки, то не стоит ничего писать боту, "
            "кроме случаев когда он просит ввести текст, сообщение с просьбой вы увидите во входящих сообщениях.\n"
            "2.Кнопка Back отвечает за возврат на предыдущее меню, "
            "поэтому дочитав эту инструкцию или доработав с ботом, вы можете вернуться нажам в на кнопку.\n"
            "3.Основное меню и его кнопки:\n"
            "Time_to_end - расскажет сколько времени осталось учиться на выбор: по введенной дате или до конца года.\n"
            "Timetable - Здесь вы сможете посмотреть свое расписание по дню недели, числу.\n"
            "Redact - Здесь вы сможете изменюить некоторую свою информацию. Например, расписание.\n"
            "Homework - Здесь вы сможете ввести домашнее задание на определенный день и предмет.\n"
            "Subject - Здесь вы сможете быстро получить ссылки на учебники по вашим предметам.\n"
            "Repetition - Здесь вы сможете сделать тест, "
            "а потом проверить себя же на своих вопросах, "
            "и таким образом закрепить материал или подготовиться к контрольной.\n"
            "Help - Сейчас вы находитесь здесь.")

    def Timetable_def(self, update, context):
        update.message.reply_text(
            "Выдаёт расписание: всё, по дню недели, числу"
            "Проверить наличие дз на число", reply_markup=self.markup_timetable)
        con = sqlite3.connect("info1.db")
        cur = con.cursor()
        otvet = cur.execute('''SELECT raspisanie FROM users_R WHERE id IS (?)''', (self.person_id,)).fetchall()
        print(self.person_id, otvet)
        sms = otvet[0][0].split('razdel')
        for i in range(len(sms)):
            s = str(self.days[i]) + ': \n' + str("\n".join(sms[i].split('/')))
            update.message.reply_text(s)
        con.close()

    def Time_to_end_def(self, update, context):
        update.message.reply_text("Здесь вы можете посмотреть сколько осталось дней до конца года или лета."
                                  "Или до введенной даты",
                                  reply_markup=self.markup_time_to_end)

    def Until_your_data(self, update, context):
        if self.is_answer is False:
            update.message.reply_text("Здесь вы можете посмотреть сколько осталось дней до введенной даты."
                                      "Введите дату (ДД.ММ.ГГГГ)")
            self.flag_until_your_data = True
        else:
            self.text = context.split('.')
            if len(self.text) < 2:
                update.message.reply_text("Вы неправильно ввели дату!"
                                          "Введите дату (пример: 23.09.2006).")
                self.flag_until_your_data = True
                self.is_answer = False
            elif context.count('.') != 2 or len(context) != 10:
                update.message.reply_text("Вы неправильно ввели дату!"
                                          "Введите дату (пример: 23.09.2006).")
                self.flag_until_your_data = True
                self.is_answer = False
            else:
                if self.text[0].isdigit() and self.text[1].isdigit() and self.text[2].isdigit():
                    your_date = dt.date(int(self.text[2]), int(self.text[1]), int(self.text[0]))
                    now_date = dt.date.today()
                    if your_date > now_date:
                        update.message.reply_text(f"До {context} осталось {(your_date - now_date).days} days!")
                    self.flag_until_your_data = True
                    self.is_answer = False
                else:
                    update.message.reply_text("Вы неправильно ввели дату!"
                                              "Введите дату (пример: 23.09.2006).")
                    self.flag_until_your_data = True
                    self.is_answer = False

    def Until_end(self, update, context):
        now_date = dt.date.today()
        a = now_date.year + 1 if now_date.month > 8 else now_date.year
        your_date = dt.date(a, 5, 31)
        if 5 < your_date.month < 9:
            your_date = dt.date(now_date.year, 8, 31)
            update.message.reply_text(f"До конца лета осталось {(your_date - now_date).days} days!")
        else:
            update.message.reply_text(f"До конца года осталось {(your_date - now_date).days} days!")

    def Redact_def(self, update, context):
        update.message.reply_text(
            "Тут можно изменить рассписание",
            reply_markup=self.markup_reda
        )

    def add_timetable(self, update, context):
        update.message.reply_text(
            "Напишите день недели")
        self.flag_add_timetable_day = True

    def Repetition_def(self, update, context):
        update.message.reply_text(
            "Здесь вы моежет создать свой собственный тест(кнопка Input), "
            "а потом потренироваться(кнопка Repetition_start) и сразу увидеть резульатат"
            "А также удалить свой предыдущий тест(кнопка Delete_test)",
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
            if len(self.result) > 0:
                shuffle(self.result)
            self.db.close()
            self.q_a = []
            update.message.reply_text(
                "Ваш вопрос записан! Чтобы добавить новый вопрос, нажмите на кнопку Input")

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
            shuffle(self.result)
            self.is_answer = False

    def Delete_test(self, update, context):
        if self.is_answer is False:
            update.message.reply_text(
                "Здесь вы можете удалить свой старый тест. "
                "Напишите 'Да', если согласны, и любое другое слово, если хотите отменить удаление")
            self.flag_agree_to_delete = True
        else:
            if context == 'Да':
                self.flag_agree_to_delete = False
                self.result.clear()
                self.db = sqlite3.connect("info1.db")
                self.sql = self.db.cursor()
                self.sql.execute(f"""DELETE from users_Repetition where id = '{self.person_id}'""")
                self.db.commit()
                self.db.close()
                update.message.reply_text(
                    "Ваш тест удален! Вы можете составить новый тест")
            else:
                self.flag_agree_to_delete = False
                update.message.reply_text(
                    "Ваш тест не был удален!")
            self.is_answer = False

    def Subject_def(self, update, context):
        update.message.reply_text(
            "Здесь вы можете получить ссылки на учебники, для этого нажмите на кнопку с нужным предметом",
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