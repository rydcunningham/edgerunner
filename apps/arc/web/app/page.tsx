import React from 'react'
import Image from 'next/image'

export default function OverviewPage() {
  return (
    <div className="min-h-screen p-8 bg-black text-white">
      {/* Header */}
      <header className="mb-12">
        <h1 className="text-4xl text-[#5EF6FF] mb-4">Project: [ARC]</h1>
        <p className="text-lg text-white/70">
          A library for optimizing and enhancing autonomous vehicle operations.
        </p>
      </header>

      {/* Getting Started Section */}
      <section className="bg-black/50 p-6 rounded-lg mb-8">
        <h2 className="text-2xl text-[#5EF6FF] mb-4">Getting Started</h2>
        <p className="mb-4 text-white/70">
          Head straight to <strong>SIM</strong> to use presets, or jack in your own data through <strong>SYSTEM &gt; FILES</strong>.
        </p>
        <p className="mb-4 text-white/70">
          Advanced configurations of vehicle types, infrastructure, and more available in <strong>SYSTEM &gt; CONFIG</strong>.
        </p>
      </section>

      {/* Example Screenshots Section */}
      <section className="bg-black/50 p-6 rounded-lg">
        <h2 className="text-2xl text-[#5EF6FF] mb-4">Visual Echoes</h2>
        <div className="space-y-4">
          <Image src="/example1.png" alt="Example 1" width={500} height={300} className="rounded" />
          <Image src="/example2.png" alt="Example 2" width={500} height={300} className="rounded" />
          <Image src="/example3.png" alt="Example 3" width={500} height={300} className="rounded" />
        </div>
      </section>
    </div>
  )
} 