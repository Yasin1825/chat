import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
#The IP is set to home address and port is set to a constant
#to ensure that the client and server has the same set of data
IP = input("Enter ip address")
PORT = int(input("Enter port"))


#Username for the client that he wishes to be called
#nickanme = input("Enter your username: ")
#Initializing a client
class Client:
    def __init__(self,ip,port):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
#Connecting the client to a particular IP and Port
        self.sock.connect((ip, port))
        msg=tkinter.Tk()
        msg.withdraw()
        self.nickname=simpledialog.askstring("nickname","please choose a nickname",parent=msg)
        self.gui_done=False
        self.running=True
        gui_thread=threading.Thread(target=self.gui_loop)
        receive_thread=threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()
#This function checks for any message broadcasted by the server
#and then displays if true
    def gui_loop(self):
        self.win=tkinter.Tk()
        self.win.config(bg="skyblue")

        self.chat_label=tkinter.Label(self.win,text="chat:",bg="lightgray")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20,pady=5)


        self.text_area=tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled')


        self.msg_label=tkinter.Label(self.win,text="message:",bg="lightgray")
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=20,pady=5)

        self.input_area=tkinter.Text(self.win,height=3)
        self.input_area.pack(padx=20,pady=5)

        self.send_button=tkinter.Button(self.win,text="send",command=self.write)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20,pady=5)

        self.gui_done=True

        self.win.protocol("WM_DELETE_WINDOW",self.stop)

        self.win.mainloop()
    def write(self):
        message=f"{self.nickname}:{self.input_area.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end')
    def stop(self):
        self.running=False
        self.win.destroy()
        self.sock.close()
        exit(0)
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'MSG':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break
client=Client(IP,PORT)
