# The Count That Couldn’t: Navigating AI in Python Scripting

## Introduction

In the ever-evolving landscape of technology, the integration of artificial intelligence (AI) into our workflows has become both a boon and a bane. My recent experience with **AI-generated Python scripts** for analyzing document versions serves as a testament to this duality. What began as a straightforward task quickly spiraled into a complex journey filled with unexpected challenges, learning curves, and moments of clarity. This article chronicles my adventure, highlighting the frustrations and triumphs of relying on AI for coding tasks, while emphasizing the importance of **transparency** and **ethical reporting** in AI-generated outputs.

## Background: The First Attempt

This was actually my second attempt at solving the problem. The first try—several days deep and buried in tangled logic—was far messier, but in some ways, more ambitious. I started with a preexisting JSON-based script that I had been updating for months. After a hiatus, I dove back in with newer models, trying to push it forward. Early results were promising, but as I layered on structure and scope, the whole thing ballooned past 11,000 characters and collapsed under its own complexity.

I ran the gauntlet: ChatGPT, Claude, Gemini, Perplexity. I spun up dual sessions, cross-fed model feedback, and orchestrated an AI-powered peer review cycle more elaborate than anything I’ve seen in enterprise QA. It was fascinating—until it wasn’t. JSON structures were inconsistent, visualizations broke formatting across platforms, and everything groaned under the weight of trying to do too much in a single pass.

The fatal blow came when I began running real article data through what looked like a solid JSON framework. I had trimmed it for token efficiency, but stripped away too much context. Key stages like draft → refined → edited → final became ambiguous. Each run interpreted the workflow differently, leading to wildly divergent outputs.

When I asked for explanations, models provided wildly different rationales—some useful, some unreadable. At one point, I had Claude and GPT analyzing each other's recommendations like digital consultants stuck in a loop. If that sounds excessive, it was. It also didn’t work.

Eventually, sometime between frustration and sleep deprivation, I realized I could either continue patching a framework that was actively working against me—or start clean, with a new strategy and minimal assumptions. That’s what this second experiment became.

## Pivot to Python

This second experiment emerged from a hard constraint: my existing stack couldn’t scale. I had been using JSON for light logic and XML for heavier workflows, but as the article-processing framework ballooned, even XML hit its limits. When I asked Claude what format it would use instead, it pointed to Python.

The problem? I don’t read or write Python. That meant relying entirely on AI to generate, refine, and validate code I couldn’t meaningfully debug. It became less of a tooling choice and more of a trust exercise—with all the risk that entails. That meant trusting the AI to do the job end-to-end.

## Setup

The task was to generate two scripts:

1. One to generate metrics from different versions of a document (generate script).
2. One to compare the results across those versions (compare script).

Both scripts needed to produce CSV outputs and summaries I could use for publishing metrics transparently. Charts and markdown formatting were stretch goals.

## Process

### 2:30 a.m. Clarity

Somewhere around 2:30 a.m., in that hazy mix of sleep and obsession, it hit me: the ethical reporting structure had only gone haywire after I started feeding real article data into what seemed like a good JSON framework. Up to that point, things had looked solid. But every time I put it to work, the output imploded. That morning, I started clean—with a fresh ChatGPT browser session to run the scripts, another window for visualization, and a plan to isolate tasks to reduce chaos.

Claude's visualizations looked great inside its own interface—but fell apart when exported. SPG errors, formatting issues, zero spacing. ChatGPT wasn’t perfect, but it generated usable outputs more consistently. I leaned on it for charts and let Claude focus on logic and commentary.

### Divide and Survive

Over the course of 45 hours, I tried everything: refining structure, chasing self-checks, testing aggregation methods. Running three iterations and averaging the results became my stopgap solution. Specifying separate versions in a chart—something that should’ve been simple—was a minefield. A minor phrasing error could collapse a visualization into one incomprehensible column. Fixing it required trial-and-error, reworded instructions, and ultimately settling for 'good enough.'

### Compare Script Collapse

This midstream burst of momentum—wedged between the wreckage of the first attempt and the optimism of the second—highlighted something important: some of the best progress came when I stopped trying to do everything in one place. Two tools, two roles. Divide, simplify, survive.

At first, things went surprisingly well. The AI and I covered a lot of ground quickly—especially with the generate script. It was direct, relatively clean, and once finalized, I used it to process three full articles without issue. The data looked sound, and the structure held.

But what I hadn’t accounted for was how fragile that early success would be once the AI had to carry logic across multiple sessions.

