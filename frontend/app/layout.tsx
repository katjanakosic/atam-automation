import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import "./globals.css"
import { StepNav } from "@/components/step-nav"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
})

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "ATAM Evaluation",
  description:
    "Expert evaluation of automated Architecture Tradeoff Analysis Method results",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen flex flex-col`}
      >
        <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
          <div className="mx-auto max-w-6xl flex items-center justify-between px-6 py-4">
            <h1 className="text-lg font-semibold tracking-tight">
              ATAM Evaluation
            </h1>
            <StepNav />
          </div>
        </header>
        <main className="flex-1">{children}</main>
        <footer className="border-t py-6 text-center text-sm text-muted-foreground">
          Automated ATAM Analysis — Expert Evaluation Interface
        </footer>
      </body>
    </html>
  )
}
