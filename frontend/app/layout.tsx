import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RentasAI",
  description: "Live-ready agentic mobility recovery for Malaysian commuters."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
