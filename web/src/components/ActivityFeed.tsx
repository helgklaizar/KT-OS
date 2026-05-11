import React, { useState, useEffect, useRef } from 'react';
import { LogEntry } from '../types';
import './ActivityFeed.css';

const ActivityFeed: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:8000/api/logs');
    
    eventSource.onmessage = (event) => {
      const newLog: LogEntry = JSON.parse(event.data);
      setLogs((prev) => [...prev, newLog]);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="activity-feed glass-panel">
      <div className="feed-header">
        <h3>Live Activity Feed</h3>
        <div className="feed-filters">
          <span className="filter active">All</span>
          <span className="filter">Terminal</span>
          <span className="filter">Thoughts</span>
          <span className="filter">Errors</span>
        </div>
      </div>
      <div className="feed-logs">
        {logs.length === 0 && (
          <div style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '1rem' }}>
            Waiting for agent activity... Drop a task into "In Progress" to begin.
          </div>
        )}
        {logs.map((log, index) => (
          <div key={index} className={`log-entry type-${log.actionType}`}>
            <span className="log-time">[{log.timestamp}]</span>
            <span className="log-agent">{log.agent}:</span>
            <span className="log-msg">{log.message}</span>
          </div>
        ))}
        <div ref={logsEndRef} className="terminal-cursor">_</div>
      </div>
    </div>
  );
};

export default ActivityFeed;
