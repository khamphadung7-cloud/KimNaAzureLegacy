name=config.py
"""
⚙️ ไฟล์ตั้งค่าหลัก
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 🌐 ตั้งค่า Bot
BOT_CONFIG = {
    "name": "KIMNA AZURE LEGACY",
    "version": "1.0.0",
    "owner": "ToneyToyau",
    "prefix": "!",
    "color": (0, 150, 255),  # RGB Color
}

# 🔐 Environment Variables
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "YOUR_TOKEN_HERE")
FLASK_PORT = int(os.environ.get("PORT", 8080))
FLASK_HOST = os.environ.get("HOST", "0.0.0.0")

# 💰 ระบบราคา
PRICING = {
    "basic": {
        "name": "แพ็คเกจพื้นฐาน",
        "price": 0,
        "features": ["คำสั่งพื้นฐาน", "ตอบสนองแบบ Real-time"]
    },
    "premium": {
        "name": "แพ็คเกจพรีเมียม",
        "price": 99,
        "features": ["ทุกอย่างใน Basic", "ระบบ Database", "Support 24/7"]
    },
    "enterprise": {
        "name": "แพ็คเกจองค์กร",
        "price": 999,
        "features": ["ทุกอย่างใน Premium", "API Custom", "ตัวแทนสนับสนุนส่วนตัว"]
    }
}

# 📝 ลิงก์ที่สำคัญ
LINKS = {
    "support_server": "https://discord.gg/your-server",
    "github": "https://github.com/aulak11238-eng",
    "website": "https://yourwebsite.com"
}
