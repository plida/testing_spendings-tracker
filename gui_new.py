import datetime
import tkinter
from tkinter import *
from tkinter import messagebox
import tkinter.simpledialog as tksd
import gui_script
import db
from tkcalendar import Calendar


class Config(Toplevel):
    def __init__(self, main):
        Toplevel.__init__(self)


class App:
    def __init__(self, root=None):
        self.root = root
        root.minsize(500, 500)
        self.main_font = ("Calibri", 25)
        self.sec_font = ("Calibri", 15)

        self.frame = Frame(self.root)
        self.frame.pack()
        self._setup_grid()
        self._setup_menu()
        self.page1 = SpendPage(master=self.root, app=self)
        self.page3 = GainPage(master=self.root, app=self)
        self.page2 = CategPage(master=self.root, app=self)

        self.totalVAR = DoubleVar()
        self.salaryVAR = DoubleVar()
        self.spendingsVAR = DoubleVar()

        Label(self.frame, text='Учёт собственных денежных средств').grid(row=0, columnspan=6)
        self._setup_labels()
        Button(self.frame, text='К тратам', command=self.make_page1).grid(row=6, column=0)
        Button(self.frame, text='К прибыли', command=self.make_page3).grid(row=6, column=1)
        Button(self.frame, text='К категориям', command=self.make_page2).grid(row=6, column=2)

    def _setup_grid(self):
        for i in range(6):
            self.root.rowconfigure(index=i, weight=1)
        for i in range(6):
            self.root.columnconfigure(index=i, weight=1)

    def _setup_menu(self):
        self.root.option_add("*tearOff", FALSE)
        main_menu = Menu()
        file_menu = Menu()
        file_menu.add_command(label="Выйти", command=self._exit_app)
        main_menu.add_cascade(label="Файл", menu=file_menu)
        main_menu.add_command(label="Справка", command=_show_info)
        self.root.config(menu=main_menu)

    def _setup_labels(self):
        Label(self.frame, textvariable=self.totalVAR, background="#fdd", font=self.main_font).grid(row=2, columnspan=4,
                                                                                                   ipady=30, ipadx=30)
        f_stats = Frame(self.frame)
        f_stats.grid(sticky=W, rowspan=2, columnspan=2, pady=50)

        f_salary = Frame(f_stats)
        f_salary.grid(sticky=W, row=0, columnspan=2)
        Label(f_salary, text="Доходы за месяц:", font=self.sec_font).grid(row=0, column=0)
        Label(f_salary, textvariable=self.salaryVAR, font=self.sec_font).grid(row=0, column=1)

        f_spendings = Frame(f_stats)
        f_spendings.grid(sticky=W, row=1, columnspan=2)
        Label(f_spendings, text="Расходы за месяц:", font=self.sec_font).grid(row=0, column=0)
        Label(f_spendings, textvariable=self.spendingsVAR, font=self.sec_font).grid(row=0, column=1)

    def _exit_app(self):
        self.root.destroy()

    def main_page(self):
        self.frame.pack()

    def make_page1(self):
        self.frame.pack_forget()
        self.page1.start_page()

    def make_page2(self):
        self.frame.pack_forget()
        self.page2.start_page()

    def make_page3(self):
        self.frame.pack_forget()
        self.page3.start_page()


class SecPage:
    def __init__(self, master=None, app=None, dialogue_window=None, title="", dbtable=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        self.Dialogue = dialogue_window

        Label(self.frame, text=title).grid(row=0, columnspan=6)
        self.dbtable = dbtable
        self.frame_buttons = Frame(self.frame)
        self.frame_buttons.grid(rowspan=3, column=0)
        self.add = Button(self.frame_buttons, text="+", command=self.add)
        self.add.grid(row=0, column=0)
        self.remove = Button(self.frame_buttons, text="-", command=self.remove)
        self.remove.grid(row=1, column=0)
        self.remove = Button(self.frame_buttons, text="F", command=self.filt)
        self.remove.grid(row=2, column=0)

        self.frame_list = Frame(self.frame)
        self.frame_list.grid(row=1, column=1)
        self.scrollbar = Scrollbar(self.frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.frame_list, background="#fff", yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT, fill=Y)
        self.listbox.config(width=50, height=20)
        self.scrollbar.config(command=self.listbox.yview)

        Button(self.frame, text='На главную страницу', command=self.go_back).grid(row=2, columnspan=6)

    def filt(self):
        var = self.Dialogue(self.master)
        data = self.dbtable.get_all_filter(var.result)
        self.fill(data)

    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data) - 1, -1, -1):
            self.listbox.insert(END, data[i])

    def remove(self):
        pass

    def add(self):
        pass


