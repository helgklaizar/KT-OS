import os
import subprocess
import logging

logger = logging.getLogger(__name__)

# Assumes the main project is at the parent of 'api' directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKTREES_DIR = os.path.join(PROJECT_ROOT, "worktrees")

def init_worktrees_dir():
    if not os.path.exists(WORKTREES_DIR):
        os.makedirs(WORKTREES_DIR)
        # Add to .gitignore if not there (naive implementation)
        gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                content = f.read()
            if "worktrees/" not in content:
                with open(gitignore_path, "a") as f:
                    f.write("\n# Agent Worktrees\nworktrees/\n")

def create_task_worktree(task_id: str) -> str:
    """
    Creates an isolated git worktree for a specific task.
    Returns the branch name.
    """
    init_worktrees_dir()
    
    branch_name = f"feature/task-{task_id}"
    worktree_path = os.path.join(WORKTREES_DIR, f"task-{task_id}")
    
    # Check if branch already exists
    try:
        subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"], 
                       cwd=PROJECT_ROOT, check=True)
        branch_exists = True
    except subprocess.CalledProcessError:
        branch_exists = False

    if os.path.exists(worktree_path):
        logger.info(f"Worktree already exists at {worktree_path}")
        return branch_name

    try:
        if branch_exists:
            # Create worktree using existing branch
            subprocess.run(["git", "worktree", "add", worktree_path, branch_name], 
                           cwd=PROJECT_ROOT, check=True, capture_output=True)
        else:
            # Create worktree and new branch
            subprocess.run(["git", "worktree", "add", "-b", branch_name, worktree_path], 
                           cwd=PROJECT_ROOT, check=True, capture_output=True)
        
        logger.info(f"Successfully created worktree for {task_id} at {worktree_path}")
        return branch_name
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create worktree: {e.stderr.decode()}")
        raise Exception(f"Git Worktree Error: {e.stderr.decode()}")

def remove_task_worktree(task_id: str):
    """
    Removes the worktree. Used for Auto-Rollback or cleanup.
    """
    worktree_path = os.path.join(WORKTREES_DIR, f"task-{task_id}")
    if os.path.exists(worktree_path):
        subprocess.run(["git", "worktree", "remove", "--force", worktree_path], 
                       cwd=PROJECT_ROOT, check=True)
