import type { ReactNode } from 'react';
import Script from 'next/script';
import './globals.css';
import HeaderBar from '@layout/HeaderBar';
import Sidebar from '@layout/Sidebar';
import ThemeProvider from '@theme/ThemeProvider';

export default function RootLayout({ children }: { children: ReactNode }) {
  const isDev = process.env.NODE_ENV === 'development';

  return (
    <html lang="en">
      <body className="min-h-screen">
        <ThemeProvider>
          <HeaderBar />
          <div className="container-max px-4 flex flex-col md:flex-row md:gap-6">
            <Sidebar />
            <main className="flex-1 py-6" role="main">
              {children}
            </main>
          </div>
        </ThemeProvider>
        {!isDev && (
          <>
            {/* Cloudflare Analytics – requires real token to be added before launch. */}
            <Script
              id="cloudflare-analytics"
              defer
              src="https://static.cloudflareinsights.com/beacon.min.js"
              data-cf-beacon='{"token": "REPLACE_WITH_TOKEN"}'
              strategy="afterInteractive"
            />
          </>
        )}
      </body>
    </html>
  );
}
