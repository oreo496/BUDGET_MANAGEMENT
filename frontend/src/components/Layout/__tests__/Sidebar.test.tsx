import { render, screen } from '@testing-library/react';
import { usePathname } from 'next/navigation';
import Sidebar from '../Sidebar';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  usePathname: jest.fn(),
}));

// Mock next/link
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => {
    return <a href={href}>{children}</a>;
  };
});

describe('Sidebar', () => {
  beforeEach(() => {
    (usePathname as jest.Mock).mockReturnValue('/');
  });

  it('renders the FUNDER logo', () => {
    render(<Sidebar />);
    expect(screen.getByText('FUNDER')).toBeInTheDocument();
  });

  it('renders all navigation items', () => {
    render(<Sidebar />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Transactions')).toBeInTheDocument();
    expect(screen.getByText('Accounts')).toBeInTheDocument();
    expect(screen.getByText('Investments')).toBeInTheDocument();
    expect(screen.getByText('Cards')).toBeInTheDocument();
    expect(screen.getByText('Loans')).toBeInTheDocument();
    expect(screen.getByText('Chat bot')).toBeInTheDocument();
    expect(screen.getByText('My Privileges')).toBeInTheDocument();
    expect(screen.getByText('Setting')).toBeInTheDocument();
  });

  it('highlights active route', () => {
    (usePathname as jest.Mock).mockReturnValue('/transactions');
    render(<Sidebar />);
    
    const transactionsLink = screen.getByText('Transactions').closest('a');
    expect(transactionsLink).toHaveClass('bg-blue-50', 'text-blue-600');
  });

  it('applies correct styling to inactive routes', () => {
    (usePathname as jest.Mock).mockReturnValue('/');
    render(<Sidebar />);
    
    const accountsLink = screen.getByText('Accounts').closest('a');
    expect(accountsLink).toHaveClass('text-gray-700');
  });
});

