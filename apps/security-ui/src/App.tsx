import { useEffect, useState } from 'react';
import { Shield, AlertTriangle, ShieldCheck, Activity } from 'lucide-react';
import './index.css';

interface Finding {
  file_path: string;
  line_number: number;
  match_content: string;
  rule_name: string;
  severity: string;
}

function App() {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/findings.json')
      .then(res => res.json())
      .then(data => {
        setFindings(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load findings", err);
        setLoading(false);
      });
  }, []);

  const criticalCount = findings.filter(f => f.severity.includes('CRITICAL')).length;
  const lowCount = findings.filter(f => f.severity.includes('LOW')).length;

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: '#fff' }}>
        <Activity size={48} className="animate-spin" />
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="header">
        <div className="title-badge">Local AI Security Engine</div>
        <h1>Aegis Command Center</h1>
        <p>Enterprise-grade secrets and PII detection powered by Rust and Apple Silicon MLX.</p>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#00ffaa' }}>
            <ShieldCheck size={32} style={{ display: 'inline', marginRight: '10px', verticalAlign: 'middle' }} />
            {findings.length === 0 ? 'Clean' : 'Alert'}
          </div>
          <div className="stat-label">System Status</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{findings.length}</div>
          <div className="stat-label">Total Findings</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: 'var(--critical-text)' }}>{criticalCount}</div>
          <div className="stat-label">Critical Risks</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: 'var(--low-text)' }}>{lowCount}</div>
          <div className="stat-label">Low Risks</div>
        </div>
      </div>

      <div className="findings-list">
        {findings.map((finding, idx) => (
          <div key={idx} className="finding-item">
            <div className="finding-header">
              <div className="finding-title">
                {finding.severity.includes('CRITICAL') ? <AlertTriangle color="#ff4a4a" size={20} /> : <Shield color="#60a5fa" size={20} />}
                {finding.rule_name}
                <span className="finding-path">{finding.file_path}:{finding.line_number}</span>
              </div>
              <span className={`severity-badge ${finding.severity.includes('CRITICAL') ? 'severity-critical' : 'severity-low'}`}>
                {finding.severity}
              </span>
            </div>
            <div className="code-snippet">
              {finding.match_content}
            </div>
          </div>
        ))}
        {findings.length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem', color: '#888' }}>
            No security findings detected. Your codebase is secure.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
