"""
🎯 KIMNA AZURE LEGACY - Cogs Manager
บัญชีรายการ Cogs ทั้งหมด
"""
import logging

logger = logging.getLogger("CogManager")

# ✅ Cogs ทั้งหมด (รวม 54 ไฟล์)
AVAILABLE_COGS = [
    # 🏗️ ระบบการตั้งค่า
    "all_in_one",           # ✨ สร้างเซิร์ฟเวอร์อัตโนมัติ
    "config",                # ⚙️ ตั้งค่าทั่วไป
    
    # 👥 ระบบสมาชิก
    "welcome",               # 👋 ต้อนรับสมาชิกใหม่
    "verification",          # ✅ ยืนยันตัวตน
    "member_info",           # ℹ️ ข้อมูลสมาชิก
    
    # 👑 ระบบยศ/บทบาท
    "role_system",           # 👑 ระบบยศ
    "auto_role",             # ⚡ ให้ยศอัตโนมัติ
    "self_roles",            # 🎯 ยศเลือกเอง
    "reaction_roles",        # 😊 ยศจากรีแอคชั่น
    "color_roles",           # 🎨 ยศสี
    
    # 💬 ห้องแชท
    "moderation",            # ⚔️ การควบคุม
    "automod",               # 🤖 อัตโนมัติ
    "word_filter",           # 🚫 กรองคำ
    "slowmode",              # ⏱️ Slow Mode
    "random_mute",           # 🔇 Mute สุ่ม
    
    # 💰 ระบบเศรษฐกิจ
    "economy",               # 💵 เศรษฐกิจ
    "bank_system",           # 🏦 ธนาคาร
    "levelup",               # 📈 ระดับ/เลเวล
    
    # 🎮 ความบันเทิง
    "fun_commands",          # 🎉 คำสั่งสนุก
    "games",                 # 🎯 เกม
    "trivia",                 # 🧠 ข้อมูลทั่วไป
    "music",                 # 🎵 ดนตรี
    
    # 📊 ระบบตรวจสอบ
    "logging",               # 📋 บันทึก
    "stats",                 # 📈 สถิติ
    "invite_tracker",        # 🔗 ติดตามคำเชิญ
    "starboard",             # ⭐ บอร์ดดาว
    
    # 📢 ระบบประกาศ/เกิวอะเวย์
    "giveaway",              # 🎁 แจกของ
    "announcement",          # 📢 ประกาศ (ถ้ามี)
    "bump_reminder",         # 📌 เตือนแบมป์
    "reminder",              # 📝 เตือนความจำ
    "scheduler",             # ⏰ ตั้งเวลา
    
    # 🎫 ระบบอื่นๆ
    "ticket",                # 🎫 ตั๋ว
    "report_system",         # ⚠️ ระบบรายงาน
    "poll_system",           # 🗳️ โพล
    "afk_system",            # 💤 AFK
    "antiraid",              # 🛡️ ป้องกัน Raid
    
    # 🏠 ยูทิลิตี้
    "utility",               # 🔧 เครื่องมือ
    "help_command",          # 📖 คำสั่ง Help
    "error_handler",         # ❌ จัดการ Error
    
    # 🎵 ระบบเสียง
    "voice_auto",            # 🔊 สร้างห้องเสียงอัตโนมัติ
    
    # 📝 ระบบอื่น
    "custom_commands",       # ✨ คำสั่งที่กำหนดเอง
    "nickname_system",       # 📛 ระบบชื่อเล่น
    "mod_notes",             # 📝 หมายเหตุ Mod
    "database",              # 🗄️ ฐานข้อมูล
    
    # 🆕 10 Cogs ใหม่
    "crypto_tracker",        # 🪙 Crypto
    "fortune_telling",       # 🔮 บอกดวง
    "image_editor",          # 🎨 แต่งรูป
    "dm_system",             # 💬 DM
    "ai_chat",               # 🤖 AI Chat
    "achievement",           # 🏆 Achievement
    "cleverbot",             # 💭 CleverBot
    "auto_respond",          # 🔄 Auto Respond
    "gpt_simple",            # 🧠 Simple GPT
    "stats_tracker",         # 📊 Stats
]

__all__ = AVAILABLE_COGS

logger.info(f"✅ Loaded {len(AVAILABLE_COGS)} Cogs")
