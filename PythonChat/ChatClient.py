import socket
from threading import Thread
from tkinter import *
from tkinter import ttk

class Global(object):
		PORt = "0"
		HOSt = "0"

class MyApp:
		def __init__(self,Parent):
				self.myParent=Parent
				Parent.title("ip")
				Parent.geometry("200x130")
				Parent.resizable(False, False)  
						
				self.label_ip=Label(Parent,text="Insert server's IP addres")
				self.label_ip.pack()

				self.entry_ip=Entry(Parent)
				self.entry_ip.pack()

				self.label_port=Label(Parent,text="Insert server's PORT number")
				self.label_port.pack()

				self.entry_port=Entry(Parent)
				self.entry_port.pack()

				self.button = Button(Parent, overrelief="solid", width=15, text='insert',command=self.ipport)
				self.button.pack()

		def ipport(self): 

				Global.PORt = self.entry_port.get()
				Global.HOSt = self.entry_ip.get()
				self.myParent.destroy()
				self.myParent.quit()

window=Tk()
myapp=MyApp(window)
window.mainloop()
PORT=int(Global.PORt)
HOST=Global.HOSt


#여기까지 포트랑 호스트 입력

#HOST = '192.168.146.1'
#PORT = 12
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

root = Tk()

root.title("OFFLINE Chat SYSTEM")
root.geometry("500x660+50+50")
root.resizable(False,False)

text=Text(root,height=45,width=45)
scrollbar = Scrollbar(root,command = text.yview)
scrollbar.pack(side = RIGHT, fill = Y)


label2= ttk.Label(root,text = '오프라인 소켓 통신 채팅 프로그램')
label2.pack()

text.pack()
text.configure(yscrollcommand=scrollbar.set)

label = ttk.Label(root, text = '보낼 메세지를 입력하세요')
label.pack()

textbox = Entry(root,width=45)
textbox.pack() 


def sendMsg(sock):
	msg = textbox.get()
	if msg == '/quit':
		sock.send(msg.encode())
		exit()

	sock.send(msg.encode())
	textbox.delete(0,'end')


def func(key):
	sendMsg(sock)
	 
root.bind("<Return>", func)

def rcvMsg(sock):
	 while True:
			try:
				data = sock.recv(1024)
				if not data:
						break
				#print(data.decode())
				text.configure(state='normal')
				text.insert("end",data.decode())
				text.insert("end","\n")
				text.see("end")
				text.configure(state='disabled')
			except:
				pass

             

t = Thread(target=rcvMsg, args = (sock,))
t.start()


root.mainloop()
