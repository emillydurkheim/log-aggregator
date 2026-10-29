from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

import models
from database import engine, get_db
from pydantic import BaseModel

# Cria as tabelas no banco automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Log Aggregator API", version="1.0")

# Schema Pydantic para validar os dados que chegam
class LogCreate(BaseModel):
    service_name: str
    level: str  # INFO, WARNING, ERROR
    message: str

class LogResponse(LogCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# 1. Rota para injetar um log (Simulando uma aplicação gerando erro)
@app.post("/logs", response_model=LogResponse, status_code=201)
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = models.LogModel(
        service_name=log.service_name,
        level=log.level.upper(),
        message=log.message
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# 2. Rota para consultar logs com filtros opcionais
@app.get("/logs", response_model=List[LogResponse])
def get_logs(
    service: Optional[str] = None,
    level: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(models.LogModel)
    if service:
        query = query.filter(models.LogModel.service_name == service)
    if level:
        query = query.filter(models.LogModel.level == level.upper())
    
    return query.order_by(models.LogModel.timestamp.desc()).limit(limit).all()

# 3. Rota de Agregação (O grande diferencial do projeto): Conta erros por serviço
@app.get("/logs/metrics/summary")
def get_logs_summary(db: Session = Depends(get_db)):
    results = (
        db.query(models.LogModel.service_name, models.LogModel.level, func.count(models.LogModel.id).label("total"))
        .group_by(models.LogModel.service_name, models.LogModel.level)
        .all()
    )
    
    summary = []
    for service, level, total in results:
        summary.append({
            "service_name": service,
            "level": level,
            "count": total
        })
    
    return summary