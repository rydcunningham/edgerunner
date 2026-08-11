import type { Metadata } from 'next'
import MediaPanel from '../components/MediaPanel'
import { aboutMedia } from '../../lib/content/about'
import { TWO_COL_GRID, TWO_COL_PAGE } from '../../lib/layout'
import { properties, site, socials } from '../../lib/site'

export const metadata: Metadata = {
  title: 'About',
  description: 'Ryan Cunningham — founder and investor across the watt-to-bit value chain.',
}

export default function About() {
  const hasMedia = Boolean(aboutMedia.length)

  return (
    <div className={`px-6 md:px-20 py-14 ${hasMedia ? TWO_COL_PAGE : 'max-w-[900px]'}`}>
      {/* Two columns starting at the same line: bio left, media rail right. */}
      <div className={hasMedia ? TWO_COL_GRID : 'mt-8'}>
        <div>
          <header className="mb-10">
            <h1 className="font-display font-bold text-2xl tracking-[0.2em] uppercase text-k-text">
              About
            </h1>
            <p className="text-k-dim mt-2">
              founder // investor.{' '}
              <a
                href={`mailto:${site.email}`}
                className="text-k-text hover:text-k-accent transition-colors"
              >
                get in touch →
              </a>
            </p>
          </header>

          <div className="space-y-6 max-w-2xl text-k-text/80 leading-relaxed">
            <p>
              Ryan is a founder and investor focused on AI infrastructure, energy systems, and
              cutting edge products across the watt-to-bit value chain. He leads{' '}
              <a
                href="https://edgerunner.io"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                Edgerunner Ventures
              </a>
              , runs{' '}
              <a
                href="/research"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                Edgerunner Research
              </a>
              , and serves as a Venture Partner at{' '}
              <a
                href="https://www.augurvc.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                Augur Energy AI Fund
              </a>
              .
            </p>
            <p>
              Previously at{' '}
              <a
                href="https://aifund.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                AI Fund
              </a>{' '}
              with Andrew Ng, he co-built and invested in 9 companies from zero to revenue. Notable
              launches include{' '}
              <a
                href="https://skyfireai.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                Skyfire AI
              </a>
              , a swarm intelligence platform for autonomous drones, and{' '}
              <a
                href="https://workhelix.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                Workhelix
              </a>
              , a GenAI workforce transformation company co-founded by Erik Brynjolfsson.
            </p>
            <p>
              At Uber, he led machine learning projects across micromobility, aerial ridesharing,
              and autonomous delivery networks. He also led product at Spiketrap (acquired by{' '}
              <a
                href="https://reddit.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                Reddit
              </a>
              ), advises on select energy-compute engagements, and executed technology M&amp;A
              transactions at Credit Suisse.
            </p>
            <p>
              He holds a BS in Finance from Georgetown University, with a minor in Economics.
              Outside of work, he is an avid Spartan Racer, martial arts practitioner, and tinkerer.
              He shares technical and business insights at{' '}
              <a
                href={properties.newsletter}
                target="_blank"
                rel="noopener noreferrer"
                className="text-k-accent/90 hover:text-k-accent transition-colors"
              >
                machineyearning.io
              </a>
              .
            </p>

            <div className="pt-6 flex items-center space-x-6">
              {socials.map((s) => (
                <a
                  key={s.label}
                  href={s.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-k-accent/90 hover:text-k-accent transition-colors uppercase text-sm tracking-wider"
                >
                  [{s.label}]
                </a>
              ))}
            </div>
          </div>
        </div>

        <MediaPanel items={aboutMedia} />
      </div>
    </div>
  )
}
