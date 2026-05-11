import React from 'react';
import type { CardType } from '../types';
import Card from './Card';
import './Column.css';

interface ColumnProps {
  title: string;
  id: string;
  cards: CardType[];
  onCardClick: (card: CardType) => void;
  onDropCard: (cardId: string, targetColumnId: string) => void;
}

const Column: React.FC<ColumnProps> = ({ title, id, cards, onCardClick, onDropCard }) => {
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault(); // Necessary to allow dropping
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const cardId = e.dataTransfer.getData('cardId');
    if (cardId) {
      onDropCard(cardId, id);
    }
  };

  return (
    <div 
      className="column glass-panel"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <div className="column-header">
        <h3 className="column-title">{title}</h3>
        <span className="column-count">{cards.length}</span>
      </div>
      <div className="column-cards">
        {cards.map(card => (
          <Card key={card.id} card={card} onClick={() => onCardClick(card)} />
        ))}
      </div>
    </div>
  );
};

export default Column;
