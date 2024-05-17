import datetime
from tkinter import *
from tkinter import messagebox
import tkinter.simpledialog as tksd
import gui_script
import db
from tkcalendar import Calendar
month_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
           'июлЬ', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

class App:
    def __init__(self, root=None):
        # параметры приложения
        self.root = root
        self.root.minsize(600, 300)
        self.root.maxsize(600, 300)
        self.root.title("Учёт собственных средств")
        self.main_font = ("Calibri", 30)
        self.sec_font = ("Calibri", 15)
        self._setup_grid()
        self._setup_menu()
        # рамка, в которую помещается главная страничка
        self.frame = Frame(self.root)
        self.frame.pack()
        # главная страничка
        self._setup_main_page()

    def _setup_main_page(self):
        self.page1 = SpendPage(master=self.root, app=self)
        self.page2 = GainPage(master=self.root, app=self)
        self.page3 = CategPage(master=self.root, app=self)

        self.totalVAR = DoubleVar()
        self.gainsVAR = DoubleVar()
        self.spendingsVAR = DoubleVar()

        Label(self.frame, text='Баланс: ', font=self.main_font).grid(row=0, column=0, sticky=W, ipady=30)

        self._setup_labels()
        self.button_frame = Frame(self.frame)
        self.button_frame.grid(row=3, columnspan=3, sticky=W, pady=5)
        Button(self.button_frame, text='К тратам', command=lambda: self.make_page(self.page1), width=15).grid(row=3, column=0, padx=5)
        Button(self.button_frame, text='К доходам', command=lambda: self.make_page(self.page2), width=15).grid(row=3, column=1, padx=5)
        Button(self.button_frame, text='К категориям', command=lambda: self.make_page(self.page3), width=15).grid(row=3, column=2, padx=5)

    def _setup_labels(self):
        Label(self.frame, textvariable=self.totalVAR, font=self.main_font).grid(row=0, column=1)
        f_stats = Frame(self.frame)
        f_stats.grid(sticky=NW, rowspan=2, columnspan=2, pady=20)

        f_gains = Frame(f_stats)
        f_gains.grid(sticky=W, row=0, columnspan=2)
        Label(f_gains, text=f"Доходы за месяц {month_list[datetime.date.today().month - 1]}:", font=self.sec_font).grid(row=0, column=0)
        Label(f_gains, textvariable=self.gainsVAR, font=self.sec_font).grid(row=0, column=1)

        f_spendings = Frame(f_stats)
        f_spendings.grid(sticky=W, row=1, columnspan=2)
        Label(f_spendings, text=f"Траты за месяц {month_list[datetime.date.today().month - 1]}:", font=self.sec_font).grid(row=0, column=0)
        Label(f_spendings, textvariable=self.spendingsVAR, font=self.sec_font).grid(row=0, column=1)

    def _setup_grid(self):
        for i in range(4):
            self.root.rowconfigure(index=i, weight=1)
            self.root.columnconfigure(index=i, weight=1)

    def _setup_menu(self):
        self.root.option_add("*tearOff", FALSE)
        # подменю "файл"
        file_menu = Menu()
        file_menu.add_command(label="Выйти", command=self._exit_app)
        # основное меню
        main_menu = Menu()
        main_menu.add_cascade(label="Файл", menu=file_menu)
        main_menu.add_command(label="Справка", command=self._show_info)
        self.root.config(menu=main_menu)

    @staticmethod
    def _show_info():
        messagebox.showinfo("Учёт собственных денежных средств", "Автор: Крестьянова Елизавета\nВерсия 2024.05.17")

    def _exit_app(self):
        self.root.destroy()

    def main_page(self):
        self.frame.pack()

    def make_page(self, page):  # переключить на другие страницы
        self.frame.pack_forget()
        page.start_page()


