#!/usr/bin/env python3
"""Quick test to verify token is loaded."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

token = os.getenv("TELEGRAM_BOT_TOKEN", "")

if token:
    print("✅ Token found!")
    print(f"   Token length: {len(token)}")
    print(f"   Token starts with: {token[:10]}...")
else:
    print("❌ Token not found!")
    print("   Check .env file in parent directory")


