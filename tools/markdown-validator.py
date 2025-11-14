#!/usr/bin/env python3
"""
Markdown Validator for Awesome Generative AI
Validates markdown entries against contribution guidelines.
"""

import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class MarkdownValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.entry_count = 0
        
    def validate_entry_format(self, line, line_num, file_name):
        """Validate entry format: [ProjectName](Link) - Description."""
        # Check for entry pattern
        entry_pattern = r'^\s*-\s*\[([^\]]+)\]\(([^\)]+)\)\s*-\s*(.+)$'
        match = re.match(entry_pattern, line)
        
        if not match:
            # Not an entry line, skip
            return True
        
        self.entry_count += 1
        name, url, description = match.groups()
        
        # Check 1: Description should end with a period
        if not description.strip().endswith('.'):
            self.errors.append({
                'type': 'missing_period',
                'file': file_name,
                'line': line_num,
                'entry': name,
                'message': f"Description should end with a period: '{description[:50]}...'"
            })
        
        # Check 2: Description should not be empty
        if not description.strip() or len(description.strip()) < 10:
            self.warnings.append({
                'type': 'short_description',
                'file': file_name,
                'line': line_num,
                'entry': name,
                'message': f"Description seems too short: '{description}'"
            })
        
        # Check 3: URL should be valid format
        if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('#') and not url.startswith('mailto:'):
            self.errors.append({
                'type': 'invalid_url',
                'file': file_name,
                'line': line_num,
                'entry': name,
                'message': f"URL format may be invalid: '{url}'"
            })
        
        # Check 4: Name should not be empty
        if not name.strip():
            self.errors.append({
                'type': 'empty_name',
                'file': file_name,
                'line': line_num,
                'entry': name,
                'message': "Project name is empty"
            })
        
        # Check 5: No trailing whitespace
        if line.rstrip() != line:
            self.warnings.append({
                'type': 'trailing_whitespace',
                'file': file_name,
                'line': line_num,
                'entry': name,
                'message': "Line has trailing whitespace"
            })
        
        # Check 6: Description should be concise (warn if too long)
        if len(description) > 200:
            self.warnings.append({
                'type': 'long_description',
                'file': file_name,
                'line': line_num,
                'entry': name,
                'message': f"Description is quite long ({len(description)} chars). Keep it concise."
            })
        
        return True
    
    def validate_section_structure(self, content, file_name):
        """Validate section structure and hierarchy."""
        lines = content.split('\n')
        current_section = None
        current_subsection = None
        
        for i, line in enumerate(lines, 1):
            # Check for main section (##)
            if line.startswith('## '):
                current_section = line.replace('## ', '').strip()
                current_subsection = None
                
                # Check if section title is in Contents
                if file_name == 'README.md' and current_section not in ['Contents', 'Recommended reading', 'Milestones']:
                    # This is a basic check - could be enhanced
                    pass
            
            # Check for subsection (###)
            elif line.startswith('### '):
                current_subsection = line.replace('### ', '').strip()
            
            # Validate entry format
            if re.match(r'^\s*-\s*\[', line):
                self.validate_entry_format(line, i, file_name)
    
    def check_duplicates(self, content, file_name):
        """Check for duplicate entries."""
        entries = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            entry_pattern = r'^\s*-\s*\[([^\]]+)\]\(([^\)]+)\)'
            match = re.match(entry_pattern, line)
            if match:
                name, url = match.groups()
                entries.append({
                    'name': name.strip().lower(),
                    'url': url.strip().lower(),
                    'line': i
                })
        
        # Check for duplicate URLs
        url_counts = defaultdict(list)
        for entry in entries:
            url_counts[entry['url']].append(entry)
        
        for url, entry_list in url_counts.items():
            if len(entry_list) > 1:
                self.warnings.append({
                    'type': 'duplicate_url',
                    'file': file_name,
                    'line': entry_list[0]['line'],
                    'entry': entry_list[0]['name'],
                    'message': f"Duplicate URL found {len(entry_list)} times: {url[:60]}..."
                })
        
        # Check for duplicate names (case-insensitive)
        name_counts = defaultdict(list)
        for entry in entries:
            name_counts[entry['name']].append(entry)
        
        for name, entry_list in name_counts.items():
            if len(entry_list) > 1:
                # Check if they're actually different URLs
                urls = set(e['url'] for e in entry_list)
                if len(urls) == 1:
                    self.warnings.append({
                        'type': 'duplicate_entry',
                        'file': file_name,
                        'line': entry_list[0]['line'],
                        'entry': entry_list[0]['name'],
                        'message': f"Duplicate entry found {len(entry_list)} times"
                    })
    
    def validate_file(self, file_path):
        """Validate a markdown file."""
        print(f"📄 Validating {file_path.name}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Validate structure
        self.validate_section_structure(content, file_path.name)
        
        # Check for duplicates
        self.check_duplicates(content, file_path.name)
        
        print(f"   Found {self.entry_count} entries")
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 70)
        print("Markdown Validation Summary")
        print("=" * 70)
        print(f"\n📊 Total entries checked: {self.entry_count}")
        print(f"❌ Errors found:         {len(self.errors)}")
        print(f"⚠️  Warnings found:       {len(self.warnings)}")
        
        if self.errors:
            print("\n❌ ERRORS (must be fixed):")
            print("-" * 70)
            for error in self.errors:
                print(f"  [{error['file']}:{error['line']}] {error['entry']}")
                print(f"    {error['message']}")
                print()
        
        if self.warnings:
            print("\n⚠️  WARNINGS (should be reviewed):")
            print("-" * 70)
            for warning in self.warnings[:20]:  # Show first 20 warnings
                print(f"  [{warning['file']}:{warning['line']}] {warning['entry']}")
                print(f"    {warning['message']}")
                print()
            
            if len(self.warnings) > 20:
                print(f"    ... and {len(self.warnings) - 20} more warnings")
                print()
    
    def save_report(self, output_path):
        """Save validation report to JSON."""
        import json
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_entries': self.entry_count,
                'errors': len(self.errors),
                'warnings': len(self.warnings)
            },
            'errors': self.errors,
            'warnings': self.warnings
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Report saved to: {output_path}")

def main():
    repo_root = Path(__file__).parent.parent
    
    validator = MarkdownValidator()
    
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
    validator.save_report(output_dir / 'markdown-validation-report.json')
    
    # Exit with error code if errors found
    if validator.errors:
        print("\n❌ Validation failed. Please fix the errors above.")
        sys.exit(1)
    elif validator.warnings:
        print("\n⚠️  Validation completed with warnings. Please review.")
        sys.exit(0)
    else:
        print("\n✅ All entries validated successfully!")
        sys.exit(0)

if __name__ == '__main__':
    main()



