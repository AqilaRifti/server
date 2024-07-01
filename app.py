import json
import fastapi
from fastapi.middleware import cors
import random
from pydantic import BaseModel

app = fastapi.FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

class FormObject(BaseModel):
    url: str

def generate_form_id():
    random_id_list = []
    for _ in range(9):
        random_id_list.append(str(random.randint(0, 9)))
    return "".join(random_id_list)

def report_to_db(form_id: str, student_name: str, date: str):
    with open("db.json", "r") as file:
        primary_data = json.loads(file.read())

    if student_name in primary_data[form_id]["data"]:
        primary_data[form_id]["data"][student_name]["counter"] += 1
        primary_data[form_id]["data"][student_name]["dates"].append(date)
        with open("db.json", "w") as file:
            file.write(json.dumps(primary_data))
        return

    primary_data[form_id]["data"][student_name] = {"counter": -3, "dates": list([date])}
    with open("db.json", "w") as file:
        file.write(json.dumps(primary_data))




def get_url_from_form_id(form_id: str):
    with open("db.json", "r") as file:
        primary_data = json.loads(file.read())
    return primary_data[form_id]["url"]

@app.get("/get/report/{form_id}")
def get_report(form_id: str):
    with open ("db.json", "r") as file:
        primary_data = json.loads(file.read())
    return primary_data[form_id]["data"]

@app.post("/create")
def create_form(form: FormObject):
    form_id = generate_form_id()
    print(form.json())
    with open("db.json", "r") as file:
        primary_data = json.loads(file.read())
    primary_data[form_id] = {"url": form.url, "data": {}}
    with open("db.json", "w") as file:
        file.write(json.dumps(primary_data))
    return {"id": form_id}

@app.get("/get/url/{form_id}")
def url_route(form_id: str):
    return {"url": get_url_from_form_id(form_id)}

@app.get("/report/{form_id}/{student_name}/{date}")
def report_route(form_id: str, student_name: str, date: str):
    report_to_db(form_id, student_name, date)
    # if credentials not in cheating_data[form_id]:
    #     cheating_data[form_id].append({credentials: 0})
    # else:
    #     cheating_data[form_id][credentials] += 1
    # print(cheating_data[form_id])
    return {"status": "OK"}
