export default function Projects() {
  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">featured projects</h2>
        <p className="text-muted-foreground">
          open source work and side projects.{' '}
          <a href="https://github.com/yourusername" className="text-primary hover:underline">
            view on GitHub
          </a>{' '}
          →
        </p>
      </header>

      <div className="space-y-8">
        <article className="space-y-2">
          <h3 className="text-primary font-mono">AI Code Assistant</h3>
          <p className="text-muted-foreground">
            A VS Code extension that helps developers write better code using GPT-4.
            Built with TypeScript and the OpenAI API.
          </p>
          <div className="flex gap-3 text-sm">
            <a href="#" className="text-muted-foreground hover:text-primary">GitHub →</a>
            <a href="#" className="text-muted-foreground hover:text-primary">Demo →</a>
          </div>
        </article>

        <article className="space-y-2">
          <h3 className="text-primary font-mono">Neural Network Visualizer</h3>
          <p className="text-muted-foreground">
            Interactive visualization tool for understanding how neural networks make decisions.
            Built with Three.js and TensorFlow.js.
          </p>
          <div className="flex gap-3 text-sm">
            <a href="#" className="text-muted-foreground hover:text-primary">GitHub →</a>
            <a href="#" className="text-muted-foreground hover:text-primary">Live Site →</a>
          </div>
        </article>

        <article className="space-y-2">
          <h3 className="text-primary font-mono">Machine Learning Blog Engine</h3>
          <p className="text-muted-foreground">
            A Next.js blog platform with AI-powered content suggestions and SEO optimization.
            Uses OpenAI's GPT-3 for content enhancement.
          </p>
          <div className="flex gap-3 text-sm">
            <a href="#" className="text-muted-foreground hover:text-primary">GitHub →</a>
          </div>
        </article>
      </div>
    </div>
  )
} 