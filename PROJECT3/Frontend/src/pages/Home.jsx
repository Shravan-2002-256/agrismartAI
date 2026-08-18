import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { FiCheckCircle, FiCloud, FiTrendingUp, FiMessageSquare, FiZap, FiShield } from 'react-icons/fi';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import Logo from '../components/common/Logo';

const Home = () => {
  const { t } = useTranslation();

  const features = [
    {
      icon: <FiCheckCircle className="text-4xl" />,
      title: 'Disease Detection',
      description: 'AI-powered crop disease identification with 92%+ accuracy',
      color: 'from-green-500 to-emerald-600',
      textColor: 'text-green-600 dark:text-green-400'
    },
    {
      icon: <FiCloud className="text-4xl" />,
      title: 'Weather Forecasts',
      description: '7-day weather predictions with crop-specific alerts',
      color: 'from-blue-500 to-cyan-600',
      textColor: 'text-blue-600 dark:text-blue-400'
    },
    {
      icon: <FiTrendingUp className="text-4xl" />,
      title: 'Market Intelligence',
      description: 'Real-time prices and AI predictions to maximize profits',
      color: 'from-purple-500 to-pink-600',
      textColor: 'text-purple-600 dark:text-purple-400'
    },
    {
      icon: <FiMessageSquare className="text-4xl" />,
      title: 'Smart AI Assistant',
      description: 'Get expert advice 24/7 in English, Hindi, Telugu, and Tamil',
      color: 'from-orange-500 to-red-600',
      textColor: 'text-orange-600 dark:text-orange-400'
    },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow">
        {/* Modern Hero Section */}
        <section className="relative bg-gradient-to-br from-primary-600 via-emerald-600 to-green-700 text-white py-24 overflow-hidden">
          {/* Decorative Background */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="text-center max-w-4xl mx-auto animate-fadeIn">
              <div className="flex justify-center mb-6">
                <Logo size="large" />
              </div>
              
              <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
                {t('welcome')}
              </h1>
              
              <p className="text-xl md:text-2xl mb-8 text-primary-50 max-w-2xl mx-auto">
                {t('tagline')} Empowering farmers with cutting-edge AI technology.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
                <Link 
                  to="/register" 
                  className="btn-professional bg-white text-primary-600 hover:bg-gray-100 shadow-lg hover:shadow-xl text-lg px-10 py-4"
                >
                   Get Started Free
                </Link>
                <Link 
                  to="/login" 
                  className="btn-professional border-2 border-white text-white hover:bg-white hover:text-primary-600 text-lg px-10 py-4"
                >
                  Sign In
                </Link>
              </div>
              
              <div className="flex items-center justify-center gap-8 text-sm text-primary-100">
                <div className="flex items-center gap-2">
                  <FiZap className="text-yellow-300" />
                  <span>AI-Powered</span>
                </div>
                <div className="flex items-center gap-2">
                  <FiShield className="text-blue-300" />
                  <span>Trusted by Farmers</span>
                </div>
                <div className="flex items-center gap-2">
                  <FiCheckCircle className="text-green-300" />
                  <span>100% Free</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section with Modern Cards */}
        <section className="py-20 bg-gray-50 dark:bg-gray-900">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16 animate-fadeIn">
              <h2 className="text-4xl font-bold mb-4 text-gray-900 dark:text-white">
                Why Choose AgriSmart AI?
              </h2>
              <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Cutting-edge AI technology designed specifically for modern farmers
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <div 
                  key={index} 
                  className="card-pro text-center group hover:scale-105 transition-all duration-300"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${feature.color} mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    <div className="text-white">
                      {feature.icon}
                    </div>
                  </div>
                  <h3 className={`text-xl font-bold mb-3 ${feature.textColor}`}>
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Statistics Section with Modern Design */}
        <section className="py-20 bg-white dark:bg-gray-800">
          <div className="container mx-auto px-4">
            <div className="grid md:grid-cols-3 gap-12 text-center">
              <div className="card-pro hover:scale-105 transition-transform duration-300">
                <div className="text-6xl font-bold bg-gradient-to-r from-primary-600 to-emerald-600 bg-clip-text text-transparent mb-3">
                  92%+
                </div>
                <div className="text-gray-600 dark:text-gray-400 font-semibold text-lg">
                  AI Detection Accuracy
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                  Industry-leading precision
                </p>
              </div>
              <div className="card-pro hover:scale-105 transition-transform duration-300">
                <div className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent mb-3">
                  38+
                </div>
                <div className="text-gray-600 dark:text-gray-400 font-semibold text-lg">
                  Disease Classes
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                  Comprehensive coverage
                </p>
              </div>
              <div className="card-pro hover:scale-105 transition-transform duration-300">
                <div className="text-6xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
                  4
                </div>
                <div className="text-gray-600 dark:text-gray-400 font-semibold text-lg">
                  Languages Supported
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                  Speak your language
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section with Modern Gradient */}
        <section className="bg-gradient-to-r from-primary-600 via-emerald-600 to-green-600 text-white py-20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-4">
              Ready to Transform Your Farming?
            </h2>
            <p className="text-xl mb-8">
              Join thousands of farmers using AI to improve their yields
            </p>
            <Link to="/register" className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition inline-block">
              Sign Up Now
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
