export default function Pagination({ currentPage, totalPages, paginate }) {
  const pageNumbers = [];

  for (let i = 1; i <= totalPages; i++) {
    pageNumbers.push(i);
  }

  // Show limited page numbers with ellipsis
  const getPageNumbers = () => {
    if (totalPages <= 7) {
      return pageNumbers;
    }
    
    // Always show first and last page
    // Show ellipsis when needed
    if (currentPage <= 3) {
      return [...pageNumbers.slice(0, 5), '...', totalPages];
    } else if (currentPage >= totalPages - 2) {
      return [1, '...', ...pageNumbers.slice(totalPages - 5)];
    } else {
      return [
        1, 
        '...', 
        currentPage - 1, 
        currentPage, 
        currentPage + 1, 
        '...', 
        totalPages
      ];
    }
  };

  const displayedPageNumbers = getPageNumbers();

  return (
    <nav className="flex justify-center mt-12">
      <ul className="inline-flex items-center -space-x-px">
        <li>
          <button
            onClick={() => paginate(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className={`ml-0 block rounded-l-lg border bg-white px-3 py-2 leading-tight ${
              currentPage === 1
                ? 'cursor-not-allowed border-gray-300 text-gray-300'
                : 'border-gray-300 text-gray-500 hover:bg-gray-100 hover:text-gray-700'
            }`}
          >
            &laquo; Previous
          </button>
        </li>

        {displayedPageNumbers.map((number, index) => (
          <li key={index}>
            {number === '...' ? (
              <span className="border border-gray-300 bg-white px-3 py-2 leading-tight text-gray-500">
                ...
              </span>
            ) : (
              <button
                onClick={() => paginate(number)}
                className={`border px-3 py-2 leading-tight ${
                  currentPage === number
                    ? 'border-blue-500 bg-blue-500 text-white hover:bg-blue-600'
                    : 'border-gray-300 bg-white text-gray-500 hover:bg-gray-100 hover:text-gray-700'
                }`}
              >
                {number}
              </button>
            )}
          </li>
        ))}

        <li>
          <button
            onClick={() => paginate(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className={`block rounded-r-lg border bg-white px-3 py-2 leading-tight ${
              currentPage === totalPages
                ? 'cursor-not-allowed border-gray-300 text-gray-300'
                : 'border-gray-300 text-gray-500 hover:bg-gray-100 hover:text-gray-700'
            }`}
          >
            Next &raquo;
          </button>
        </li>
      </ul>
    </nav>
  );
}