class SecPage:
    def __init__(self, master=None, app=None, dialogue_window=None, title="", dbtable=None):
        self.main_font = ("Calibri", 15)
        self.sec_font = ("Calibri", 10)
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        self.Dialogue = dialogue_window
        self.dbtable = dbtable
        Label(self.frame, text=title, font=self.main_font).grid(row=0, columnspan=6)
        self._setup_buttons()
        self._setup_listbox()

    def _setup_buttons(self):
        self.frame_buttons = Frame(self.frame)
        self.frame_buttons.grid(row=1, rowspan=4, column=0, sticky=NW, padx=10)
        self.add = Button(self.frame_buttons, text="+", command=self.add, width=2, font=self.sec_font)
        self.add.grid(row=0, column=0, ipady=3, pady=3, sticky=N)
        self.remove = Button(self.frame_buttons, text="-", command=self.remove, width=2, font=self.sec_font)
        self.remove.grid(row=1, column=0, ipady=3, pady=3)
        self.remove = Button(self.frame_buttons, text="Ф", command=self.filt, width=2, font=self.sec_font)
        self.remove.grid(row=2, column=0, ipady=3, pady=3)
        self.remove = Button(self.frame_buttons, text="С", command=self.sort, width=2, font=self.sec_font)
        self.remove.grid(row=3, column=0, ipady=3, pady=3, sticky=S)
        Button(self.frame, text='На главную страницу', command=self.go_back).grid(row=2, columnspan=6, pady=5)

    def _setup_listbox(self):
        self.frame_list = Frame(self.frame)
        self.frame_list.grid(row=1, column=1)
        self.scrollbar = Scrollbar(self.frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.frame_list, background="#fff", yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT, fill=Y)
        self.listbox.config(width=50, height=10)
        self.scrollbar.config(command=self.listbox.yview)

    def add(self):
        pass

    def remove(self):
        pass

    def filt(self):
        var = self.Dialogue(self.master)
        data = self.dbtable.get_all_filter(var.result)
        self.fill(data)

    def sort(self):
        pass

    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data) - 1, -1, -1):
            self.listbox.insert(END, data[i])


class SpendPage(SecPage):
    def __init__(self, master=None, app=None):
        self.asks_for = "Введите ID"
        super().__init__(master, app, SpendDialog, "Траты", db.Spendings)

    def add(self):
        var_spending = self.Dialogue(self.master)
        result = gui_script.add_spending(var_spending.result)
        if result == True:
            data = db.Spendings.get_all()
            self.fill(data)
        elif result == "EXIT":
            return
        elif result == "ERR_empty":
            messagebox.showerror("Ошибка (траты)", "Строки не должны быть пустыми!")
        elif result == "ERR_value":
            messagebox.showerror("Ошибка (траты)", "Стоимость должна быть положительным числом меньше 10^9!")
        elif result == "ERR_toolong":
            messagebox.showerror("Ошибка (траты)", "Название траты слишком длинное!")
        elif not result:
            messagebox.showerror("Ошибка (траты)", "Ошибка при добавлении траты!")

    def remove(self):
        selection = self.listbox.curselection()
        if selection:
            var = self.listbox.selection_get()
            var = var[0:var.find(" ")]
        else:
            return
        gui_script.remove_spending(var)
        data = db.Spendings.get_all()
        self.fill(data)

    def sort(self):
        data = db.Spendings.get_all()
        print(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data) - 1, -1, -1):
            ins = [str(data[i][0]), str(data[i][1]), data[i][2], str(data[i][3]), data[i][4].strftime('%d/%m/%Y')]
            self.listbox.insert(END, " ".join(ins))


class GainPage(SecPage):
    def __init__(self, master=None, app=None):
        self.asks_for = "Введите ID"
        super().__init__(master, app, GainDialog, "Доходы", db.Gains)

    def add(self):
        var_gain = self.Dialogue(self.master)
        result = gui_script.add_gain(var_gain.result)
        if result == True:
            data = db.Gains.get_all()
            self.fill(data)
        elif result == "EXIT":
            return
        elif result == "ERR_empty":
            messagebox.showerror("Ошибка (доходы)", "Строки не должны быть пустыми!")
        elif result == "ERR_value":
            messagebox.showerror("Ошибка (доходы)", "Стоимость должна быть положительным числом меньше 10^9!")
        elif result == "ERR_toolong":
            messagebox.showerror("Ошибка (доходы) ", "Название дохода слишком длинное!")
        elif not result:
            messagebox.showerror("Ошибка (доходы)", "Ошибка при добавлении дохода!")

    def remove(self):
        selection = self.listbox.curselection()
        if selection:
            var = self.listbox.selection_get()
            var = var[0:var.find(" ")]
        else:
            return
        gui_script.remove_gain(var)
        data = db.Gains.get_all()
        self.fill(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data) - 1, -1, -1):
            ins = [str(data[i][0]), str(data[i][1]), str(data[i][2]), data[i][3].strftime('%d/%m/%Y')]
            self.listbox.insert(END, " ".join(ins))


