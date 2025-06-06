import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import MuiProvider from "../mui-provider";
import { AppBar, Toolbar, IconButton } from "@mui/material";
import { LightMode } from "@mui/icons-material";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <MuiProvider>
          <div style={{
            width: '100%',
            position: 'fixed',
            top: 0,
            left: 0,
            zIndex: 100,
            background: 'rgba(24,28,36,0.65)',
            borderBottom: '2px solid #ffcb05',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: 56,
            backdropFilter: 'blur(10px) saturate(200%)',
            WebkitBackdropFilter: 'blur(10px) saturate(200%)',
            boxShadow: '0 2px 16px 0 rgba(255,203,5,0.10)',
          }}>
            <span style={{ fontWeight: 900, fontSize: '1.6rem', color: '#ffcb05', letterSpacing: 1 }}>
              Pokebase
            </span>
          </div>
          <div className="content-wrapper" style={{ minHeight: '100vh', background: 'none', paddingTop: 56 }}>
            {children}
          </div>
        </MuiProvider>
      </body>
    </html>
  );
}
