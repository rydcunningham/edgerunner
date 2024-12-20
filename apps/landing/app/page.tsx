import React from 'react'

export default function Page() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-[62.5vw] h-[27vh] rounded-xl backdrop-blur-xl bg-gray/30 border border-white/30 flex flex-col items-center justify-center gap-4">
        <img
          src="/edgerunner_wordmark.png"
          alt="edgerunner"
          className="w-72 h-auto object-contain"
        />
        <p className="text-white/80 text-sm">coming soon</p>
      </div>
    </div>
  )
} 