'use client'
import React from 'react'

export default function Page() {
  const [showLogs, setShowLogs] = React.useState(true)

  return (
    <div className="min-h-screen relative">
      <div className="w-full h-screen p-6 pl-[60px] pb-8">
        <div className="grid grid-cols-2 h-[calc(100vh-120px)] gap-6">
          {/* Left Column */}
          <div className="flex flex-col h-full space-y-6">
            {/* Metrics Section */}
            <div className="grid grid-cols-3 gap-4">
              {/* Big Number */}
              <div className="terminal-box p-4">
                <div className="text-[11px] text-white/50 mb-2">ACTIVE AGENTS</div>
                <div className="text-[#5EF6FF] text-4xl font-bold">247</div>
              </div>
              
              {/* Bar Chart */}
              <div className="terminal-box p-4">
                <div className="text-[11px] text-white/50 mb-2">RESOURCE USAGE</div>
                <div className="h-20 flex items-end space-x-1">
                  {[40, 60, 30, 80, 50].map((height, i) => (
                    <div key={i} className="flex-1">
                      <div 
                        className="bg-[#5EF6FF] w-full transition-all" 
                        style={{ height: `${height}%` }}
                      />
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Line Chart */}
              <div className="terminal-box p-4">
                <div className="text-[11px] text-white/50 mb-2">PERFORMANCE</div>
                <div className="h-20 flex items-end">
                  <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path
                      d="M0,50 L20,30 L40,45 L60,20 L80,35 L100,25"
                      fill="none"
                      stroke="#5EF6FF"
                      strokeWidth="2"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* Terminal/Income Statement Toggle Box */}
            <div className="terminal-box flex-grow overflow-hidden p-4">
              <div className="flex justify-between items-center mb-2">
                <div className="text-[11px] text-white/50">
                  {showLogs ? 'LOGS' : 'INCOME STATEMENT'}
                </div>
                <div className="flex items-center space-x-4">
                  <button 
                    className={`text-[11px] ${showLogs ? 'text-[#5EF6FF]' : 'text-white/50'} hover:text-[#5EF6FF] transition-colors`}
                    onClick={() => setShowLogs(true)}
                  >
                    LOGS
                  </button>
                  <span className="text-white/50">·</span>
                  <button 
                    className={`text-[11px] ${!showLogs ? 'text-[#5EF6FF]' : 'text-white/50'} hover:text-[#5EF6FF] transition-colors`}
                    onClick={() => setShowLogs(false)}
                  >
                    FINANCIALS
                  </button>
                </div>
              </div>

              {showLogs ? (
                // Terminal Logs View
                <div className="font-mono text-[11px] space-y-1 h-[calc(100%-24px)] overflow-y-auto">
                  <div className="text-white/50">[INFO] Simulation initialized</div>
                  <div className="text-white/50">[INFO] Loading agent configurations...</div>
                  <div className="text-[#5EF6FF]">[WARN] Resource allocation at 75%</div>
                  <div className="text-white/50">[INFO] Agent pathfinding optimized</div>
                  <div className="text-white/50">[DEBUG] Cache hit ratio: 0.89</div>
                  <div className="text-[#5EF6FF]">[WARN] Network latency spike detected</div>
                  <div className="text-white/50">[INFO] Rebalancing workload...</div>
                  <div className="text-white/50 animate-pulse">_</div>
                </div>
              ) : (
                // Income Statement View
                <div className="font-mono text-[11px] space-y-4 h-[calc(100%-24px)] overflow-y-auto p-2">
                  <div className="border-b border-white/10 pb-4">
                    <div className="flex justify-between items-center">
                      <span className="text-white/50">REVENUE (TRIP FARES)</span>
                      <span className="text-[#5EF6FF]">$842,150</span>
                    </div>
                  </div>
                  
                  <div className="space-y-2 border-b border-white/10 pb-4">
                    <div className="flex justify-between items-center">
                      <span className="text-white/50">ENERGY COSTS</span>
                      <span className="text-white/50">($215,430)</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-white/50">MAINTENANCE COSTS</span>
                      <span className="text-white/50">($156,780)</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-white/50">OPERATING PROFIT</span>
                      <span className="text-[#5EF6FF]">$469,940</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-white/50">OPERATING MARGIN</span>
                      <span className="text-[#5EF6FF]">55.8%</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Map */}
          <div className="terminal-box h-full p-4">
            <div className="text-[11px] text-white/50 mb-2">MAP</div>
            <div className="w-full h-[calc(100%-24px)] bg-black/30 flex items-center justify-center rounded">
              <div className="text-white/50 text-sm">
                Kepler.gl map loading...
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 