class SpendPage(SecPage):
    def __init__(self, master=None, app=None):
        self.asks_for = "Введите ID"
        super().__init__(master, app, SpendDialog, "Траты", db.Spendings)

    def add(self):
        var_spending = self.Dialogue(self.master)
        gui_script.add_spending(var_spending.result)
        data = db.Spendings.get_all()
        self.fill(data)

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

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data) - 1, -1, -1):
            ins = [str(data[i][0]), str(data[i][1]), data[i][2], str(data[i][3]), data[i][4].strftime('%d/%m/%Y')]
            self.listbox.insert(END, " ".join(ins))


class GainPage(SecPage):
    def __init__(self, master=None, app=None):
        self.asks_for = "Введите ID"
        super().__init__(master, app, GainDialog, "Прибыль", db.Gains)

    def add(self):
        var_gain = self.Dialogue(self.master)
        gui_script.add_gain(var_gain.result)
        data = db.Gains.get_all()
        self.fill(data)

    def remove(self):
        selection = self.listbox.curselection()
        if selection:
            var = self.listbox.selection_get()
            var = var[0:var.find(" ")]
        else:
            return
        print(var)
        gui_script.remove_gain(var)
        data = db.Gains.get_all()
        self.fill(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data)-1, -1, -1):
            ins = [str(data[i][0]), str(data[i][1]), str(data[i][2]), data[i][3].strftime('%d/%m/%Y')]
            self.listbox.insert(END, " ".join(ins))


class CategPage(SecPage):
    def __init__(self, master=None, app=None):
        self.asks_for = "Введите название категории"
        super().__init__(master, app, CategDialog, "Категории", db.Categories)

    def add(self):
        var_category = self.Dialogue(self.master)
        gui_script.add_category(var_category.result)
        data = db.Categories.get_all()
        self.fill(data)

    def remove(self):
        selection = self.listbox.curselection()
        if selection:
            var = self.listbox.selection_get()
        else:
            return
        gui_script.remove_category(var)
        data = db.Categories.get_all()
        self.fill(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data)-1, -1, -1):
            self.listbox.insert(END, data[i])


class SpendDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Название:").grid(row=0)
        Label(master, text="Категория:").grid(row=1)
        Label(master, text="Стоимость:").grid(row=2)
        Label(master, text="Дата:").grid(row=3)

        self.e1 = Entry(master)
        categories = db.Categories.get_all()

        self.frame_list = Frame(master)
        self.scrollbar = Scrollbar(self.frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.l1 = Listbox(self.frame_list, yscrollcommand=self.scrollbar.set)
        for category in categories:
            self.l1.insert(END, category)
        self.l1.pack(side=LEFT, fill=Y)
        self.scrollbar.config(command=self.l1.yview)

        self.e2 = Entry(master)
        self.e3 = Calendar(master, selectmode='day',
               year=datetime.date.today().year, month=datetime.date.today().month)

        self.e1.grid(row=0, column=1)
        self.frame_list.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)

        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        selection = self.l1.curselection()
        if selection:
            second = self.l1.selection_get()
        else:
            second = ""
        third = self.e2.get()
        fourth = self.e3.selection_get()
        self.result = [first, second, third, fourth]
        return self.result


class GainDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Название:").grid(row=0)
        Label(master, text="Стоимость:").grid(row=1)
        Label(master, text="Дата:").grid(row=2)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Calendar(master, selectmode='day',
                           year=datetime.date.today().year, month=datetime.date.today().month)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        return self.e1  # initial focus

    def apply(self):
        first = self.e1.get()
        third = self.e2.get()
        fourth = self.e3.selection_get()
        self.result = [first, third, fourth]


class CategDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Название:").grid(row=0)
        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        return self.e1  # initial focus

    def apply(self):
        first = self.e1.get()
        self.result = first
