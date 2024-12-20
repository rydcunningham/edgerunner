'use client'

import React from 'react'

export default function LandingPage() {
  return (
    <div className="w-80 h-[33vh] rounded-xl backdrop-blur-xl bg-white/20 border border-white/30 flex flex-col items-center justify-center gap-4">
      <img
        src="/wordmark.png"
        alt="edgerunner"
        className="w-32 h-auto object-contain"
      />
      <p className="text-white/80 text-sm">coming soon</p>
    </div>
  )
} 