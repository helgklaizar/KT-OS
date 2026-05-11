import React, { useState } from 'react';
import './StuckModal.css';
import type { CardType } from '../types';

interface StuckModalProps {
  card: CardType;
  onClose: () => void;
  onSubmit: (response: string) => void;
}

const StuckModal: React.FC<StuckModalProps> = ({ card, onClose, onSubmit }) => {
  const [input, setInput] = useState('');

  return (
    <div className="modal-overlay">
      <div className="modal-content glass-panel">
        <div className="modal-header">
          <h3>⚠️ Stuck Protocol Activated</h3>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="agent-message">
            <span className="agent-name">{card.agentRole}:</span>
            <p>I cannot proceed with <strong>#{card.id} {card.title}</strong>. I need human input or credentials to connect to the local SQLite database.</p>
          </div>
          
          <div className="human-input">
            <label>Provide Context or Keys:</label>
            <textarea 
              value={input} 
              onChange={e => setInput(e.target.value)}
              placeholder="e.g., 'The DB path is ./data/dev.db' or provide an API key..."
              rows={4}
            />
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={() => onSubmit(input)}>Send to Agent</button>
        </div>
      </div>
    </div>
  );
};

export default StuckModal;
