#!/usr/bin/env python3
"""
UPLOAD_TO_DRIVE.PY
Sube videos editados a Google Drive
"""

import os
import json
import logging
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DriveUploader:
    def __init__(self):
        # Leer credenciales desde variable de entorno (GitHub Actions)
        credentials_json = os.getenv("GOOGLE_CREDENTIALS")
        
        if not credentials_json:
            raise ValueError("GOOGLE_CREDENTIALS not found in environment")
        
        credentials_dict = json.loads(credentials_json)
        
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        
        self.service = build('drive', 'v3', credentials=credentials)
        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        
        logger.info("✅ DriveUploader inicializado")
    
    def upload_videos(self, directory="media/EditedVideos"):
        """Sube todos los videos de un directorio"""
        video_dir = Path(directory)
        videos = list(video_dir.glob("*.mp4"))
        
        if not videos:
            logger.warning(f"⚠️  No hay videos en {directory}")
            return []
        
        logger.info(f"📤 Subiendo {len(videos)} videos...")
        
        uploaded = []
        
        for video_path in videos:
            try:
                file_metadata = {
                    'name': video_path.name,
                    'parents': [self.folder_id] if self.folder_id else []
                }
                
                media = MediaFileUpload(str(video_path), mimetype='video/mp4')
                
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink'
                ).execute()
                
                logger.info(f"✅ Subido: {file.get('name')} (ID: {file.get('id')})")
                uploaded.append(file)
                
            except Exception as e:
                logger.error(f"❌ Error subiendo {video_path.name}: {str(e)}")
        
        logger.info(f"✅ Total subidos: {len(uploaded)}/{len(videos)}")
        return uploaded

def main():
    logger.info("="*60)
    logger.info("UPLOAD_TO_DRIVE - Iniciando")
    logger.info("="*60)
    
    uploader = DriveUploader()
    uploader.upload_videos()
    
    logger.info("✅ Upload completado")

if __name__ == "__main__":
    main()
