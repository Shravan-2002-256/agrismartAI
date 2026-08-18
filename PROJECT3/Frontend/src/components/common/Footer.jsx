import { useTranslation } from 'react-i18next';

const Footer = () => {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-800 text-white mt-auto">
      <div className="container mx-auto px-4 py-6">
        <div className="text-center">
          <p className="text-sm">
            © {currentYear} {t('app_name')}. All rights reserved.
          </p>
          <p className="text-xs text-gray-400 mt-2">
            {t('tagline')}
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
