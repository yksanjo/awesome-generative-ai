"""FastAPI application for RepoBoard API."""

import sys
import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db_session, SessionLocal
from db.models import Repo, RepoSummary, Board, BoardItem, CurationScore, SocialSignals
from shared.schemas import (
    RepoMetadata, RepoSummary as RepoSummarySchema, Board as BoardSchema,
    BoardWithRepos, RepoWithSummary
)

# For Pydantic v2 compatibility
try:
    from pydantic import BaseModel
    PYDANTIC_V2 = True
except ImportError:
    PYDANTIC_V2 = False
from shared.config import settings

app = FastAPI(
    title="RepoBoard API",
    description="API for GitHub repository curation and boards",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    """Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def repo_to_dict(repo: Repo) -> dict:
    """Convert SQLAlchemy Repo to dict for Pydantic."""
    return {
        "url": repo.url,
        "full_name": repo.full_name,
        "name": repo.name,
        "owner": repo.owner,
        "description": repo.description,
        "readme": repo.readme,
        "languages": repo.languages or {},
        "stars": repo.stars,
        "forks": repo.forks,
        "watchers": repo.watchers,
        "open_issues": repo.open_issues,
        "created_at": repo.created_at,
        "updated_at": repo.updated_at,
        "pushed_at": repo.pushed_at,
        "default_branch": repo.default_branch,
        "topics": repo.topics or [],
        "license": repo.license,
        "archived": repo.archived,
        "file_tree": repo.file_tree,
        "commit_count": repo.commit_count,
        "contributor_count": repo.contributor_count,
        "star_velocity": repo.star_velocity,
    }


def summary_to_dict(summary: RepoSummary) -> dict:
    """Convert SQLAlchemy RepoSummary to dict for Pydantic."""
    return {
        "repo_id": summary.repo_id,
        "summary": summary.summary,
        "tags": summary.tags or [],
        "category": summary.category,
        "skill_level": summary.skill_level,
        "skill_level_numeric": summary.skill_level_numeric,
        "project_health": summary.project_health,
        "project_health_score": summary.project_health_score,
        "use_cases": summary.use_cases or [],
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "RepoBoard API", "version": "1.0.0"}


@app.get("/repos", response_model=List[RepoWithSummary])
async def list_repos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    language: Optional[str] = None,
    min_stars: Optional[int] = Query(None, ge=0),
    skill_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List repositories with optional filters."""
    query = db.query(Repo).filter(Repo.archived == False)
    
    if category:
        query = query.join(RepoSummary).filter(RepoSummary.category == category)
    
    if language:
        # Filter by language in languages JSON field
        query = query.filter(Repo.languages.has_key(language))
    
    if min_stars:
        query = query.filter(Repo.stars >= min_stars)
    
    if skill_level:
        query = query.join(RepoSummary).filter(RepoSummary.skill_level == skill_level)
    
    repos = query.offset(skip).limit(limit).all()
    
    result = []
    for repo in repos:
        summary = repo.summary
        result.append(RepoWithSummary(
            repo=RepoMetadata(**repo_to_dict(repo)),
            summary=RepoSummarySchema(**summary_to_dict(summary)) if summary else None
        ))
    
    return result


@app.get("/repos/{repo_id}", response_model=RepoWithSummary)
async def get_repo(repo_id: int, db: Session = Depends(get_db)):
    """Get a single repository by ID."""
    repo = db.query(Repo).filter(Repo.id == repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    summary = repo.summary
    return RepoWithSummary(
        repo=RepoMetadata(**repo_to_dict(repo)),
        summary=RepoSummarySchema(**summary_to_dict(summary)) if summary else None
    )


@app.get("/boards", response_model=List[BoardSchema])
async def list_boards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all boards."""
    query = db.query(Board)
    
    if category:
        query = query.filter(Board.category == category)
    
    boards = query.order_by(Board.created_at.desc()).offset(skip).limit(limit).all()
    return [
        BoardSchema(
            id=board.id,
            name=board.name,
            description=board.description,
            category=board.category,
            repo_count=board.repo_count,
            created_at=board.created_at,
            updated_at=board.updated_at,
        )
        for board in boards
    ]


@app.get("/boards/{board_id}", response_model=BoardWithRepos)
async def get_board(board_id: int, db: Session = Depends(get_db)):
    """Get a board with its repositories."""
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Get board items ordered by rank
    items = db.query(BoardItem).filter(
        BoardItem.board_id == board_id
    ).order_by(BoardItem.rank_position).all()
    
    repos = []
    for item in items:
        repo = db.query(Repo).filter(Repo.id == item.repo_id).first()
        if repo:
            summary = repo.summary
            repos.append(RepoWithSummary(
                repo=RepoMetadata(**repo_to_dict(repo)),
                summary=RepoSummarySchema(**summary_to_dict(summary)) if summary else None
            ))
    
    return BoardWithRepos(
        board=BoardSchema(
            id=board.id,
            name=board.name,
            description=board.description,
            category=board.category,
            repo_count=board.repo_count,
            created_at=board.created_at,
            updated_at=board.updated_at,
        ),
        repos=repos
    )


@app.get("/search")
async def search_repos(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search repositories by name, description, or tags."""
    try:
        from sqlalchemy import or_, case
        
        # Start with base query - repos that are not archived
        base_query = db.query(Repo).filter(Repo.archived == False)
        
        # Simple text search (in production, use full-text search)
        search_term = f"%{q}%"
        
        # Build search conditions
        # Search in name (always exists)
        name_match = Repo.name.ilike(search_term)
        
        # Search in description (may be None)
        desc_match = case(
            (Repo.description.isnot(None), Repo.description.ilike(search_term)),
            else_=False
        )
        
        # For summary search, we need to join with RepoSummary
        # Use outerjoin to include repos without summaries
        query = base_query.outerjoin(RepoSummary)
        
        # Search in summary (may not exist or be None)
        summary_match = case(
            (
                (RepoSummary.id.isnot(None)) & (RepoSummary.summary.isnot(None)),
                RepoSummary.summary.ilike(search_term)
            ),
            else_=False
        )
        
        # Combine all search conditions with OR
        query = query.filter(or_(name_match, desc_match, summary_match))
        
        # Execute query
        repos = query.limit(limit).all()
        
        # If no repos, return empty list immediately
        if not repos:
            return []
        
        # Build result
        result = []
        for repo in repos:
            try:
                summary = repo.summary
                repo_dict = repo_to_dict(repo)
                summary_dict = summary_to_dict(summary) if summary else None
                
                # Create response objects
                repo_metadata = RepoMetadata(**repo_dict)
                summary_schema = RepoSummarySchema(**summary_dict) if summary_dict else None
                
                result.append(RepoWithSummary(
                    repo=repo_metadata,
                    summary=summary_schema
                ))
            except Exception as e:
                # Skip repos that can't be serialized
                import traceback
                print(f"Warning: Skipping repo {repo.id if repo else 'unknown'} due to error: {e}")
                traceback.print_exc()
                continue
        
        return result
    except Exception as e:
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"Search error: {error_detail}")
        print(traceback_str)
        # Return empty list instead of raising error if database is empty
        if "does not exist" in error_detail.lower() or "relation" in error_detail.lower():
            return []
        raise HTTPException(status_code=500, detail=f"Search failed: {error_detail}")


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get overall statistics."""
    total_repos = db.query(Repo).filter(Repo.archived == False).count()
    total_boards = db.query(Board).count()
    total_categories = db.query(RepoSummary.category).distinct().count()
    
    return {
        "total_repos": total_repos,
        "total_boards": total_boards,
        "total_categories": total_categories,
    }


@app.get("/repos/{repo_id}/social-signals")
async def get_social_signals(repo_id: int, db: Session = Depends(get_db)):
    """Get social signals for a repository."""
    signals = db.query(SocialSignals).filter(SocialSignals.repo_id == repo_id).first()
    if not signals:
        raise HTTPException(status_code=404, detail="Social signals not found for this repository")
    
    return {
        "repo_id": signals.repo_id,
        "reddit_mentions": signals.reddit_mentions,
        "reddit_upvotes": signals.reddit_upvotes,
        "reddit_subreddits": signals.reddit_subreddits or [],
        "hn_mentions": signals.hn_mentions,
        "hn_points": signals.hn_points,
        "hn_comments": signals.hn_comments,
        "stackoverflow_questions": signals.stackoverflow_questions,
        "stackoverflow_views": signals.stackoverflow_views,
        "stackoverflow_score": signals.stackoverflow_score,
        "npm_weekly_downloads": signals.npm_weekly_downloads,
        "pypi_weekly_downloads": signals.pypi_weekly_downloads,
        "package_name": signals.package_name,
        "twitter_mentions": signals.twitter_mentions,
        "social_score": signals.social_score,
        "last_updated": signals.last_updated,
    }


@app.get("/repos/ranked-by-social-signals")
async def get_repos_ranked_by_social_signals(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get repositories ranked by social signals (real-world usage)."""
    repos = db.query(Repo).join(SocialSignals).filter(
        Repo.archived == False
    ).order_by(
        SocialSignals.social_score.desc()
    ).offset(skip).limit(limit).all()
    
    result = []
    for repo in repos:
        summary = repo.summary
        signals = db.query(SocialSignals).filter(SocialSignals.repo_id == repo.id).first()
        result.append({
            "repo": RepoMetadata(**repo_to_dict(repo)),
            "summary": RepoSummarySchema(**summary_to_dict(summary)) if summary else None,
            "social_signals": {
                "social_score": signals.social_score if signals else 0,
                "reddit_upvotes": signals.reddit_upvotes if signals else 0,
                "hn_points": signals.hn_points if signals else 0,
                "npm_weekly_downloads": signals.npm_weekly_downloads if signals else 0,
                "pypi_weekly_downloads": signals.pypi_weekly_downloads if signals else 0,
            } if signals else None
        })
    
    return result


@app.get("/use-case-finder")
async def find_repos_for_use_case(
    query: str = Query(..., min_length=3, description="What do you want to build? e.g., 'build a REST API'"),
    language: Optional[str] = Query("python", description="Programming language filter"),
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Find repositories matching a use case using AI.
    
    Example queries:
    - "I want to build a REST API"
    - "scrape websites"
    - "process images"
    - "create a web scraper"
    - "build a machine learning model"
    """
    try:
        from use_case_finder.use_case_matcher import UseCaseFinder
        
        finder = UseCaseFinder()
        result = finder.find_repos_for_use_case(
            user_query=query,
            language=language,
            limit=limit,
            db=db
        )
        
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Use-case finder error: {str(e)}")


@app.post("/chat")
async def chat_endpoint(request: dict, db: Session = Depends(get_db)):
    """Chat endpoint for conversational interface."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from api.conversation import ConversationHandler
    
    user_message = request.get("message", "")
    if not user_message:
        return {"response": "Please send a message!", "repos": []}
    
    # Initialize conversation handler
    conversation_handler = ConversationHandler()
    
    # Understand intent
    intent = conversation_handler.understand_intent(user_message)
    
    response_text = ""
    repos = []
    
    # Handle based on intent
    if intent.get("intent") == "search":
        query = intent.get("query", user_message)
        # Search repos
        search_query = db.query(Repo).join(RepoSummary).filter(Repo.archived == False)
        search_term = f"%{query}%"
        search_query = search_query.filter(
            (Repo.name.ilike(search_term)) |
            (Repo.description.ilike(search_term)) |
            (RepoSummary.summary.ilike(search_term))
        )
        repo_results = search_query.limit(5).all()
        
        repos = []
        for repo in repo_results:
            summary = repo.summary
            repos.append({
                "repo": repo_to_dict(repo),
                "summary": summary_to_dict(summary) if summary else None
            })
        
        if repos:
            response_text = f"Found {len(repos)} repositories matching '{query}':"
        else:
            response_text = f"I couldn't find any repositories matching '{query}'. Try a different search term!"
    
    elif intent.get("intent") == "trending":
        # Get trending repos
        trending_repos = db.query(Repo).filter(
            Repo.archived == False,
            Repo.stars >= 100
        ).order_by(Repo.stars.desc()).limit(5).all()
        
        repos = []
        for repo in trending_repos:
            summary = repo.summary
            repos.append({
                "repo": repo_to_dict(repo),
                "summary": summary_to_dict(summary) if summary else None
            })
        
        response_text = "Here are some trending repositories:"
    
    elif intent.get("intent") == "boards":
        # Get boards
        boards = db.query(Board).limit(5).all()
        if boards:
            board_names = ", ".join([b.name for b in boards])
            response_text = f"I have these curated boards: {board_names}. Use /boards to see them all!"
        else:
            response_text = "No boards available yet. Generate some boards first!"
    
    else:
        # Conversational response
        response_text = conversation_handler.generate_conversational_response(user_message)
    
    return {
        "response": response_text,
        "repos": repos
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)

