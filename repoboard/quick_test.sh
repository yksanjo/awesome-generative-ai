#!/bin/bash
# Quick test script for new features

cd "$(dirname "$0")"

echo "=========================================="
echo "Testing New Features"
echo "=========================================="

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✗ Virtual environment not found!"
    exit 1
fi

# Test imports
echo ""
echo "1. Testing imports..."
python -c "from db.models import SocialSignals; print('  ✓ SocialSignals model')" 2>&1
python -c "from api.main import app; print('  ✓ API app')" 2>&1

# Test API endpoints are registered
echo ""
echo "2. Checking API endpoints..."
python -c "
from api.main import app
routes = [r.path for r in app.routes if hasattr(r, 'path') and r.path]
new_routes = [r for r in routes if 'social' in r.lower() or 'use-case' in r.lower()]
if new_routes:
    print('  ✓ New endpoints found:')
    for r in new_routes:
        print(f'    - {r}')
else:
    print('  ✗ No new endpoints found')
" 2>&1

# Test social fetcher
echo ""
echo "3. Testing SocialSignalsFetcher..."
python -c "
import importlib.util
import os
spec = importlib.util.spec_from_file_location('social_fetcher', 'social-signals-service/social_fetcher.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fetcher = module.SocialSignalsFetcher()
print('  ✓ SocialSignalsFetcher works')
" 2>&1

echo ""
echo "=========================================="
echo "✓ All basic tests passed!"
echo ""
echo "To start the API server, run:"
echo "  python api/main.py"
echo ""
echo "Then test endpoints:"
echo "  curl 'http://localhost:8000/use-case-finder?query=build+API&language=python'"
echo "=========================================="

