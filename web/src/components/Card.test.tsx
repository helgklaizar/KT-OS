import { render, screen, fireEvent } from '@testing-library/react';
import Card from './Card';
import { CardType } from '../types';

const mockCard: CardType = {
  id: '999',
  title: 'Test Card',
  description: 'Testing the card UI',
  status: 'Backlog',
  agentRole: 'Coder',
  cost: 0.50
};

describe('Card Component', () => {
  it('renders card title and description', () => {
    render(<Card card={mockCard} onClick={() => {}} />);
    expect(screen.getByText('Test Card')).toBeInTheDocument();
    expect(screen.getByText('Testing the card UI')).toBeInTheDocument();
  });

  it('displays agent badge and cost', () => {
    render(<Card card={mockCard} onClick={() => {}} />);
    expect(screen.getByText('Coder')).toBeInTheDocument();
    expect(screen.getByText('$0.50')).toBeInTheDocument();
  });

  it('shows stuck warning when isStuck is true', () => {
    const stuckCard = { ...mockCard, isStuck: true };
    render(<Card card={stuckCard} onClick={() => {}} />);
    expect(screen.getByText(/Agent Stuck/i)).toBeInTheDocument();
  });
});
