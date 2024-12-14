export default function Bio() {
  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">Ryan Cunningham</h2>
        <p className="text-muted-foreground">
          founder // investor.{' '}
          <a href="mailto:rc@edgerunner.io" className="text-primary hover:underline">
            get in touch →
          </a>{' '}
        </p>
      </header>

      <div className="space-y-8">
        <section className="space-y-4">
          <h2 className="text-xl font-mono">Experience</h2>
          <div className="space-y-6 text-muted-foreground">
            <div>
              <h3 className="text-primary">Senior AI Engineer</h3>
              <div className="text-sm text-muted-foreground">2023 - Present</div>
              <p className="mt-2">Leading development of ML-powered developer tools</p>
            </div>
            <div>
              <h3 className="text-primary">Software Engineer</h3>
              <div className="text-sm text-muted-foreground">2021 - 2023</div>
              <p className="mt-2">Full-stack development with React, Node.js, and Python</p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-xl font-mono">Education</h2>
          <div className="text-muted-foreground">
            <h3 className="text-primary">B.S. Computer Science</h3>
            <div className="text-sm text-muted-foreground">2017 - 2021</div>
            <p className="mt-2">Focus on machine learning and distributed systems</p>
          </div>
        </section>
      </div>
    </div>
  )
} 