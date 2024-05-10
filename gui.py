import datetime
import tkinter
from tkinter import *
from tkinter import messagebox
import tkinter.simpledialog as tksd
import gui_script
import db
from tkcalendar import Calendar


def _show_info():
    messagebox.showinfo("Учёт собственных денежных средств", "Автор: Крестьянова Елизавета\nВерсия 2024.05.07")


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
        self.page1 = Page1(master=self.root, app=self)
        self.page2 = Page2(master=self.root, app=self)

        self.totalVAR = DoubleVar()
        self.salaryVAR = DoubleVar()
        self.spendingsVAR = DoubleVar()

        Label(self.frame, text='Учёт собственных денежных средств').grid(row=0, columnspan=6)
        self._setup_labels()
        Button(self.frame, text='К тратам', command=self.make_page1).grid(row=6, column=0)
        Button(self.frame, text='К категориям', command=self.make_page2).grid(row=6, column=1)

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
        Label(f_salary, text="Зарплата:", font=self.sec_font).grid(row=0, column=0)
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

    def open_categories_win(self):
        self.winCateg.start()


class Page1:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        self.new_category_name = StringVar()

        Label(self.frame, text="Траты").grid(row=0, columnspan=6)

        self.frame_buttons = Frame(self.frame)
        self.frame_buttons.grid(rowspan=2, column=0)
        self.add = Button(self.frame_buttons, text="+", command=self.add_spending)
        self.add.grid(row=0, column=0)
        self.remove = Button(self.frame_buttons, text="-", command=self.remove_spending)
        self.remove.grid(row=1, column=0)

        self.frame_list = Frame(self.frame)
        self.frame_list.grid(row=1, column=1)
        self.scrollbar = Scrollbar(self.frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.frame_list, background="#fff", yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT, fill=Y)
        self.listbox.config(width=50, height=20)
        self.scrollbar.config(command=self.listbox.yview)

        Button(self.frame, text='На главную страницу', command=self.go_back).grid(row=2, columnspan=6)

    def add_spending(self):
        var_category = MyDialog(self.master)
        gui_script.add_spending(var_category.result)
        data = db.Spendings.get_all()
        self.fill_spendings(data)

    def remove_spending(self):
        var = tksd.askstring(title="Input", prompt="Enter something")
        gui_script.remove_spending(var)
        data = db.Spendings.get_all()
        self.fill_spendings(data)

    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()

    def fill_spendings(self, data):
        self.listbox.delete(0, END)
        for spending in data:
            self.listbox.insert(END, spending)


class Page2:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        self.new_category_name = StringVar()

        Label(self.frame, text="Категории").grid(row=0, columnspan=6)

        self.frame_buttons = Frame(self.frame)
        self.frame_buttons.grid(rowspan=2, column=0)
        self.add = Button(self.frame_buttons, text="+", command=self.add_category)
        self.add.grid(row=0, column=0)
        self.remove = Button(self.frame_buttons, text="-", command=self.remove_category)
        self.remove.grid(row=1, column=0)

        self.frame_list = Frame(self.frame)
        self.frame_list.grid(row=1, column=1)
        self.scrollbar = Scrollbar(self.frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.frame_list, background="#fff", yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT)
        self.listbox.config(width=25, height=10)
        self.scrollbar.config(command=self.listbox.yview)

        Button(self.frame, text='На главную страницу', command=self.go_back).grid(row=2, columnspan=6)

    def add_category(self):
        var = tksd.askstring(title="Input", prompt="Enter something")
        gui_script.add_category(var)
        data = db.Categories.get_all()
        self.fill_categories(data)

    def remove_category(self):
        var = tksd.askstring(title="Input", prompt="Enter something")
        gui_script.remove_category(var)
        data = db.Categories.get_all()
        self.fill_categories(data)

    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()

    def fill_categories(self, data):
        self.listbox.delete(0, END)
        for category in data:
            self.listbox.insert(END, category)


class MyDialog(tksd.Dialog):
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
               year=2024, month=5,
               day=22)

        self.e1.grid(row=0, column=1)
        self.frame_list.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)

        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.l1.selection_get()
        third = self.e2.get()
        fourth = self.e3.selection_get()
        self.result = [first, second, third, fourth]
        print(self.result)

