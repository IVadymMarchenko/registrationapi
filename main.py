from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import todos
from src.routes import auth
app=FastAPI()

app.include_router(auth.router,prefix='/api')
app.include_router(todos.router,prefix='/api')

@app.get('/')
def index():
    return {'message':'Todo Application'}


@app.get('/api/healthchecker')
async def healthchecker(db: AsyncSession=Depends(get_db)):
    try:
        result=await db.execute(text('SELECT 1'))
        result=result.fetchone()
        if result is None:
            raise HTTPException(status_code=500,detail='Error connecting to DB')
        return {'message': 'Welcome to fastAPI'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='Error connecting to DB')