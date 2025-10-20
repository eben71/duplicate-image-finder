import "../styles/globals.css";
import ThemeProvider from "@theme/ThemeProvider";
import Sidebar from "@layout/Sidebar";
import HeaderBar from "@layout/HeaderBar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
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
