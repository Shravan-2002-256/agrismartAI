# AgriSmart AI - Frontend

React-based frontend for the AgriSmart AI agricultural advisory platform.

## Features

- 🔐 **Authentication**: Login and registration
- 🌿 **Disease Detection**: Upload and analyze crop disease images
- 🌤️ **Weather Forecasts**: 7-day weather predictions with alerts
- 💰 **Market Prices**: Real-time pricing and predictions
- 🌍 **Multi-language**: English, Hindi, Telugu, Tamil support
- 📱 **Responsive Design**: Works on all devices

## Tech Stack

- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Internationalization**: i18next
- **File Upload**: React Dropzone

## Quick Start

### 1. Prerequisites

- Node.js 16+ and npm

### 2. Installation

```bash
cd Frontend

# Install dependencies
npm install
```

### 3. Environment Setup

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 4. Run Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

### 5. Build for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

## Project Structure

```
Frontend/
├── src/
│   ├── components/
│   │   └── common/
│   │       ├── Header.jsx
│   │       ├── Footer.jsx
│   │       ├── Layout.jsx
│   │       ├── Loader.jsx
│   │       ├── PrivateRoute.jsx
│   │       └── LanguageSelector.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── DiseaseDetection.jsx
│   │   ├── Weather.jsx
│   │   ├── MarketPrices.jsx
│   │   ├── Profile.jsx
│   │   └── History.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── apiService.js
│   ├── utils/
│   │   ├── constants.js
│   │   └── helpers.js
│   ├── i18n/
│   │   ├── config.js
│   │   └── locales/
│   │       ├── en.json
│   │       ├── hi.json
│   │       ├── te.json
│   │       └── ta.json
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features by Page

### Home
- Landing page with features overview
- Call-to-action for registration

### Login/Register
- User authentication
- Form validation
- Multi-language support

### Dashboard
- Overview statistics
- Recent detections
- Quick action cards
- Crop list

### Disease Detection
- Image upload (drag & drop)
- Real-time disease detection
- Confidence scores
- Treatment recommendations

### Weather
- Current weather display
- 7-day forecast
- Crop-specific alerts

### Market Prices
- Current market prices
- Historical price charts
- 7-day price predictions
- Trend analysis

### Profile
- User information management
- Crop management (add, view, delete)
- Language preferences

### History
- All disease detections
- Image gallery
- Detection metadata

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| VITE_API_URL | Backend API URL | http://localhost:8000/api/v1 |

## Styling

The app uses Tailwind CSS for styling with a custom configuration:

- Primary color: Green (agriculture theme)
- Responsive breakpoints
- Custom components in `index.css`

## Internationalization

Supported languages:
- English (en)
- Hindi (hi)
- Telugu (te)
- Tamil (ta)

Language files are in `src/i18n/locales/`

## API Integration

All API calls are centralized in `src/services/apiService.js`:

- Authentication
- Disease Detection
- Weather Forecasts
- Market Prices
- Chatbot
- User Profile

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

### Vercel (Recommended)

```bash
npm run build
# Deploy dist/ folder to Vercel
```

### Netlify

```bash
npm run build
# Deploy dist/ folder to Netlify
```

## License

MIT License

## Support

For issues and questions, contact the development team.
