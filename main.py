import json
from random import choice
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel


debug = False

db_file = "db.json"


# Functions
def read_database():
	data = []
	with open(db_file, 'r') as file:
		temp = json.load(file)
		for entry in temp:
			data.append(entry)
			if debug:
				print(entry)
	return data


def create_note_cards(data_from_read_database):
	note_cards = []
	i = 0
	for data_entry in data_from_read_database:
		note_cards.append(NoteCard(data_from_read_database[i]['Importance'],data_from_read_database[i]['Class'],
								   data_from_read_database[i]['Denomination'], data_from_read_database[i]['Question'],
								   data_from_read_database[i]['Answer']))
		i += 1
	return note_cards


def add_note_card_to_db(note):
	db = read_database()
	to_append = {"Importance": note.importance, "Class": note.cls, "Denomination": note.denomination,
				 "Question": note.question, "Answer": note.answer}
	db.append(to_append)
	with open(db_file, 'w') as file:
		json.dump(db, file, indent=1)


# Classes
class NoteCard:
	def __init__(self, importance, cls, denomination, question, answer):
		self.cls = cls
		self.denomination = denomination
		self.importance = importance
		self.question = question
		self.answer = answer

	def __str__(self):
		return f'Class: {self.cls}\nDenomination: {self.denomination}\nQuestion: {self.question}\nAnswer: {self.answer}'


class NoteDeck:
	def __init__(self):
		self.all_cards = []
		self.shuffle_list = []
		read_db = read_database()
		print(read_db)
		note_card_list = create_note_cards(read_db)
		for note in note_card_list:
			self.all_cards.append(note)

	def total_notes(self):
		return len(self.all_cards)

	def give_one(self, cls):
		i = 0
		for note in self.all_cards:
			if note.cls == cls:
				self.shuffle_list.append(note)
				i += 1
		return choice(self.shuffle_list)


# Init
app = FastAPI(debug=True)

app.add_middleware(
	CORSMiddleware,
	# allow_origins=origins,
	allow_origin_regex='https?://.*',
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

#Data
with open("db.json") as f:
	notes = json.load(f)


class _Note(BaseModel):
	importance: str
	cls: str
	denomination: str
	question: str
	answer: str


# Route
@app.get('/api/notes')
async def get_notes():
	return {"notes": notes}


@app.get('/api/notes/{class}')
async def get_notes_for_class(cls):
		cls_notes = []
		for item in notes:
			if item['Class'] == cls:
				cls_notes.append(item)
		return {"Class": cls_notes}


@app.get('/api/notes/{class}/{denomination}')
async def get_notes_for_class_and_denomination(cls, denomination):
	cls_notes = []
	for item in notes:
		if item['Class'] == cls:
			if item['Denomination'] == denomination:
				cls_notes.append(item)
	return cls_notes


@app.get('/api/notes/{class}/{denomination}/{importance}')
async def get_notes_for_class_and_denomination_and_importance(cls, denomination, importance):
	cls_notes = []
	for item in notes:
		if item['Class'] == cls:
			if item['Denomination'] == denomination:
				if item['Importance'] == importance:
					cls_notes.append(item)
	return cls_notes



@app.post("/addnotes/")
async def create_note(note: _Note):
	tmp = NoteCard(note.importance, note.cls, note.denomination,  note.question, note.answer)
	add_note_card_to_db(tmp)
	return note


if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8000)
