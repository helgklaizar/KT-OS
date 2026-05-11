export type AgentRole = 'Architect' | 'Coder' | 'Reviewer' | 'Manager' | 'Scout' | null;

export interface CardType {
  id: string;
  title: string;
  description: string;
  status: 'Backlog' | 'To Do' | 'In Progress' | 'Blocked' | 'Review' | 'Done';
  agentRole: AgentRole;
  gitBranch?: string; // Auto-generated isolated branch
  isStuck?: boolean; // True if agent triggers "Stuck Protocol"
  cost?: number; // Cost in USD for this task
}

export interface LogEntry {
  id: string;
  timestamp: string;
  agent: AgentRole;
  actionType: 'thought' | 'command' | 'file_change' | 'error' | 'system';
  message: string;
}
