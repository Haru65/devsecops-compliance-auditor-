import git
import os
import tempfile
import shutil
import logging
from git import Repo

logger = logging.getLogger(__name__)

def git_clone(git_repo_url: str):
    logger.info(f"Starting to clone repository: {git_repo_url}")
    
    # Create a temporary directory for cloning
    temp_dir = tempfile.mkdtemp()
    clone_path = os.path.join(temp_dir, "repo")
    
    try:
        # Validate URL format
        if not git_repo_url.startswith(('http://', 'https://', 'git@')):
            return {
                "status": "error",
                "message": "Invalid git URL format. Must start with http://, https://, or git@"
            }
        
        logger.info(f"Cloning to: {clone_path}")
        
        # Clone the repository using GitPython
        repo = Repo.clone_from(git_repo_url, clone_path)
        
        logger.info(f"Repository cloned successfully to: {clone_path}")
        
        # Get repository information
        repo_info = {
            "active_branch": repo.active_branch.name,
            "commit_count": len(list(repo.iter_commits())),
            "latest_commit": {
                "hash": repo.head.commit.hexsha,
                "message": repo.head.commit.message.strip(),
                "author": str(repo.head.commit.author),
                "date": repo.head.commit.committed_datetime.isoformat()
            }
        }
        
        # List files in the repository
        files = []
        for root, dirs, filenames in os.walk(clone_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), clone_path)
                files.append(rel_path)
        
        return {
            "status": "success",
            "repo": git_repo_url,
            "message": "Repository cloned and analyzed successfully",
            "clone_path": clone_path,
            "repo_info": repo_info,
            "files": files[:20],  # Show first 20 files
            "total_files": len(files)
        }
        
    except git.exc.GitCommandError as e:
        return {
            "status": "error",
            "message": f"Git command failed: {str(e)}"
        }
    except git.exc.InvalidGitRepositoryError:
        return {
            "status": "error",
            "message": "Invalid Git repository URL"
        }
    except git.exc.GitError as e:
        return {
            "status": "error",
            "message": f"Git error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }
    finally:
        # Optionally clean up the temporary directory
        # Uncomment the next line if you want to auto-delete after scanning
        # shutil.rmtree(temp_dir, ignore_errors=True)
        pass

def analyze_repository_files(clone_path: str):
    """Analyze files in the cloned repository for compliance issues"""
    try:
        compliance_issues = []
        
        for root, dirs, files in os.walk(clone_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
                
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, clone_path)
                
                # Example compliance checks
                if file.endswith(('.py', '.js', '.java', '.cpp')):
                    # Check for potential security issues
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            # Simple checks (expand these based on your compliance needs)
                            if 'password' in content.lower() and '=' in content:
                                compliance_issues.append({
                                    "file": rel_path,
                                    "issue": "Potential hardcoded password",
                                    "line": content.lower().find('password')
                                })
                                
                            if 'api_key' in content.lower() and '=' in content:
                                compliance_issues.append({
                                    "file": rel_path,
                                    "issue": "Potential hardcoded API key",
                                    "line": content.lower().find('api_key')
                                })
                    except:
                        continue
        
        return compliance_issues
        
    except Exception as e:
        return [{"error": f"Analysis failed: {str(e)}"}]