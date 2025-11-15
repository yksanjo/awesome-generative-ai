#!/usr/bin/env python3
"""
Quick test script to verify RepoBoard setup.
Run this to check if everything is configured correctly.
"""

import sys
import os

print("=" * 50)
print("RepoBoard Setup Test")
print("=" * 50)

# Check 1: Python version
print("\n1. Checking Python version...")
print(f"   Python: {sys.version}")
if sys.version_info < (3, 9):
    print("   ⚠️  Warning: Python 3.9+ recommended")
else:
    print("   ✅ Python version OK")

# Check 2: Virtual environment
print("\n2. Checking virtual environment...")
venv_path = sys.prefix
if 'venv' in venv_path or 'virtualenv' in venv_path:
    print(f"   ✅ Virtual environment active: {venv_path}")
else:
    print(f"   ⚠️  Warning: May not be in virtual environment")
    print(f"   Current Python: {sys.executable}")

# Check 3: Dependencies
print("\n3. Checking dependencies...")
dependencies = {
    'sqlalchemy': 'SQLAlchemy',
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'pydantic': 'Pydantic',
    'requests': 'Requests',
    'telegram': 'python-telegram-bot',
}

missing = []
for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} - MISSING")
        missing.append(name)

if missing:
    print(f"\n   Install missing: pip install {' '.join(missing)}")

# Check 4: Environment variables
print("\n4. Checking environment variables...")
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    print("   ✅ .env file exists")
    with open(env_file, 'r') as f:
        content = f.read()
        if 'TELEGRAM_BOT_TOKEN' in content:
            print("   ✅ TELEGRAM_BOT_TOKEN found in .env")
        else:
            print("   ⚠️  TELEGRAM_BOT_TOKEN not in .env")
else:
    print("   ⚠️  .env file not found")

# Check 5: API files
print("\n5. Checking API files...")
api_main = os.path.join(os.path.dirname(__file__), 'api', 'main.py')
if os.path.exists(api_main):
    print("   ✅ api/main.py exists")
else:
    print("   ❌ api/main.py missing")

# Check 6: Bot files
print("\n6. Checking bot files...")
bot_main = os.path.join(os.path.dirname(__file__), 'telegram-bot', 'bot.py')
if os.path.exists(bot_main):
    print("   ✅ telegram-bot/bot.py exists")
else:
    print("   ❌ telegram-bot/bot.py missing")

# Check 7: Test API import
print("\n7. Testing API import...")
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from api import main
    print("   ✅ API imports successfully")
except Exception as e:
    print(f"   ❌ API import failed: {e}")

# Summary
print("\n" + "=" * 50)
if missing:
    print("❌ Some dependencies are missing. Install them first.")
    print(f"   Run: pip install {' '.join([d.lower().replace(' ', '-') for d in missing])}")
else:
    print("✅ Setup looks good! You can start the API and bot now.")
print("=" * 50)


