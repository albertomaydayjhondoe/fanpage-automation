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
        """Constructor - Inicializa el generador de videos"""
        # Leer API key desde .env
        self.runway_api_key = os.getenv("RUNWAY_API_KEY")
        
        if not self.runway_api_key:
            logger.error("❌ RUNWAY_API_KEY no encontrada en .env")
            raise ValueError("RUNWAY_API_KEY no configurada")
        
        self.runway_url = "https://api.runwayml.com/v1"
        self.output_dir = Path("media/GeneratedVideos")

        # Crear carpeta si no existe
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ VideoGenerator inicializado")
        logger.info(f"📁 Directorio de salida: {self.output_dir}")
    
    def get_random_prompt(self):
        """Retorna un prompt aleatorio para generar video"""
        prompts = [
            "Coche deportivo en autopista nocturna, neón azul, lluvia intensa, atmósfera cyberpunk",
            "Joker riendo en caos urbano, colores dorados y púrpura, atmósfera psicológica",
            "Escena de robo estilo GTA, dinero volando, persecución urbana nocturna",
            "Pelea de anime épica, efectos luminosos, explosión de colores vibrantes",
            "Ciudad futurista con neón, código digital cayendo, atmósfera Matrix",
            "Lamborghini acelerando en túnel con luces, efecto motion blur",
            "Samurai en combate bajo la lluvia, slow motion, estética cinematográfica",
            "Explosión urbana con partículas, cámara lenta, colores saturados",
        ]
        
        selected = random.choice(prompts)
        logger.info(f"📝 Prompt seleccionado: {selected[:60]}...")
        return selected
    
    def generate_with_runway(self, prompt, video_id):
        """
        Llama a Runway API para generar video
        
        Args:
            prompt (str): Descripción del video a generar
            video_id (str): ID único del video
            
        Returns:
            str: URL del video generado, o None si falla
        """
        try:
            logger.info(f"🎬 Generando video {video_id}...")
            
            # Headers con autorización
            headers = {
                "Authorization": f"Bearer {self.runway_api_key}",
                "Content-Type": "application/json"
            }
            
            # Payload con configuración del video
            payload = {
                "prompt": prompt,
                "duration": 20,  # 20 segundos
                "format": "mp4",
                "quality": "high"
            }
            
            # POST request a Runway API
            response = requests.post(
                f"{self.runway_url}/generate",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            # Verificar respuesta
            if response.status_code == 200:
                result = response.json()
                video_url = result.get("video_url")
                logger.info(f"✅ Video generado exitosamente")
                logger.info(f"🔗 URL: {video_url}")
                return video_url
            else:
                logger.error(f"❌ Error API: {response.status_code}")
                logger.error(f"Respuesta: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"❌ Timeout esperando respuesta de Runway API")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error(f"❌ Error de conexión a Runway API")
            return None
            
        except Exception as e:
            logger.error(f"❌ Exception inesperada: {str(e)}")
            return None
    
    def download_video(self, video_url, video_id):
        """
        Descarga video desde URL a disco local
        
        Args:
            video_url (str): URL del video a descargar
            video_id (str): ID del video
            
        Returns:
            str: Ruta del archivo descargado, o None si falla
        """
        try:
            logger.info(f"📥 Descargando {video_id}...")
            
            # GET request para descargar
            response = requests.get(video_url, timeout=120)
            
            if response.status_code == 200:
                # Generar nombre de archivo con timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = self.output_dir / f"{video_id}_{timestamp}.mp4"
                
                # Guardar archivo
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content) / (1024 * 1024)  # MB
                logger.info(f"✅ Guardado en: {filename}")
                logger.info(f"📦 Tamaño: {file_size:.2f} MB")
                return str(filename)
            else:
                logger.error(f"❌ Error descargando: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Exception descargando: {str(e)}")
            return None
    
    def generate_batch(self, num_videos=5):
        """
        Genera múltiples videos en batch
        
        Args:
            num_videos (int): Número de videos a generar
            
        Returns:
            list: Lista de videos generados exitosamente
        """
        logger.info(f"🚀 Iniciando batch: {num_videos} videos")
        
        generated = []
        
        for idx in range(num_videos):
            # Generar ID único
            video_id = f"vid_{datetime.now().strftime('%Y%m%d')}_{idx:02d}"
            
            logger.info(f"\n{'='*50}")
            logger.info(f"VIDEO {idx+1}/{num_videos} - ID: {video_id}")
            logger.info(f"{'='*50}")
            
            # PASO 1: Obtener prompt aleatorio
            prompt = self.get_random_prompt()
            
            # PASO 2: Generar video con Runway
            video_url = self.generate_with_runway(prompt, video_id)
            
            if video_url:
                # PASO 3: Descargar video
                video_path = self.download_video(video_url, video_id)
                
                if video_path:
                    generated.append({
                        "video_id": video_id,
                        "prompt": prompt,
                        "path": video_path,
                        "url": video_url,
                        "timestamp": datetime.now().isoformat()
                    })
                    logger.info(f"✅ Video {idx+1} completado exitosamente")
                else:
                    logger.warning(f"⚠️  Video {idx+1} generado pero no descargado")
            else:
                logger.warning(f"⚠️  Video {idx+1} falló en generación")
            
            # PASO 4: Delay entre videos (no saturar API)
            if idx < num_videos - 1:
                delay = random.uniform(15, 30)
                logger.info(f"⏳ Esperando {delay:.0f}s antes del siguiente video...")
                time.sleep(delay)
        
        # Resumen final
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ BATCH COMPLETO: {len(generated)}/{num_videos} exitosos")
        logger.info(f"{'='*60}")
        
        # Guardar resumen en JSON
        if generated:
            summary_file = Path("logs") / f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(summary_file, 'w') as f:
                json.dump(generated, f, indent=2)
            logger.info(f"📄 Resumen guardado en: {summary_file}")
        
        return generated


def main():
    """Función principal"""
    print("\n" + "🎬"*30)
    print("AUTO_GENERATE.PY - GENERADOR AUTOMÁTICO DE VIDEOS")
    print("🎬"*30 + "\n")
    
    logger.info("="*60)
    logger.info("Iniciando proceso de generación")
    logger.info("="*60)
    
    try:
        # Crear generador
        generator = VideoGenerator()
        
        # Generar 5 videos
        results = generator.generate_batch(num_videos=5)
        
        # Mostrar resultados
        if results:
            logger.info(f"\n✅ Proceso completado exitosamente")
            logger.info(f"📊 Videos generados: {len(results)}")
            logger.info(f"📁 Ubicación: media/GeneratedVideos/")
        else:
            logger.warning(f"\n⚠️  No se generó ningún video")
            
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        logger.error(f"\n❌ Error fatal: {str(e)}")
        raise
    finally:
        logger.info("\n" + "="*60)
        logger.info("Proceso finalizado")
        logger.info("="*60 + "\n")


if __name__ == "__main__":
    main()