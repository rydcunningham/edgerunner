export default function Page() {
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
                <div className="text-[#F75049] text-4xl font-bold">247</div>
              </div>
              
              {/* Bar Chart */}
              <div className="terminal-box p-4">
                <div className="text-[11px] text-white/50 mb-2">RESOURCE USAGE</div>
                <div className="h-20 flex items-end space-x-1">
                  {[40, 60, 30, 80, 50].map((height, i) => (
                    <div key={i} className="flex-1">
                      <div 
                        className="bg-[#F75049] w-full transition-all" 
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
                      stroke="#F75049"
                      strokeWidth="2"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* Terminal */}
            <div className="terminal-box flex-grow overflow-hidden p-4">
              <div className="text-[11px] text-white/50 mb-2">SIMULATION LOGS</div>
              <div className="font-mono text-[11px] space-y-1 h-[calc(100%-24px)] overflow-y-auto">
                <div className="text-white/50">[INFO] Simulation initialized</div>
                <div className="text-white/50">[INFO] Loading agent configurations...</div>
                <div className="text-[#F75049]">[WARN] Resource allocation at 75%</div>
                <div className="text-white/50">[INFO] Agent pathfinding optimized</div>
                <div className="text-white/50">[DEBUG] Cache hit ratio: 0.89</div>
                <div className="text-[#F75049]">[WARN] Network latency spike detected</div>
                <div className="text-white/50">[INFO] Rebalancing workload...</div>
                <div className="text-white/50 animate-pulse">_</div>
              </div>
            </div>
          </div>

          {/* Right Column - Map */}
          <div className="terminal-box h-full p-4">
            <div className="text-[11px] text-white/50 mb-2">SIMULATION MAP</div>
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