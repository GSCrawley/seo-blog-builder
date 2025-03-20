import { useState } from 'react';
import siteConfig from '../site.config';

export default function AffiliateDisclosure() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="mb-8 rounded-lg bg-blue-50 p-4 text-sm text-gray-700">
      <div className="flex justify-between">
        <div className="flex items-start">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="mr-2 h-5 w-5 text-blue-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div>
            <p className="font-medium">Affiliate Disclosure</p>
            <p className={isExpanded ? '' : 'line-clamp-1'}>
              {siteConfig.affiliateDisclosure}
            </p>
          </div>
        </div>
        <button
          className="ml-2 text-blue-600 hover:text-blue-800"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? 'Show less' : 'Read more'}
        </button>
      </div>
    </div>
  );
}
