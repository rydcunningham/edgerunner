export default function CV() {
  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">/cv</h2>
      </header>

      <div className="space-y-16">
        <section className="space-y-6">
          <h2 className="text-xl font-mono">Experience</h2>
          <div className="space-y-8">
            <article className="space-y-4">
              <h3 className="text-primary font-mono">SHACK15 Ventures</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Early-stage technology venture capital in San Francisco</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">Co-Founder & Partner</div>
                <div className="text-muted-foreground font-mono">2024</div>
              </div>
            </article>

            <article className="space-y-4">
              <h3 className="text-primary font-mono">AI Fund</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Incubated and invested in 9 enterprise AI companies with Andrew Ng, from zero to revenue</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">Principal</div>
                <div className="text-muted-foreground font-mono">2021-24</div>
              </div>
            </article>

            <article className="space-y-4">
              <h3 className="text-primary font-mono">Spiketrap</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Led strategic pivot in contextual ads enablement before acquisition by Reddit</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">Director of Product</div>
                <div className="text-muted-foreground font-mono">2020-21</div>
              </div>
            </article>

            <article className="space-y-4">
              <h3 className="text-primary font-mono">Uber</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Spearheaded entry into micromobility, launched urban air mobility division, scaled international food delivery</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">Product Lead</div>
                <div className="text-muted-foreground font-mono">2017-20</div>
              </div>
            </article>

            <article className="space-y-4">
              <h3 className="text-primary font-mono">Credit Suisse</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Executed $10bn+ in internet, blockchain, payments, and D2C transactions</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">Investment Banking</div>
                <div className="text-muted-foreground font-mono">2014-16</div>
              </div>
            </article>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-xl font-mono">Board Positions</h2>
          <div className="space-y-8">
            <article className="space-y-4">
              <h3 className="text-primary font-mono">AI Companies</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Board Observer at Echelon.ai, Kula, Speechlab, Workhelix, ValidMind, FourthBrain, Bearing AI</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">Board Observer</div>
                <div className="text-muted-foreground font-mono">2021-24</div>
              </div>
            </article>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-xl font-mono">Education</h2>
          <div className="space-y-8">
            <article className="space-y-4">
              <h3 className="text-primary font-mono">Stanford University</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Advanced NLP, deep learning, and decision-making algos.</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">AI Certificate</div>
                <div className="text-muted-foreground font-mono">2021</div>
              </div>
            </article>

            <article className="space-y-4">
              <h3 className="text-primary font-mono">Georgetown University</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Major in Finance, minor in Economics and CS. Core focus on China Studies, Information Economics, and Information Warfare</p>
                <div className="text-muted-foreground font-mono whitespace-nowrap">BS Business</div>
                <div className="text-muted-foreground font-mono">2010-14</div>
              </div>
            </article>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-xl font-mono">Certifications</h2>
          <div className="space-y-8">
            <article className="space-y-4">
              <h3 className="text-primary font-mono">FINRA</h3>
              <div className="grid grid-cols-[1fr,auto,auto] gap-8">
                <p className="text-muted-foreground">Series 65 and 79 certifications</p>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>
  )
} 