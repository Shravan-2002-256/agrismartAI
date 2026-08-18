// Pagination Component
// Reusable pagination for lists and grids
// Supports page numbers and previous/next navigation

import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';

const Pagination = ({ 
  currentPage = 1, 
  totalPages = 1, 
  onPageChange,
  itemsPerPage = 10,
  totalItems = 0
}) => {
  if (totalPages <= 1) return null;

  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5; // Show max 5 page numbers

    if (totalPages <= maxVisible) {
      // Show all pages
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Smart pagination with ellipsis
      if (currentPage <= 3) {
        pages.push(1, 2, 3, 4, '...', totalPages);
      } else if (currentPage >= totalPages - 2) {
        pages.push(1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
      } else {
        pages.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages);
      }
    }

    return pages;
  };

  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 py-4">
      {/* Items info */}
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Showing <span className="font-semibold text-gray-900 dark:text-white">{startItem}</span> to{' '}
        <span className="font-semibold text-gray-900 dark:text-white">{endItem}</span> of{' '}
        <span className="font-semibold text-gray-900 dark:text-white">{totalItems}</span> results
      </p>

      {/* Pagination controls */}
      <div className="flex items-center gap-2">
        {/* Previous button */}
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="p-2 rounded-lg border border-gray-300 dark:border-gray-600 
                     hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 
                     disabled:cursor-not-allowed transition-colors"
          aria-label="Previous page"
        >
          <FiChevronLeft className="text-gray-600 dark:text-gray-400" />
        </button>

        {/* Page numbers */}
        <div className="flex items-center gap-1">
          {getPageNumbers().map((page, index) => {
            if (page === '...') {
              return (
                <span
                  key={`ellipsis-${index}`}
                  className="px-3 py-2 text-gray-500 dark:text-gray-400"
                >
                  ...
                </span>
              );
            }

            return (
              <button
                key={page}
                onClick={() => onPageChange(page)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                  currentPage === page
                    ? 'bg-primary-600 text-white shadow-md scale-105'
                    : 'border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                {page}
              </button>
            );
          })}
        </div>

        {/* Next button */}
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="p-2 rounded-lg border border-gray-300 dark:border-gray-600 
                     hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 
                     disabled:cursor-not-allowed transition-colors"
          aria-label="Next page"
        >
          <FiChevronRight className="text-gray-600 dark:text-gray-400" />
        </button>
      </div>
    </div>
  );
};

export default Pagination;
