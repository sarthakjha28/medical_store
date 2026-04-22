from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from db import get_connection
app = FastAPI()

# do not remove this below code it is the framework
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/register")
async def register(request: Request):
    data = await request.json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {"message": "All fields required"}

    conn = get_connection()
    cursor = conn.cursor()

    query = "insert into medical_user (name, email, password) values (%s, %s, %s)"
    cursor.execute(query, (name, email, password))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "User registered successfully"}


@app.post("/login")
async def login(request: Request):
    data = await request.json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"message": "All fields required"}

    conn = get_connection()
    cursor = conn.cursor()

    query = "select * from medical_user where email=%s and password=%s"
    cursor.execute(query, (email, password)) #This line talks to the database

    user = cursor.fetchone() #This line reads the result...gives the first matching row 

    cursor.close()
    conn.close()

    if user:
        return {
            "status": True,
            "message": "Login successful",
            "name": user[1]   # name column
        }
    else:
        return {"status": False, "message": "Invalid credentials"}
    

@app.get("/medicines")
def get_medicines():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = "select * from medicines"
    cursor.execute(query)

    medicines = cursor.fetchall()

    cursor.close()
    conn.close()

    return medicines   



@app.post("/add-to-cart")
async def add_to_cart(request: Request):
    data = await request.json()

    name = data.get("name")
    price = data.get("price")
    images_url = data.get("images_url")

    conn = get_connection()
    cursor = conn.cursor()

    # check if item already exists
    check_query = "select * from medicine_cart where name = %s"
    cursor.execute(check_query, (name,))
    existing_item = cursor.fetchone()

    if existing_item:
        # increase quantity
        update_query = "update medicine_cart set quantity = quantity + 1 where name = %s"
        cursor.execute(update_query, (name,))
    else:
        # insert new item
        insert_query = "insert into medicine_cart (name, price, images_url, quantity) values (%s, %s, %s, %s)"
        cursor.execute(insert_query, (name, price, images_url, 1))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Item added to cart"}


@app.get("/cart")
def get_cart():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = "select * from medicine_cart"
    cursor.execute(query)

    cart_items = cursor.fetchall()

    cursor.close()
    conn.close()
        
    return cart_items



@app.post("/remove-item")
async def remove_item(request: Request):
    data = await request.json()

    name = data.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    query = "delete from medicine_cart where name=%s limit 1"
    cursor.execute(query, (name,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Item removed"}


@app.post("/increase-qty")
async def increase_qty(request: Request):
    data = await request.json()
    name = data.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    query = "update medicine_cart set quantity = quantity + 1 where name = %s"
    cursor.execute(query, (name,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Quantity increased"}



@app.post("/decrease-qty")
async def decrease_qty(request: Request):
    data = await request.json()
    name = data.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    # get current quantity
    cursor.execute("select quantity from medicine_cart where name = %s", (name,))
    result = cursor.fetchone()

    if result:
        qty = result[0]

        if qty > 1:
            cursor.execute("update medicine_cart set quantity = quantity - 1 where name = %s", (name,))
        else:
            # if quantity becomes 0 → delete item
            cursor.execute("delete from medicine_cart where name = %s", (name,))

        conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Quantity updated"}


@app.delete("/clear-cart")
def clear_cart():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("delete from medicine_cart")
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Cart cleared"}








@app.get("/")
def home():
    return {"msg": "API medical store is working"}