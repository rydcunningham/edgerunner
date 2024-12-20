import React from 'react'
import './globals.css'

export const metadata = {
  title: 'edgerunner.io',
  description: 'Coming soon',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      {/* Previous version with static background:
      <body 
        className="min-h-screen"
        style={{
          backgroundImage: "url('/abstract_gray.avif')",
          backgroundSize: 'cover',
        }}
      >
      */}
      <body className="min-h-screen relative">
        <video 
          autoPlay 
          loop 
          muted 
          playsInline
          className="fixed inset-0 w-full h-full object-cover z-0"
        >
          <source src="/background2.mp4" type="video/mp4" />
        </video>
        <div className="fixed inset-0 bg-black/30 z-[1]" />
        <div className="relative z-10">
          {children}
        </div>
      </body>
    </html>
  )
} 