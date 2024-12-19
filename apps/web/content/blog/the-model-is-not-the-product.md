---
title: "The model is not the product"
subtitle: "Or: we need to talk about ROI."
date: "2024-05-31"
excerpt: "As AI hype continues to rip, a nagging question is popping up in boardroom circles - are we actually seeing real impact from our AI strategies?"
---

_This post is part 1 of a 2-part series on evolving "model-centric" building and investing themes. We'll explore economic challenges of inference and product strategy implications. Stay tuned for part 2 next week, where we'll dive into the tactical side of model routing and other cost optimizations for teams and businesses._

# The elephant in the boardroom

As AI hype continues to rip, a nagging question is popping up in boardroom circles - are we actually seeing real impact from our AI strategies?

A few weeks ago, we co-hosted an event with Reinvent Futures here at SHACK15, which brought together leaders from the tech and sustainability spheres. Matt Kropp, CTO of BCG X (BCG's tech build & design unit), kicked things off with a pretty clear signal from their clients: "we're now getting to the point where there's some question about whether we're actually getting impact."

The surveys definitely back this up, and I'm personally hearing this more and more among consumers and enterprises alike.

* Consumers are feeling the squeeze of subscription fees, as research labs start to lock the best models behind paywalls.
* Enterprises are still feeling pressure from their boards to adopt GenAI tools (89% say AI and GenAI are in top 3 tech priorities for this year), but struggle to figure out which ones to use.
* Even with a hefty "enterprise" discount, no sane CIO or CFO is going to greenlight a plan that charges $240 per user per year for access to OpenAI's finest, because they first want to know… what will I actually use this for?

LLMs are becoming commoditized, so teams building AI products they want businesses to use need to focus on building complete solutions solving concrete problems. Simply participating in the LLM gold rush isn't enough anymore, because **the model is not the product**.

# Model-centric missteps

Over 70% of people haven't even used generative AI tools yet, let alone know the difference between distinct models. While I'm grateful for leaderboards from Stanford, HuggingFace, and most recently Scale, the benchmarks we use are somewhat academic, or at least lack the specificity one could use making a business decision about which model to go with.

The first chapter of the AI arms race has had VCs shoveling money towards teams building model-centric research labs. These models are great across a range of tasks, but lack significant differentiation from one another, and may eventually fall short of investor expectations. Inflection's implosion and Stability AI's public struggle demonstrate the eventual risks of this model-centric approach.

<figure>
  <img src="/img/fireship-code-report.webp" alt="Fireship's The Code Report" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    Credit: Fireship's "The Code Report"
  </figcaption>
</figure>

Inflection in particular shows that war chests are not a guarantee of product-market fit. Despite raising $1.3B last year alone, they were late to an already crowded party and failed to gain traction. Their Pi assistant, while friendly and acclaimed by users, ultimately may not have been distinct enough from the ChatGPTs, Claudes, and Geminis of the world to warrant much attention.

Similarly, Stability, despite hitting unicorn status in 2022 thanks to the buzz around Stable Diffusion, failed to build a compelling business around their family of open-source models. The financial situation became pretty dire: in Q1 2024, they reportedly lost $30M on a meager $5M in revenue (with nearly $100M in unpaid cloud compute bills). So despite great contributions to open source, they didn't create a revenue model which could support demand for its service, hampering their ability to raise more cash.

<figure>
  <img src="/img/dreamstudio-stability.webp" alt="DreamStudio interface" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    The original DreamStudio from Stability. Credit: Product Hunt
  </figcaption>
</figure>

# Behold "AI Operating Systems"

So if the model-centric approach is losing its luster, what are market leaders doing instead? They're shifting their focus from best-in-class general models to tightly integrated ecosystems.

OpenAI is doubling down on the sci-fi dream of an always-on, hyper-personalized AI companion (_Her_, but IRL), while Google and Apple are leveraging existing product and device ecosystems to make their models indispensable across every touchpoint. Meanwhile, Microsoft is betting on "Copilot+" branding as a value-add for its PC and productivity software businesses.

Each player is trying to weave LLMs into a stickier, more defensible product strategy as the go-to "AI Operating System." Google, Apple, and Microsoft have extensive network effects they can already leverage for lock-in, and while OpenAI is playing catch-up here, their market share with ChatGPT has so far been substantial enough to dictate the pace of development.

After all, what's stickier than love ✨

But while this AI OS approach may be useful for consumer lock-in, it doesn't solve the primary problems businesses have integrating models into their own products and services. Businesses aren't buying models or ecosystems - they're "hiring" them to perform specific jobs-to-be-done. And they need the flexibility to choose the best, fastest, and cheapest option for each job, not to be beholden to a single provider.

# Unsustainable inference costs

Even the most seamless ecosystem will struggle if the economics don't add up. The cost of at-scale inference is staggering, and it doesn't seem like any vendors serving models today are making a profit.

<figure>
  <img src="/img/semianalysis-chart.webp" alt="AI inference costs chart" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    Source: SemiAnalysis
  </figcaption>
</figure>

This introduces some weird market dynamics.

Token-as-a-service providers are playing by a predictable growth-at-all-costs playbook: sacrificing near-term profitability for user acquisition, then making it up on volume once you've cornered the market. So for the time being, no one really knows what the willingness-to-pay is, because token prices are being kept artificially low.

As we've seen with Inflection and Stability, that strategy may have its limits, especially if they fail to distinguish their open offerings from paid ones. In turn, these failures may cause disillusionment, consolidation, and upward pricing trends.

At first glance, this could seem like a good thing (VC-subsidized prices, yay), but there are significant risks. Basing your own product strategy on unsustainably low prices can cause a severe hangover to your cost structure if and when those prices eventually do rise. Moreover, vendor lock-in carries the risk of your chosen model suddenly becoming unavailable or prohibitively expensive if they fail to hit profitability. You need to be careful not to anchor your product too much on the idiosyncrasies of a single vendor's model family.

A valid counter would be that Moore's Law is naturally driving down inference costs overtime, hence the "make it up on volume later" meme. While this is true that there's about a 3x reduction per year in physical compute required to hit a given performance target, it's also true that training costs for frontier models are rising by a similar rate at 3.1x per year. So if you want last year's model, that will be cheaper, but if you want the latest and greatest, you're still going to have to pay.

In short, the current economics of AI inference are concerningly unstable, and businesses should be strategic in navigating that when building products that use external models.

# Recommendations

To recap, the path to real impact and ROI remains unclear for many businesses under pressure to adopt AI in their products and services. So, what's a savvy team to do when crafting their strategy? Two options stand out in contrast to the model-centric approach:

1. **Highly optimized token-as-a-service providers** like DeepInfra offer a compelling value proposition, by focusing solely on efficient model hosting and serving. By comparing models and hosts on independent leaderboards like Artificial Analysis, businesses can find the best bang for their inference buck.
2. **Model routers** like Martian and OpenRouter take this a step further by dynamically allocating queries across multiple models based on cost, speed, and performance. They're constantly tracking the model tokenomics and quality with insane prompt-specific granularity, which lets customers tap into the best available models for any use case without vendor lock-in.

<figure>
  <img src="/img/artificial-analysis.webp" alt="Artificial Analysis leaderboard" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    Source: Artificial Analysis
  </figcaption>
</figure>

Of course, each solution has their tradeoffs, which we'll dive into next week with a tactical breakdown in part 2. We'll explore, model routing, fine-tuning, leaderboarding, and more practical takeaways for AI strategies. Until then, I'd recommend reading Cerebral Valley's deep dive with the Martian team to get familiar with what they're up to.

But for now, the key takeaways are this: **the model is not the product**, and the businesses that will thrive are those that **match the right model to the right job at the best price.** 