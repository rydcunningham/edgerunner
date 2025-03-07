import React from 'react'

export default function Page() {
  return (
    <div className="min-h-screen relative">
      <div className="w-full max-w-[1000px]">
        <div className="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
          {/* Main content */}
          <div className="flex flex-col items-start justify-center px-12 pl-24 lg:pl-24 lg:pr-0 pt-24 lg:pt-0">
            <div className="space-y-4">
              <div className="flex flex-col items-left lg:items-start">
                <img
                  src="/glyph.png"
                  alt="Edgerunner Ventures Logo"
                  className="w-[80px] h-auto mb-4"
                />
                <h1 className="text-[#F75049] text-3xl tracking-wide">
                  EDGERUNNER_VENTURES
                </h1>
              </div>
              <p className="text-white/50 text-base">
                backing the cutting <span className="text-[#F75049]">edge</span>.
              </p>
            </div>
          </div>

          {/* Terminal text
          <div className="flex items-start lg:items-center justify-start pl-24 lg:pl-12 mt-12 lg:mt-0">
            <div className="font-rajdhani uppercase tracking-widest bg-black/20 p-6 rounded-lg border border-white/10 max-w-[400px]">
              <div className="space-y-3">
                <div><span className="text-white/50">{'>'}</span><span className="text-[#F75049]"> focus: [ai, infra, deeptech]</span></div>
                <div><span className="text-white/50">{'>'}</span><span className="text-[#F75049]"> stage: [angel, pre-seed, seed]</span></div>
                <div><span className="text-white/50">{'>'}</span><span className="text-[#F75049]"> location: [sf, atx]</span></div>
                <div><span className="text-white/50">{'>'}</span><span className="text-[#F75049]"> _</span></div>
              </div>
            </div>
          </div>
           */}
        </div>
      </div>
    </div>
  )
} 