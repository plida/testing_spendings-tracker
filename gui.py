import datetime
from tkinter import *
from tkinter import messagebox
import tkinter.simpledialog as tksd
import gui_script
import db
from tkcalendar import Calendar

month_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
              'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']


class App:
    def __init__(self, root=None):
        # параметры приложения
        self._root = root
        self._root.minsize(600, 300)
        self._root.maxsize(600, 300)
        self._root.title("Учёт собственных средств")
        self.main_font = ("Calibri", 30)
        self.sec_font = ("Calibri", 15)
        self.totalVAR = DoubleVar()
        self.gainsVAR = DoubleVar()
        self.spendingsVAR = DoubleVar()
        self._setup_grid()
        self._setup_menu()
        # рамка, в которую помещается главная страничка
        self._frame = Frame(self._root)
        self._frame.pack()
        # главная страничка
        self._setup_main_page()

    def _setup_main_page(self):
        self.page1 = SpendPage(master=self._root, app=self)
        self.page2 = GainPage(master=self._root, app=self)
        self.page3 = CategPage(master=self._root, app=self)

        Label(self._frame, text='Баланс: ', font=self.main_font).grid(row=0, column=0, sticky=W, ipady=30)

        self._setup_labels()
        self.button_frame = Frame(self._frame)
        self.button_frame.grid(row=3, columnspan=3, sticky=W, pady=5)
        Button(self.button_frame, text='К тратам', command=lambda: self.make_page(self.page1), width=15) \
            .grid(row=3, column=0, padx=5)
        Button(self.button_frame, text='К доходам', command=lambda: self.make_page(self.page2), width=15) \
            .grid(row=3, column=1, padx=5)
        Button(self.button_frame, text='К категориям', command=lambda: self.make_page(self.page3), width=15) \
            .grid(row=3, column=2, padx=5)

    def _setup_labels(self):
        Label(self._frame, textvariable=self.totalVAR, font=self.main_font).grid(row=0, column=1)
        _f_stats = Frame(self._frame)
        _f_stats.grid(sticky=NW, rowspan=2, columnspan=2, pady=20)

        f_gains = Frame(_f_stats)
        f_gains.grid(sticky=W, row=0, columnspan=2)
        Label(f_gains, text=f"Доходы за месяц {month_list[datetime.date.today().month - 1]}:", font=self.sec_font).grid(
            row=0, column=0)
        Label(f_gains, textvariable=self.gainsVAR, font=self.sec_font).grid(row=0, column=1)

        _f_spendings = Frame(_f_stats)
        _f_spendings.grid(sticky=W, row=1, columnspan=2)
        Label(_f_spendings, text=f"Траты за месяц {month_list[datetime.date.today().month - 1]}:",
              font=self.sec_font).grid(row=0, column=0)
        Label(_f_spendings, textvariable=self.spendingsVAR, font=self.sec_font).grid(row=0, column=1)

    def _setup_grid(self):
        for i in range(10):
            self._root.rowconfigure(index=i, weight=1)
            self._root.columnconfigure(index=i, weight=1)

    def _setup_menu(self):
        self._root.option_add("*tearOff", FALSE)
        # подменю "файл"
        file_menu = Menu()
        file_menu.add_command(label="Выйти", command=self._exit_app)
        # основное меню
        main_menu = Menu()
        main_menu.add_cascade(label="Файл", menu=file_menu)
        main_menu.add_command(label="Справка", command=self._show_info)
        self._root.config(menu=main_menu)

    @staticmethod
    def _show_info():
        messagebox.showinfo("Учёт собственных денежных средств", "Автор: Крестьянова Елизавета\nВерсия 2024.05.17")

    def _exit_app(self):
        self._root.destroy()

    def main_page(self):
        self._frame.pack()

    def make_page(self, page):  # переключить на другие страницы
        self._frame.pack_forget()
        page.start_page()


class SecPage:
    def __init__(self, master=None, app=None, dialogue_window=None, title="", _dbtable=None):
        self.main_font = ("Calibri", 15)
        self.sec_font = ("Calibri", 10)
        self.master = master
        self.app = app
        self._frame = Frame(self.master)
        self._dialogue = dialogue_window
        self._dbtable = _dbtable
        Label(self._frame, text=title, font=self.main_font).grid(row=0, columnspan=6)
        self._setup_buttons()
        self._setup_listbox()

    def _setup_buttons(self):
        self._frame_buttons = Frame(self._frame)
        self._frame_buttons.grid(row=1, rowspan=4, column=0, sticky=NW, padx=10)
        self.add = Button(self._frame_buttons, text="+", command=self.add, width=2, font=self.sec_font)
        self.add.grid(row=0, column=0, ipady=3, pady=3, sticky=N)
        self.remove = Button(self._frame_buttons, text="-", command=self.remove, width=2, font=self.sec_font)
        self.remove.grid(row=1, column=0, ipady=3, pady=3)
        self.remove = Button(self._frame_buttons, text="Ф", command=self.filt, width=2, font=self.sec_font)
        self.remove.grid(row=2, column=0, ipady=3, pady=3)
        self.remove = Button(self._frame_buttons, text="С", command=self.sort, width=2, font=self.sec_font)
        self.remove.grid(row=3, column=0, ipady=3, pady=3, sticky=S)
        Button(self._frame, text='На главную страницу', command=self.go_back).grid(row=2, columnspan=6, pady=5)

    def _setup_listbox(self):
        self._frame_list = Frame(self._frame)
        self._frame_list.grid(row=1, column=1)
        self.scrollbar = Scrollbar(self._frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self._frame_list, background="#fff", yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=LEFT, fill=Y)
        self.listbox.config(width=50, height=10)
        self.scrollbar.config(command=self.listbox.yview)

    def add(self):
        pass

    def remove(self):
        pass

    def filt(self):
        var = self._dialogue(self.master)
        data = self._dbtable.get_all_filter(var.result)
        self.fill(data)

    def sort(self):
        pass

    def start_page(self):
        self._frame.pack()

    def go_back(self):
        self._frame.pack_forget()
        self.app.main_page()

    def fill(self, data):
        self.listbox.delete(0, END)
        for i in range(len(data) - 1, -1, -1):
            self.listbox.insert(END, data[i])


