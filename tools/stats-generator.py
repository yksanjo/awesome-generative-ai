#!/usr/bin/env python3
"""
Stats Generator for Awesome Generative AI
Generates statistics about the repository that can be shared on social media or documentation.
"""

import re
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def extract_links_from_markdown(content):
    """Extract all markdown links from content."""
    # Pattern: [text](url)
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    matches = re.findall(pattern, content)
    return matches

def count_projects_by_category(content):
    """Count projects in each category."""
    categories = defaultdict(int)
    current_category = None
    
    lines = content.split('\n')
    for line in lines:
        # Check for category headers (## or ###)
        if line.startswith('## '):
            current_category = line.replace('## ', '').strip()
        elif line.startswith('### '):
            current_category = line.replace('### ', '').strip()
        
        # Count links in each category
        if current_category and re.search(r'\[.*?\]\(.*?\)', line):
            categories[current_category] += 1
    
    return categories

def extract_opensource_projects(content):
    """Count open source projects marked with #opensource."""
    opensource_pattern = r'#opensource'
    matches = re.findall(opensource_pattern, content, re.IGNORECASE)
    return len(matches)

def generate_stats():
    """Generate comprehensive statistics about the repository."""
    repo_root = Path(__file__).parent.parent
    
    stats = {
        'generated_at': datetime.now().isoformat(),
        'main_list': {},
        'discoveries_list': {},
        'total': {}
    }
    
    # Analyze main README
    readme_path = repo_root / 'README.md'
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        links = extract_links_from_markdown(readme_content)
        categories = count_projects_by_category(readme_content)
        opensource_count = extract_opensource_projects(readme_content)
        
        stats['main_list'] = {
            'total_projects': len(links),
            'categories': dict(categories),
            'opensource_projects': opensource_count,
            'total_categories': len(categories)
        }
    
    # Analyze Discoveries list
    discoveries_path = repo_root / 'DISCOVERIES.md'
    if discoveries_path.exists():
        with open(discoveries_path, 'r', encoding='utf-8') as f:
            discoveries_content = f.read()
        
        links = extract_links_from_markdown(discoveries_content)
        categories = count_projects_by_category(discoveries_content)
        opensource_count = extract_opensource_projects(discoveries_content)
        
        stats['discoveries_list'] = {
            'total_projects': len(links),
            'categories': dict(categories),
            'opensource_projects': opensource_count,
            'total_categories': len(categories)
        }
    
    # Calculate totals
    stats['total'] = {
        'total_projects': stats['main_list'].get('total_projects', 0) + stats['discoveries_list'].get('total_projects', 0),
        'total_opensource': stats['main_list'].get('opensource_projects', 0) + stats['discoveries_list'].get('opensource_projects', 0)
    }
    
    return stats

def print_stats(stats):
    """Print statistics in a readable format."""
    print("=" * 60)
    print("Awesome Generative AI - Repository Statistics")
    print("=" * 60)
    print(f"\nGenerated: {stats['generated_at']}\n")
    
    print("📊 MAIN LIST")
    print("-" * 60)
    main = stats['main_list']
    print(f"Total Projects: {main.get('total_projects', 0)}")
    print(f"Open Source Projects: {main.get('opensource_projects', 0)}")
    print(f"Categories: {main.get('total_categories', 0)}")
    
    if main.get('categories'):
        print("\nTop Categories:")
        sorted_cats = sorted(main['categories'].items(), key=lambda x: x[1], reverse=True)[:10]
        for cat, count in sorted_cats:
            print(f"  • {cat}: {count}")
    
    print("\n🔍 DISCOVERIES LIST")
    print("-" * 60)
    disc = stats['discoveries_list']
    print(f"Total Projects: {disc.get('total_projects', 0)}")
    print(f"Open Source Projects: {disc.get('opensource_projects', 0)}")
    print(f"Categories: {disc.get('total_categories', 0)}")
    
    print("\n📈 TOTALS")
    print("-" * 60)
    total = stats['total']
    print(f"Total Projects: {total.get('total_projects', 0)}")
    print(f"Total Open Source: {total.get('total_opensource', 0)}")
    print("=" * 60)

def save_stats_json(stats, output_path):
    """Save statistics as JSON."""
    import json
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Statistics saved to: {output_path}")

def save_stats_markdown(stats, output_path):
    """Save statistics as Markdown for easy sharing."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Awesome Generative AI - Statistics\n\n")
        f.write(f"*Last updated: {stats['generated_at']}*\n\n")
        
        f.write("## 📊 Main List\n\n")
        main = stats['main_list']
        f.write(f"- **Total Projects:** {main.get('total_projects', 0)}\n")
        f.write(f"- **Open Source Projects:** {main.get('opensource_projects', 0)}\n")
        f.write(f"- **Categories:** {main.get('total_categories', 0)}\n\n")
        
        if main.get('categories'):
            f.write("### Top Categories\n\n")
            sorted_cats = sorted(main['categories'].items(), key=lambda x: x[1], reverse=True)
            for cat, count in sorted_cats:
                f.write(f"- {cat}: {count}\n")
            f.write("\n")
        
        f.write("## 🔍 Discoveries List\n\n")
        disc = stats['discoveries_list']
        f.write(f"- **Total Projects:** {disc.get('total_projects', 0)}\n")
        f.write(f"- **Open Source Projects:** {disc.get('opensource_projects', 0)}\n")
        f.write(f"- **Categories:** {disc.get('total_categories', 0)}\n\n")
        
        f.write("## 📈 Totals\n\n")
        total = stats['total']
        f.write(f"- **Total Projects:** {total.get('total_projects', 0)}\n")
        f.write(f"- **Total Open Source:** {total.get('total_opensource', 0)}\n")
    
    print(f"✅ Statistics saved to: {output_path}")

if __name__ == '__main__':
    stats = generate_stats()
    print_stats(stats)
    
    # Save outputs
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    save_stats_json(stats, output_dir / 'stats.json')
    save_stats_markdown(stats, output_dir / 'STATS.md')

