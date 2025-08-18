import { TrendingUp } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-black text-white border-b-4 border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-center py-8">
          <div className="flex items-center space-x-3">
            <TrendingUp className="h-10 w-10" />
            <div className="text-center">
              <h1 className="text-4xl font-bold">Finance Assistant</h1>
              <p className="text-xl text-gray-300 mt-2">AI-Powered Financial Analysis Platform</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
