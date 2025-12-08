import { render, screen } from '@testing-library/react';
import CreditCard from '../CreditCard';

describe('CreditCard', () => {
  const defaultProps = {
    balance: 'E£ 273,907.37',
    cardHolder: 'Mohamed Elhosieny',
    validThru: '07/28',
    cardNumber: '3778 **** **** 1234',
  };

  it('renders card balance', () => {
    render(<CreditCard {...defaultProps} />);
    expect(screen.getByText('E£ 273,907.37')).toBeInTheDocument();
  });

  it('renders card holder name when provided', () => {
    render(<CreditCard {...defaultProps} />);
    expect(screen.getByText('Mohamed Elhosieny')).toBeInTheDocument();
  });

  it('renders card number', () => {
    render(<CreditCard {...defaultProps} />);
    expect(screen.getByText('3778 **** **** 1234')).toBeInTheDocument();
  });

  it('renders CVV when showCVV is true', () => {
    render(<CreditCard {...defaultProps} showCVV />);
    expect(screen.getByText('CVV')).toBeInTheDocument();
  });

  it('does not render card holder when not provided', () => {
    const { cardHolder, ...props } = defaultProps;
    render(<CreditCard {...props} />);
    expect(screen.queryByText('CARD HOLDER')).not.toBeInTheDocument();
  });
});

