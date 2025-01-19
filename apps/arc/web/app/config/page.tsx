'use client'

import React, { useState } from 'react'
import Image from 'next/image'

export default function ConfigPage() {
  const [activeSection, setActiveSection] = useState('DOCS')

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
                  <Image src="/placeholder.png" alt="Ground Vehicle" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">AVs are full-size ground vehicles which ferry variable numbers of people from place to place anywhere on the map.</p>
              </div>
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">AERIAL</h4>
                <div className="terminal-box mb-2">
                  <Image src="/placeholder.png" alt="Aerial Vehicle" width={500} height={300} className="rounded" />
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
                  <Image src="/placeholder.png" alt="Droid" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">DROIDs are ground-based mini AVs responsible primarily for delivery operations, especially of heavier cargo. They cannot carry people.</p>
              </div>
              <div>
                <h4 className="text-xl text-[#5EF6FF] mb-2">DRONE</h4>
                <div className="terminal-box mb-2">
                  <Image src="/placeholder.png" alt="Drone" width={500} height={300} className="rounded" />
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
                  <Image src="/placeholder.png" alt="Depot" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">Ground-based charging and maintenance centers for autonomous vehicles. Has multiple chargers and maintenance bays.</p>
              </div>

              {/* Skyports */}
              <div>
                <h3 className="text-2xl text-[#5EF6FF] mb-4">SKYPORTs</h3>
                <div className="terminal-box mb-2">
                  <Image src="/placeholder.png" alt="Skyport" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">Towers for handling eVTOL charging, maintenance, and passenger egress/ingress operations. Has multiple pads for simultaneous takeoff and landing of multiple aircraft.</p>
              </div>

              {/* Droneports */}
              <div>
                <h3 className="text-2xl text-[#5EF6FF] mb-4">DRONEPORTs</h3>
                <div className="terminal-box mb-2">
                  <Image src="/placeholder.png" alt="Droneport" width={500} height={300} className="rounded" />
                </div>
                <p className="text-white/70">Miniature skyports which handle similar operations for drone delivery operations. Small enough that single towers can be installed at partner restaurants. Usually installed alongside DEPOTs.</p>
              </div>
            </div>
          </section>
        </div>
      ) : (
        <div>
          {/* INPUT Section Placeholder */}
          <h2 className="text-3xl text-[#5EF6FF] mb-4">INPUT</h2>
          <p className="text-white/70">Create a new ARC input file here.</p>
        </div>
      )}
    </div>
  )
} 