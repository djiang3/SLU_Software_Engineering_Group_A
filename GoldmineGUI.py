from Tkinter import *
from PIL import Image, ImageTk
import re
import os
import zmq
import urllib2
import json

#string constants
ALPHANUMERIC_UNDERSCORE = "^[a-zA-Z0-9_ ]*$"

#alert number constants
ALERT_INVALID_INPUT = 0
ALERT_NO_NETWORK_CONNECTION = 1
ALERT_NO_SERVER_CONNECTION = 2
ALERT_FAILED_SENTIMENT_ANALYZER = 3
ALERT_FAILED_GET_TWEETS = 4
ALERT_FAILED_FINANCE_INFO = 5
ALERT_DATE_RANGE_ERROR = 6

MAX_LENGTH_COMPANY_NAME = 32

ALERT_ARRAY = ["Invalid Input", "No Network Connection", "Server Problems", \
		"Sentiment Analyzer Failure", "Aaron's Fault...", "Floundering Financials", "Invalid Date Range"]


class Application(Frame):

	def __init__(self, parent, socket):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.companies = []
		self.socket = socket
		self.previousSelectedCompany = ""

		self.companiesAdded = []
		self.startDatesAdded = []
		self.endDatesAdded = []

		self.tweetInfoDict = {}
		self.stockInfoDict = {}

		self.parent.title("GoldMine")		

		self.companyListBox = Listbox(self.parent)
		self.companyListBox.pack(expand=1)
		
		self.startDateListBox = Listbox(self.parent)
		self.startDateListBox.pack(expand=1)

		self.endDateListBox = Listbox(self.parent)
		self.endDateListBox.pack(expand=1)

		self.topLabel = Label(self.parent, text="Please Choose a Company From the List:")
		self.topLabel.pack()
		
		#self.enterNameMax = MaxLengthEntry(self.parent, maxLength=MAX_LENGTH_COMPANY_NAME)
		#self.enterNameMax.pack()

		companies = self.refreshCompanyList()
		self.listCompanies = companies
		self.listVariableCompany = StringVar()
		self.listVariableCompany.set(self.listCompanies[0])
		self.companyDrop = OptionMenu(self.parent, self.listVariableCompany, *self.listCompanies)
		self.companyDrop.pack()

		startDates = self.refreshDateList()
		self.listStartDates = startDates
		self.listVariableStartDate = StringVar()
		self.listVariableStartDate.set(self.listStartDates[0])
		self.startDateDrop = OptionMenu(self.parent, self.listVariableStartDate, *self.listStartDates)
		self.startDateDrop.pack()

		self.listEndDates = startDates
		self.listVariableEndDate = StringVar()
		self.listVariableEndDate.set(self.listEndDates[0])
		self.endDateDrop = OptionMenu(self.parent, self.listVariableEndDate, *self.listEndDates)
		self.endDateDrop.pack()		

		self.addButton = Button(self.parent, text="+", command=self.addCompany)
		self.addButton.pack()

		self.retrieveDataButton = Button(self.parent, text="Get My Data", command=self.retrieveData)
		self.retrieveDataButton.pack()

		self.refreshButton = Button(self.parent, text="Refresh Company List", command=self.refreshCompanyList)
		self.refreshButton.pack()
		#self.restoreMainMenu()
		

	def addCompany(self):
		company = self.listVariableCompany.get()
		startDate = self.listVariableStartDate.get()
		endDate = self.listVariableEndDate.get()

		startYear = int(startDate[0:4])
		endYear = int(endDate[0:4])
		startMonth = int(startDate[5:7])
		endMonth = int(endDate[5:7])
		startDay = int(startDate[8:10])
		endDay = int(endDate[8:10])

		if(company != "" and company not in self.companiesAdded):
			if(endYear < startYear):
				self.showAlertDialogue(ALERT_DATE_RANGE_ERROR)
			elif(endMonth < startMonth):
				self.showAlertDialogue(ALERT_DATE_RANGE_ERROR)
			elif(endDay < startDay):
				self.showAlertDialogue(ALERT_DATE_RANGE_ERROR)
			else:
				self.companyListBox.insert(END, company)
				self.companiesAdded.append(company)
				self.startDateListBox.insert(END, startDate)
				self.startDatesAdded.append(startDate)
				self.endDateListBox.insert(END, endDate)
				self.endDatesAdded.append(endDate)


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


	def hideMainMenu(self):
		self.refreshButton.pack_forget()
		self.companyListBox.pack_forget()
		self.enterNameMax.pack_forget()
		self.addButton.pack_forget()
		self.retrieveDataButton.pack_forget()
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
		self.startDateListBox.pack(expand=1)
		self.endDateListBox.pack(expand=1)
		self.topLabel.pack()
		self.enterNameMax.pack()
		self.addButton.pack()
		self.retrieveDataButton.pack()
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


	def retrieveData(self):
		tempData = []

		messageDict = {'type':'gui_tweet_pull', 'companies':self.companiesAdded, 'start_dates':self.startDatesAdded, 'end_dates':self.endDatesAdded}
		message = json.dumps(messageDict)
		self.socket.send(message)
		message = self.socket.recv()
		rcvd = json.loads(message)
		for r in rcvd:
			print r

		return 0
		


	def refreshCompanyList(self):
		dict = {'type': 'gui_get_companies'}
		list = self.refreshListFromDB(dict)

		return list


	def refreshDateList(self):
		company = self.listVariableCompany.get().lower()
		dict = {'type': 'gui_get_dates', 'company': company}
		list = self.refreshListFromDB(dict)

		return list


	def refreshListFromDB(self, messageDict):
		tempData = []
		message = json.dumps(messageDict)
		self.socket.send(message)
		message = self.socket.recv()
		rcvd = json.loads(message)
		for r in rcvd:
			tempData.append(r.title())

		return tempData


	def onCompanySelect(self):
		currentCompany = self.listVariableCompany.get()
		if(self.previousSelectedCompany != currentCompany):
			newDates = self.refreshDateList()
			sMenu = self.startDateDrop['menu']
			sMenu.delete(0, END)
			eMenu = self.endDateDrop['menu']
			eMenu.delete(0, END)

			for nd in newDates:
				sMenu.add_command(label=nd, command=lambda v=self.listVariableStartDate, l=nd: v.set(l))
				eMenu.add_command(label=nd, command=lambda v=self.listVariableEndDate, l=nd: v.set(l))
			
			self.listVariableStartDate.set(newDates[0])
			self.listVariableEndDate.set(newDates[0])

			self.previousSelectedCompany = currentCompany

		self.parent.after(250, self.onCompanySelect)


		
		

	
class MaxLengthEntry(Entry):

	def __init__(self, parent, value="", maxLength=None, **kw):
		self.maxLength = maxLength
		apply(Entry.__init__, (self, parent), kw)

	def validate(self, value):
		if self.maxLength:
			value = value[:self.maxLength]
		return value



def main():


	#connect to server
	try:
		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:5555")
	except IOException as ioe:
		print "Could not connect to server"
		sys.exit(1)

	root = Tk()
	
	image = Image.open("res/gold.jpg")
	#image.resize((400, 500), Image.ANTIALIAS)
	background = ImageTk.PhotoImage(image=image)
	backgroundLabel = Label(root, image=background)
	backgroundLabel.place(x=0, y=0)

	width = background.width()
	height = background.height()

	root.geometry('%dx%d+0+0' % (width, height))

	app = Application(root, socket)

	root.after(250, app.onCompanySelect)
	root.mainloop()


if __name__=='__main__':
	main()
