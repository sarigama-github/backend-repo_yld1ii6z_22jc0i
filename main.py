import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from bson import ObjectId

from database import db, create_document
from schemas import Submission, FileDoc

app = FastAPI(title="Citywide Investors API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "service": "Citywide Investors API"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "Unknown"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response

@app.post("/api/submissions")
async def create_submission(
    request: Request,
    property_address: str = Form(...),
    guide_price: Optional[str] = Form(None),
    rental_income_occupancy: Optional[str] = Form(None),
    issues: Optional[str] = Form(None),
    contact_details: str = Form(...),
    brochure_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    file_id: Optional[str] = None
    if file is not None:
        content = await file.read()
        file_doc = FileDoc(
            filename=file.filename,
            content_type=file.content_type,
            size=len(content) if content else 0,
            content=content,
        )
        file_id = create_document("filedoc", file_doc)

    submission = Submission(
        property_address=property_address,
        guide_price=guide_price,
        rental_income_occupancy=rental_income_occupancy,
        issues=issues,
        contact_details=contact_details,
        brochure_url=brochure_url,
        file_id=file_id,
        source_ip=request.client.host if request.client else None,
    )

    submission_id = create_document("submission", submission)

    return {"ok": True, "id": submission_id}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"ok": False, "error": exc.detail})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
