import Image from 'next/image';
import siteConfig from '../site.config';

export default function AuthorBox({ author }) {
  // Default author is from site config
  const authorName = author || siteConfig.defaultAuthor;
  
  // This would normally be a lookup to an authors database
  // For the template, we'll just use a placeholder
  const authorInfo = {
    name: authorName,
    bio: `${authorName} is a content creator specializing in detailed guides and reviews.`,
    image: '/assets/author-placeholder.jpg'
  };

  return (
    <div className="author-box rounded-lg border border-gray-200 bg-gray-50 p-6">
      <h3 className="mb-4 text-lg font-medium text-gray-900">About the Author</h3>
      <div className="flex flex-col items-center space-y-4 sm:flex-row sm:space-x-6 sm:space-y-0">
        <div className="relative h-24 w-24 overflow-hidden rounded-full">
          <Image
            src={authorInfo.image}
            alt={authorInfo.name}
            fill
            sizes="96px"
            className="object-cover"
          />
        </div>
        <div>
          <h4 className="mb-2 text-lg font-medium">{authorInfo.name}</h4>
          <p className="text-gray-600">{authorInfo.bio}</p>
        </div>
      </div>
    </div>
  );
}
