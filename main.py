    def __init__(self):
        self.raspisanie = []
        reply_keyboard = [['/Time_to_end', '/Timetable'],
                          ['/Redact', '/Homework'],
                          ['/Subject', '/Repetition', '/Help']]
        redact_keyboard = [['/Redact_Timetable'],
                           ['/Back']]
        subjects_keyboard = [['/Math', '/Russian'],
                             ['/Biology', '/Chemistry'],
                             ['/Geography', '/History'],
                             ['/Back']]
        self.markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        self.markup_subj = ReplyKeyboardMarkup(subjects_keyboard, one_time_keyboard=False)
        self.markup_reda = ReplyKeyboardMarkup(redact_keyboard, one_time_keyboard=False)
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
        dp.add_handler(CommandHandler("Back", self.start))
        dp.add_handler(CommandHandler("Redact_Timetable", self.add_timetable))
        self.updater.start_polling()
        self.updater.idle()

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
            "Ля ля ля большой текст о способностях",
            reply_markup=self.markup_reda
        )

    def add_timetable(self, update, context):
        update.message.reply_text(
            "Напишите день недели")
        if update.message.text == 'Понедельник':
            print(1)
            update.message.reply_text(
                "Напишите расписание уроков, начиная с первого(если есть окно или уроки начинаются не с "
                "первого поставьте '-') в конце введите 'Готово'")
            while update.message.text != 'Готово':
                ras.append(update.message.text)
            self.raspisanie[0] = ras


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
