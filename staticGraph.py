from Tkinter import *
import requests
from io import BytesIO
import urllib
import time
from PIL import Image, ImageTk

class graphTypeSelect:
	def makeGraph(self, user,graphPath):
		global me,win
		me=user
		win = Tk()
		win.title('StackOverFlow Recommendation System')
		win.geometry('640x550')
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
		photo = ImageTk.PhotoImage(Image.open(""+graphPath+"").resize((640,300),Image.ANTIALIAS))
		panel = Label(frame3, image = photo)
		panel.pack()
		

		frame4 = Frame(win)
		frame4.pack()
		back = Button(frame4,text="Go Back to HOME",command=self.backToHome)
		back.pack()
		
		win.mainloop()

	def backToHome(self):
		win.destroy()
		from home import home
		home().makeWindow(me)