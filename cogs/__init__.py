"""
🎯 KIMNA AZURE LEGACY - Cogs Manager
"""
import os
import logging

logger = logging.getLogger("CogManager")

# ✅ Cogs ทั้งหมด
AVAILABLE_COGS = [
    "fun_commands",
    "games",
    "utility",
    "moderation",
    "economy",
    "stats",
    "role_system",
    "welcome",
    "music",
    "images",
]

__all__ = AVAILABLE_COGS
