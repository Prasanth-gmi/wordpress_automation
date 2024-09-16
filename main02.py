from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from crewai import Crew, Process
from tasks import Tasks
from agents import Agents
from langchain_groq import ChatGroq

app = FastAPI()

@app.get("/product_owner/", response_class=HTMLResponse)
async def get_product_owner_task_page():
    return FileResponse("outs/product_owner.md")