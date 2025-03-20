import Link from 'next/link';
import siteConfig from '../site.config';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-50 py-8">
      <div className="mx-auto max-w-6xl px-4">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <h3 className="mb-4 text-lg font-bold">About</h3>
            <p className="text-gray-600">
              {siteConfig.description}
            </p>
          </div>
          <div>
            <h3 className="mb-4 text-lg font-bold">Quick Links</h3>
            <ul className="space-y-2">
              {siteConfig.mainNav.map((item) => (
                <li key={item.path}>
                  <Link 
                    href={item.path}
                    className="text-gray-600 hover:text-blue-600 hover:underline"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="mb-4 text-lg font-bold">Legal</h3>
            <ul className="space-y-2">
              {siteConfig.footerLinks.map((item) => (
                <li key={item.path}>
                  <Link 
                    href={item.path}
                    className="text-gray-600 hover:text-blue-600 hover:underline"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-200 pt-8 text-center">
          <p className="text-gray-600">
            &copy; {currentYear} {siteConfig.title}. All rights reserved.
          </p>
          <p className="mt-2 text-sm text-gray-500">
            {siteConfig.affiliateDisclosure}
          </p>
        </div>
      </div>
    </footer>
  );
}
