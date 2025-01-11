export default function Bio() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Fixed Header Content */}
      <div className="fixed top-24 left-24 right-24 z-40">
        <h2 className="text-white/90 text-2xl font-medium mb-4">Bio</h2>
        <p className="text-white/80">
          founder, investor, builder.{' '}
          <a href="mailto:rc@edgerunner.io" className="text-white/80 hover:text-[#F75049] transition-colors">
            get in touch →
          </a>{' '}
        </p>
      </div>

      {/* Main Content */}
      <div className="mt-56 px-24 grid grid-cols-[1fr,auto] gap-16">
        {/* Text Content */}
        <div className="space-y-6 max-w-3xl">
          <p className="text-white/80 leading-relaxed">
            Ryan is a founder and investor focused on AI infrastructure, dev tools, and autonomous systems. He currently leads SHACK15 Ventures, investing in early-stage AI and deep tech startups.
          </p>
          <p className="text-white/80 leading-relaxed">
            Previously, he built and invested in 9 enterprise AI companies at AI Fund with Andrew Ng, from zero to revenue. Before that, he led product at Spiketrap (acquired by Reddit), launched Uber's micromobility division ($10B+ GMV), and executed $10bn+ in tech transactions at Credit Suisse.
          </p>
          <p className="text-white/80 leading-relaxed">
            He holds a BS in Finance from Georgetown University, with minors in Computer Science and Economics. He also completed Stanford's AI Professional Program, focusing on advanced NLP and deep learning.
          </p>
          <p className="text-white/80 leading-relaxed">
            Outside of work, he's an avid pilot, endurance athlete, and homelab enthusiast. Currently building a self-hosted AI infrastructure stack on consumer hardware.
          </p>
        </div>

        {/* Image */}
        <div className="w-[360px]">
          <div className="aspect-[9/16] rounded-xl overflow-hidden bg-background/[var(--glass-opacity)] border border-border">
            <img 
              src="/headshot.jpg" 
              alt="Ryan Cunningham"
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </div>
  )
} 