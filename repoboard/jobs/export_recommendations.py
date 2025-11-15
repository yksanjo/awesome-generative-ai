"""Export recommendations to various formats."""

import json
import csv
from typing import List, Dict, Any
from datetime import datetime


class RecommendationExporter:
    """Export recommendations to multiple formats."""
    
    def __init__(self, recommendations: Dict[str, List[Dict[str, Any]]]):
        self.recommendations = recommendations
    
    def export_json(self, filename: str = "recommendations.json"):
        """Export to JSON."""
        with open(filename, "w") as f:
            json.dump(self.recommendations, f, indent=2, default=str)
        print(f"✅ Exported JSON to {filename}")
    
    def export_csv(self, filename: str = "recommendations.csv"):
        """Export to CSV (flattened)."""
        rows = []
        for category, recs in self.recommendations.items():
            for rec in recs:
                rows.append({
                    "category": category,
                    "rank": rec.get("rank", ""),
                    "name": rec.get("name", ""),
                    "url": rec.get("url", ""),
                    "description": rec.get("description", ""),
                    "stars": rec.get("stars", 0),
                    "forks": rec.get("forks", 0),
                    "language": rec.get("language", ""),
                    "topics": ", ".join(rec.get("topics", [])),
                    "score": rec.get("score", 0),
                    "star_velocity": rec.get("star_velocity", 0),
                    "why_recommended": rec.get("why_recommended", "")
                })
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
        print(f"✅ Exported CSV to {filename}")
    
    def export_markdown(self, filename: str = "recommendations.md"):
        """Export to Markdown."""
        md = f"# Repository Recommendations\n\n"
        md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += "---\n\n"
        
        for category, recs in self.recommendations.items():
            md += f"## {category.replace('_', ' ').title()}\n\n"
            
            for rec in recs:
                md += f"### {rec['rank']}. {rec['name']}\n\n"
                md += f"- **Stars**: {rec['stars']:,} | **Forks**: {rec['forks']:,}"
                if rec.get('language'):
                    md += f" | **Language**: {rec['language']}"
                md += "\n"
                md += f"- **URL**: {rec['url']}\n"
                md += f"- **Description**: {rec['description']}\n"
                
                if rec.get('topics'):
                    md += f"- **Topics**: {', '.join(rec['topics'])}\n"
                
                md += f"- **Why recommended**: {rec.get('why_recommended', 'Quality repository')}\n"
                md += f"- **Score**: {rec.get('score', 0):.3f}\n"
                
                if rec.get('star_velocity'):
                    md += f"- **Star velocity**: {rec['star_velocity']:.1f} stars/day\n"
                
                md += "\n"
            
            md += "---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md)
        
        print(f"✅ Exported Markdown to {filename}")
    
    def export_awesome_list(self, filename: str = "AWESOME.md"):
        """Export to Awesome list format."""
        md = f"# Awesome Curated Repositories\n\n"
        md += f"*Auto-curated recommendations - Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        md += "A curated list of recommended GitHub repositories.\n\n"
        md += "---\n\n"
        
        for category, recs in self.recommendations.items():
            category_name = category.replace('_', ' ').title()
            md += f"## {category_name}\n\n"
            
            for rec in recs:
                md += f"- [{rec['name']}]({rec['url']})"
                if rec.get('description'):
                    md += f" - {rec['description']}"
                md += f" ⭐ {rec['stars']:,}"
                if rec.get('language'):
                    md += f" | {rec['language']}"
                md += "\n"
            
            md += "\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md)
        
        print(f"✅ Exported Awesome list to {filename}")
    
    def export_all(self, base_filename: str = "recommendations"):
        """Export to all formats."""
        import os
        base_dir = os.path.dirname(base_filename) or "."
        base_name = os.path.basename(base_filename)
        
        self.export_json(f"{base_filename}.json")
        self.export_csv(f"{base_filename}.csv")
        self.export_markdown(f"{base_filename}.md")
        awesome_path = os.path.join(base_dir, f"AWESOME_{base_name}.md")
        self.export_awesome_list(awesome_path)


def main():
    """Example usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Export recommendations")
    parser.add_argument("--input", type=str, required=True, help="Input JSON file")
    parser.add_argument("--format", type=str, choices=["json", "csv", "md", "awesome", "all"], default="all")
    parser.add_argument("--output", type=str, help="Output filename (without extension)")
    
    args = parser.parse_args()
    
    # Load recommendations
    with open(args.input, "r") as f:
        recommendations = json.load(f)
    
    exporter = RecommendationExporter(recommendations)
    
    output_base = args.output or "recommendations"
    
    if args.format == "all":
        exporter.export_all(output_base)
    elif args.format == "json":
        exporter.export_json(f"{output_base}.json")
    elif args.format == "csv":
        exporter.export_csv(f"{output_base}.csv")
    elif args.format == "md":
        exporter.export_markdown(f"{output_base}.md")
    elif args.format == "awesome":
        exporter.export_awesome_list(f"AWESOME_{output_base}.md")


if __name__ == "__main__":
    main()

