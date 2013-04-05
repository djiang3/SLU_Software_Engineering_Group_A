from Tkinter import *
from PIL import Image, ImageTk
import re

#string constants
ALPHANUMERIC_UNDERSCORE = "^[a-zA-Z0-9_ ]*$"

#alert number constants
ALERT_INVALID_INPUT = 0
ALERT_NO_NETWORK_CONNECTION = 1
ALERT_NO_SERVER_CONNECTION = 2
ALERT_FAILED_SENTIMENT_ANALYZER = 3
ALERT_FAILED_GET_TWEETS = 4
ALERT_FAILED_FINANCE_INFO = 5


class Application(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.companies = []
		self.alerts = ["Invalid Input", \
				"No Network", \
				"Sh*tty Server", \
				"Abhorrent Analyzer", \
				"Aaron's Fault...", \
				"Floundering Financials"]

		self.parent.title("GoldMine")



#		self.backgroundImage = Image.open("drunk-baby-piggy.jpg")
#		connectome = ImageTk.PhotoImage(self.backgroundImage)

#		w = connectome.width()
#		h = connectome.height()

#		parent.geometry=("%dx%d+0+0" % (w, h))

#		self.backgroundLabel = Label(parent, image=connectome)
#		self.backgroundLabel.pack(side='top', fill='both', expand='yes')


		self.topLabel = Label(self.parent, text="Enter a Company Name")
		self.topLabel.pack()
		
		self.enterName = Entry(self.parent)
		self.enterName.pack()

		self.addButton = Button(self.parent, text="+", command=self.addCompany)
		self.addButton.pack()

		self.searchButton = Button(self.parent, text="Start the Fun!", command=self.initiateScripts)
		self.searchButton.pack()


	def addCompany(self):
		company = self.enterName.get()
		newCompany = ""
		if(company != ""):
			if not re.match(ALPHANUMERIC_UNDERSCORE, company):
				self.alertInvalidCharacters(ALERT_INVALID_INPUT)
				self.enterName.delete(0, END)
			else:
				newCompanyPresentation = self.parseInputForPresentation(company)
				newCompanyGetTweets = self.parseInputForGetTweets(company)
				self.companies.append(newCompanyGetTweets)
				newLabel = Label(self.parent, text=newCompanyPresentation)
				newLabel.pack()
				self.enterName.delete(0, END)


	def parseInputForPresentation(self, input):
		input = self.genericParse(input)
		input = input.title()

		return input
		

	def parseInputForGetTweets(self, input):
		input = self.genericParse(input)
		input = input.replace(" ", "_")

		return input


	def genericParse(self, input):
		input = input.lstrip()
                input = input.rstrip()
                input = input.lower()

		return input


	def alertInvalidCharacters(self, alertNum):
		alert = Toplevel()
		alert.title("Something Went Wrong!")
		alertMessage = Message(alert, text=self.alerts[alertNum])
		alertMessage.pack()
		dismiss = Button(alert, text="Dismiss", command=alert.destroy)
		dismiss.pack()

	
	def initiateScripts(self):
		#TODO call goldmine shell to start all processes
		return 0
		
		


def main():

	root = Tk()
	root.geometry("500x500+150+150")
	app = Application(root)
	root.mainloop()


if __name__=='__main__':
	main()
