#!/usr/bin/env python3
"""
AUTO_GENERATE.PY
Genera videos automáticamente usando Runway API
"""

import os
import json
import time
import random
import logging
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VideoGenerator:
    def __init__(self):
        """Inicializa el generador de videos"""
        self.runway_api_key = os.getenv("RUNWAY_API_KEY")
        self.runway_url = "https://api.runwayml.com/v1"
        self.output_dir = Path("media/GeneratedVideos")
        
        # Crear carpeta si no existe
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ VideoGenerator inicializado")
    
    def get_random_prompt(self):
        """Retorna un prompt aleatorio para generar video"""
        prompts = [
            "Coche en autopista nocturna, neón azul, lluvia, beat trap agresivo",
            "Joker riendo, caos psicológico, colores dorados, beat trap power",
            "Robo GTA, dinero volando, persecución urbana, beat trap heavy",
            "Pelea anime, efectos glow, colores explotan, beat trap intenso",
            "Neon futuro, ciudad digital, código corriendo, beat trap minimalista",
        ]
        
        selected = random.choice(prompts)
        logger.info(f"📝 Prompt seleccionado: {selected[:50]}...")
        return selected
    
    def generate_with_runway(self, prompt, video_id):
        """Llama Runway API para generar video"""
        try:
            logger.info(f"🎬 Generando video {video_id}...")
            
            headers = {
                "Authorization": f"Bearer {self.runway_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": prompt,
                "duration": 20,
                "format": "mp4",
                "quality": "high"
            }
            
            response = requests.post(
                f"{self.runway_url}/generate",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                video_url = result.get("video_url")
                logger.info(f"✅ Video generado: {video_url}")
                return video_url
            else:
                logger.error(f"❌ Error API: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Exception: {str(e)}")
            return None
    
    def download_video(self, video_url, video_id):
        """Descarga video desde URL"""
        try:
            logger.info(f"📥 Descargando {video_id}...")
            
            response = requests.get(video_url, timeout=120)
            
            if response.status_code == 200:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{self.output_dir}/{video_id}_{timestamp}.mp4"
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"✅ Guardado en: {filename}")
                return filename
            else:
                logger.error(f"❌ Error descargando: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Exception: {str(e)}")
            return None
    
    def generate_batch(self, num_videos=5):
        """Genera N videos en batch"""
        logger.info(f"🚀 Iniciando batch: {num_videos} videos")
        
        generated = []
        
        for idx in range(num_videos):
            video_id = f"vid_{datetime.now().strftime('%Y%m%d')}__{idx:02d}"
            
            prompt = self.get_random_prompt()
            video_url = self.generate_with_runway(prompt, video_id)
            
            if video_url:
                video_path = self.download_video(video_url, video_id)
                
                if video_path:
                    generated.append({
                        "video_id": video_id,
                        "prompt": prompt,
                        "path": video_path
                    })
            
            if idx < num_videos - 1:
                delay = random.uniform(15, 30)
                logger.info(f"⏳ Esperando {delay:.0f}s...")
                time.sleep(delay)
        
        logger.info(f"✅ Batch completo: {len(generated)}/{num_videos}")
        return generated

def main():
    """Función principal"""
    logger.info("="*60)
    logger.info("AUTO_GENERATE.PY - Iniciando")
    logger.info("="*60)
    
    generator = VideoGenerator()
    generator.generate_batch(num_videos=5)
    
    logger.info("✅ Ejecución completada")

if __name__ == "__main__":
    main()
