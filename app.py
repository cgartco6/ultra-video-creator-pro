from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
import shutil

app = FastAPI(title="Ultra Video Creator - Simple Working Version")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1 style="text-align:center; color:#fff; background:#111; padding:40px; font-family:Arial;">
        Ultra Video Creator<br>
        <small>Upload song + describe character</small>
    </h1>
    <form action="/generate" method="post" enctype="multipart/form-data" style="max-width:600px; margin:auto; padding:20px;">
        <input type="text" name="character" placeholder="Character: beautiful sexy singer, dragon, elf, Viking..." style="width:100%; padding:12px; margin:10px 0; font-size:16px;"><br>
        <input type="text" name="prompt" placeholder="Song prompt or scene" style="width:100%; padding:12px; margin:10px 0; font-size:16px;"><br>
        <input type="file" name="audio" accept="audio/*" style="margin:15px 0;"><br><br>
        <button type="submit" style="padding:15px 40px; font-size:18px; background:#8b00ff; color:white; border:none; cursor:pointer;">Generate Video</button>
    </form>
    """

@app.post("/generate")
async def generate(character: str = Form(...), prompt: str = Form(...), audio: UploadFile = File(...)):
    Path("outputs").mkdir(exist_ok=True)
    
    # Save uploaded audio
    audio_path = f"outputs/{audio.filename}"
    with open(audio_path, "wb") as f:
        f.write(await audio.read())
    
    # Simulate video output
    video_path = f"outputs/{character.replace(' ', '_')}.mp4"
    with open(video_path, "w") as f:
        f.write("This is a simulated video file. In full version this would be real MP4 with avatar.")

    return {
        "status": "success",
        "character": character,
        "video_path": video_path,
        "message": "Video generated (simulation for now)"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting server at http://localhost:3000")
    uvicorn.run(app, host="0.0.0.0", port=3000)
