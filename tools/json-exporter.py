#!/usr/bin/env python3
"""
JSON Exporter for Awesome Generative AI
Converts the markdown lists to structured JSON format for programmatic access.
"""

import re
import json
from pathlib import Path
from datetime import datetime

def parse_markdown_list(content, source_file):
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

def export_to_json():
    """Export both README and DISCOVERIES to JSON."""
    repo_root = Path(__file__).parent.parent
    
    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'source': 'awesome-generative-ai'
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
        
        output['main_list']['projects'] = parse_markdown_list(readme_content, 'README.md')
        output['main_list']['categories'] = extract_categories(readme_content)
    
    # Process DISCOVERIES
    discoveries_path = repo_root / 'DISCOVERIES.md'
    if discoveries_path.exists():
        with open(discoveries_path, 'r', encoding='utf-8') as f:
            discoveries_content = f.read()
        
        output['discoveries_list']['projects'] = parse_markdown_list(discoveries_content, 'DISCOVERIES.md')
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
    print("🔄 Exporting Awesome Generative AI to JSON...")
    data = export_to_json()
    
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    save_json(data, output_dir / 'awesome-generative-ai.json')
    save_minified_json(data, output_dir / 'awesome-generative-ai.min.json')
    
    print("\n✨ Export complete!")

