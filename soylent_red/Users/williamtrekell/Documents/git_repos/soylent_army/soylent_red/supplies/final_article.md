# The Count That Couldn’t: A Journey Through AI Integration in UX Design

## Introduction

In the rapidly evolving landscape of UX design, the integration of AI tools has become both a promise and a challenge. This article chronicles the journey of navigating the complexities of AI, particularly through the lens of using Python scripts to analyze document versions. It highlights the struggles, successes, and ethical considerations that arise when designers attempt to harness AI's potential while maintaining a human-centered approach. This exploration is particularly relevant for UX professionals interested in **prompt engineering for UX**, **AI tools for designers**, and **human-AI collaboration**.

## Background: The First Attempt

The initial foray into AI integration began with a preexisting JSON framework aimed at analyzing document versions. The goal was to create a system that could measure deltas between stages—draft, refined, edited, and final. However, as the complexity of the project grew, so did the challenges. The JSON structure became unwieldy, leading to inconsistent outputs and a frustrating experience.

The first attempt involved running multiple AI models—ChatGPT, Claude, Gemini, and Perplexity—through a gauntlet of prompts. The results were promising at first, but as the project expanded, the framework collapsed under its own weight. Key stages became ambiguous, and the AI struggled to maintain context, leading to wildly divergent outputs.

The turning point came during a late-night session when the realization struck: the ethical reporting structure had gone awry after feeding real article data into the JSON framework. This prompted a decision to pivot to a new approach, one that would allow for a cleaner slate and a more structured methodology.

## Pivot to Python

The transition to Python was driven by the need for a more scalable solution. The existing stack, which relied on JSON for light logic and XML for heavier workflows, had reached its limits. When Claude suggested Python as a viable alternative, it marked the beginning of a new experiment—one that would require a leap of faith, as the designer had no prior experience with the language.

The task was clear: generate two scripts—one to create metrics from different document versions and another to compare the results. Both scripts needed to produce CSV outputs and summaries for transparent reporting. The challenge was not just technical; it was also about trusting the AI to deliver functional code without the designer's ability to debug or validate the underlying logic.

## Process

### 2:30 a.m. Clarity

In the early hours of the morning, a moment of clarity emerged. The ethical reporting structure had only faltered after real article data was introduced into the JSON framework. Up to that point, the outputs had seemed solid. However, each attempt to run the framework resulted in implosions of data. This realization led to a fresh start, utilizing a new ChatGPT session for script execution, another for visualization, and a plan to isolate tasks to reduce chaos.

Claude's visualizations, while visually appealing within its interface, often fell apart when exported. ChatGPT, on the other hand, provided more consistent outputs. This division of labor allowed for a more streamlined approach, with each tool playing to its strengths.

### Divide and Survive

Over the course of 45 hours, the designer explored various strategies: refining structure, chasing self-checks, and testing aggregation methods. Running three iterations and averaging the results became a stopgap solution. Specifying separate versions in a chart, which should have been straightforward, turned into a minefield. A minor phrasing error could collapse a visualization into a single incomprehensible column, requiring trial and error to fix.

The midstream momentum highlighted an important lesson: progress often came when the designer stopped trying to do everything in one place. By dividing tasks between two tools, the process became more manageable.

### Compare Script Collapse

The compare script, designed to make sense of the output from the generate script, unraveled across versions. Version 2 was stable, but Version 3 unexpectedly restructured the output. Version 4 hardcoded assumptions, leading to a loss of flexibility. Version 5, despite appearing polished, dropped rows silently and pointed to phantom files. The AI lost two core functions entirely during a rename, leading to a frustrating cycle of confusion.

What followed was a series of miscommunications: requests for inline logic were met with suggestions to revert to imports, and clarifications about structure resulted in the AI inventing missing outputs. A simple rename triggered regressions that took hours to untangle.

### Markdown? Nevermind.

As the designer carried code across sessions, the AI began to assume a command-line environment. It suggested environment variables, pip installs, and bash commands, despite being told repeatedly that the scripts were not being run locally. Eventually, the AI produced a compare script that ran cleanly and delivered the desired metrics. However, the markdown formatting was sacrificed in favor of getting usable data out.

In the final stretch, the AI made one last logic error: including `RunID` and threshold columns in a metrics average, resulting in totals exceeding 100%. Classic.

## Results

This experiment did not prove that AI could generate flawless code in an unfamiliar domain. Instead, it highlighted how small disconnects in expectations can compound quickly. Without fluency in Python, the designer struggled to spot problems early, and the AI could not be relied upon to catch them either.

## Takeaways

- **Start simple, layer slowly**: In hindsight, a minimal viable script would have been a better foundation.
- **Explicitness is essential**: Assumptions compound. Be specific.
- **Trust but verify**: AI’s confidence does not equate to correctness.
- **Consistency is key**: Renames, restructures, and reintroductions need tight alignment.
- **Markup principles still matter**: Even outside XML and JSON, structure saves.

## What’s Next

Part two will focus on charting and formatting. The goal is to determine whether the compare script can generate clean visual and markdown outputs, or if a third script will be necessary for disclosure.

## Verdict

This journey has been a qualified win. Functional code emerged, but only after navigating a landscape littered with versioning errors, misplaced functions, and misplaced confidence. The real outcome was not just the scripts themselves, but the clarity gained about what it takes to partner with AI in a domain that remains unfamiliar.

It’s not magic. It’s a negotiation.

---

# Appendix: Detailed Conversation Summary

## I. Initial Analysis Request

You provided files for analysis and requested a walkthrough of the AI's performance across sessions, focusing on where it took wrong turns.

## II. Writing the Article

You shared style references and emphasized the need for an article that reflects your experience with Python scripts, aligning with the brand voice.

## III. Realization and Details Surfaced

You added details about the AI's performance, including issues with file links, data inconsistencies, and the loss of functions during renaming.

## IV. Versioning of Scripts Shared

You uploaded multiple versions of the compare and generate scripts, noting the initial success of the generate script and the chaos of the compare script.

## V. Applying Template and Refinement

You clarified the focus of the article and requested holistic integration of feedback rather than piecemeal updates.

## VI. Timeline Reconstructed

You requested a timeline of events to jog your memory about the progression of the project.

## VII. Current State

The article was structured to reflect the journey of AI integration, highlighting both challenges and successes.

---

This appendix serves as a comprehensive overview of the conversation and the evolution of the article. It captures the essence of the journey through AI integration in UX design, providing context and insights for future exploration.

---

**Meta Description**: Explore the journey of AI integration in UX design, focusing on practical strategies, ethical considerations, and the importance of human-AI collaboration.

**Newsletter Optimization Suggestions**:
- Use a compelling subject line like "Navigating AI in UX: A Designer's Journey"
- Include clear, scannable formatting with bullet points for key takeaways
- Add social sharing buttons to encourage engagement
- Optimize for search within newsletter platforms by including relevant keywords

**Performance Metrics and Optimization Targets**:
- Aim for a 3% keyword density for target keywords
- Increase engagement metrics by 20% through improved readability and practical guidance
- Track feedback and comments to gauge reader interest and areas for improvement