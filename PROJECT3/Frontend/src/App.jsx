import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { useState, useEffect } from 'react'

// Pages
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import DiseaseDetection from './pages/DiseaseDetection'
import Weather from './pages/Weather'
import MarketPrices from './pages/MarketPrices'
import Profile from './pages/Profile'
import History from './pages/History'
import Chatbot from './pages/Chatbot'
import Insights from './pages/Insights'
import IrrigationCalculator from './pages/IrrigationCalculator'
import DiseaseAnalytics from './pages/DiseaseAnalytics'

// Components
import PrivateRoute from './components/common/PrivateRoute'
import KeyboardShortcuts from './components/common/KeyboardShortcuts'
import TourGuide from './components/common/TourGuide'
import { NotificationContainer } from './components/common/NotificationToast'

function App() {
  const [showTour, setShowTour] = useState(false);

  useEffect(() => {
    // Show tour for first-time users
    const tourShown = localStorage.getItem('agrismart_tour_shown');
    const isAuthenticated = localStorage.getItem('token');
    
    if (!tourShown && isAuthenticated) {
      setTimeout(() => setShowTour(true), 1000);
    }
  }, []);

  return (
    <Router>
      <div className="App">
        {/* Global Components */}
        <KeyboardShortcuts />
        <TourGuide isOpen={showTour} onComplete={() => setShowTour(false)} />
        <NotificationContainer />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected Routes */}
          <Route path="/dashboard" element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } />
          
          <Route path="/disease-detection" element={
            <PrivateRoute>
              <DiseaseDetection />
            </PrivateRoute>
          } />
          
          <Route path="/weather" element={
            <PrivateRoute>
              <Weather />
            </PrivateRoute>
          } />
          
          <Route path="/market" element={
            <PrivateRoute>
              <MarketPrices />
            </PrivateRoute>
          } />
          
          <Route path="/profile" element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          } />
          
          <Route path="/history" element={
            <PrivateRoute>
              <History />
            </PrivateRoute>
          } />
          
          <Route path="/chatbot" element={
            <PrivateRoute>
              <Chatbot />
            </PrivateRoute>
          } />
          
          <Route path="/insights" element={
            <PrivateRoute>
              <Insights />
            </PrivateRoute>
          } />
          
          <Route path="/irrigation-calculator" element={
            <PrivateRoute>
              <IrrigationCalculator />
            </PrivateRoute>
          } />
          
          <Route path="/disease-analytics" element={
            <PrivateRoute>
              <DiseaseAnalytics />
            </PrivateRoute>
          } />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </div>
    </Router>
  )
}

export default App
