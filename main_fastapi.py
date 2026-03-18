
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# FastAPI app
app = FastAPI(title="Tanyain API", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/tanyain_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# AI Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    business_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    faqs = relationship("FAQ", back_populates="owner")
    chats = relationship("ChatHistory", back_populates="client")

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    answer = Column(Text)
    category = Column(String)
    embedding = Column(Text)  # Store embeddings as JSON string
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="faqs")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_response = Column(Text)
    session_id = Column(String)
    client_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("User", back_populates="chats")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    business_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: str = None

class ChatMessage(BaseModel):
    message: str
    session_id: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# AI Functions
def generate_embedding(text: str):
    return model.encode([text])[0].tolist()

def find_best_answer(question: str, user_id: int, db: Session):
    question_embedding = generate_embedding(question)
    
    faqs = db.query(FAQ).filter(FAQ.owner_id == user_id).all()
    
    if not faqs:
        return "Maaf, belum ada FAQ yang tersedia."
    
    similarities = []
    for faq in faqs:
        if faq.embedding:
            faq_embedding = eval(faq.embedding)  # Convert string back to list
            similarity = cosine_similarity([question_embedding], [faq_embedding])[0][0]
            similarities.append((similarity, faq.answer))
    
    if not similarities:
        return "Maaf, belum ada FAQ yang tersedia."
    
    best_match = max(similarities, key=lambda x: x[0])
    
    if best_match[0] < 0.3:  # Threshold
        return "Maaf, saya belum mengerti pertanyaan Anda."
    
    return best_match[1]

# Routes
@app.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        business_name=user.business_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if not db_user.is_approved:
        raise HTTPException(status_code=403, detail="Account not approved yet")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/faqs")
def create_faq(faq: FAQCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    embedding = generate_embedding(faq.question)
    
    db_faq = FAQ(
        question=faq.question,
        answer=faq.answer,
        category=faq.category,
        embedding=str(embedding),
        owner_id=current_user.id
    )
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    
    return {"message": "FAQ created successfully", "faq_id": db_faq.id}

@app.get("/faqs")
def get_faqs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    faqs = db.query(FAQ).filter(FAQ.owner_id == current_user.id).all()
    return faqs

@app.post("/chat")
def chat(message: ChatMessage, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bot_response = find_best_answer(message.message, current_user.id, db)
    
    # Save chat history
    chat_history = ChatHistory(
        user_message=message.message,
        bot_response=bot_response,
        session_id=message.session_id,
        client_id=current_user.id
    )
    db.add(chat_history)
    db.commit()
    
    return {"response": bot_response}

@app.get("/analytics")
def get_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_chats = db.query(ChatHistory).filter(ChatHistory.client_id == current_user.id).count()
    total_faqs = db.query(FAQ).filter(FAQ.owner_id == current_user.id).count()
    
    return {
        "total_chats": total_chats,
        "total_faqs": total_faqs,
        "user": current_user.business_name
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
