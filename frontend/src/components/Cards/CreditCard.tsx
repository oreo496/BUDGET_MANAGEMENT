interface CreditCardProps {
  balance: string;
  cardHolder?: string;
  validThru?: string;
  cardNumber: string;
  showCVV?: boolean;
  bankLogo?: string;
  bankName?: string;
  className?: string;
}

export default function CreditCard({
  balance,
  cardHolder,
  validThru,
  cardNumber,
  showCVV = false,
  bankLogo,
  bankName,
  className = '',
}: CreditCardProps) {
  return (
    <div className={`relative bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl p-6 text-white shadow-lg ${className}`}>
      {bankLogo && (
        <div className="absolute top-4 right-4">
          <div className="text-2xl font-bold">{bankLogo}</div>
        </div>
      )}
      
      <div className="flex items-center justify-between mb-4">
        <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
          <div className="w-6 h-6 bg-white rounded"></div>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" className="sr-only peer" defaultChecked />
          <div className="w-11 h-6 bg-white/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
        </label>
      </div>
      
      <div className="mb-4">
        <div className="text-sm text-blue-100 mb-1">Balance</div>
        <div className="text-2xl font-bold">{balance}</div>
      </div>
      
      {cardHolder && (
        <div className="mb-2">
          <div className="text-xs text-blue-100 mb-1">CARD HOLDER</div>
          <div className="text-sm font-medium">{cardHolder}</div>
        </div>
      )}
      
      {validThru && (
        <div className="mb-4">
          <div className="text-xs text-blue-100 mb-1">VALID THRU</div>
          <div className="text-sm font-medium">{validThru}</div>
        </div>
      )}
      
      {showCVV && (
        <div className="mb-4">
          <div className="text-xs text-blue-100 mb-1">CVV</div>
          <div className="text-sm font-medium">***</div>
        </div>
      )}
      
      <div className="mt-4">
        <div className="text-xs text-blue-100 mb-1">CARD NUMBER</div>
        <div className="text-lg font-mono tracking-wider">{cardNumber}</div>
      </div>
    </div>
  );
}

