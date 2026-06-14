name=keep_alive.py
"""
🏓 ระบบ Keep-Alive สำหรับ Render.com
Ping URL ตัวเอง ทุก 5 นาที เพื่อให้บอทไม่หลับ
"""
import requests
import asyncio
import logging
from threading import Thread
from time import sleep

logger = logging.getLogger("KeepAlive")

class KeepAlive:
    """ระบบ Keep-Alive สำหรับ Render"""
    
    def __init__(self, url: str = None):
        """
        Args:
            url: URL ของ Render App (เช่น https://your-app-name.onrender.com)
        """
        self.url = url or "http://localhost:8080"
        self.is_running = False
    
    def ping(self):
        """Ping URL เพื่อให้บอทไม่หลับ"""
        try:
            response = requests.get(f"{self.url}/ping", timeout=10)
            if response.status_code == 200:
                logger.info(f"✅ Keep-Alive Ping สำเร็จ: {response.json().get('message', 'Pong!')}")
                return True
            else:
                logger.warning(f"⚠️ Keep-Alive ได้ Status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Keep-Alive Ping ล้มเหลว: {e}")
            return False
    
    def start(self):
        """เริ่มต้น Keep-Alive ในเธรด"""
        self.is_running = True
        thread = Thread(target=self._run_keep_alive, daemon=True)
        thread.start()
        logger.info("✅ Keep-Alive Thread เริ่มต้นแล้ว")
    
    def _run_keep_alive(self):
        """Loop สำหรับ Ping ทุก 5 นาที"""
        while self.is_running:
            try:
                sleep(300)  # 5 นาที
                self.ping()
            except Exception as e:
                logger.error(f"❌ Error ใน Keep-Alive: {e}")
                sleep(60)  # ถ้าผิดพลาด ลองใหม่ใน 1 นาที

# ใช้งาน
if __name__ == "__main__":
    # ตั้ง URL ของ Render App ของคุณ
    RENDER_URL = "https://your-app-name.onrender.com"  # แก้ให้เป็น URL จริง
    
    keep_alive = KeepAlive(url=RENDER_URL)
    keep_alive.start()
    
    # ให้เธรดทำงาน
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Keep-Alive หยุดทำงาน")
        keep_alive.is_running = False
