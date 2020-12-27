from pydantic import BaseModel
import functionsSQL

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
	# tmp = _list
	# return tmp

a = list_to_class(functionsSQL.find_entries_on_class_name("spanish"))
print(type(a))
