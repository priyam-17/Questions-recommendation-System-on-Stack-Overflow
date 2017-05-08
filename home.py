from Tkinter import *
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import urllib
from dbInteraction import dbInteraction
from recommend import recommend
from graphPlot import graphPlot
import re
import webbrowser
from PIL import Image, ImageTk
from staticGraph import graphTypeSelect

class popupWindow(object):
    def __init__(self,master,choice):
    	global top, var, rORg
    	rORg = choice
        top=self.top=Toplevel(master)
        top.geometry('340x80')
        self.l=Label(top,text="Select one of the Popular Topics")
        self.l.pack()
        var = StringVar(top)
        var.set('Python')
        choices = ['Python', 'Java', 'C', 'PHP','SQL', 'JavaScript']
        option = OptionMenu(top, var, *choices)
        option.pack()
        self.b=Button(top,text='Ok',command=self.select)
        self.b.pack()

    def select(self):
        sf = var.get()
        win.destroy()
        if(rORg=="recommend"):
        	recommend(me,sf)
        else:
        	graphPlot(me,sf)
        
class graphOption(object):
	def __init__(self,master,user):
		global parent, top, sGraph, me
		parent = master
		me = user
		top=self.top=Toplevel(master)
		top.geometry('340x130')
		self.l=Label(top,text="Select a type of graph")
		self.l.pack()
		b1 = Button(top,text="Tags Network",command=self.graphOne)
		b2 = Button(top,text="Graph based on tags mapping",command=self.tagGraph)
		b3 = Button(top,text="Treemap",command=self.graphTwo)
		b4 = Button(top,text="Reputation scatter plot", command=self.graphThree)
		b1.pack()
		b2.pack()
		b3.pack()
		b4.pack()
		sGraph = graphTypeSelect()

	def tagGraph(self):
		top.destroy()
		popupWindow(parent,"graph")

	def graphOne(self):
		top.destroy()
		parent.destroy()
		sGraph.makeGraph(me,"graph1.jpg")

	def graphTwo(self):
		top.destroy()
		parent.destroy()
		sGraph.makeGraph(me,"graph2.jpg")

	def graphThree(self):
		top.destroy()
		parent.destroy()
		sGraph.makeGraph(me,"graph3.png")

class home:
	def makeWindow(self,user):
		global select, frame3, win, me, mysql
		me = user
		win = Tk()
		win.title('StackOverFlow Recommendation System')
		win.geometry('640x480')
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

		mysql = dbInteraction()
		
		if mysql.checkIfPresent()=="false":
			questionURI = requests.get('https://api.stackexchange.com/2.2/questions?pagesize=100&order=desc&sort=votes&min=100&site=stackoverflow')
			questionsData = questionURI.json()
			for i in questionsData['items']:
				question = BeautifulSoup(i['title'], "html.parser")
				text = re.sub(r'[^a-zA-Z0-9 ]',r'',question.get_text())
				listbox.insert(END, text)
				tags = ','.join(i['tags'])
				try:
					owner = i['owner']['user_id']
				except:
					owner = 0;
				answerURI = requests.get('https://api.stackexchange.com/2.2/questions/'+str(i['question_id'])+'/answers?order=desc&sort=votes&site=stackoverflow');
				answerData = answerURI.json()
				for answer in answerData['items']:
					try:
						ownerAnswer = answer['owner']['user_id']
					except:
						ownerAnswer = 0;

					mysql.insertAnswers(answer['answer_id'],ownerAnswer,answer['score'],answer['creation_date'],i['question_id'])

				mysql.insertQuestion(i['question_id'],text,owner,i['score'],i['creation_date'],tags,i['view_count'],i['answer_count'],i['link'])
		else:
			data = mysql.getAllQuestion().split(',')
			for d in data:
				if len(d.strip())>0:
					listbox.insert(END, d)


		frame4 = Frame(win)
		frame4.pack(pady=20)
		recommendButton = Button(frame4, text="Recommended Question",command=self.recommendCallback)
		recommendButton.pack(side=LEFT)
		graphicalAnalysis = Button(frame4, text="Graph Basesd on questions",command=self.graph)
		graphicalAnalysis.pack(side=RIGHT)

		win.mainloop()

	def selection(self,event):
		w = event.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		link = mysql.getLink(str(value))
		webbrowser.open(str(link))

	def recommendCallback(self):
		popupWindow(win,"recommend")

	def graph(self):
		graphOption(win,me)		
