'use client'

import React, { useState } from 'react'
import Image from 'next/image'

export default function ConfigPage() {
  const [activeSection, setActiveSection] = useState('DOCS')
  const [showOptional, setShowOptional] = useState(false)

  return (
    <div className="min-h-screen p-8 bg-black text-white">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl text-[#5EF6FF]">CONFIGURATION</h2>
        <div className="flex space-x-4">
          <button 
            className={`text-[#5EF6FF] hover:text-white ${activeSection === 'INPUT' ? 'underline' : ''}`}
            onClick={() => setActiveSection('INPUT')}
          >
            INPUT
          </button>
          <button 
            className={`text-[#5EF6FF] hover:text-white ${activeSection === 'DOCS' ? 'underline' : ''}`}
            onClick={() => setActiveSection('DOCS')}
          >
            DOCS
          </button>
        </div>
      </div>

      {activeSection === 'DOCS' ? (
        <div>
          {/* Vehicles Section */}
          <section className="mb-12">
            <h2 className="text-3xl text-[#5EF6FF] mb-4">VEHICLES</h2>
            <p className="mb-8 text-white/70">Explore the range of vehicles designed for various operations.</p>

            {/* Rideshare */}
            <h3 className="text-2xl text-[#5EF6FF] mb-4">RIDESHARE</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">GROUND</h4>
                <div className="terminal-box mb-2">
                  <Image src="/vehicles/AV.png" alt="Ground Vehicle" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">AVs are full-size ground vehicles which ferry variable numbers of people from place to place anywhere on the map.</p>
              </div>
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">AERIAL</h4>
                <div className="terminal-box mb-2">
                  <Image src="/vehicles/eVTOL.png" alt="Aerial Vehicle" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">eVTOLs are aerial ridesharing vehicles which can ferry up to 5 passengers between Skyports via straight-line distance or fixed Skyways.</p>
              </div>
            </div>

            {/* Delivery */}
            <h3 className="text-2xl text-[#5EF6FF] mb-4">DELIVERY</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">DROID</h4>
                <div className="terminal-box mb-2">
                  <Image src="/vehicles/droid.png" alt="Droid" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">DROIDs are ground-based mini AVs responsible primarily for delivery operations, especially of heavier cargo. They cannot carry people.</p>
              </div>
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">DRONE</h4>
                <div className="terminal-box mb-2">
                  <Image src="/vehicles/UAV.png" alt="Drone" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">DRONEs are UAVs that, while smaller than their eVTOL counterparts, can be just as fast. They are responsible for small package delivery operations.</p>
              </div>
            </div>
          </section>

          {/* Infrastructure Section */}
          <section>
            <h2 className="text-3xl text-[#5EF6FF] mb-4">INFRASTRUCTURE</h2>
            <p className="mb-8 text-white/70">Charging, operations, and maintenance facilities for autonomous vehicles.</p>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Depots */}
              <div>
                <h3 className="text-2xl text-[#5EF6FF] mb-4">DEPOTs</h3>
                <div className="terminal-box mb-2">
                  <Image src="/infra/depot.png" alt="Depot" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">Ground-based charging and maintenance centers for autonomous vehicles. Has multiple chargers and maintenance bays.</p>
              </div>

              {/* Skyports */}
              <div>
                <h3 className="text-2xl text-[#5EF6FF] mb-4">SKYPORTs</h3>
                <div className="terminal-box mb-2">
                  <Image src="/infra/skyport.png" alt="Skyport" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">Towers for handling eVTOL charging, maintenance, and passenger egress/ingress operations. Has multiple pads for simultaneous takeoff and landing of multiple aircraft.</p>
              </div>

              {/* Droneports */}
              <div>
                <h3 className="text-2xl text-[#5EF6FF] mb-4">DRONEPORTs</h3>
                <div className="terminal-box mb-2">
                  <Image src="/infra/droneport.png" alt="Droneport" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">Miniature skyports which handle similar operations for drone delivery operations. Small enough that single towers can be installed at partner restaurants. Usually installed alongside DEPOTs.</p>
              </div>
            </div>
          </section>
        </div>
      ) : (
        <div className="space-y-8">
          {/* Fleet Configuration */}
          <h2 className="text-2xl text-[#5EF6FF] mb-4">FLEET</h2>
          <section className="terminal-box p-6">
            <h3 className="text-lg text-[#5EF6FF] mb-4">VEHICLES</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Ground Vehicles */}
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">GROUND VEHICLES</h4>
                <label className="block text-white/70 text-sm mb-2">Fleet Size</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="100" />
                {showOptional && (
                  <div className="mt-4 space-y-4">
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Battery Capacity (kWh)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="75" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Miles per kWh</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="4" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Max Passengers</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="4" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Vehicle Capex ($)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="100000" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Battery Replacement Cost ($)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="15000" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Vehicle Useful Life (miles)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="100000" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Battery Useful Life (miles)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="30000" />
                    </div>
                  </div>
                )}
              </div>

              {/* Aerial Vehicles */}
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">AERIAL VEHICLES</h4>
                <label className="block text-white/70 text-sm mb-2">Fleet Size</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="100" />
                {showOptional && (
                  <div className="mt-4 space-y-4">
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Battery Capacity (kWh)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="75" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Miles per kWh</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="4" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Max Passengers</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="4" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Vehicle Capex ($)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="100000" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Battery Replacement Cost ($)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="15000" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Vehicle Useful Life (miles)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="100000" />
                    </div>
                    <div>
                      <label className="block text-white/70 text-sm mb-2">Battery Useful Life (miles)</label>
                      <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="30000" />
                    </div>
                  </div>
                )}
              </div>
            </div>
            <div className="flex justify-end mt-4">
              <button 
                className="text-[#5EF6FF] hover:text-white text-sm"
                onClick={() => setShowOptional(!showOptional)}
              >
                {showOptional ? 'Hide Optional Inputs' : 'Show Optional Inputs'}
              </button>
            </div>
          </section>

          {/* Pricing Configuration */}
          <section className="terminal-box p-6">
            <h3 className="text-lg text-[#5EF6FF] mb-4">PRICING</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-white/70 text-sm mb-2">Base Pickup Fee ($)</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="3.00" />
              </div>
              <div>
                <label className="block text-white/70 text-sm mb-2">Per Mile Rate ($)</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="0.80" />
              </div>
              
              {/* Surge Pricing */}
              <div className="col-span-2">
                <h4 className="text-lg text-[#5EF6FF] mb-4">Surge Periods</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white/70 text-sm mb-2">Morning Rush (7-9 AM)</label>
                    <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="1.2" />
                  </div>
                  <div>
                    <label className="block text-white/70 text-sm mb-2">Evening Rush (5-8 PM)</label>
                    <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="1.2" />
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Costs Configuration */}
          <section className="terminal-box p-6">
            <h3 className="text-lg text-[#5EF6FF] mb-4">COSTS</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-white/70 text-sm mb-2">Energy Cost ($/kWh)</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="0.1625" />
              </div>
              <div>
                <label className="block text-white/70 text-sm mb-2">Vehicle Cost per Mile ($)</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="0.08" />
              </div>
            </div>
          </section>

          {/* Geospatial Configuration */}
          <section className="terminal-box p-6">
            <h3 className="text-lg text-[#5EF6FF] mb-4">GEOSPATIAL</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-white/70 text-sm mb-2">Service Area Radius (miles)</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="4" />
              </div>
              <div>
                <label className="block text-white/70 text-sm mb-2">Average City Speed (mph)</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="15" />
              </div>
            </div>
          </section>

          {/* Infrastructure Configuration */}
          <h2 className="text-2xl text-[#5EF6FF] mb-4">INFRASTRUCTURE</h2>
          <section className="terminal-box p-6">
            <h3 className="text-lg text-[#5EF6FF] mb-4">CHARGING INFRASTRUCTURE</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-white/70 text-sm mb-2">Number of Depots</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="1" />
              </div>
              <div>
                <label className="block text-white/70 text-sm mb-2">Chargers per Depot</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="5" />
              </div>
              <div>
                <label className="block text-white/70 text-sm mb-2">Number of Skyports</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="0" />
              </div>
              <div>
                <label className="block text-white/70 text-sm mb-2">Pads per Skyport</label>
                <input type="number" className="w-full bg-black/30 border border-[#5EF6FF]/20 rounded p-2 text-white" placeholder="6" />
              </div>
            </div>
          </section>

          {/* Submit Button */}
          <div className="flex justify-end">
            <button className="bg-[#5EF6FF]/20 hover:bg-[#5EF6FF]/30 text-[#5EF6FF] px-6 py-2 rounded transition-colors">
              Generate Config
            </button>
          </div>
        </div>
      )}
    </div>
  )
} 