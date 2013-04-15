
from Tkinter import *
from PIL import Image, ImageTk
import re
import subprocess
import os

#string constants
ALPHANUMERIC_UNDERSCORE = "^[a-zA-Z0-9_ ]*$"

#alert number constants
ALERT_INVALID_INPUT = 0
ALERT_NO_NETWORK_CONNECTION = 1
ALERT_NO_SERVER_CONNECTION = 2
ALERT_FAILED_SENTIMENT_ANALYZER = 3
ALERT_FAILED_GET_TWEETS = 4
ALERT_FAILED_FINANCE_INFO = 5

MAX_LENGTH_COMPANY_NAME = 32

ALERT_ARRAY = ["Invalid Input", "No Network Connection", "Server Problems", \
		"Sentiment Analyzer Failure", "Aaron's Fault...", "Floundering Financials"]


class Application(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.companies = []

		self.parent.title("GoldMine")		

		self.companyListBox = Listbox(self.parent)
		self.companyListBox.pack(expand=1)

		self.topLabel = Label(self.parent, text="Please Choose a Company From the List:")
		self.topLabel.pack()
		
		#self.enterNameMax = MaxLengthEntry(self.parent, maxLength=MAX_LENGTH_COMPANY_NAME)
		#self.enterNameMax.pack()

		self.listCompanies = ["Microsoft", "Google", "Amazon", "IBM", "Yahoo"]
		self.listVariable = StringVar()
		self.listVariable.set(self.listCompanies[0])
		self.companyDrop = OptionMenu(self.parent, self.listVariable, *self.listCompanies)
		self.companyDrop.pack()

		self.addButton = Button(self.parent, text="+", command=self.addCompany)
		self.addButton.pack()

		self.searchButton = Button(self.parent, text="Get My Data", command=self.retreiveData)
		self.searchButton.pack()

		self.refreshButton = Button(self.parent, text="Refresh", command=self.refreshData)
		self.refreshButton.pack()
		#self.restoreMainMenu()
		

	def addCompany(self):
		company = self.listVariable.get()
		newCompany = ""
		if(company != ""):
			self.companyListBox.insert(END, company)

	#use to poulate list
	def parseInputForPresentation(self, input):
		input = self.genericParse(input)
		input = input.title()

		return input
		
	#use for refresh
	def parseInputForGetTweets(self, input):
		input = self.genericParse(input)
		input = input.replace(" ", "_")

		return input


	def genericParse(self, input):
		input = input.lstrip()
                input = input.rstrip()
                input = input.lower()

		return input


	def showAlertDialogue(self, alertNum):
		alert = Toplevel()
		alert.title("Something Went Wrong!")
		alertMessage = Message(alert, text=ALERT_ARRAY[alertNum])
		alertMessage.pack()
		dismiss = Button(alert, text="Dismiss", command=alert.destroy)
		dismiss.pack()

	def retreiveData(self):
		#get data from database
		return 0
			
				
	def refreshData(self):
		#TODO reload data from database
		return 0

	def hideMainMenu(self):
		self.refreshButton.pack_forget()
		self.companyListBox.pack_forget()
		self.enterNameMax.pack_forget()
		self.addButton.pack_forget()
		self.searchButton.pack_forget()
		self.refreshButton.pack_forget()
		self.topLabel.pack_forget()

	def hideSentimentMenu(self):
		self.label1.pack_forget()
		self.label2.pack_forget()
		self.graph1.pack_forget()
		self.graph2.pack_forget()
		self.backSentiment.pack_forget()

	def restoreMainMenu(self):
		self.hideSentimentMenu()

		self.companyListBox.pack(expand=1)
		self.topLabel.pack()
		self.enterNameMax.pack()
		self.addButton.pack()
		self.searchButton.pack()
		self.refreshButton.pack()

	def showGraph(self):
		self.hideSentimentMenu()

		self.graphLabel = Label(self.parent, text="Move Along. Nothing to See Here...")
		self.graphLabel.pack(expand=1)
		self.backGraph = Button(self.parent, text="Back", command=self.restoreSentiment)
		self.backGraph.pack(side=BOTTOM)

	def restoreSentiment(self):
		self.hideGraph()

		self.label1.pack()
		self.graph1.pack()
		self.label2.pack()
		self.graph2.pack()
		self.backSentiment.pack(side=BOTTOM)


	def hideGraph(self):
		self.graphLabel.pack_forget()
		self.backGraph.pack_forget()



	

	
class MaxLengthEntry(Entry):

	def __init__(self, parent, value="", maxLength=None, **kw):
		self.maxLength = maxLength
		apply(Entry.__init__, (self, parent), kw)

	def validate(self, value):
		if self.maxLength:
			value = value[:self.maxLength]
		return value


def main():

	root = Tk()
	
	image = Image.open("res/gold.jpg")
	#image.resize((400, 500), Image.ANTIALIAS)
	background = ImageTk.PhotoImage(image=image)
	backgroundLabel = Label(root, image=background)
	backgroundLabel.place(x=0, y=0)

	width = background.width()
	height = background.height()

	root.geometry('%dx%d+0+0' % (width, height))

	print width
	print height

	app = Application(root)
	root.mainloop()


if __name__=='__main__':
	main()
