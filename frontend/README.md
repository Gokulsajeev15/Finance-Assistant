# Finance Assistant Frontend

A modern React frontend built with Vite for the Finance Assistant API.

## Features

- 🏢 **Company Search**: Search and browse Fortune 500 companies
- 📊 **Technical Analysis**: Interactive stock analysis with RSI, Moving Averages, and Bollinger Bands
- 🤖 **AI Assistant**: Natural language financial queries
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- ⚡ **Fast Development**: Built with Vite for lightning-fast development

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Finance Assistant API running on http://localhost:8000

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to http://localhost:3000

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Header.jsx
│   │   ├── SearchBar.jsx
│   │   ├── CompanyCard.jsx
│   │   ├── TechnicalAnalysis.jsx
│   │   └── AIChat.jsx
│   ├── services/
│   │   └── api.js          # API service layer
│   ├── App.jsx             # Main application component
│   ├── main.jsx            # Application entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── package.json
├── vite.config.js          # Vite configuration
└── tailwind.config.js      # Tailwind CSS configuration
```

## API Integration

The frontend integrates with the Finance Assistant API through:
- Company data endpoints
- Technical analysis endpoints
- AI query processing
- Real-time financial data

## Development

The application is configured with:
- Hot module replacement for fast development
- Proxy configuration for API calls
- ESLint for code quality
- Tailwind CSS for styling
