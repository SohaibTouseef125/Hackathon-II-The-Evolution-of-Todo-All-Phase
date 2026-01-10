'use client';

import Link from 'next/link';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: { name: string; href: string }[];
  actions?: React.ReactNode;
}

export default function PageHeader({ title, subtitle, breadcrumbs, actions }: PageHeaderProps) {
  return (
    <div className="mb-8">
      {breadcrumbs && (
        <nav className="sm:hidden" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-4">
            {breadcrumbs.map((crumb, index) => (
              <li key={index} className="flex items-center">
                <Link href={crumb.href} className="text-sm font-medium text-gray-500 hover:text-gray-700">
                  {crumb.name}
                </Link>
                {index < breadcrumbs.length - 1 && (
                  <svg className="flex-shrink-0 w-5 h-5 text-gray-300 mx-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </li>
            ))}
          </ol>
        </nav>
      )}

      <div className="hidden sm:block">
        {breadcrumbs && (
          <ol className="flex items-center space-x-4">
            {breadcrumbs.map((crumb, index) => (
              <li key={index}>
                <Link href={crumb.href} className="text-sm font-medium text-gray-500 hover:text-gray-700">
                  {crumb.name}
                </Link>
                {index < breadcrumbs.length - 1 && (
                  <svg className="flex-shrink-0 w-5 h-5 text-gray-300 mx-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </li>
            ))}
          </ol>
        )}
      </div>

      <div className="mt-2 md:flex md:items-center md:justify-between">
        <div className="flex-1 min-w-0">
          <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            {title}
          </h1>
          {subtitle && (
            <p className="mt-1 text-sm text-gray-500">
              {subtitle}
            </p>
          )}
        </div>
        <div className="mt-4 flex md:mt-0 md:ml-4 space-x-3">
          {actions}
        </div>
      </div>
    </div>
  );
}