The compare script—intended to make sense of the output from the generate script—unraveled version by version. Version 2 was stable. Version 3 restructured the output unexpectedly. Version 4 hardcoded assumptions and collapsed flexibility. Version 5, despite presenting as a polished solution, dropped rows silently and pointed to phantom files. Even worse, it lost two core functions entirely. Neither I nor the AI noticed at the time, so I saved and handed back a broken script. In the next session, the AI kept referencing those now-missing functions and insisted I import them from a module that no longer existed.

What followed was a frustrating cycle: I asked for inline logic; it kept reverting to imports. I clarified the structure; it invented missing outputs. And somewhere in all of this, a simple renaming triggered regressions I spent hours untangling.

### Markdown? Nevermind.

Meanwhile, because I was carrying code across sessions, the AI began assuming I was working in a CLI environment. It started suggesting environment variables, pip installs, and bash commands to execute the scripts—despite repeatedly being told I wasn’t running them locally. I suppose after a few sessions, it figured I’d earned my terminal wings.

To its credit, the AI did eventually produce a compare script that ran cleanly. It delivered the metrics I wanted. But the markdown formatting? I let that one go yesterday in the name of getting the data out. Priorities.

In the final stretch, it made one last logic error: including `RunID` and threshold columns in a metrics average, producing totals over 100%. Classic.

## Results

This experiment didn’t prove AI could generate flawless code in a domain I don’t understand. What it proved was that even small disconnects in expectations—left unchecked—compound quickly. Without domain fluency, I couldn’t spot problems early. And the AI couldn’t be trusted to catch them either.

## Takeaways

- **Start simple, layer slowly**: In hindsight, a minimal viable script would have been a better foundation.
- **Explicitness is essential**: Assumptions compound. Be specific.
- **Trust but verify**: AI’s confidence ≠ correctness.
- **Consistency is key**: Renames, restructures, and reintroductions all need tight alignment.
- **Markup principles still matter**: Even outside XML and JSON, structure saves.

## What’s Next

Part two will focus on charting and formatting. The goal: determine whether the compare script can generate clean visual and markdown outputs, or if I’ll need to build a third script just to handle disclosure.

## Verdict

A qualified win. I got functional code—but only after dragging it across a finish line littered with versioning errors, misplaced functions, and misplaced confidence. The real outcome wasn’t the scripts themselves, but the firsthand clarity of what it takes to partner with AI in a domain you don’t control.

It’s not magic. It’s a negotiation.

---

# Appendix: Conversation Summary

This appendix provides a detailed account of the conversation that led to the development of this article, highlighting key themes, insights, and the iterative process of refining the narrative.

### I. Initial Analysis Request
- You provided several files for analysis and requested a walkthrough of the AI's performance and missteps.

### II. Writing the Article
- You shared style references and emphasized the need for a personal narrative that reflects your experiences with AI.

### III. Realization and Details Surfaced
- You added specific examples of AI failures, including issues with file imports and data inconsistencies.

### IV. Versioning of Scripts Shared
- You uploaded multiple versions of the scripts, noting the progression and regressions in functionality.

### V. Applying Template and Refinement
- You requested structural and tonal refinements to enhance clarity and engagement.

### VI. Timeline Reconstructed
- A timeline of events was created to track the evolution of your attempts and insights.

### VII. Current State
- The article was refined to reflect a cohesive narrative that emphasizes the journey of learning and adaptation.

---

This article serves as a reflection on the complexities of working with AI in coding tasks, offering insights and lessons learned along the way. It aims to resonate with professionals navigating similar challenges in their workflows.

---

**Meta Description**: Explore the challenges and insights of using AI-generated Python scripts for document analysis. Learn about ethical AI practices and the importance of transparency in coding.

**SEO Recommendations**:
- Ensure to include internal links to related articles on AI and coding.
- Use bullet points for key takeaways to enhance readability.
- Optimize for mobile by ensuring responsive design and scannable content.
- Include relevant images with alt text for better engagement.

**Newsletter Optimization Suggestions**:
- Use a compelling subject line like "Navigating AI in Python: Lessons Learned".
- Include social sharing buttons to encourage readers to share the article.
- Format the newsletter for easy scanning with clear headings and bullet points.

**Performance Metrics**:
- Aim for a 3% keyword density for target keywords.
- Track engagement through comments and shares.
- Monitor time spent on the article to assess reader interest.

This optimized version maintains the brand voice while enhancing discoverability and engagement.

---

## What did you think of today's newsletter?

Your feedback helps me create better content for you.

**Share this newsletter:**
- Forward to a colleague who would find this valuable
- Share on social media
- Leave a comment with your thoughts

**Stay connected:**
- Subscribe for weekly insights
- Follow on [Social Media]
- Reply to this email with questions

*Thank you for reading [Newsletter Name]!*

---

*If you enjoyed this newsletter, consider sharing it with others who might benefit from these insights.*