import React from 'react'

export default function Page() {
  // Format current date as YYYY.MM.DD
  const formattedDate = new Date().toISOString().split('T')[0].replace(/-/g, '.')

  return (
    <>
      {/* Loading Screen */}
      <div className="loading-screen fixed inset-0 z-50 flex items-center justify-center bg-black">
        <div className="w-[202px]">
          <p className="text-[#F75049] text-sm tracking-wider mb-2">LOADING...</p>
          <div className="progress-container">
            <div className="progress-bar" />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="min-h-screen relative flex flex-col">
        {/* Navigation */}
        <nav className="fixed top-8 left-6 z-10">
          <ul className="flex space-x-8">
            <li>
              <a href="#" className="text-white/30 hover:text-[#F75049] active:text-[#F75049] text-sm uppercase tracking-wider transition-colors">
                Consequat
              </a>
            </li>
            <li>
              <a href="#" className="text-white/30 hover:text-[#F75049] active:text-[#F75049] text-sm uppercase tracking-wider transition-colors">
                Adipiscing
              </a>
            </li>
            <li>
              <a href="#" className="text-white/30 hover:text-[#F75049] active:text-[#F75049] text-sm uppercase tracking-wider transition-colors">
                Vestibulum
              </a>
            </li>
            <li>
              <a href="#" className="text-white/30 hover:text-[#F75049] active:text-[#F75049] text-sm uppercase tracking-wider transition-colors">
                Phasellus
              </a>
            </li>
          </ul>
        </nav>
        <div className="flex-1 flex flex-col items-left justify-center px-24 pl-24">
          <img
            src="img/edgerunner_wordmark.png"
            alt="edgerunner"
            className="w-72 h-auto object-contain mb-8"
          />
          <div className="space-y-4 text-left">
            <h2 className="text-white/90 text-2xl font-medium">Welcome to Edgerunner</h2>
            <p className="text-white/70 text-lg">
              UNDER CONSTRUCTION
            </p>
            <p className="text-white/50 text-base">
              Full site launching soon
            </p>
          </div>
        </div>

        {/* Date text */}
        <div className="fixed left-6 top-20 origin-top-left -rotate-90">
          <p className="text-white/30 text-sm tracking-wider">{formattedDate}</p>
        </div>

        {/* Left bar with slashes */}
        <div className="fixed left-6 top-1/2 -translate-y-1/2">
          <img
            src="assets/left bar.svg"
            alt="Decorative left bar"
            className="h-[50vh] w-auto"
          />
        </div>

        {/* Gradient descent visualization */}
        <div className="fixed right-48 top-1/2 -translate-y-1/2">
          <img
            src="assets/gradient_descent.svg"
            alt="Gradient descent visualization"
            className="w-[30vw] h-auto"
          />
        </div>

        {/* Footer bar */}
        <div className="fixed bottom-12 left-9 right-9">
          <img
            src="assets/footer bar.svg"
            alt="Decorative footer bar"
            className="w-full h-auto"
          />
        </div>

        {/* Bottom text */}
        <div className="fixed bottom-4 left-9">
          <p className="text-white/30 text-xs">EDGERUNNER VENTURES © 2025</p>
        </div>
      </div>
    </>
  )
} 