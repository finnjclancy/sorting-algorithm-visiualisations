import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Algorithm Visualizer",
  description: "Visualize sorting algorithms and graph traversals",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main className="min-h-screen p-4 md:p-8">
          {children}
        </main>
        <footer className="p-4 text-right text-xs text-gray-500">
          finn clancy 2025
        </footer>
      </body>
    </html>
  );
}
