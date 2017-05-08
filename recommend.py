from Tkinter import *
import requests
from io import BytesIO
import urllib
import webbrowser
from PIL import Image, ImageTk
import home
from dbInteraction import dbInteraction

class recommend:
	def __init__(self,user, topic):
		global mysql,me, win
		win = Tk()
		win.title('StackOverFlow Recommendation System')
		win.geometry('640x480')
		me = user
		userURI = requests.get('https://api.stackexchange.com/2.2/users/'+user+'?order=desc&sort=reputation&site=stackoverflow')
		userData = userURI.json()['items'][0]
		URL = userData['profile_image']
		u = urllib.urlopen(URL)
		raw_data = u.read()
		u.close()
		im = Image.open(BytesIO(raw_data))
		image = ImageTk.PhotoImage(im)
		bronze = userData['badge_counts']['bronze']
		silver = userData['badge_counts']['silver']
		gold = userData['badge_counts']['gold']
		reputation = userData['reputation']
		frame1 = Frame(win)
		frame1.pack()
		labelName = Label(frame1,text=userData['display_name'],font = "Helvetica 16 bold italic")
		labelName.pack()
		labelPic = Label(image=image)
		labelPic.pack()
		frame2 = Frame(win)       # Row of buttons
		frame2.pack()
		b1 = Button(frame2,text="Bronze Badges "+str(bronze))
		b2 = Button(frame2,text="Sliver Badges "+str(silver))
		b3 = Button(frame2,text="Gold Badges "+str(gold))
		b4 = Button(frame2,text="Reputation "+str(reputation))
		b1.pack(side=LEFT); b2.pack(side=LEFT)
		b3.pack(side=LEFT); b4.pack(side=LEFT)

		frame3 = Frame(win)
		frame3.pack()
		scrollbar = Scrollbar(frame3)
		scrollbar.pack(side=RIGHT, fill=Y,pady=20)
		listbox = Listbox(frame3,yscrollcommand=scrollbar.set,selectmode=SINGLE)
		listbox.config(width=0)
		listbox.pack(pady=20)
		listbox.bind('<Double-1>', self.selection)

		frame4 = Frame(win)
		frame4.pack()
		back = Button(frame4,text="Go Back to HOME", command=self.backToHome)
		back.pack(side=RIGHT)

		mysql = dbInteraction()

		data = mysql.getRecommenedQuestions(topic).split('@@')
		lengthOfData = len(data)
		if lengthOfData<8:
			for d in data[0:]:
				listbox.insert(END, d)
		elif bronze<1:
			for d in data[0:lengthOfData/3]:
				listbox.insert(END, d)
		elif bronze>5:
			for d in data[(lengthOfData/3)*2:]:
				listbox.insert(END, d)
		elif bronze>=1:
			for d in data[lengthOfData/3:(lengthOfData/3)*2]:
				listbox.insert(END, d)

		win.mainloop()

	def selection(self,event):
		w = event.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		link = mysql.getLink(str(value))
		webbrowser.open(str(link))


	def backToHome(self):
		win.destroy()
		from home import home
		home().makeWindow(me)