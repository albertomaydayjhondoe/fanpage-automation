#!/usr/bin/env python3
"""
DOWNLOAD_FROM_DRIVE.PY
Descarga videos desde Google Drive
"""

import os
import json
import logging
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DriveDownloader:
    def __init__(self):
        credentials_json = os.getenv("GOOGLE_CREDENTIALS")
        
        if not credentials_json:
            raise ValueError("GOOGLE_CREDENTIALS not found")
        
        credentials_dict = json.loads(credentials_json)
        
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        
        self.service = build('drive', 'v3', credentials=credentials)
        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        
        logger.info("✅ DriveDownloader inicializado")
    
    def download_videos(self, output_dir="media/GeneratedVideos"):
        """Descarga videos desde Google Drive"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Buscar archivos en la carpeta
        query = f"'{self.folder_id}' in parents and mimeType='video/mp4'"
        
        results = self.service.files().list(
            q=query,
            fields="files(id, name)",
            pageSize=100
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            logger.warning("⚠️  No hay videos para descargar")
            return []
        
        logger.info(f"📥 Descargando {len(files)} videos...")
        
        downloaded = []
        
        for file in files:
            try:
                request = self.service.files().get_media(fileId=file['id'])
                
                file_path = output_path / file['name']
                
                fh = io.FileIO(str(file_path), 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                logger.info(f"✅ Descargado: {file['name']}")
                downloaded.append(file['name'])
                
            except Exception as e:
                logger.error(f"❌ Error descargando {file['name']}: {str(e)}")
        
        logger.info(f"✅ Total descargados: {len(downloaded)}/{len(files)}")
        return downloaded

def main():
    logger.info("="*60)
    logger.info("DOWNLOAD_FROM_DRIVE - Iniciando")
    logger.info("="*60)
    
    downloader = DriveDownloader()
    downloader.download_videos()
    
    logger.info("✅ Download completado")

if __name__ == "__main__":
    main()
