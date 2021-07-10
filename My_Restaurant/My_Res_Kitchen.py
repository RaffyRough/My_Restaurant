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
        receive_thread = threading.Thread(target=self.receive_thread)
        receive_thread.start()


class KitchenWindow(Client):
    # Kitchen window will created using tkinter.
    # Child class of Client, inheriting the necessary server attributes to connect to the server
    def __init__(self):
        super().__init__(HOST, PORT)
        self.root = tk.Tk()
        self.display = tk.Text(self.root, height=10, width=45, bg='Orange', bd=4)
        self.display.pack()
        self.root.geometry('500x500')
        self.clear_button = ttk.Button(self.root, text='Clear', command=self.clearScreen)
        self.clear_button.pack()
        self.root.mainloop()

    def clearScreen(self):
        self.display.delete('1.0', 'end')

    def _displayOrder(self):
        # will display orders received from the server as long as is running
        if self.running:
            order = self.sock.recv(1024).decode('utf-8')
            self.display.insert(tk.END, order)

    def receive_thread(self):
        while self.running:
            try:
                self._displayOrder()


            except ConnectionAbortedError:
                break



if __name__ == '__main__':
    k = KitchenWindow()




