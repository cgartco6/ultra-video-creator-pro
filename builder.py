import os
import shutil
import subprocess
import json
from pathlib import Path

class ProjectBuilder:
    def __init__(self, project_name="ultra-video-creator"):
        self.root = Path(project_name)
        self.structure = {
            "backend": ["app", "services", "ai", "models"],
            "frontend": ["app", "components", "lib"],
            "mobile": ["src"],
            "scripts": [],
            "docker": [],
            "docs": [],
            "ai_models": ["comfy", "avatar", "lip_sync"]
        }

    def create_structure(self):
        for dir_name, subdirs in self.structure.items():
            base = self.root / dir_name
            base.mkdir(parents=True, exist_ok=True)
            for sub in subdirs:
                (base / sub).mkdir(parents=True, exist_ok=True)

        # Add key files
        self.write_file(self.root / "README.md", "# Ultra Video Creator\nNext-gen AI film studio.")
        self.write_file(self.root / "docker-compose.yml", self.docker_compose())
        self.write_file(self.root / "requirements.txt", "fastapi\nuvicorn\nprisma\ncelery\nredis\nffmpeg-python")
        self.write_file(self.root / "package.json", json.dumps(self.frontend_package(), indent=2))

    def write_file(self, path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def docker_compose(self):
        return """version: '3.9'
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ultravid
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
  redis:
    image: redis:7
  minio:
    image: minio/minio
    command: server /data
    ports: ["9000:9000"]
"""

    def frontend_package(self):
        return {
            "name": "ultra-frontend",
            "scripts": {"dev": "next dev", "build": "next build"},
            "dependencies": {
                "next": "15.0.0",
                "react": "19.0.0-rc",
                "tailwindcss": "latest",
                "@ffmpeg/ffmpeg": "latest"
            }
        }

    def generate_backend(self):
        # FastAPI main
        self.write_file(self.root / "backend/app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Ultra Video Creator API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health(): return {"status": "alive"}

# TODO: Add routes for /generate/avatar, /render/movie, /upload etc.
print("Backend ready")
""")

        # AI service example (SadTalker-like stub)
        self.write_file(self.root / "backend/services/ai/avatar.py", """
import subprocess
def generate_singing_avatar(audio_path: str, prompt: str, genre: str):
    # In production: call ComfyUI API or custom pipeline
    print(f"Generating {genre} avatar singing from {audio_path}")
    # Placeholder: return video path
    return "/output/avatar.mp4"
""")

    def generate_frontend(self):
        self.write_file(self.root / "frontend/app/page.tsx", """
'use client';
import { useState } from 'react';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8">
      <h1 className="text-6xl font-bold mb-8">Ultra Video Creator</h1>
      <input 
        value={prompt} 
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe your scene: Viking warrior singing power ballad..."
        className="w-full p-4 bg-zinc-900 rounded-xl text-lg"
      />
      <button className="mt-6 px-10 py-4 bg-violet-600 rounded-full text-xl font-semibold">
        Generate Blockbuster
      </button>
    </div>
  );
}
""")

    def create_scripts(self):
        # setup.sh
        self.write_file(self.root / "scripts/setup.sh", """#!/bin/bash
echo "Setting up Ultra Video Creator..."
git init
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install --prefix frontend
docker-compose up -d
echo "Ready! Access frontend at http://localhost:3000"
""")
        os.chmod(self.root / "scripts/setup.sh", 0o755)

        # Windows .bat
        self.write_file(self.root / "scripts/setup.bat", """
@echo off
echo Setting up Ultra Video Creator...
call python -m venv venv
call venv\\Scripts\\activate
pip install -r requirements.txt
cd frontend && npm install
docker-compose up -d
echo Ready!
""")

        # PowerShell
        self.write_file(self.root / "scripts/setup.ps1", """
Write-Host "Setting up Ultra Video Creator..."
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Set-Location frontend; npm install; Set-Location ..
docker-compose up -d
Write-Host "Project ready. Run 'npm run dev' in frontend."
""")

    def build(self):
        self.create_structure()
        self.generate_backend()
        self.generate_frontend()
        self.create_scripts()
        print(f"✅ Full project generated at: {self.root.absolute()}")
        print("Next steps: cd into folder and run ./scripts/setup.sh")

if __name__ == "__main__":
    builder = ProjectBuilder()
    builder.build()
