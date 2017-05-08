import MySQLdb
import datetime
import sys

class dbInteraction:
	def __init__(self):
		global db
		db = MySQLdb.connect("localhost","root","root","stackapi" )

	def insertQuestion(self,question_id,title,user_id,score,creation_date,question_tags,view_count,answer_count,link):
		cursor = db.cursor()
		timeStamp = datetime.datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')
		sql = "insert into question_table values ('"+str(question_id)+"','"+title+"','"+str(user_id)+"','"+str(score)+"','"+timeStamp+"','"+str(question_tags)+"','"+str(view_count)+"','"+str(answer_count)+"','"+str(link)+"')"
		try:
		   # Execute the SQL command
		   cursor.execute(sql)
		   db.commit()
		except:
		   # Rollback in case there is any error
		   db.rollback()
		   print sys.exc_info()
		cursor.close()

	def insertAnswers(self,answer_id,user_id,score,creation_date,question_id):
		cursor = db.cursor()
		timeStamp = datetime.datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')
		sql = "insert into answer_table values ('"+str(answer_id)+"','"+str(user_id)+"','"+str(score)+"','"+timeStamp+"','"+str(question_id)+"')"
		try:
		   cursor.execute(sql)
		   # Commit your changes in the database
		   db.commit()
		except:
		   db.rollback()
		   print sys.exc_info()
		cursor.close()

	def getAllQuestion(self):
		cursor = db.cursor()
		sql = "select title from question_table"
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			data = ""
			for row in results:
				data = data+""+row[0]+","
		except:
			print sys.exc_info()
		cursor.close()
		return str(data)

	def checkIfPresent(self):
		cursor = db.cursor()
		sql = "select question_id from question_table limit 1"
		try:
			cursor.execute(sql)
			row  = cursor.fetchone()

			if row is not None:
				return "true"
			else:
				return "false"
		except:
			print sys.exc_info()
		cursor.close()

	def getLink(self,title):
		cursor = db.cursor()
		sql = "select link from question_table where title='"+str(title)+"'"
		try:
			cursor.execute(sql)
			results = cursor.fetchone()
			data = ""
			if results is not None:
				print str(results[0])
				return str(results[0])
		except:
			print sys.exc_info()
		cursor.close()

	def getTopicMapping(self,topic):
		cursor = db.cursor()
		sql = "select question_tags from question_table where question_tags like '%"+str(topic)+",%'"
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			data = ""
			for row in results:
				data = data+""+row[0]+","
		except:
			print sys.exc_info()
		cursor.close()
		return str(data)

	def getRecommenedQuestions(self,topic):
		cursor = db.cursor()
		sql = "select title from question_table where question_tags like '%"+str(topic)+",%' order by score asc"
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			data = ""
			for row in results:
				data = data+""+row[0]+"@@"
		except:
			print sys.exc_info()
		cursor.close()
		return str(data)
