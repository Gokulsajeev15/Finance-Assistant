const CompanyCard = ({ company }) => {
  const formatNumber = (num) => {
    if (!num) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(num * 1000000); // Assuming values are in millions
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-900">{company.company}</h3>
          <p className="text-gray-600">#{company.rank} • {company.ticker}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Sector</p>
          <p className="font-medium">{company.sector || 'N/A'}</p>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-500">Revenue</p>
          <p className="text-lg font-semibold text-green-600">{formatNumber(company.revenue)}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Profit</p>
          <p className="text-lg font-semibold text-blue-600">{formatNumber(company.profit)}</p>
        </div>
      </div>
      
      {company.industry && (
        <div className="border-t pt-4">
          <p className="text-sm text-gray-500">Industry</p>
          <p className="text-sm text-gray-900">{company.industry}</p>
        </div>
      )}
    </div>
  );
};

export default CompanyCard;
