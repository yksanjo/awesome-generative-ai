"""
Export RepoBoard boards to awesome-style markdown lists.
Perfect for personal curation and publishing to GitHub.
"""

import sys
import os
from datetime import datetime
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db
from db.models import Board, BoardItem, Repo, RepoSummary


def export_board_to_markdown(board_id: int, output_file: str = None) -> str:
    """Export a single board to awesome-style markdown."""
    with get_db() as db:
        board = db.query(Board).filter(Board.id == board_id).first()
        if not board:
            return ""
        
        items = db.query(BoardItem).filter(
            BoardItem.board_id == board_id
        ).order_by(BoardItem.rank_position).all()
        
        markdown = f"# {board.name}\n\n"
        markdown += f"{board.description}\n\n"
        markdown += f"*Auto-curated by RepoBoard - Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        markdown += "---\n\n"
        
        for item in items:
            repo = db.query(Repo).filter(Repo.id == item.repo_id).first()
            if not repo:
                continue
            
            summary = repo.summary
            
            # Format: - [Name](URL) - Description
            markdown += f"- [{repo.full_name}]({repo.url})"
            
            if summary:
                # Add category/tags
                tags_str = ", ".join(summary.tags[:3])
                markdown += f" - {summary.summary[:100]}"
                if tags_str:
                    markdown += f" `{tags_str}`"
            elif repo.description:
                markdown += f" - {repo.description[:100]}"
            
            # Add stats
            markdown += f" ⭐ {repo.stars}"
            if repo.languages:
                top_lang = max(repo.languages.items(), key=lambda x: x[1])[0]
                markdown += f" | {top_lang}"
            
            markdown += "\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"✅ Exported to {output_file}")
        
        return markdown


def export_all_boards_to_markdown(output_dir: str = "awesome-lists") -> Dict[str, str]:
    """Export all boards to separate markdown files."""
    os.makedirs(output_dir, exist_ok=True)
    
    with get_db() as db:
        boards = db.query(Board).all()
        
        exported = {}
        for board in boards:
            # Create filename from board name
            filename = board.name.lower().replace(" ", "-").replace("/", "-")
            filename = "".join(c for c in filename if c.isalnum() or c == "-")
            filepath = os.path.join(output_dir, f"{filename}.md")
            
            markdown = export_board_to_markdown(board.id, filepath)
            exported[board.name] = filepath
        
        return exported


def export_combined_awesome_list(output_file: str = "AWESOME.md") -> str:
    """Export all boards as a combined awesome list."""
    with get_db() as db:
        boards = db.query(Board).order_by(Board.category, Board.name).all()
        
        markdown = "# Awesome Curated Repositories\n\n"
        markdown += f"*Auto-curated by RepoBoard - Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        markdown += "This is an automatically curated list of GitHub repositories organized by topic.\n\n"
        markdown += "---\n\n"
        
        current_category = None
        for board in boards:
            # Group by category
            if board.category and board.category != current_category:
                if current_category:
                    markdown += "\n"
                markdown += f"## {board.category}\n\n"
                current_category = board.category
            
            markdown += f"### {board.name}\n\n"
            markdown += f"{board.description}\n\n"
            
            # Get top repos from this board
            items = db.query(BoardItem).filter(
                BoardItem.board_id == board.id
            ).order_by(BoardItem.rank_position).limit(10).all()
            
            for item in items:
                repo = db.query(Repo).filter(Repo.id == item.repo_id).first()
                if not repo:
                    continue
                
                summary = repo.summary
                markdown += f"- [{repo.full_name}]({repo.url})"
                
                if summary:
                    markdown += f" - {summary.summary[:80]}"
                elif repo.description:
                    markdown += f" - {repo.description[:80]}"
                
                markdown += f" ⭐ {repo.stars}\n"
            
            if board.repo_count > 10:
                markdown += f"\n*... and {board.repo_count - 10} more repositories*\n"
            
            markdown += "\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"✅ Exported combined list to {output_file}")
        
        return markdown


def main():
    """Main export function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Export RepoBoard to awesome-style markdown")
    parser.add_argument("--board-id", type=int, help="Export specific board by ID")
    parser.add_argument("--all", action="store_true", help="Export all boards to separate files")
    parser.add_argument("--combined", action="store_true", help="Export all boards as one file")
    parser.add_argument("--output", type=str, help="Output file or directory")
    
    args = parser.parse_args()
    
    if args.board_id:
        output = args.output or f"board-{args.board_id}.md"
        export_board_to_markdown(args.board_id, output)
    elif args.all:
        output_dir = args.output or "awesome-lists"
        exported = export_all_boards_to_markdown(output_dir)
        print(f"\n✅ Exported {len(exported)} boards:")
        for name, path in exported.items():
            print(f"  - {name}: {path}")
    elif args.combined:
        output = args.output or "AWESOME.md"
        export_combined_awesome_list(output)
    else:
        # Default: export combined list
        export_combined_awesome_list()


if __name__ == "__main__":
    main()

