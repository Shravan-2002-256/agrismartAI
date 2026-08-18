import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { FiLogOut, FiUser, FiMenu, FiX } from 'react-icons/fi';
import { authService } from '../../services/apiService';
import { useState } from 'react';
import LanguageSelector from './LanguageSelector';
import Notifications from '../Notifications';
import ThemeToggle from './ThemeToggle';
import Logo from './Logo';
import Tooltip from './Tooltip';
import { featureDescriptions } from '../../utils/featureDescriptions';

const Header = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isAuthenticated = authService.isAuthenticated();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const navLinks = [
    { path: '/dashboard', label: t('dashboard'), key: 'dashboard' },
    { path: '/disease-detection', label: t('disease_detection'), key: 'disease_detection' },
    { path: '/disease-analytics', label: t('disease_analytics'), key: 'disease_analytics' },
    { path: '/irrigation-calculator', label: t('irrigation_calculator'), key: 'irrigation_calculator' },
    { path: '/weather', label: t('weather'), key: 'weather' },
    { path: '/market', label: t('market_prices'), key: 'market' },
    { path: '/history', label: t('history'), key: 'history' },
    { path: '/insights', label: t('insights'), key: 'insights' },
    { path: '/chatbot', label: t('chat'), key: 'chat' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to={isAuthenticated ? '/dashboard' : '/'} className="hover:opacity-80 transition-opacity">
            <Logo size="default" />
          </Link>

          {/* Desktop Navigation */}
          {isAuthenticated && (
            <nav className="hidden lg:flex items-center space-x-1">
              {navLinks.map((link) => (
                <Tooltip key={link.path} text={featureDescriptions[link.key]} position="bottom">
                  <Link
                    to={link.path}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      location.pathname === link.path
                        ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                    }`}
                  >
                    {link.label}
                  </Link>
                </Tooltip>
              ))}
            </nav>
          )}

          {/* Right Side Actions */}
          <div className="hidden md:flex items-center gap-3">
            <ThemeToggle />
            <LanguageSelector />
            
            {isAuthenticated && (
              <>
                <div className="h-6 w-px bg-gray-300 dark:bg-gray-700" />
                <Notifications />
                <Link
                  to="/profile"
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                    {authService.getCurrentUser()?.name?.[0]?.toUpperCase() || 'U'}
                  </div>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{t('profile')}</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                >
                  <FiLogOut />
                  <span>{t('logout')}</span>
                </button>
              </>
            )}
            
            {!isAuthenticated && (
              <>
                <Link to="/login" className="btn-secondary-pro text-sm">
                  {t('login')}
                </Link>
                <Link to="/register" className="btn-primary-pro text-sm">
                  {t('register')}
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-gray-700"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pb-4">
            {isAuthenticated && (
              <nav className="flex flex-col space-y-2 mb-4">
                {navLinks.map((link) => (
                  <Link
                    key={link.path}
                    to={link.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`px-4 py-2 rounded ${
                      location.pathname === link.path
                        ? 'bg-primary-100 text-primary-700'
                        : 'hover:bg-gray-100'
                    }`}
                  >
                    {link.label}
                  </Link>
                ))}
              </nav>
            )}

            <div className="flex flex-col space-y-2">
              <LanguageSelector />
              
              {isAuthenticated ? (
                <>
                  <Link
                    to="/profile"
                    onClick={() => setMobileMenuOpen(false)}
                    className="btn-secondary"
                  >
                    <FiUser className="inline mr-2" />
                    {t('profile')}
                  </Link>
                  <button onClick={handleLogout} className="btn-secondary text-red-600">
                    <FiLogOut className="inline mr-2" />
                    {t('logout')}
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="btn-secondary">
                    {t('login')}
                  </Link>
                  <Link to="/register" className="btn-primary">
                    {t('register')}
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
