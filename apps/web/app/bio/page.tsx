import Image from 'next/image'

export default function Bio() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Fixed Header Content */}
      <div className="fixed top-24 left-24 right-24 z-40">
        <h2 className="text-white/90 text-2xl font-medium mb-4">Bio</h2>
        <p className="text-white/80">
          founder // investor{'. '}
          <a href="mailto:rc@edgerunner.io" className="text-white/80 hover:text-[#F75049] transition-colors">
            get in touch →
          </a>{' '}
        </p>
        <div className="mt-2">
          <a
            href="/cv.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm uppercase tracking-wider text-white/60 hover:text-[#F75049] transition-colors"
          >
            [CV]
          </a>
        </div>
      </div>

      {/* Main Content */}
      <div className="mt-56 px-24 grid grid-cols-[1fr,auto] gap-16">
        {/* Text Content */}
        <div className="space-y-6 max-w-3xl">
          <p className="text-white/80 leading-relaxed">
            Ryan is a founder and investor focused on AI infrastructure and autonomous systems. He leads <a href="https://edgerunner.io" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">Edgerunner Ventures</a>, investing in early-stage AI, robotics, and deep tech startups, and serves as a Venture Partner at <a href="https://shack15.ventures" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">SHACK15 Ventures</a>.
          </p>
          <p className="text-white/80 leading-relaxed">
            Previously at <a href="https://aifund.ai" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">AI Fund</a> with Andrew Ng, he co-built and invested in 9 AI companies from zero to revenue. Notable launches include <a href="https://skyfireai.com" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">Skyfire</a>, <a href="https://workhelix.com" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">Workhelix</a>, and <a href="https://rapidfire.ai" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">Rapidfire</a>. At Uber, he led AI initiatives across micromobility, urban air mobility (patented ML system for eVTOL acoustics), and autonomous delivery networks. He also led product at Spiketrap (acquired by <a href="https://reddit.com" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">Reddit</a>), and executed technology M&A transactions at Credit Suisse.
          </p>
          <p className="text-white/80 leading-relaxed">
            He holds a BS in Finance from Georgetown University, with a minor in Economics, and studied advanced NLP and deep learning systems through Stanford's AI Graduate Certificate program.
          </p>
          <p className="text-white/80 leading-relaxed">
            Outside of work, he is an active endurance athlete, Krav Maga practitioner, and homelab enthusiast. He shares his technical and business insights at <a href="https://machineyearning.io" target="_blank" rel="noopener noreferrer" className="text-[#F75049]/90 hover:text-[#F75049] transition-colors">machineyearning.io</a>.
          </p>

          {/* Social Links */}
          <div className="pt-6">
            <div className="flex items-center space-x-6">
              <a 
                href="https://twitter.com/rydcunningham" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-[#F75049]/90 hover:text-[#F75049] transition-colors uppercase text-sm tracking-wider"
              >
                [x]
              </a>
              <a 
                href="https://github.com/rydcunningham" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-[#F75049]/90 hover:text-[#F75049] transition-colors uppercase text-sm tracking-wider"
              >
                [github]
              </a>
              <a 
                href="https://linkedin.com/in/rydcunningham" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-[#F75049]/90 hover:text-[#F75049] transition-colors uppercase text-sm tracking-wider"
              >
                [linkedin]
              </a>
              <a 
                href="https://machineyearning.io" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-[#F75049]/90 hover:text-[#F75049] transition-colors uppercase text-sm tracking-wider"
              >
                [substack]
              </a>
            </div>
          </div>
        </div>

        {/* Image */}
        <div className="w-[400px] relative">
          <Image
            src="/assets/square_grabber.svg"
            alt=""
            width={20}
            height={400}
            className="absolute -left-3.5 top-0 w-auto"
          />
          <div className="relative">
            <div className="aspect-[1/1] overflow-hidden" style={{
              clipPath: 'polygon(0% 0%, 97% 0%, 100% 3%, 100% 97%, 97% 100%, 0% 100%)'
            }}>
              <Image 
                src="/img/prof.jpeg" 
                alt="Ryan Cunningham"
                width={400}
                height={400}
                className="w-full h-full object-contain"
              />
            </div>
            <Image
              src="/assets/square_frame.svg"
              alt=""
              width={400}
              height={400}
              className="absolute inset-0 z-10"
            />
          </div>
        </div>
      </div>
    </div>
  )
} 