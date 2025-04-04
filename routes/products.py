from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import get_db
from repository.users import JWTRepo 
from models.products import ProductCreate, ProductUpdate, ProductResponse
from models.users import ResponseSchema  
from tables.products import Product

router = APIRouter(
    tags=["Products"]
)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print(f"Received Token: {token}")

    payload = JWTRepo.decode_token(token)
    print(f"Decoded Payload: {payload}")

    if not payload or "error" in payload or "sub" not in payload:
        error_detail = "Invalid token" if "error" in payload else "Missing user identification"
        print(f"Auth failed: {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_detail
        )
    return payload["sub"]

@router.post('/products', response_model=ResponseSchema)
def add_product(product: ProductCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    try:
        print(f"Authenticated user: {user}")
        print(f"Creating product: {product}")
        
        existing_product = db.query(Product).filter(Product.name == product.name).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with name '{product.name}' already exists"
            )
            
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        product_response = ProductResponse.from_orm(new_product)
        
        return ResponseSchema(
            code="200",
            status="success",
            message="Product added successfully",
            result=product_response
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error creating product: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.put('/products/{product_id}', response_model=ResponseSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        existing_product.name = product.name
        existing_product.description = product.description
        existing_product.price = product.price
        db.commit()
        db.refresh(existing_product)
        
        product_response = ProductResponse.from_orm(existing_product)
        
        return ResponseSchema(
            code="200",
            status="success",
            message="Product updated successfully",
            result=product_response
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )

@router.delete('/products/{product_id}', response_model=ResponseSchema)
def delete_product(product_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        db.delete(product)
        db.commit()
        return ResponseSchema(
            code="200",
            status="success",
            message="Product deleted successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal error")
