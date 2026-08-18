import Header from '../common/Header';
import Footer from '../common/Footer';
import FloatingChatWidget from '../common/FloatingChatWidget';

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>
      <Footer />
      
      {/* Floating Chat Widget - Shows on all pages except /chatbot */}
      <FloatingChatWidget />
    </div>
  );
};

export default Layout;
