from tkinter import *
from tkinter.filedialog import *
from date_form import *
from text_l import *
from dbaseObject import *
import getpass
from dictionarify import *
#developed and maintained by Andrew Waddell

class Dbase_gui:
	def __init__(self):
		self.__username = input("Enter username: ")
		self.__password = getpass.getpass('Enter password: ')
		window = Tk()
		window.title("AM Client v0.01a")
		window.iconbitmap('donuts.ico')
		window.geometry('250x150')
		self.lbl = Label(window, text='Enter Product Id(s):')
		self.lbl2 = Label(window, text="")
		self.ent_field = Text(window, height = 1, width = 20)
		#function name only, no parentheses at the end
		self.btsub = Button(window, text="Click to submit", command = self.get_text) 
		self.btsub2 = Button(window, text="Submit from .csv file", command = self.get_file)
		self.lbl.pack()
		self.ent_field.pack()
		self.btsub.pack()
		self.btsub2.pack()
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
		#print(StringVar)
		if ',' in StringVar:
			sub_lst = StringVar.split(',')
			for i in sub_lst:
				self.lbl2["text"] = "Submitting data"
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
			try:
				p_id = i["Product Id"]
			except KeyError as KE:
				print("ERROR: File must contain a Product Id header")
			else:
				self.sub_id(p_id)
		print("Finished submitting {0} to database".format(fname1.split('/')[len(fname1.split('/'))-1]))
	def sub_id(self, x):
		if str(x).isdigit():
			self.dbObject.cust_com("INSERT INTO id_to_check (product_id, date_added) VALUES (\"{0}\", \"{1}\");".format(x, date_form()))
			print("Submitted {0}".format(x))
		else:
			raise TypeError("{0} is not a product id".format(x))

#test_inst = Scraper_gui()
if __name__ == "__main__":
	test_inst = Dbase_gui()
