from fastapi import FastAPI
from app.routes import dashboard, upload, classify, send, report, download_report, settings

app = FastAPI(title="API 3 - EXPORT Automation")

app.include_router(dashboard.router)
app.include_router(upload.router)
app.include_router(classify.router)
app.include_router(send.router)
app.include_router(report.router)
app.include_router(download_report.router)
app.include_router(settings.router)
