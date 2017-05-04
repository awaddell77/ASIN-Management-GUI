from tkinter import *
from tkinter.filedialog import *
from date_form import *
from text_l import *
from dbaseObject import *
import getpass
from dictionarify import *

class Dbase_gui:
	def __init__(self):
		self.__username = input("Enter username: ")
		self.__password = getpass.getpass('Enter password: ')
		window = Tk()
		self.lbl = Label(window, text='Enter text')
		self.lbl2 = Label(window, text="Submit data")
		self.ent_field = Text(window, height = 1, width = 10)
		#function name only, no parentheses at the end
		self.btsub = Button(window, text="Click to submit", command = self.get_text) 
		self.btsub2 = Button(window, text="Open file", command = self.get_file)
		self.btsub3 = Button(window, text="Select Directory", command = self.set_dir)
		self.ent_field.pack()
		self.lbl.pack()
		self.btsub.pack()
		self.btsub2.pack()
		self.btsub3.pack()
		self.lbl2.pack()
		self.fname = ''
		self.dir_n = ''
		self.lst = []
		#self.creds = text_l('C:\\Users\\Owner\\Documents\\Important\\catcred.txt')
		self.dbObject = Db_mngmnt(self.__username, self.__password, 'asins', '192.168.5.90')
		window.mainloop() 
	def get_text(self):
		StringVar = self.ent_field.get('1.0', 'end')
		StringVar = re.sub('\n', '', StringVar)
		print(StringVar)
		if ',' in StringVar:
			sub_lst = StringVar.split(',')
			for i in sub_lst:
				self.sub_id(str(i).strip(' '))
		else:
			self.sub_id(str(StringVar).strip(' '))
		self.lst.append(StringVar)
		self.lbl2["text"] = "Submitted data"
		self.ent_field.delete('1.0', 'end')
	def get_lst(self):
		return self.lst
	def get_file(self):
		fname1 = askopenfilename()
		if '.csv' not in fname1.split('/')[len(fname1.split('/'))-1]:
			raise TypeError("Can only import CSV files")
		self.fname = fname1
		dict_lst = dictionarify(fname1)
		for i in dict_lst:
			self.sub_id(i["Product Id"])
		print("Finished submitting {0} to database".format(fname1.split('/')[len(fname1.split('/'))-1]))
	def set_dir(self):
		new_dir = askdirectory()
		self.dir_n = new_dir
		print("Directory is now", new_dir)
	def sub_id(self, x):
		if str(x).isdigit():
			self.dbObject.cust_com("INSERT INTO id_to_check (product_id, date_added) VALUES (\"{0}\", \"{1}\");".format(x, date_form()))
			print("Submitted {0}".format(x))
		else:
			raise TypeError("{0} is not a product id".format(x))

#test_inst = Scraper_gui()
if __name__ == "__main__":
	test_inst = Dbase_gui()
