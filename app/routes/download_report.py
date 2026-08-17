from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io
from app.reports.report_generator import generate_csv_report

router = APIRouter()

@router.get("/download-report")
def download_report():
    csv_data = generate_csv_report()
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=campaign_report.csv"}
    )
