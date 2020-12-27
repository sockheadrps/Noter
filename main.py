import functionsSQL
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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


# Data
class _Note(BaseModel):
	importance: str
	cls: str
	denomination: str
	question: str
	answer: str


def list_to_class(_list):
	new_list = []
	for i in _list[0]:
		new_list.append(i)
	new_list_class = _Note(
		importance=new_list[0],
		cls = new_list[1],
		denomination=new_list[2],
		question=new_list[3],
		answer=new_list[4]
	)
	return new_list_class


# Route
app.mount("/static", StaticFiles(directory="templates"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/add_note/", response_class=HTMLResponse)
async def add_note(request: Request):
	return templates.TemplateResponse("form.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def view_notes(request: Request):
	return templates.TemplateResponse("main.html", {"request": request})


@app.get('/api/notes')
async def get_notes():
	return {"notes": functionsSQL.find_all_entires()}


@app.get('/api/notes/{class}')
async def get_notes_for_class(cls):
	return functionsSQL.find_entries_on_class_name(cls)


@app.get('/api/notes/{class}/{denomination}')
async def get_notes_for_class_and_denomination(cls, denomination):
	return functionsSQL.find_entries_on_class_name_and_denomination(cls, denomination)


@app.get('/api/notes/{cls}/{denomination}/{importance}')
async def get_notes_for_class_and_denomination_and_importance(cls, denomination, importance):
	return functionsSQL.find_entries_on_class_name_and_denomination_and_importance(cls, denomination, importance)

@app.get('/api/notes/random/{cls}/{denomination}/{importance}')
async def get_random_notes(cls, denomination, importance):
	if denomination == "None":
		denomination = ""
	if importance == "None":
		importance = ""
	return functionsSQL.find_random_notecard(cls, denomination, importance)


@app.post("/add_note_to_db/")
async def create_note(note: _Note):
	"""
	Adds note to database
	:param note: of _note type
	:return: code response
	"""
	functionsSQL.insert_note_card_into_sql(note)
	return {
		"Code": "Success",
		"Message": "Note created!"
	}


@app.get("/dashboard")
async def test_endpoint(request: Request):
	a = list_to_class(functionsSQL.find_entries_on_class_name("spanish"))
	return templates.TemplateResponse("dashboard.html", {
		"request": request,
		"importance": a.importance,
		"class": a.cls.capitalize(),
		"denomination": a.denomination.capitalize(),
		"question": a.question.capitalize(),
		"answer": a.answer.capitalize()
	})


@app.get("/tests")
async def test_endpoint(request: Request):
	return templates.TemplateResponse("test.html", {"request": request})


if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8000)
