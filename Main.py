from Tkinter import *
import requests
from bs4 import BeautifulSoup
from home import home

class MyDialog:

    def __init__(self):
    	global top
        top = Tk()
        top.title('StackOverFlow Recommendation System')
        top.geometry('300x100')
        self.myLabel = Label(top, text='Enter your user ID below')
        self.myLabel.pack()
        self.myEntryBox = Entry(top)
        self.myEntryBox.pack()
        self.myEntryBox.insert(0, "1144035")
        self.mySubmitButton = Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()
        top.mainloop()

    def send(self):
        user = self.myEntryBox.get()
        top.destroy()
        homeObj = home()
        homeObj.makeWindow(user)

MyDialog()


