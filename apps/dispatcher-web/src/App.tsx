
import Board from './components/Board';
import ActivityFeed from './components/ActivityFeed';
import { RBACProvider } from './components/RBAC';


function App() {
  return (
    <RBACProvider>
      <header className="app-header">
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '1rem' }}>
          <h1 className="app-title">AI Dispatcher</h1>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>v1.0 (Local First)</span>
        </div>
        
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Token Budget</span>
            <span style={{ fontSize: '1rem', color: 'var(--accent-orange)', fontWeight: 600, fontFamily: 'monospace' }}>$12.45 / $50.00</span>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Project Health</span>
            <span style={{ fontSize: '1rem', color: 'var(--accent-green)', fontWeight: 600 }}>94%</span>
          </div>

          <div className="user-profile">
            <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'var(--bg-card)', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem' }}>PO</div>
          </div>
        </div>
      </header>
      <main style={{ display: 'flex', flexGrow: 1, overflow: 'hidden' }}>
        <Board />
        <ActivityFeed />
      </main>
    </RBACProvider>
  );
}

export default App;