class CategPage(SecPage):
    def __init__(self, master=None, app=None):
        self.asks_for = "Введите название категории"
        super().__init__(master, app, CategDialog, "Категории", db.Categories)
        self.listbox.config(width=15)

    def add(self):
        var_category = self.Dialogue(self.master)
        result =  gui_script.add_category(var_category.result)
        if result == True:
            data = db.Categories.get_all()
            self.fill(data)
        elif result == "ERR_exists":
            messagebox.showinfo("Ошибка (категории)", "Категория уже существует.")
        elif result == "ERR_toolong":
            messagebox.showerror("Ошибка (категории)", "Слишком длинное имя категории!")
        elif result == "EXIT":
            return
        else:
            messagebox.showerror("Ошибка (категории)", "Ошибка при добавлении категории...")

    def remove(self):
        selection = self.listbox.curselection()
        if selection:
            var = self.listbox.selection_get()
        else:
            messagebox.showerror("Ошибка (категории)", "Выберите строку на удаление!")
            return
        gui_script.remove_category(var)
        data = db.Categories.get_all()
        self.fill(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data) - 1, -1, -1):
            self.listbox.insert(END, data[i])


class SpendDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Название:").grid(row=0)
        Label(master, text="Категория:").grid(row=1)
        Label(master, text="Стоимость:").grid(row=2)
        Label(master, text="Дата:").grid(row=3)
        self.e1 = Entry(master)
        self._setup_listbox(master)  # self.e2
        self.e3 = Entry(master)
        self.e4 = Calendar(master, selectmode='day',
                           year=datetime.date.today().year, month=datetime.date.today().month)
        self.e1.grid(row=0, column=1, sticky=W)
        self.e3.grid(row=2, column=1, sticky=W)
        self.e4.grid(row=3, column=1, sticky=W)

        self.e1.config(width=29)
        self.e3.config(width=29)

        return self.e1  # initial focus

    def _setup_listbox(self, master):
        self.frame_list = Frame(master)
        self.frame_list.grid(row=1, column=1, sticky=W)
        self.scrollbar = Scrollbar(self.frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.e2 = Listbox(self.frame_list, background="#fff", yscrollcommand=self.scrollbar.set)
        self.e2.pack(side=LEFT, fill=Y)
        self.e2.config(width=29, height=10)
        self.scrollbar.config(command=self.e2.yview)
        categories = db.Categories.get_all()
        for category in categories:
            self.e2.insert(END, category)

    def apply(self):
        first = self.e1.get()
        selection = self.e2.curselection()
        if selection:
            second = self.e2.selection_get()
        else:
            second = ""
        third = self.e3.get()
        fourth = self.e4.selection_get()
        self.result = [first, second, third, fourth]


class GainDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Название:").grid(row=0)
        Label(master, text="Стоимость:").grid(row=1)
        Label(master, text="Дата:").grid(row=2)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Calendar(master, selectmode='day',
                           year=datetime.date.today().year, month=datetime.date.today().month)

        self.e1.grid(row=0, column=1, sticky="W")
        self.e2.grid(row=1, column=1, sticky="W")
        self.e3.grid(row=2, column=1, sticky="W")

        self.e1.config(width=29)
        self.e2.config(width=29)

        return self.e1  # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        third = self.e3.selection_get()
        self.result = [first, second, third]


class CategDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Название:").grid(row=0)
        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.e1.config(width=50)
        return self.e1  # initial focus

    def apply(self):
        first = self.e1.get()
        self.result = first




