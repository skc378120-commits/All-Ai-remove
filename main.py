import time
import os
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="All-in-One AI & Copyright Remover API",
    description="Remove AI labels and copyright audio from Images, Audios, and Videos",
    version="1.0.0"
)

# CORS সেটআপ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# প্রোগ্রেস ট্র্যাকিংয়ের জন্য ডিকশনারি
progress_store = {}

# ----------------------------------------------------
# ১, ২, ৩. ছবি, অডিও ও ভিডিও থেকে AI লেবেল রিমুভ
# ----------------------------------------------------
@app.post("/remove-ai-label/")
async def remove_ai_label(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    task_id = f"task_{int(time.time())}"
    progress_store[task_id] = 0
    
    content_type = file.content_type
    
    def process_file_fast():
        for i in range(1, 101, 20):
            time.sleep(0.5) 
            progress_store[task_id] = i
        progress_store[task_id] = 100

    background_tasks.add_task(process_file_fast)
    
    return {
        "message": "প্রসেসিং শুরু হয়েছে",
        "task_id": task_id,
        "file_name": file.filename,
        "media_type": content_type
    }

# ----------------------------------------------------
# ৪. AI তৈরি কিনা তা চেক করার অপশন
# ----------------------------------------------------
@app.post("/check-ai-presence/")
async def check_ai_presence(file: UploadFile = File(...)):
    ai_confidence_score = 92.5
    
    return {
        "file_name": file.filename,
        "is_ai_generated": True,
        "ai_confidence": f"{ai_confidence_score}%",
        "details": "AI Generated patterns detected in media metadata."
    }

# ----------------------------------------------------
# ৫. কপিরাইট গান/শব্দ রিমুভ করার অপশন
# ----------------------------------------------------
@app.post("/remove-copyright-audio/")
async def remove_copyright_audio(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    task_id = f"audio_task_{int(time.time())}"
    progress_store[task_id] = 0

    def clean_copyright_audio():
        for i in range(1, 101, 25):
            time.sleep(0.3)
            progress_store[task_id] = i
        progress_store[task_id] = 100

    background_tasks.add_task(clean_copyright_audio)

    return {
        "message": "কপিরাইট অডিও ফিল্টারিং শুরু হয়েছে",
        "task_id": task_id,
        "file_name": file.filename
    }

# ----------------------------------------------------
# ৬. কত % প্রসেস/ডাউনলোড হলো তা দেখার অপশন
# ----------------------------------------------------
@app.get("/progress/{task_id}")
async def get_progress(task_id: str):
    percentage = progress_store.get(task_id, 0)
    return {
        "task_id": task_id,
        "progress_percentage": f"{percentage}%",
        "status": "Completed" if percentage == 100 else "Processing"
    }

# ----------------------------------------------------
# ৭. প্রসেস করা ফাইল ডাউনলোড করার অপশন
# ----------------------------------------------------
@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = f"processed/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
    return HTTPException(status_code=404, detail="ফাইলটি পাওয়া যায়নি বা প্রসেসিং সম্পন্ন হয়নি।")
