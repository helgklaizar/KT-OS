import os
from pathlib import Path

class AntigravityContextBuilder:
    """
    Absorbed from 'antigravity-bar'.
    Parses ~/.gemini/antigravity/ to build the ultimate system prompt.
    """
    def __init__(self):
        self.antigravity_path = os.path.expanduser("~/.gemini/antigravity")
        self.workflows_path = os.path.join(self.antigravity_path, "global_workflows")

    def build_system_prompt(self, workflow_name: str = None) -> str:
        prompt = "You are operating within the Omni-Agent OS.\n\n"
        
        # 1. Load global rules (System Instructions)
        global_rules_path = os.path.join(self.antigravity_path, "RULES.md")
        if os.path.exists(global_rules_path):
            with open(global_rules_path, 'r', encoding='utf-8') as f:
                prompt += f"=== GLOBAL RULES ===\n{f.read()}\n\n"

        # 2. Load specific workflow if requested
        if workflow_name and os.path.exists(self.workflows_path):
            workflow_file = os.path.join(self.workflows_path, f"{workflow_name}.md")
            if os.path.exists(workflow_file):
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    prompt += f"=== ACTIVE WORKFLOW: {workflow_name} ===\n{f.read()}\n\n"
            else:
                prompt += f"Warning: Workflow '{workflow_name}' not found in Antigravity.\n"

        return prompt
