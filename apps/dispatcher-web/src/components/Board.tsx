import React, { useState, useEffect } from 'react';
import Column from './Column';
import StuckModal from './StuckModal';
import type { CardType } from '../types';

const COLUMNS = [
  { id: 'Backlog', title: 'Backlog' },
  { id: 'To Do', title: 'To Do' },
  { id: 'In Progress', title: 'Agent Thinking (In Progress)' },
  { id: 'Blocked', title: 'Blocked (Human Needed)' },
  { id: 'Review', title: 'Gatekeeper Review' },
  { id: 'Done', title: 'Done' }
];

const Board: React.FC = () => {
  const [cards, setCards] = useState<CardType[]>([]);
  const [selectedStuckCard, setSelectedStuckCard] = useState<CardType | null>(null);

  const fetchCards = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/cards');
      if (res.ok) {
        const data = await res.json();
        setCards(data);
      }
    } catch (error) {
      console.error("Failed to fetch cards. Make sure backend is running.", error);
    }
  };

  useEffect(() => {
    fetchCards();
  }, []);

  const handleCardClick = (card: CardType) => {
    if (card.isStuck) {
      setSelectedStuckCard(card);
    }
  };

  const handleStuckSubmit = async (response: string) => {
    if (selectedStuckCard) {
      try {
        await fetch(`http://localhost:8000/api/cards/${selectedStuckCard.id}/unstuck`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ response })
        });
        await fetchCards();
      } catch (error) {
        console.error("Failed to unstuck.", error);
      }
    }
    setSelectedStuckCard(null);
  };

  const handleDropCard = async (cardId: string, targetColumnId: string) => {
    // Optimistic UI update
    setCards(prevCards => 
      prevCards.map(c => c.id === cardId ? { ...c, status: targetColumnId as any } : c)
    );

    // Backend sync
    try {
      await fetch(`http://localhost:8000/api/cards/${cardId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: targetColumnId })
      });
      await fetchCards(); // Ensure sync to get new gitBranch
    } catch (error) {
      console.error("Failed to update status on backend.", error);
      await fetchCards(); // Rollback on error
    }
  };

  return (
    <div className="board-container">
      {COLUMNS.map(col => (
        <Column 
          key={col.id} 
          id={col.id} 
          title={col.title} 
          cards={cards.filter(c => c.status === col.id)}
          onCardClick={handleCardClick}
          onDropCard={handleDropCard}
        />
      ))}

      {selectedStuckCard && (
        <StuckModal 
          card={selectedStuckCard} 
          onClose={() => setSelectedStuckCard(null)}
          onSubmit={handleStuckSubmit}
        />
      )}
    </div>
  );
};

export default Board;
