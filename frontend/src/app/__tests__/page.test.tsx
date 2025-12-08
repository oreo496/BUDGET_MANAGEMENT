import { render, screen } from '@testing-library/react';
import Dashboard from '../page';

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

jest.mock('@/components/Cards/CreditCard', () => {
  return function MockCreditCard({ balance }: { balance: string }) {
    return <div data-testid="credit-card">{balance}</div>;
  };
});

describe('Dashboard Page', () => {
  it('renders dashboard layout', () => {
    render(<Dashboard />);
    expect(screen.getByTestId('main-layout')).toBeInTheDocument();
    expect(screen.getByText('Overview')).toBeInTheDocument();
  });

  it('renders primary card section', () => {
    render(<Dashboard />);
    const cards = screen.getAllByTestId('credit-card');
    expect(cards.length).toBeGreaterThan(0);
  });
});

