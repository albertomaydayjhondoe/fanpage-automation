#!/usr/bin/env python3
"""
BATCH_EDIT.PY
Edita videos con FFmpeg automáticamente
"""

import os
import subprocess
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/editing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VideoEditor:
    def __init__(self):
        self.input_dir = Path("media/GeneratedVideos")
        self.output_dir = Path("media/EditedVideos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def apply_filters(self, input_video, output_video):
        """Aplica filtros cinematográficos"""
        logger.info(f"✂️  Editando: {input_video.name}")
        
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(input_video),
            "-vf", (
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "eq=contrast=1.4:brightness=-0.15:saturation=0.8,"
                "colorchannelmixer=rr=1:gg=0.8:bb=1.3"
            ),
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "23",
            "-c:a", "aac",
            "-y",
            str(output_video)
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, capture_output=True, timeout=300)
            logger.info(f"✅ Video editado: {output_video.name}")
            return True
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return False
    
    def process_batch(self):
        """Procesa todos los videos"""
        logger.info("="*60)
        logger.info("BATCH_EDIT - Iniciando")
        logger.info("="*60)
        
        videos = list(self.input_dir.glob("*.mp4"))
        
        if not videos:
            logger.warning("⚠️  No hay videos para editar")
            return
        
        logger.info(f"Encontrados {len(videos)} videos")
        
        for video_path in videos:
            output_path = self.output_dir / f"edited_{video_path.name}"
            self.apply_filters(video_path, output_path)
        
        logger.info("✅ Edición completada")

def main():
    editor = VideoEditor()
    editor.process_batch()

if __name__ == "__main__":
    main()
