import { render, screen, fireEvent } from '@testing-library/react';
import Transactions from '../page';

// Mock the components
jest.mock('@/components/Layout/MainLayout', () => {
  return function MockMainLayout({ children, title }: { children: React.ReactNode; title: string }) {
    return (
      <div data-testid="main-layout">
        <h1>{title}</h1>
        {children}
      </div>
    );
  };
});

describe('Transactions Page', () => {
  it('renders transactions page', () => {
    render(<Transactions />);
    expect(screen.getByText('Transactions')).toBeInTheDocument();
  });

  it('renders transaction tabs', () => {
    render(<Transactions />);
    expect(screen.getByText('All Transactions')).toBeInTheDocument();
    expect(screen.getByText('Income')).toBeInTheDocument();
    expect(screen.getByText('Expense')).toBeInTheDocument();
  });

  it('switches between tabs', () => {
    render(<Transactions />);
    
    const incomeTab = screen.getByText('Income');
    fireEvent.click(incomeTab);
    
    expect(incomeTab.closest('button')).toHaveClass('text-blue-600');
  });

  it('displays transaction table', () => {
    render(<Transactions />);
    expect(screen.getByText('Description')).toBeInTheDocument();
    expect(screen.getByText('Amount')).toBeInTheDocument();
  });
});

