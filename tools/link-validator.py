#!/usr/bin/env python3
"""
Link Validator for Awesome Generative AI
Validates all URLs in README.md and DISCOVERIES.md to check for broken/dead links.
"""

import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from collections import defaultdict

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("❌ Error: 'requests' library not found.")
    print("   Install it with: pip install requests")
    sys.exit(1)

class LinkValidator:
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set a user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Awesome-List-Link-Validator/1.0)'
        })
        
        self.results = {
            'valid': [],
            'broken': [],
            'timeout': [],
            'skipped': [],
            'errors': []
        }
        
    def extract_links(self, content, source_file):
        """Extract all markdown links from content."""
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.findall(pattern, content)
        
        links = []
        for name, url in matches:
            # Skip anchor links and mailto links
            if url.startswith('#') or url.startswith('mailto:'):
                continue
            
            # Handle relative links
            if not url.startswith('http'):
                continue
                
            links.append({
                'name': name.strip(),
                'url': url.strip(),
                'source_file': source_file
            })
        
        return links
    
    def validate_link(self, link_info):
        """Validate a single link."""
        url = link_info['url']
        name = link_info['name']
        source = link_info['source_file']
        
        # Skip certain domains that might block automated requests
        skip_domains = ['twitter.com', 'x.com', 'linkedin.com']
        domain = urlparse(url).netloc.lower()
        if any(skip in domain for skip in skip_domains):
            self.results['skipped'].append({
                **link_info,
                'reason': 'Domain skipped (may block automated requests)'
            })
            return
        
        try:
            # Use HEAD request first (faster), fall back to GET if needed
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            
            # Some servers don't support HEAD, try GET
            if response.status_code == 405:
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True, stream=True)
            
            status_code = response.status_code
            
            if 200 <= status_code < 400:
                self.results['valid'].append({
                    **link_info,
                    'status_code': status_code
                })
            else:
                self.results['broken'].append({
                    **link_info,
                    'status_code': status_code,
                    'reason': f'HTTP {status_code}'
                })
                
        except requests.exceptions.Timeout:
            self.results['timeout'].append({
                **link_info,
                'reason': 'Request timeout'
            })
        except requests.exceptions.ConnectionError as e:
            self.results['broken'].append({
                **link_info,
                'reason': f'Connection error: {str(e)[:100]}'
            })
        except requests.exceptions.TooManyRedirects:
            self.results['broken'].append({
                **link_info,
                'reason': 'Too many redirects'
            })
        except Exception as e:
            self.results['errors'].append({
                **link_info,
                'reason': f'Error: {str(e)[:100]}'
            })
    
    def validate_file(self, file_path):
        """Validate all links in a markdown file."""
        print(f"📄 Processing {file_path.name}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = self.extract_links(content, file_path.name)
        print(f"   Found {len(links)} links to validate")
        
        for i, link in enumerate(links, 1):
            print(f"   [{i}/{len(links)}] Checking: {link['name'][:50]}...", end='\r')
            self.validate_link(link)
            # Small delay to be respectful
            time.sleep(0.1)
        
        print(f"   [{len(links)}/{len(links)}] Complete!                    ")
    
    def print_summary(self):
        """Print validation summary."""
        total = (len(self.results['valid']) + 
                len(self.results['broken']) + 
                len(self.results['timeout']) + 
                len(self.results['skipped']) + 
                len(self.results['errors']))
        
        print("\n" + "=" * 70)
        print("Link Validation Summary")
        print("=" * 70)
        print(f"\n✅ Valid links:     {len(self.results['valid']):4d}")
        print(f"❌ Broken links:    {len(self.results['broken']):4d}")
        print(f"⏱️  Timeout links:   {len(self.results['timeout']):4d}")
        print(f"⏭️  Skipped links:   {len(self.results['skipped']):4d}")
        print(f"⚠️  Error links:     {len(self.results['errors']):4d}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📊 Total links:      {total:4d}")
        
        if self.results['broken']:
            print("\n❌ BROKEN LINKS:")
            print("-" * 70)
            for link in self.results['broken']:
                print(f"  • {link['name'][:40]:40s} | {link['reason']}")
                print(f"    {link['url']}")
                print(f"    ({link['source_file']})")
                print()
        
        if self.results['timeout']:
            print("\n⏱️  TIMEOUT LINKS (may need manual check):")
            print("-" * 70)
            for link in self.results['timeout']:
                print(f"  • {link['name'][:40]:40s}")
                print(f"    {link['url']}")
                print(f"    ({link['source_file']})")
                print()
        
        if self.results['errors']:
            print("\n⚠️  ERROR LINKS:")
            print("-" * 70)
            for link in self.results['errors']:
                print(f"  • {link['name'][:40]:40s} | {link['reason']}")
                print(f"    {link['url']}")
                print(f"    ({link['source_file']})")
                print()
    
    def save_report(self, output_path):
        """Save validation report to JSON."""
        import json
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total': (len(self.results['valid']) + 
                         len(self.results['broken']) + 
                         len(self.results['timeout']) + 
                         len(self.results['skipped']) + 
                         len(self.results['errors'])),
                'valid': len(self.results['valid']),
                'broken': len(self.results['broken']),
                'timeout': len(self.results['timeout']),
                'skipped': len(self.results['skipped']),
                'errors': len(self.results['errors'])
            },
            'results': self.results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Report saved to: {output_path}")

def main():
    repo_root = Path(__file__).parent.parent
    
    validator = LinkValidator(timeout=10, max_retries=2)
    
    # Validate README.md
    readme_path = repo_root / 'README.md'
    if readme_path.exists():
        validator.validate_file(readme_path)
    else:
        print(f"⚠️  README.md not found at {readme_path}")
    
    # Validate DISCOVERIES.md
    discoveries_path = repo_root / 'DISCOVERIES.md'
    if discoveries_path.exists():
        validator.validate_file(discoveries_path)
    else:
        print(f"⚠️  DISCOVERIES.md not found at {discoveries_path}")
    
    # Print summary
    validator.print_summary()
    
    # Save report
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    validator.save_report(output_dir / 'link-validation-report.json')
    
    # Exit with error code if broken links found
    if validator.results['broken'] or validator.results['errors']:
        print("\n⚠️  Validation completed with errors. Please review broken links.")
        sys.exit(1)
    else:
        print("\n✅ All links validated successfully!")
        sys.exit(0)

if __name__ == '__main__':
    main()



