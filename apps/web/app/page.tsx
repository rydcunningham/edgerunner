import React from 'react'

export default function Page() {
  return (
    <div className="min-h-screen relative flex flex-col">
      {/* Gradient descent visualization */}
      <div className="fixed right-48 top-1/2 -translate-y-1/2">
        <img
          src="assets/gradient_descent.svg"
          alt="Gradient descent visualization"
          className="w-[30vw] h-auto"
        />
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-left justify-center px-24 pl-24">
        <img
          src="img/edgerunner_wordmark.png"
          alt="edgerunner"
          className="w-72 h-auto object-contain mb-8"
        />
        <div className="space-y-4 text-left">
          <h2 className="text-white/90 text-2xl font-medium">EDGERUNNER VENTURES</h2>
          <p className="text-white/50 text-base">
            Full site launching soon
          </p>
        </div>
      </div>
    </div>
  )
} 