#!/usr/bin/env python3
"""Quick test script for new features."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all new modules can be imported."""
    print("Testing imports...")
    
    try:
        from db.models import SocialSignals
        print("✓ SocialSignals model imported")
    except Exception as e:
        print(f"✗ SocialSignals import failed: {e}")
        return False
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'social_fetcher', 
            'social-signals-service/social_fetcher.py'
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("✓ SocialSignalsFetcher imported")
    except Exception as e:
        print(f"✗ SocialSignalsFetcher import failed: {e}")
        return False
    
    try:
        from api.main import app
        print("✓ API app imported")
        
        # Check for new endpoints
        routes = [r.path for r in app.routes if hasattr(r, 'path') and r.path]
        new_endpoints = [
            r for r in routes 
            if 'social' in r.lower() or 'use-case' in r.lower()
        ]
        
        if new_endpoints:
            print(f"✓ New endpoints found: {len(new_endpoints)}")
            for endpoint in sorted(new_endpoints):
                print(f"  - {endpoint}")
        else:
            print("✗ New endpoints not found")
            return False
            
    except Exception as e:
        print(f"✗ API import failed: {e}")
        return False
    
    return True

def test_social_fetcher():
    """Test social signals fetcher."""
    print("\nTesting SocialSignalsFetcher...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'social_fetcher', 
            'social-signals-service/social_fetcher.py'
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        fetcher = module.SocialSignalsFetcher()
        print("✓ SocialSignalsFetcher instantiated")
        print(f"  - Has fetch_all_signals: {hasattr(fetcher, 'fetch_all_signals')}")
        print(f"  - Has fetch_reddit_signals: {hasattr(fetcher, 'fetch_reddit_signals')}")
        print(f"  - Has fetch_hn_signals: {hasattr(fetcher, 'fetch_hn_signals')}")
        return True
    except Exception as e:
        print(f"✗ SocialSignalsFetcher test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_model():
    """Test database model."""
    print("\nTesting database model...")
    
    try:
        from db.models import SocialSignals
        from db.connection import SessionLocal
        
        # Check if table exists (won't create it, just check structure)
        print("✓ SocialSignals model structure:")
        print(f"  - Table name: {SocialSignals.__tablename__}")
        print(f"  - Columns: {[c.name for c in SocialSignals.__table__.columns]}")
        
        # Test database connection
        db = SessionLocal()
        print("✓ Database connection successful")
        db.close()
        
        return True
    except Exception as e:
        print(f"✗ Database model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing New Features: Social Signals & Use-Case Finder")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Social Fetcher", test_social_fetcher()))
    results.append(("Database Model", test_database_model()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! Features are ready to use.")
        print("\nNext steps:")
        print("1. Run database migration to create social_signals table")
        print("2. Start API: python api/main.py")
        print("3. Test endpoints: curl http://localhost:8000/use-case-finder?query=build+API")
    else:
        print("✗ Some tests failed. Check errors above.")
    print("=" * 60)
    
    sys.exit(0 if all_passed else 1)

