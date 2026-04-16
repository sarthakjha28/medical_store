from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from db import get_connection
app = FastAPI()

# do not remove this below code it is the framework
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/save-user")
async def save_user(request:Request):
    data = await request.json()
    

    firstname = data["firstname"]
    lastname = data["lastname"]
    email = data["email"]
    phone = data["phone"]
    age = data["age"]
    dateofvisit = data["dateofvisit"]
    time = data["time"]
    doctor = data["doctor"]

    conn= get_connection()
    cursor=conn.cursor()

    sql= "insert into hospital (firstname, lastname, email, phone, age, dateofvisit, time, doctor) values (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql,(firstname, lastname,email,phone,age,dateofvisit,time,doctor))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message":"user saved successfully"}

# @app.post("/get-user")
# async def get_user(request:Request):
#     data = await request.json()
    
#     id = data["id"]

#     conn= get_connection()
#     cursor=conn.cursor()

#     sql = "select * from patients where id = %s"
#     cursor.execute(sql, (id,))   
#     data = cursor.fetchone()

  

    conn.commit()
    cursor.close()
    conn.close()


    # Define keys for the dictionary
    keys = ['id', 'firstname', 'lastname', 'email', 'phone', 'age', 'dateofvisit', 'time', 'doctor']

    # Convert to dict
    data_dict = dict(zip(keys, data))

    
    return data_dict


@app.get("/")
def home():
    return {"msg": "API hospital  working"}
#venv\Scripts\activate
