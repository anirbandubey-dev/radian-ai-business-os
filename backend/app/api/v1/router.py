from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.me import router as me_router
from app.api.v1.crm import router as crm_router
from app.api.v1.leads import router as leads_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(me_router)
api_router.include_router(crm_router)
api_router.include_router(leads_router)
for resource in ("accounts", "contacts", "leads", "deals", "activities", "tasks", "calendar", "insights", "predictions", "recommendations", "anomalies", "data", "pipelines", "executions", "lineage"):
    router = APIRouter(prefix=f"/{resource}", tags=[resource])
    api_router.include_router(router)

