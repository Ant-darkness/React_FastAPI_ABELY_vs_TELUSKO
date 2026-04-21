from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

products = [
        Product(id=1, name="Rice", description="Best Food", price=40.09, quantity=98),
        Product(id=2, name="Maize", description="Best Food in History", price=89, quantity=200),
        Product(id=3, name="Wheat", description="Best Food for alcohol", price=70.00, quantity=908),
        Product(id=4, name="Beans", description="Best Food for students", price=400, quantity=2908),
        Product(id=5, name="SunFlower", description="Best Oil Giver", price=480.40, quantity=678),
        Product(id=6, name="Onions", description="Best For cooking", price=870, quantity=6754)
    ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()



@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products



@app.get("/products/{id}")
def get_one_product(id: int, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        return db_products

    return "product not Found"


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()

    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name 
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated Successfully!"
    else:
        return "Product Not Found"
    


@app.delete("/products/{id}")
def delete_product(id: int, product: Product, db: Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
    else: 
        return "Product Not Found"



