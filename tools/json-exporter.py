#!/usr/bin/env python3
"""
JSON Exporter for Awesome Generative AI
Converts the markdown lists to structured JSON format for programmatic access.
"""

import re
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

def parse_markdown_list(content, source_file, fetch_github_stats_flag=False, github_token=None):
    """Parse markdown content and extract structured data."""
    projects = []
    current_section = None
    current_subsection = None
    
    lines = content.split('\n')
    
    for line in lines:
        # Main section (##)
        if line.startswith('## '):
            current_section = line.replace('## ', '').strip()
            current_subsection = None
        # Subsection (###)
        elif line.startswith('### '):
            current_subsection = line.replace('### ', '').strip()
        # Project entry: [Name](URL) - Description
        elif re.match(r'^\s*-\s*\[', line):
            match = re.match(r'^\s*-\s*\[([^\]]+)\]\(([^\)]+)\)\s*-\s*(.+)$', line)
            if match:
                name, url, description = match.groups()
                
                # Check for #opensource tag
                is_opensource = '#opensource' in line.lower()
                
                # Extract GitHub link if present
                github_link = None
                if 'github.com' in url:
                    github_link = url
                
                project = {
                    'name': name.strip(),
                    'url': url.strip(),
                    'description': description.strip().rstrip('.'),
                    'section': current_section,
                    'subsection': current_subsection,
                    'opensource': is_opensource,
                    'source_file': source_file
                }
                
                if github_link:
                    project['github'] = github_link
                    
                    # Optionally fetch GitHub stats
                    if fetch_github_stats_flag:
                        print(f"   Fetching stats for {name[:40]:40s}...", end='\r')
                        stats = fetch_github_stats(github_link, github_token)
                        if stats:
                            project['github_stats'] = stats
                        time.sleep(0.5)  # Rate limiting
                
                projects.append(project)
    
    return projects

def extract_categories(content):
    """Extract all categories and their hierarchy."""
    categories = []
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('## '):
            category = line.replace('## ', '').strip()
            categories.append({
                'name': category,
                'level': 1,
                'type': 'section'
            })
        elif line.startswith('### '):
            subcategory = line.replace('### ', '').strip()
            categories.append({
                'name': subcategory,
                'level': 2,
                'type': 'subsection'
            })
    
    return categories

def extract_github_repo_info(github_url):
    """Extract owner and repo name from GitHub URL."""
    # Handle various GitHub URL formats
    patterns = [
        r'github\.com/([^/]+)/([^/?#]+)',
        r'github\.com/([^/]+)/([^/?#]+)/?$',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, github_url)
        if match:
            return match.group(1), match.group(2).rstrip('/')
    return None, None

def fetch_github_stats(github_url, github_token=None):
    """Fetch GitHub repository statistics (stars, forks, etc.)."""
    owner, repo = extract_github_repo_info(github_url)
    if not owner or not repo:
        return None
    
    # Use GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    else:
        headers['Accept'] = 'application/vnd.github.v3+json'
    
    try:
        import requests
        response = requests.get(api_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'watchers': data.get('watchers_count', 0),
                'open_issues': data.get('open_issues_count', 0),
                'language': data.get('language'),
                'updated_at': data.get('updated_at'),
                'created_at': data.get('created_at'),
                'description': data.get('description'),
                'archived': data.get('archived', False)
            }
        elif response.status_code == 404:
            # Repository not found or private
            return None
        elif response.status_code == 403:
            # Rate limited or forbidden
            return {'error': 'rate_limited'}
        else:
            return None
    except ImportError:
        # requests not available
        return None
    except Exception:
        # Any other error
        return None

def export_to_json(fetch_github_stats=False, github_token=None):
    """Export both README and DISCOVERIES to JSON."""
    repo_root = Path(__file__).parent.parent
    
    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'source': 'awesome-generative-ai',
            'github_stats_included': fetch_github_stats
        },
        'main_list': {
            'projects': [],
            'categories': []
        },
        'discoveries_list': {
            'projects': [],
            'categories': []
        }
    }
    
    # Process main README
    readme_path = repo_root / 'README.md'
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        print("📄 Processing README.md...")
        output['main_list']['projects'] = parse_markdown_list(
            readme_content, 'README.md', fetch_github_stats, github_token
        )
        output['main_list']['categories'] = extract_categories(readme_content)
    
    # Process DISCOVERIES
    discoveries_path = repo_root / 'DISCOVERIES.md'
    if discoveries_path.exists():
        with open(discoveries_path, 'r', encoding='utf-8') as f:
            discoveries_content = f.read()
        
        print("📄 Processing DISCOVERIES.md...")
        output['discoveries_list']['projects'] = parse_markdown_list(
            discoveries_content, 'DISCOVERIES.md', fetch_github_stats, github_token
        )
        output['discoveries_list']['categories'] = extract_categories(discoveries_content)
    
    # Add summary statistics
    output['statistics'] = {
        'main_list': {
            'total_projects': len(output['main_list']['projects']),
            'opensource_projects': sum(1 for p in output['main_list']['projects'] if p.get('opensource')),
            'total_categories': len(output['main_list']['categories'])
        },
        'discoveries_list': {
            'total_projects': len(output['discoveries_list']['projects']),
            'opensource_projects': sum(1 for p in output['discoveries_list']['projects'] if p.get('opensource')),
            'total_categories': len(output['discoveries_list']['categories'])
        },
        'total': {
            'total_projects': len(output['main_list']['projects']) + len(output['discoveries_list']['projects']),
            'total_opensource': sum(1 for p in output['main_list']['projects'] + output['discoveries_list']['projects'] if p.get('opensource'))
        }
    }
    
    return output

def save_json(data, output_path):
    """Save data as JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON exported to: {output_path}")
    print(f"   Total projects: {data['statistics']['total']['total_projects']}")

def save_minified_json(data, output_path):
    """Save data as minified JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
    print(f"✅ Minified JSON exported to: {output_path}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Export Awesome Generative AI to JSON')
    parser.add_argument('--github-stats', action='store_true',
                        help='Fetch GitHub statistics (stars, forks, etc.) for GitHub projects')
    parser.add_argument('--github-token', type=str, default=None,
                        help='GitHub personal access token (optional, increases rate limit)')
    args = parser.parse_args()
    
    print("🔄 Exporting Awesome Generative AI to JSON...")
    if args.github_stats:
        print("📊 GitHub stats will be fetched (this may take a while)...")
        if not args.github_token:
            print("⚠️  No GitHub token provided. Using unauthenticated API (60 requests/hour limit)")
    
    data = export_to_json(args.github_stats, args.github_token)
    
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    save_json(data, output_dir / 'awesome-generative-ai.json')
    save_minified_json(data, output_dir / 'awesome-generative-ai.min.json')
    
    print("\n✨ Export complete!")

