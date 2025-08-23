# app/routers/github.py
from fastapi import APIRouter, HTTPException
from app.services.github_service import github_service

router = APIRouter()

@router.get("/test-connection")
async def test_github_connection():
    """Test GitHub API connection"""
    try:
        result = github_service.test_connection()
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repo/{repo_url:path}")
async def get_repository_info(repo_url: str):
    """Get basic information about a repository"""
    try:
        repo = github_service.get_repo(repo_url)
        return {
            "name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "url": repo.html_url,
            "language": repo.language
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/repo/{repo_url:path}/contents")
async def get_repository_contents(repo_url: str, path: str = ""):
    """Get contents of a repository path"""
    try:
        contents = github_service.get_repo_contents(repo_url, path)
        
        # Format the response
        result = []
        for content in contents:
            result.append({
                "name": content.name,
                "path": content.path,
                "type": content.type,  # 'file' or 'dir'
                "size": content.size,
                "download_url": content.download_url
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))