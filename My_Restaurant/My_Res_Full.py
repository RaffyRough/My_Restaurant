# Waiter system will have properties of a client
# To Do: import a kitchen
from tkinter import ttk
import tkinter as tk
import threading
import socket

#===================================== Constants =========================================
HOST = '127.0.0.1.'
PORT = 55556

#===================================== Classes ===========================================
class Client:
    # Client will be the parent class of Window
    # This means each window will have properties of a client and thus able to connect to server
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))


        self.gui_done = False
        self.running = True



    #======================= Client Class Methods ========================================


class Window(Client):
    # Child class of Client, inheriting the necessary server attributes to connect to the server
    # Window will be a tkinter gui, instantiated with necessary widgets
    # mainloop will also be called in the __init__ function so window will run on instantiation
    total = 0          # total cost of the orders
    # menus will be Class variables as well.
    food_menu = {'|fries|':5, '|Burger|':10, '|Pizza|':15, '|Chicken|':8, '|Fish|':7.50}
    food_list = [str(item) for item in food_menu.keys()]
    soda_menu = {'|Sprite|':2, '|Coke|':2, '|Fanta|':2.50, '|Ginger|':2.50, '|Diet Coke|':2.50, '|Juice|':4}
    soda_list = [str(item) for item in soda_menu.keys()]
    spirit_menu = {'|Wine|':12.00, '|Rum|':6.50, '|Gin|':8, '|Vodka|':8, '|Brandy|':14, '|Whiskey|':14}
    spirit_list = [str(item) for item in spirit_menu.keys()]
    cocktail_menu = {'|Mojitos|':18, '|Pina Colada|':15, '|Daiquiris|':16, '|Mai Tai|':18, '|Martini|':18}
    cocktail_list = [str(item) for item in cocktail_menu.keys()]

    def __init__(self):
        super().__init__(HOST, PORT)
        # Initialise the tkinter, display, buttons & combo boxes
        self.root = tk.Tk()
        self.display = tk.Text(self.root, height=10, width=45, bg='Orange', bd=4)
        self.display.pack()
        self.root.geometry('500x500')
        self.root.title('Waiter Window')
        self.root.wm_resizable(width=True, height=True)
        self.price_display = tk.Text(self.root, height=3, width=15, bg='Orange', bd=4)
        self.price_display.pack()

        # Initialise combo boxes
        self.box_1 = ttk.Combobox(self.root, values=Window.food_list)
        self.box_1.pack()
        self.box_2 = ttk.Combobox(self.root, values=Window.soda_list)
        self.box_2.pack()
        self.box_3 = ttk.Combobox(self.root, values=Window.spirit_list)
        self.box_3.pack()
        self.box_4 = ttk.Combobox(self.root, values=Window.cocktail_list)
        self.box_4.pack()

        # Initialise buttons
        self.button_1 = ttk.Button(self.root, text='Select')
        self.button_1.place(x=321, y=226)
        self.button_1.bind('<Button>', self.onClick_1)
        self.button_2 = ttk.Button(self.root, text='Select')
        self.button_2.place(x=321, y=249)
        self.button_2.bind('<Button>', self.onClick_2)
        self.button_3 = ttk.Button(self.root, text='Select')
        self.button_3.place(x=321, y=272)
        self.button_3.bind('<Button>', self.onClick_3)
        self.button_4 = ttk.Button(self.root, text='Select')
        self.button_4.place(x=321, y=295)
        self.button_4.bind('<Button>', self.onClick_4)
        self.net_total_button = ttk.Button(self.root, text='Total')
        self.net_total_button.place(x=210, y=320)
        self.net_total_button.bind('<Button>', self.netTotal)

    #====================== Window Class Methods ==========================
    def run(self):
        self.root.mainloop()

    def onClick_1(self, e):
        """:argument e -> event that is bound to execution of this func
            func does alot of heavy lifting. It gets the order selected, displays it to the waiter display, adds
            cost of meal to the total and then sends it to the server via the cls.write func
        """
        self.display.insert(tk.END, self.box_1.get())
        order = f'{self.box_1.get()}'

        if self.box_1.get() != 'Select':
            Window.total += float(self.food_menu[order])
            self.price_display.delete('1.0', 'end')
            self.price_display.insert(tk.END, Window.total)
            self._write(order)


    def onClick_2(self, e):
        """:arg e -> event that is bound to execution of this func"""

        self.display.insert(tk.END, self.box_2.get())
        if self.box_2.get() != 'Select':
            Window.total += float(self.soda_menu[self.box_2.get()])
            self.price_display.delete('1.0', 'end')
            self.price_display.insert(tk.END, Window.total)

    def onClick_3(self, e):
        """":arg e -> event that is bound to execution of this func"""

        self.display.insert(tk.END, self.box_3.get())
        if self.box_3.get() != 'Select':
            Window.total += float(self.spirit_menu[self.box_3.get()])
            self.price_display.delete('1.0', 'end')
            self.price_display.insert(tk.END, Window.total)

    def onClick_4(self, e):
        """:arg e -> event that is bound to execution of this func"""

        self.display.insert(tk.END, self.box_4.get())
        if self.box_4.get() != 'Select':
            Window.total += float(self.cocktail_menu[self.box_4.get()])
            self.price_display.delete('1.0', 'end')
            self.price_display.insert(tk.END, Window.total)

    def netTotal(self, e):
        """:arg e -> event that is bound to execution of this func"""
        net_total = Window.total * 1.10
        self.price_display.delete('1.0', 'end')
        self.price_display.insert(tk.END, net_total)

    def _write(self, order):
        """:arg order -> An order procured from onClick_1 func to be sent to the server"""

        self.sock.send(order.encode('utf-8'))


w = Window()
if __name__ == '__main__':
    w.run()

