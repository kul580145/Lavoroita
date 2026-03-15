from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import shutil, os, sqlite3
from datetime import datetime

app = FastAPI()

os.makedirs("uploads", exist_ok=True)

def init_db():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        job_title TEXT,
        company TEXT,
        site TEXT,
        status TEXT,
        applied_date TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "CV আপলোড সফল!", "filename": file.filename}

@app.post("/start-apply")
async def start_apply(position: str = Form(...)):
    from job_scraper import scrape_jobs
    jobs = scrape_jobs(position)
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    results = []
    for job in jobs:
        c.execute('''INSERT INTO applications 
                     (job_title, company, site, status, applied_date)
                     VALUES (?, ?, ?, ?, ?)''',
                  (job["title"], job["company"], job["site"],
                   "Applied", datetime.now().strftime("%Y-%m-%d %H:%M")))
        results.append(job)
    conn.commit()
    conn.close()
    return {"message": f"{len(results)} টি জবে Apply করা হয়েছে!", "results": results}

@app.get("/applications")
def get_applications():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM applications ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return {"applications": [
        {"id": r[0], "title": r[1], "company": r[2],
         "site": r[3], "status": r[4], "date": r[5]}
        for r in rows
    ]}
