from sqlalchemy.orm import Session
from tables.products import Product

class ProductRepo:
    @staticmethod
    def create(db: Session, product_data):
        product = Product(**product_data.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update(db: Session, product_id: int, product_data):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in product_data.dict(exclude_unset=True).items():
                setattr(product, key, value)
            db.commit()
            db.refresh(product)
            return product
        return None

    @staticmethod
    def delete(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        return False
