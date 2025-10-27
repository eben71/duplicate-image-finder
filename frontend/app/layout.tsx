import type { ReactNode } from "react";
import "./globals.css";
import HeaderBar from "@layout/HeaderBar";
import Sidebar from "@layout/Sidebar";
import ThemeProvider from "@theme/ThemeProvider";

export default function RootLayout({ children }: { children: ReactNode }) {
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
      </body>
    </html>
  );
}
