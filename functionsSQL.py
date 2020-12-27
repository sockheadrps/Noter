import sqlite3
from random import choice
import json


def init_db():
	connection = sqlite3.connect('db_sql.db')
	cursor = connection.cursor()
	table_creation_command = """CREATE TABLE IF NOT EXISTS noteCards 
								(importance TEXT, 
								cls TEXT, 
								denomination TEXT, 
								question TEXT, 
								answer TEXT)"""
	cursor.execute(table_creation_command)
	connection.commit()
	connection.close()


def insert_note_card_into_sql(note_card):
	importance = note_card.importance.lower()
	cls = note_card.cls.lower()
	denomination = note_card.denomination.lower()
	question = note_card.question.lower()
	answer = note_card.answer.lower()
	connection = sqlite3.connect('db_sql.db')
	cursor = connection.cursor()
	cursor.execute("INSERT INTO noteCards VALUES (?, ?, ?, ?, ?)", (importance, cls, denomination, question, answer))
	connection.commit()
	connection.close()


def find_all_entires():
	connection = sqlite3.connect('db_sql.db')
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM noteCards")
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result


def find_entries_on_class_name(classname):
	connection = sqlite3.connect('db_sql.db')
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM noteCards where cls = ?", (classname, ))
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result


def find_entries_on_class_name_and_denomination(classname, denomination):
	connection = sqlite3.connect('db_sql.db')
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM noteCards where cls = ? AND denomination = ?", (classname, denomination))
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result


def find_entries_on_class_name_and_denomination_and_importance(classname, denomination, importance):
	connection = sqlite3.connect('db_sql.db')
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM noteCards where cls = ? AND denomination = ? AND importance = ? ", (
		classname, denomination, importance))
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result


def find_random_notecard(classname, denomination=None, importance=None):
	connection = sqlite3.connect('db_sql.db')
	cursor = connection.cursor()
	if denomination == "None":
		denomination = ""

	if importance == "None":
		importance = ""
	classname = classname.lower()

	if classname and denomination and importance:
		cursor.execute("SELECT * FROM noteCards where cls = ? AND denomination = ? AND importance = ? ", (
			classname, denomination, importance))
		result = cursor.fetchall()
		connection.commit()
		connection.close()
		return choice(result)

	if classname and denomination and not importance:
		cursor.execute("SELECT * FROM noteCards where cls = ? AND denomination = ?", (
			classname, denomination))
		result = cursor.fetchall()
		connection.commit()
		connection.close()
		return choice(result)

	if classname and not denomination and not importance:
		cursor.execute("SELECT * FROM noteCards where cls = ?", (
			classname, ))
		result = cursor.fetchall()
		connection.commit()
		connection.close()
		return choice(result)

a = find_random_notecard('math')
print(a)
# print(type(a[1]))