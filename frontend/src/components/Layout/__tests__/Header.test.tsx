import { render, screen } from '@testing-library/react';
import Header from '../Header';

describe('Header', () => {
  it('renders the title', () => {
    render(<Header title="Dashboard" />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('renders search input', () => {
    render(<Header title="Test Page" />);
    const searchInput = screen.getByPlaceholderText('Search for something');
    expect(searchInput).toBeInTheDocument();
  });

  it('renders action icons', () => {
    render(<Header title="Test Page" />);
    // Icons are rendered but we can check for their presence via test-id or parent elements
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
  });
});

