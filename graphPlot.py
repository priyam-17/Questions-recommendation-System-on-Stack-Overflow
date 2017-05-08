from Tkinter import *
import requests
from io import BytesIO
import urllib
import time
from PIL import Image, ImageTk
from dbInteraction import dbInteraction

class graphPlot:
	def __init__(self,user, topic):
		global win, can, me
		win = Tk()
		win.title('StackOverFlow Recommendation System')
		win.geometry('640x550')
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
		can = Canvas(frame3, width=640, height=300)
		can.pack()

		frame4 = Frame(win)
		frame4.pack()
		back = Button(frame4,text="Go Back to HOME", command=self.backToHome)
		back.pack(side=RIGHT)

		mysql = dbInteraction()

		arrayOfData=[]
		arrayOfUsed=[]

		allTags = mysql.getTopicMapping(topic).split(',')
		for tag in allTags:
			singleTag = str(tag)
			#tempVar = next((s for s in arrayOfUsed if singleTag in s), None)
			if(singleTag not in arrayOfUsed and singleTag!=str(topic).lower() and singleTag!=""):
				arrayOfUsed.append(singleTag)
				arrayOfData.append({''+singleTag+'':1})
			elif singleTag!=str(topic).lower() and singleTag!="":
				element = arrayOfUsed[arrayOfUsed.index(singleTag)]
				pos = arrayOfUsed.index(singleTag)
				arrayOfData[pos][element] = arrayOfData[pos][element]+1
			else:
				print "Tag same as topic"

		#print arrayOfData
		self.sortByValue(arrayOfData, topic)
		
		win.mainloop()

	def sortByValue(self, dictionary, topic):
		sortedList = []
		for pos in range(len(dictionary)):
			curr_element = next(iter(dictionary[pos]))
			curr_value = dictionary[pos][curr_element]
			count = 0
			if len(sortedList)>0 and curr_element!=str(topic).lower():
				for elePos in range(len(sortedList)):
					count = count+1
					if(count==6):
						count = 0
						break
					element = next(iter(sortedList[elePos]))
					value = sortedList[elePos][element]
					if curr_value>value:
						sortedList.insert(elePos,{str(curr_element):curr_value})
						count = 0
						break
					elif len(sortedList)<6:
						if elePos==len(sortedList)-1:
							sortedList.append({str(curr_element):curr_value})
						continue
					else:
						continue

			elif curr_element!=str(topic).lower():
				sortedList.append({str(curr_element):curr_value})
			else:
				continue
		print sortedList
		self.makeGraph(sortedList[:5],topic)

	def makeGraph(self,arrayOfData,topic):
		can.delete("all")
		can.create_line(50, 200, 600, 200)
		can.create_text(320,280, text="Top 5 Topics used with "+topic)
		xStart = 100
		xEnd = 160
		color = ['red','blue','grey','green','cyan']
		for dataPos in range(len(arrayOfData)):

			element = next(iter(arrayOfData[dataPos]))
			value = arrayOfData[dataPos][element]

			can.create_rectangle(xStart, 200, xEnd, 200-(value*10), fill=color[dataPos],tags=""+str(element).upper().replace(' ','_')+"")
			can.create_text(xStart+30,220, font=("Purisa", 8), text=str(element).upper(),width=50)
			can.create_text(xStart+30,180, font=("Purisa", 12), text=str(value))

			xStart = xStart+90
			xEnd = xEnd+90

	def backToHome(self):
		win.destroy()
		from home import home
		home().makeWindow(me)
