import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from time import time

path='/home/pi/Desktop/CBI/test images'
imagefiles = os.listdir(path)

class UI:

	def __init__(self):
		
		self.__master = Tk()
		self.__master.geometry('500x500')
		self.__master.title('GUI')
		self.__scrollbar = Scrollbar(self.__master)
		self.__tree = ttk.Treeview(self.__master,
		 yscrollcommand=self.__scrollbar.set)
		self.__tree['columns'] = ('one', 'two','three')
		
		self.__tree.column('#0', width=270, minwidth=270, stretch=YES)
		self.__tree.column('one', width=150, minwidth=150, stretch=NO)
		self.__tree.column('two', width=400, minwidth=200)
		self.__tree.column('three',width=80, minwidth=5, strech=NO)
		
		self.__tree.heading('#0',text='Name',anchor=W)
		self.__tree.heading('one', text='Date added', anchor=W)
		self.__tree.heading('two', text='Type', anchor=W)
		self.__tree.heading('three', text='Size', anchor=W)
		
		for file in imagefiles:
			self.__tree.insert('','end','',text=file)
		
		self.__tree.grid(row=1, column=1, rowspan=3, columnspan=3)
		self.__bind('<Double-1>',self.doubleclick)
		
	def doubleclick(self, event):
		file = self.__tree.identify('item',event.x, event.y)
		filename = self.__tree.item(file, 'text')
		file_path = os.path.join('/home/pi/Desktop/CBI/test images',filename)
		self.load_image(file_path)
		
	def load_image(self, file_path):
		img = Image.open(file_path)
		self.__image = ImageTk.PhotoImage(img)
		self.__imageopener = Toplevel(sef.__master)
		self.__imageopener.title('Image')
		self.__imageopener.geometry('500x500')	
		label = Label(self.__imageopener,image=self.__image)
		label.pack(expand=True, fill=BOTH)

	
	def start(self):
		self.__master.mainloop()

def main():
	ui = UI()
	ui.start()
