#!/usr/bin/env python3
"""
BOT_ENGAGEMENT.PY
Bot agresivo de engagement para fanpages
"""

import os
import time
import random
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AggressiveBot:
    def __init__(self, fanpage_number):
        self.fanpage_number = fanpage_number
        self.api_key = os.getenv(f"TIKTOK_API_KEY_FANPAGE_{fanpage_number}")
        
        if not self.api_key:
            raise ValueError(f"API key no encontrada para fanpage {fanpage_number}")
        
        logger.info(f"🤖 Bot inicializado para Fanpage {fanpage_number}")
    
    def aggressive_like_loop(self, num_likes=200):
        """Da likes agresivamente"""
        logger.info(f"🔥 MODO AGRESIVO: {num_likes} likes")
        
        for i in range(num_likes):
            # Simula like
            logger.info(f"👍 Like {i+1}/{num_likes}")
            
            delay = random.uniform(30, 60)
            
            if i > 0 and i % 50 == 0:
                delay = random.uniform(300, 600)
                logger.info(f"⏸️  Break humano: {delay/60:.1f} min")
            
            time.sleep(delay)
        
        logger.info(f"✅ Ciclo completo")
    
    def aggressive_comment_loop(self, num_comments=50):
        """Comenta agresivamente"""
        comments = ["🔥", "Increíble", "Wow", "🎬"]
        
        for i in range(num_comments):
            comment = random.choice(comments)
            logger.info(f"💬 Comentario {i+1}: {comment}")
            time.sleep(random.uniform(120, 300))
        
        logger.info(f"✅ {num_comments} comentarios realizados")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fanpage', type=int, required=True)
    args = parser.parse_args()
    
    logger.info(f"{'='*60}")
    logger.info(f"BOT AGGRESSIVE - FANPAGE {args.fanpage}")
    logger.info(f"{'='*60}")
    
    bot = AggressiveBot(args.fanpage)
    bot.aggressive_like_loop(200)
    bot.aggressive_comment_loop(50)
    
    logger.info(f"✅ Bot completado")

if __name__ == "__main__":
    main()
