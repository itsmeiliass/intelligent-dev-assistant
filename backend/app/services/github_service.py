# app/services/github_service.py
import os
from github import Github, GithubException
from github.Repository import Repository
from github.ContentFile import ContentFile
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GitHubService:
    def __init__(self):
        # Get the token from environment variables
        self.access_token = os.getenv('GITHUB_ACCESS_TOKEN')
        
        if not self.access_token:
            raise ValueError("GitHub access token not found. Please set GITHUB_ACCESS_TOKEN in your .env file")
        
        # Initialize PyGithub client
        self.g = Github(self.access_token)
    
    def get_repo(self, repo_url: str) -> Repository:
        """
        Get a GitHub repository by URL
        Example: https://github.com/username/repo-name -> username/repo-name
        """
        try:
            # Extract owner/repo from URL
            if "github.com/" in repo_url:
                path_parts = repo_url.split("github.com/")[1].split("/")
                repo_name = f"{path_parts[0]}/{path_parts[1]}"
            else:
                repo_name = repo_url  # Assume it's already in owner/repo format
            
            # Get the repository
            repo = self.g.get_repo(repo_name)
            return repo
            
        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"Repository not found: {repo_url}")
            else:
                raise Exception(f"GitHub API error: {e}")
    
    def get_repo_contents(self, repo_url: str, path: str = ""):
        """
        Get contents of a repository (files and directories)
        """
        try:
            repo = self.get_repo(repo_url)
            contents = repo.get_contents(path)
            return contents
            
        except Exception as e:
            raise Exception(f"Failed to get repository contents: {e}")
    
    def get_file_content(self, repo_url: str, file_path: str) -> str:
        """
        Get the content of a specific file from a repository
        """
        try:
            repo = self.get_repo(repo_url)
            file_content = repo.get_contents(file_path)
            
            if isinstance(file_content, ContentFile):
                # Decode the content from bytes to string
                return file_content.decoded_content.decode('utf-8')
            else:
                raise ValueError(f"Path {file_path} is a directory, not a file")
                
        except Exception as e:
            raise Exception(f"Failed to get file content: {e}")
    
    def test_connection(self) -> bool:
        """
        Test if the GitHub connection is working
        """
        try:
            # Try to get the authenticated user
            user = self.g.get_user()
            return f"Connected as: {user.login}"
        except Exception as e:
            return f"Connection failed: {e}"

# Create a global instance for easy access
github_service = GitHubService()