class SpendPage(SecPage):
    def __init__(self, master=None, app=None):
        self.listbox_data = []
        super().__init__(master, app, SpendDialog, "Траты", db.Spendings)

    def add(self):
        var_spending = self._dialogue(self.master)
        result = gui_script.add_spending(var_spending.result)
        if result == "EXIT":
            return
        elif result == "ERR_future":
            messagebox.showerror("Ошибка (доходы)", "Нельзя вводить будущую дату!")
        elif result == "ERR_empty":
            messagebox.showerror("Ошибка (траты)", "Строки не должны быть пустыми!")
        elif result == "ERR_value":
            messagebox.showerror("Ошибка (траты)", "Стоимость должна быть положительным числом меньше 10^9!")
        elif result == "ERR_toolong":
            messagebox.showerror("Ошибка (траты)", "Название траты слишком длинное!")
        elif result:
            data = db.Spendings.get_all()
            self.fill(data)
        elif not result:
            messagebox.showerror("Ошибка (траты)", "Ошибка при добавлении траты!")
        self.app.spendingsVAR.set(gui_script.calculate_month_spend())
        self.app.gainsVAR.set(gui_script.calculate_month_gain())
        self.app.totalVAR.set(gui_script.calculate_total())

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
        self.app.spendingsVAR.set(gui_script.calculate_month_spend())
        self.app.gainsVAR.set(gui_script.calculate_month_gain())
        self.app.totalVAR.set(gui_script.calculate_total())

    def sort(self):
        var = SortSpendDialog(self.master)
        print(var.result)
        if var.result:
            data = gui_script.sort(self.listbox_data, var.result[0])
            print(data, var.result[0])
            self.listbox.delete(0, END)
            if var.result[1] == 1:
                data.reverse()
            self.fill(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        self.listbox_data = data
        for i in range(len(data)):
            ins = [str(data[i][0]), str(data[i][1]), data[i][2], str(data[i][3]), data[i][4].strftime('%d/%m/%Y')]
            self.listbox.insert(END, " ".join(ins))


class GainPage(SecPage):
    def __init__(self, master=None, app=None):
        self.listbox_data = []
        super().__init__(master, app, GainDialog, "Доходы", db.Gains)

    def add(self):
        var_gain = self._dialogue(self.master)
        result = gui_script.add_gain(var_gain.result)
        if result == "EXIT":
            return
        elif result == "ERR_future":
            messagebox.showerror("Ошибка (доходы)", "Нельзя вводить будущую дату!")
        elif result == "ERR_empty":
            messagebox.showerror("Ошибка (доходы)", "Строки не должны быть пустыми!")
        elif result == "ERR_value":
            messagebox.showerror("Ошибка (доходы)", "Стоимость должна быть положительным числом меньше 10^9!")
        elif result == "ERR_toolong":
            messagebox.showerror("Ошибка (доходы) ", "Название дохода слишком длинное!")
        if result:
            data = db.Gains.get_all()
            self.fill(data)
        elif not result:
            messagebox.showerror("Ошибка (доходы)", "Ошибка при добавлении дохода!")
        self.app.spendingsVAR.set(gui_script.calculate_month_spend())
        self.app.gainsVAR.set(gui_script.calculate_month_gain())
        self.app.totalVAR.set(gui_script.calculate_total())

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
        self.app.spendingsVAR.set(gui_script.calculate_month_spend())
        self.app.gainsVAR.set(gui_script.calculate_month_gain())
        self.app.totalVAR.set(gui_script.calculate_total())

    def sort(self):
        var = SortGainDialog(self.master)
        if var.result:
            data = gui_script.sort(self.listbox_data, var.result[0])
            self.listbox.delete(0, END)
            if var.result[1] == 1:
                data.reverse()
            self.fill(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        self.listbox_data = data
        for i in range(len(data)):
            ins = [str(data[i][0]), str(data[i][1]), str(data[i][2]), data[i][3].strftime('%d/%m/%Y')]
            self.listbox.insert(END, " ".join(ins))


class CategPage(SecPage):
    def __init__(self, master=None, app=None):
        self.listbox_data = []
        super().__init__(master, app, CategDialog, "Категории", db.Categories)
        self.listbox.config(width=20)

    def add(self):
        var_category = self._dialogue(self.master)
        result = gui_script.add_category(var_category.result)
        print(result)
        if result == "ERR_exists":
            messagebox.showinfo("Ошибка (категории)", "Категория уже существует.")
        elif result == "ERR_too_long":
            messagebox.showerror("Ошибка (категории)", "Слишком длинное имя категории!")
        elif result == "EXIT":
            return
        if result:
            data = db.Categories.get_all()
            self.fill(data)
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

    def sort(self):
        var = SortCategDialog(self.master)
        data = self.listbox_data
        self.listbox.delete(0, END)
        if var.result == 0:
            data = sorted(data)
        if var.result == 1:
            data = sorted(data, reverse=True)
        self.fill(data)

    def fill(self, data):
        self.listbox.delete(0, END)
        self.listbox_data = data
        for i in range(len(data)):
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
        self._frame_list = Frame(master)
        self._frame_list.grid(row=1, column=1, sticky=W)
        self.scrollbar = Scrollbar(self._frame_list, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.e2 = Listbox(self._frame_list, background="#fff", yscrollcommand=self.scrollbar.set)
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


class SortSpendDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Отсортировать:").grid(row=0)
        self._frame1 = Frame(master)
        self._frame1.grid(row=1, rowspan=5, column=0)
        self._radio_var1 = IntVar()
        Radiobutton(self._frame1, text='По ID', variable=self._radio_var1, value=0, command=self.selection1).grid(row=0)
        Radiobutton(self._frame1, text='По названию', variable=self._radio_var1, value=1, command=self.selection1).grid(
            row=1)
        Radiobutton(self._frame1, text='По категории', variable=self._radio_var1, value=2, command=self.selection1).grid(
            row=2)
        Radiobutton(self._frame1, text='По стоимости', variable=self._radio_var1, value=3, command=self.selection1).grid(
            row=3)
        Radiobutton(self._frame1, text='По дате', variable=self._radio_var1, value=4, command=self.selection1).grid(row=4)
        self._frame2 = Frame(master)
        self._frame2.grid(row=1, rowspan=2, column=1)
        self._radio_var2 = IntVar()
        Radiobutton(self._frame2, text='A-Я', variable=self._radio_var2, value=0, command=self.selection2).grid(row=0)
        Radiobutton(self._frame2, text='Я-A', variable=self._radio_var2, value=1, command=self.selection2).grid(row=1)
        self._radio_var1.set(0)
        self._radio_var2.set(0)
        self._result1 = self._radio_var1.get()
        self._result2 = self._radio_var2.get()

    def selection1(self):
        self._result1 = self._radio_var1.get()

    def selection2(self):
        self._result2 = self._radio_var2.get()

    def apply(self):
        self.result = (self._result1, self._result2)


class SortGainDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Отсортировать:").grid(row=0)
        self._frame1 = Frame(master)
        self._frame1.grid(row=1, rowspan=4, column=0)
        self._radio_var1 = IntVar()
        Radiobutton(self._frame1, text='По ID', variable=self._radio_var1, value=0, command=self.selection1).grid(row=0)
        Radiobutton(self._frame1, text='По названию', variable=self._radio_var1, value=1, command=self.selection1).grid(
            row=1)
        Radiobutton(self._frame1, text='По стоимости', variable=self._radio_var1, value=2, command=self.selection1).grid(
            row=2)
        Radiobutton(self._frame1, text='По дате', variable=self._radio_var1, value=3, command=self.selection1).grid(row=3)
        self._frame2 = Frame(master)
        self._frame2.grid(row=1, rowspan=2, column=1)
        self._radio_var2 = IntVar()
        Radiobutton(self._frame2, text='A-Я', variable=self._radio_var2, value=0, command=self.selection2).grid(row=0)
        Radiobutton(self._frame2, text='Я-A', variable=self._radio_var2, value=1, command=self.selection2).grid(row=1)
        self._radio_var1.set(0)
        self._radio_var2.set(0)
        self._result1 = self._radio_var1.get()
        self._result2 = self._radio_var2.get()

    def selection1(self):
        self._result1 = self._radio_var1.get()

    def selection2(self):
        self._result2 = self._radio_var2.get()

    def apply(self):
        self.result = (self._result1, self._result2)


class SortCategDialog(tksd.Dialog):
    def body(self, master):
        Label(master, text="Отсортировать:").grid(row=0)
        self._frame = Frame(master)
        self._frame.grid(row=1, rowspan=4, column=0)
        self._radio_var = IntVar()
        Radiobutton(self._frame, text='A-Я', variable=self._radio_var, value=0, command=self.selection).grid(row=0)
        Radiobutton(self._frame, text='Я-A', variable=self._radio_var, value=1, command=self.selection).grid(row=1)
        self._radio_var.set(0)
        self.result = self._radio_var.get()

    def selection(self):
        self.result = self._radio_var.get()

    def apply(self):
        self.result = self._radio_var.get()
