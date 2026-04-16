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
@app.post("/register")
async def register_user(request:Request):
    data = await request.json()

    name= data.get("name")
    email= data.get("email")
    password= data.get("password")

    conn= get_connection()
    cursor= conn.cursor()

    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values= (name,email,password)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "User saved successfully"}


@app.post("/login")
async def login_user(request: Request):
    data = await request.json()

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True) 

    # mysql give results row by row to avoid this store results in one memory we use buffered = true 

    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    values = (email, password)

    cursor.execute(query, values)
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid email or password"}
    

@app.get("/products")
def get_products():
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = "SELECT * FROM products"
    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close() 
    conn.close()

    return products


@app.post("/add-to-cart")
async def add_to_cart(request: Request):
    data = await request.json()

    name = data.get("name")
    price = data.get("price")
    images_url = data.get("images_url")

    conn = get_connection()
    cursor = conn.cursor()

    check_query="select * from cart where name = %s"
    cursor.execute(check_query,(name,))
    existing_item = cursor.fetchone()

    if existing_item:
        update_query = "update cart set quantity = quantity + 1 where name = %s"
        cursor.execute(update_query,(name,))

    else:
        insert_query = "insert into cart (name,price,images_url,quantity) values (%s,%s,%s,%s)"
        values = (name,price,images_url,1)
        cursor.execute(insert_query,values)

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Product added to cart"}



@app.get("/cart")
def get_cart():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = "SELECT * FROM cart"
    cursor.execute(query)

    cart_items = cursor.fetchall()

    cursor.close()
    conn.close()

    return cart_items

@app.get("/cartItems")
def get_cart():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    query = "SELECT * FROM cart"
    cursor.execute(query)

    cart_items = cursor.fetchall()

    cursor.close()
    conn.close()

    return cart_items


@app.delete("/clear-cart")
def clear_cart():
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM cart"
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Cart cleared"}

@app.put("/increase-quantity")
async def increase_quantity(request: Request):
    data = await request.json()
    name = data.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE cart SET quantity = quantity + 1 WHERE name = %s"
    cursor.execute(query, (name,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Quantity increased"}


@app.put("/decrease-quantity")
async def decrease_quantity(request: Request):
    data = await request.json()
    name = data.get("name")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    # check current quantity
    cursor.execute("SELECT quantity FROM cart WHERE name = %s", (name,))
    item = cursor.fetchone()

    if item:
        if item["quantity"] > 1:
            cursor.execute("UPDATE cart SET quantity = quantity - 1 WHERE name = %s", (name,))
        else:
            cursor.execute("DELETE FROM cart WHERE name = %s", (name,))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Quantity decreased"}


@app.post("/add-product")
async def add_product(request: Request):
    data = await request.json()

    name = data.get("name")
    price = data.get("price")
    images_url = data.get("images_url")

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO products (name, price, images_url) VALUES (%s, %s, %s)"
    values = (name, price, images_url)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Product added successfully"}


@app.post("/delete-product")
async def delete_product(request: Request):
    data = await request.json()

    name = data.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM products WHERE name = %s"
    values = (name,)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Product deleted successfully"} 






# @app.get("/")
# def home():
#     return {"msg": "register_ecommerce is working"}



