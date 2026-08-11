---
title: "It's time to move on from copilots"
subtitle: "We can build better than this."
date: "2024-05-14"
excerpt: "I've been saying for months I don't like to invest in application-layer AI startups. Here's why - and what it would take to change my mind."
---

# The first wave under-delivered

When ChatGPT debuted, a friend raved to me about [Sudowrite](https://www.sudowrite.com), a thoughtfully designed fiction-writing app created by James Yu and Amit Gupta. Sudowrite leverages LLMs to help authors stay in flow, organizing LLM calls into purpose-built features for tasks like world-building, pacing, and outlining. With a vibrant user community stress-testing new features, millions in annual revenue, profitability, and fewer than 10 employees, Sudowrite exemplifies what’s possible when generative AI products are built with deep user empathy and domain knowledge.

At the time, I thought this foreshadowed a wave of similarly well-designed AI products across many industries.

A year and a half later, that prediction remains mostly unfulfilled.

Many first-wave AI startups have failed to deliver little more than thin UI wrappers around generic LLMs. I’ve critiqued [Jasper](https://www.jasper.ai) before, and it looks like [Tome](https://tome.app) (text-to-powerpoint) may be next on the chopping block. Turns out defining your ideal customer profile and product is crucial before hiring sales reps.

This trend extends beyond software. First-gen consumer AI hardware like the [Humane AI Pin](https://hu.ma.ne/) and [Rabbit R1](https://www.rabbit.tech/) have been dead-on-arrival, tethered to the latency, limits, and hallucinations of off-the-shelf LLMs. As [MKBHD](https://www.youtube.com/watch?v=fq1HoC_E8K4) (Marques Brownlee) put it, they’ve failed to deliver compelling (or even passable) user experiences.

<figure>
  <img src="/img/marques-brownlee-rabbit-humane.png" alt="MKBHD reviews of Humane AI Pin and Rabbit R1" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    MKBHD's reviews of first-gen AI hardware have been brutal
  </figcaption>
</figure>

This “wrapper” or “copilot” design philosophy is at the center of my beef with application-layer startups, and why I generally avoid investing in them (with limited exceptions I’ll cover at the end of this post*).

Most seem to follow the same playbook - inject someone else’s LLM into a user-facing SaaS model, christen it a “copilot”, and ignore competitive analyses because they misread [Christensen's Innovator's Dilemma](https://www.amazon.com/Innovators-Dilemma-Technologies-Management-Innovation/dp/1633691780). At its current stage, generative AI has been more of a sustaining innovation for incumbents, not a disruptive one they’ve been reluctant to adopt.

Yes, I’m aware many copilots claim to be much more than a wrapper. Some emphasize that they use fine-tuned, domain-specific models that outperform generic LLMs. However, even category leaders building these kinds of products can be paper tigers. Case in point - Harvey, the buzziest player in AI x legaltech.

# Harvey: Legal Jasper?
I’m going to go on record and say what I’m seeing with Harvey smacks a great deal like Jasper last year - Harvey’s last raise pegged them at $700M+, but leaked screenshots of their tool leave a lot to be desired.

First, let’s understand how Harvey views itself in the AI x legaltech landscape.

<figure>
  <img src="/img/harvey-screens.webp" alt="Harvey.ai" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    Source: Harvey.ai
  </figcaption>
</figure>

Harvey describes itself to investors and customers as an application layer that is ["foundation model agnostic."](https://www.harvey.ai/blog/harvey-raises-80m-series-b)

They highlight that a team of in-house attorneys and experts ������structure application and model calls” to create a best-in-class legal LLM. Off the bat, this sounds like an expensive consulting agreement for lawyers to do prompt engineering.

They also have no plans to provide real-time access to the internet for legal research, because their focus is on not providing “wrong or tainted responses.”

Let’s see how that philosophy manifests into actual product.

## Lacking basic integrations
Harvey’s legal research capabilities are slim. The only searchable source is SEC filings - no US case law or EUR-Lex integrations, despite APIs for these services being freely available.

As an attorney, when conducting legal research you’re looking for relevant cases, rulings, and written opinions from the court on your area of interest. This helps you vet whether there’s established precedent in your favor or which arguments are most likely to work.

A baseline expectation for a production-grade legal research app is that generated outputs map to real cases. These integrations would ground any generated cases in discrete outputs, and a well-designed system would assert the outputs map to real cases before including them.

To be sure, [LlamaIndex](https://www.llamaindex.ai) built [secinsights.ai](https://secinsights.ai) (RAG for SEC filings) in September 2023 as a feature-complete demo of their toolkit - really impressive work for LlamaIndex, and a great open-source contribution. But what has Harvey actually built on top of this?

<figure>
  <img src="/img/harvey-research.webp" alt="Harvey's legal research interface" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    These screengrabs are from earlier this year - I expect (and hope) the product has improved a lot since then.
  </figcaption>
</figure>

## CYA
Very little, it would seem. The “Assistant” tool is a bare-bones LLM wrapper with lengthy disclaimers about how LLMs hallucinate and you shouldn’t take anything Harvey says seriously.

<figure>
  <img src="/img/harvey-assistant.webp" alt="Harvey's Assistant interface" />
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    Your legal AI tool priced at $700M.
  </figcaption>
</figure>

Neither a wall of disclaimers nor a black box “fine-tuned by the best lawyers” instills confidence. Harvey may argue their in-house experts can prompt-hack a robust model for legal work, but don’t expect customers to trust an opaque, unverifiable system, no matter how well-built it claims to be.

If your Harvard-trained associate handed you a legal brief with a note saying “but idk I make stuff up sometimes,” you’d fire them on the spot. Or in [this real-life case](https://www.reuters.com/legal/new-york-lawyers-who-used-chatgpt-cite-fake-cases-sanctioned-by-judge-2023-06-22/), you’d so thoroughly embarrass the lawyers who submitted it that you wouldn’t even need to disbar them.

Let me be clear - in domains where the cost of errors are severe (e.g. legal, finance, accounting) or even life-threatening (e.g. healthcare, pharma) you absolutely should not design a system solely around a zero-shot LLM.* LLMs are stochastic by nature, and need to use external resources to provide verifiable, discrete responses.

What you can do instead is create a modular system with explainability, grounding, and auditability built-in - something more akin to an “agent-based” approach.

_\* This is part of a greater degree of skepticism I have with “domain-specific models,” which is a topic for a future post - the observation that beyond a certain level of model intelligence, your domain-specific data does not matter._

# Agents "Do No Harm."
While Harvey bets on an offline, domain-specific model, [Hippocratic AI](https://www.hippocratic.ai/) has the opposite tack. They break physician-patient interactions into individual “specialist models,” (i.e. ‘agents’ or ‘modules’) narrowly scoped to address individual workflows like checklists, medication, labs & vitals, etc..

It’s a fantastic example of an agentic system in action, especially notable for its clout and adoption in such a sensitive domain - healthcare - where the cost of a mistake can be deadly.

Listen to this [AI-patient conversation](https://twitter.com/hippocraticai/status/1766867180440277137) at 2x speed, and observe the agents in action:

<figure>
  <div style="padding:56.25% 0 0 0;position:relative;">
    <iframe 
      src="https://player.vimeo.com/video/1011049583?h=c7c3c93b5b&amp;badge=0&amp;autopause=0&amp;player_haswell=0&amp;quality_selector=1" 
      frameborder="0" 
      allow="autoplay; fullscreen; picture-in-picture" 
      style="position:absolute;top:0;left:0;width:100%;height:100%;" 
      title="Hippocratic AI Demo">
    </iframe>
  </div>
  <script src="https://player.vimeo.com/api/player.js"></script>
  <figcaption className="text-sm text-muted-foreground mt-2 text-center">
    Bonus points for anyone who heard "delve" as a clear AI giveaway.
  </figcaption>
</figure>

* The primary agent for Linda prioritizes good bedside manner, building rapport, and providing empathetic guidance
* The “checklist specialist” balances extracting info and moving the conversation forward
* For each checklist item, Linda has a specialist “support agent” for tasks like reviewing meds, answering insurance questions, or giving nutrition tips
* These interlinked agents share data and RAG into specific knowledge bases

Hippocratic stress-tested with 1,200+ clinicians in simulated patient-actor conversations, and are achieving verifiable parity (or supremacy) on all 5 of the surveyed dimensions: bedside manner, patient education, conversation quality, clinical readiness, and medical safety.

I’ll dive deeper into agentic systems design in a future post, but the key takeaway is you can mimic these techniques for building sophisticated AI that consistently works, even in the most sensitive domains. I don’t think customers would accept less, and neither should investors or founders.

# What’s next: beyond copilots
I mentioned at the top of this post that as a general rule, I don’t like to invest in application-layer companies. Here are the exceptions to that rule:
1. You’re selling into a highly sensitive regulatory domain. This makes it harder to sell into, but drastically improves customer stickiness, AND
2. You (the founder(s)) have unfair channel access / distribution into these regulated customers, AND
3. Because you know these customers so well, you’ve designed a task-specific agentic system that meets or exceeds human-level performance on each of the scoped modules

Application-layer companies that meet these criteria have a better shot at building defensible, long-term value. We need modular, explainable systems that leverage generative AI while grounding it in domain knowledge and rigorous evals. Agentic systems, à la Hippocratic AI, are great examples of this. Looking forward to seeing many more like it in Chapter Two of this cycle.

Each of these "support agents" is a separate language model ranging between 50-100B parameters. But you can do quite a lot with even smaller models - the system's performance, rated by nurses, was as good or better for each of the 5 assessed parameters. Source: Eric Topol, [Ground Truths](https://erictopol.substack.com/p/a-big-week-in-medical-ai)

