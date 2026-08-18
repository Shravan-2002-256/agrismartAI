// Share Modal Component
// Allows sharing detection results via multiple channels
// WhatsApp, Email, Copy Link

import { useState } from 'react';
import { FiShare2, FiX, FiCopy, FiMail, FiCheck } from 'react-icons/fi';
import { toast } from 'react-toastify';

const ShareModal = ({ isOpen, onClose, detection }) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !detection) return null;

  const shareUrl = `${window.location.origin}/detection/${detection.id}`;
  const shareText = `AgriSmart AI Detection: ${detection.disease_detected} - ${detection.confidence}% confidence`;

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopied(true);
      toast.success('Link copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast.error('Failed to copy link');
    }
  };

  const shareViaWhatsApp = () => {
    const message = encodeURIComponent(`${shareText}\n\n${shareUrl}`);
    window.open(`https://wa.me/?text=${message}`, '_blank');
  };

  const shareViaEmail = () => {
    const subject = encodeURIComponent('AgriSmart AI Detection Result');
    const body = encodeURIComponent(`${shareText}\n\nView details: ${shareUrl}`);
    window.location.href = `mailto:?subject=${subject}&body=${body}`;
  };

  const shareNative = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AgriSmart AI Detection',
          text: shareText,
          url: shareUrl
        });
      } catch (error) {
        console.log('Share cancelled');
      }
    } else {
      toast.info('Native sharing not supported on this device');
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 animate-fadeIn">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-md w-full">
        {/* Header */}
        <div className="border-b border-gray-200 dark:border-gray-700 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
              <FiShare2 className="text-primary-600 dark:text-primary-400 text-xl" />
            </div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Share Detection
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <FiX className="text-gray-600 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          {/* Detection Preview */}
          <div className="p-4 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Sharing:</p>
            <p className="font-bold text-gray-900 dark:text-white">{detection.disease_detected}</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {detection.confidence}% confidence • {detection.crop_type}
            </p>
          </div>

          {/* Share Options */}
          <div className="space-y-2">
            {/* WhatsApp */}
            <button
              onClick={shareViaWhatsApp}
              className="w-full flex items-center gap-3 p-4 rounded-lg border-2 border-gray-200 dark:border-gray-600
                         hover:border-green-500 dark:hover:border-green-400 transition-all group"
            >
              <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                <span className="text-2xl">💬</span>
              </div>
              <div className="text-left flex-1">
                <p className="font-semibold text-gray-900 dark:text-white group-hover:text-green-600 
                              dark:group-hover:text-green-400">
                  Share on WhatsApp
                </p>
                <p className="text-xs text-gray-600 dark:text-gray-400">Send to your contacts</p>
              </div>
            </button>

            {/* Email */}
            <button
              onClick={shareViaEmail}
              className="w-full flex items-center gap-3 p-4 rounded-lg border-2 border-gray-200 dark:border-gray-600
                         hover:border-blue-500 dark:hover:border-blue-400 transition-all group"
            >
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <FiMail className="text-blue-600 dark:text-blue-400 text-xl" />
              </div>
              <div className="text-left flex-1">
                <p className="font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 
                              dark:group-hover:text-blue-400">
                  Share via Email
                </p>
                <p className="text-xs text-gray-600 dark:text-gray-400">Send detailed report</p>
              </div>
            </button>

            {/* Copy Link */}
            <button
              onClick={copyToClipboard}
              className="w-full flex items-center gap-3 p-4 rounded-lg border-2 border-gray-200 dark:border-gray-600
                         hover:border-primary-500 dark:hover:border-primary-400 transition-all group"
            >
              <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
                {copied ? (
                  <FiCheck className="text-green-600 dark:text-green-400 text-xl" />
                ) : (
                  <FiCopy className="text-primary-600 dark:text-primary-400 text-xl" />
                )}
              </div>
              <div className="text-left flex-1">
                <p className="font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 
                              dark:group-hover:text-primary-400">
                  {copied ? 'Link Copied!' : 'Copy Link'}
                </p>
                <p className="text-xs text-gray-600 dark:text-gray-400 truncate">{shareUrl}</p>
              </div>
            </button>

            {/* Native Share (if supported) */}
            {navigator.share && (
              <button
                onClick={shareNative}
                className="w-full flex items-center gap-3 p-4 rounded-lg border-2 border-gray-200 dark:border-gray-600
                           hover:border-purple-500 dark:hover:border-purple-400 transition-all group"
              >
                <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
                  <span className="text-2xl">📱</span>
                </div>
                <div className="text-left flex-1">
                  <p className="font-semibold text-gray-900 dark:text-white group-hover:text-purple-600 
                                dark:group-hover:text-purple-400">
                    More Options
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">Use device share menu</p>
                </div>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShareModal;
