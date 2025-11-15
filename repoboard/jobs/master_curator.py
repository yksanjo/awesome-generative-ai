"""Master curator script - fetch, analyze, recommend, and export in one go."""

import os
import json
import argparse
from datetime import datetime

# Import our modules
from enhanced_fetch import EnhancedRepoFetcher
from advanced_recommendations import AdvancedRecommendationEngine
from export_recommendations import RecommendationExporter
from analyze_repos import RepoAnalyzer


def main():
    """Master curator workflow."""
    parser = argparse.ArgumentParser(
        description="Master curator: fetch, analyze, recommend, and export",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick fetch and recommend
  python jobs/master_curator.py --fetch --recommend --export

  # Fetch specific languages and topics
  python jobs/master_curator.py --fetch --languages python javascript --topics ml web-dev

  # Generate all recommendation types
  python jobs/master_curator.py --input repos.json --recommend --all-types

  # Full workflow
  python jobs/master_curator.py --fetch --analyze --recommend --export --all-types
        """
    )
    
    # Fetch options
    parser.add_argument("--fetch", action="store_true", help="Fetch repositories")
    parser.add_argument("--languages", nargs="+", help="Languages to fetch")
    parser.add_argument("--topics", nargs="+", help="Topics to fetch")
    parser.add_argument("--orgs", nargs="+", help="Organizations to fetch")
    parser.add_argument("--limit", type=int, default=50, help="Per category limit")
    parser.add_argument("--no-trending", action="store_true", help="Skip trending")
    parser.add_argument("--no-updated", action="store_true", help="Skip recently updated")
    parser.add_argument("--no-rising", action="store_true", help="Skip rising stars")
    parser.add_argument("--no-gems", action="store_true", help="Skip hidden gems")
    
    # Input/Output
    parser.add_argument("--input", type=str, help="Input JSON file (skip fetch)")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory")
    
    # Analysis
    parser.add_argument("--analyze", action="store_true", help="Analyze repositories")
    
    # Recommendations
    parser.add_argument("--recommend", action="store_true", help="Generate recommendations")
    parser.add_argument("--all-types", action="store_true", help="Generate all recommendation types")
    parser.add_argument("--rec-languages", nargs="+", help="Languages for recommendations")
    parser.add_argument("--rec-topics", nargs="+", help="Topics for recommendations")
    parser.add_argument("--rec-limit", type=int, default=10, help="Recommendations per category")
    
    # Export
    parser.add_argument("--export", action="store_true", help="Export recommendations")
    parser.add_argument("--export-format", type=str, choices=["json", "csv", "md", "awesome", "all"], default="all")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    repos = []
    
    # Step 1: Fetch repositories
    if args.fetch:
        print("=" * 80)
        print("STEP 1: FETCHING REPOSITORIES")
        print("=" * 80)
        
        fetcher = EnhancedRepoFetcher()
        repos = fetcher.comprehensive_fetch(
            languages=args.languages or ["python", "javascript", "go"],
            topics=args.topics or ["machine-learning", "web-development"],
            orgs=args.orgs,
            include_trending=not args.no_trending,
            include_updated=not args.no_updated,
            include_rising=not args.no_rising,
            include_hidden_gems=not args.no_gems,
            per_category_limit=args.limit
        )
        
        # Save fetched repos
        repos_file = os.path.join(args.output_dir, "fetched_repos.json")
        with open(repos_file, "w") as f:
            json.dump(repos, f, indent=2, default=str)
        print(f"\n💾 Saved {len(repos)} repos to {repos_file}")
    
    elif args.input:
        print(f"📦 Loading repos from {args.input}...")
        with open(args.input, "r") as f:
            repos = json.load(f)
        print(f"✅ Loaded {len(repos)} repositories")
    
    else:
        print("❌ Error: Must specify --fetch or --input")
        return
    
    if not repos:
        print("❌ No repositories to process")
        return
    
    # Step 2: Analyze
    if args.analyze:
        print("\n" + "=" * 80)
        print("STEP 2: ANALYZING REPOSITORIES")
        print("=" * 80)
        
        analyzer = RepoAnalyzer(repos)
        analyzer.analyze()
        analyzer.print_report()
        
        analysis_file = os.path.join(args.output_dir, "analysis.json")
        analyzer.export_json(analysis_file)
    
    # Step 3: Generate recommendations
    if args.recommend:
        print("\n" + "=" * 80)
        print("STEP 3: GENERATING RECOMMENDATIONS")
        print("=" * 80)
        
        engine = AdvancedRecommendationEngine(repos)
        recommendations = {}
        
        if args.all_types:
            print("🔍 Generating all recommendation types...")
            recommendations = engine.get_all_recommendations(limit_per_category=args.rec_limit)
        else:
            # Default recommendations
            recommendations = {
                "top_overall": engine.recommend_top_overall(args.rec_limit),
                "rising_stars": engine.recommend_rising_stars(limit=args.rec_limit),
                "hidden_gems": engine.recommend_hidden_gems(limit=args.rec_limit)
            }
        
        if args.rec_languages:
            print(f"🔍 Generating language recommendations: {', '.join(args.rec_languages)}")
            lang_recs = engine.get_language_recommendations(args.rec_languages, limit=args.rec_limit)
            recommendations.update(lang_recs)
        
        if args.rec_topics:
            print(f"🔍 Generating topic recommendations: {', '.join(args.rec_topics)}")
            topic_recs = engine.get_topic_recommendations(args.rec_topics, limit=args.rec_limit)
            recommendations.update(topic_recs)
        
        # Save recommendations
        recs_file = os.path.join(args.output_dir, "recommendations.json")
        with open(recs_file, "w") as f:
            json.dump(recommendations, f, indent=2, default=str)
        print(f"\n💾 Saved recommendations to {recs_file}")
        
        # Step 4: Export
        if args.export:
            print("\n" + "=" * 80)
            print("STEP 4: EXPORTING RECOMMENDATIONS")
            print("=" * 80)
            
            exporter = RecommendationExporter(recommendations)
            base_name = os.path.join(args.output_dir, "recommendations")
            
            if args.export_format == "all":
                exporter.export_all(base_name)
            elif args.export_format == "json":
                exporter.export_json(f"{base_name}.json")
            elif args.export_format == "csv":
                exporter.export_csv(f"{base_name}.csv")
            elif args.export_format == "md":
                exporter.export_markdown(f"{base_name}.md")
            elif args.export_format == "awesome":
                exporter.export_awesome_list(os.path.join(args.output_dir, "AWESOME.md"))
    
    print("\n" + "=" * 80)
    print("✅ MASTER CURATOR COMPLETE")
    print("=" * 80)
    print(f"\n📁 Output directory: {args.output_dir}")
    print("\nGenerated files:")
    if args.fetch:
        print(f"  - fetched_repos.json")
    if args.analyze:
        print(f"  - analysis.json")
    if args.recommend:
        print(f"  - recommendations.json")
    if args.export:
        if args.export_format == "all":
            print(f"  - recommendations.json")
            print(f"  - recommendations.csv")
            print(f"  - recommendations.md")
            print(f"  - AWESOME_recommendations.md")
        else:
            print(f"  - recommendations.{args.export_format}")


if __name__ == "__main__":
    main()

