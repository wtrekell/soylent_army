# Engaging Experiment

## Hypothesis

AI can produce functional, reliable Python code for a metrics system outside my domain expertise—specifically, to compare and analyze document versions—without requiring me to debug or understand the underlying language.

## Context

This was actually my second attempt at solving the problem.

The first try—several days deep and buried in tangled logic—was far messier, but in some ways, more ambitious. That version started with a preexisting script I'd been updating for months. After a hiatus, I dove back in with newer models, trying to push it forward. Early results were promising, but as I layered on structure and scope, the whole thing ballooned past 11,000 characters and collapsed under its own complexity.

I ran the gauntlet: ChatGPT, Claude, Gemini, Perplexity. I spun up dual sessions, cross-fed model feedback, and orchestrated an AI-powered peer review cycle more elaborate than anything I’ve seen in enterprise QA. It was fascinating—until it wasn’t. JSON structures were inconsistent, visualizations broke formatting across platforms, and everything groaned under the weight of trying to do too much in a single pass.

The fatal blow came when I began running real article data through what looked like a solid JSON framework. I had trimmed it for token efficiency, but stripped away too much context. Key stages like draft → refined → edited → final became ambiguous. Each run interpreted the workflow differently, leading to wildly divergent outputs.

When I asked for explanations, models provided wildly different rationales—some useful, some unreadable. At one point I had Claude and GPT analyzing each other's recommendations like digital consultants stuck in a loop. If that sounds excessive, it was. It also didn’t work.

Eventually, sometime between frustration and sleep deprivation, I realized I could either continue patching a framework that was actively working against me—or start clean, with a new strategy and minimal assumptions.

That’s what this second experiment became.

This experiment emerged from the limitations of my existing process. I had been using JSON to structure light logic for AI workflows and XML for heavier, multi-step ones. But as one particular project ballooned in complexity, even XML exceeded its usable context window. When I asked Claude what format would suit this logic best, the answer came back: Python.

The problem? I don’t read or write Python. That meant trusting the AI to do the job end-to-end.

## Setup

The task was to generate two scripts:

1. One to generate metrics from different versions of a document (generate script).
2. One to compare the results across those versions (compare script).

Both scripts needed to produce CSV outputs and summaries I could use for publishing metrics transparently. Charts and markdown formatting were stretch goals.

## Process

### Sleep-Deprived Insight

Somewhere around 2:30 a.m., in that hazy mix of sleep and obsession, it hit me: the ethical reporting structure had only gone haywire after I started feeding real article data into what seemed like a good JSON framework. Up to that point, things had looked solid. But every time I put it to work, the output imploded. That morning, I started clean—with a fresh ChatGPT browser session to run the scripts, another window for visualization, and a plan to isolate tasks to reduce chaos.

### Visualization Dysfunction

Claude's visualizations looked great inside its own interface but fell apart when exported—SPG errors, formatting issues, zero spacing. ChatGPT, despite occasionally spitting out oversimplified charts, at least delivered usable outputs most of the time. I leaned on it for graphs, while Claude helped with commentary and code logic.

### Refactoring for Sanity

I probably spent 45 hours in total trying to get ethical reporting right—refining structure, chasing self-checks, testing aggregation methods. I started experimenting with running three rounds and averaging them out. Good enough was looking increasingly like the only achievable goal.

Even simple things like specifying separate versions in a chart proved surprisingly difficult. More than once, a miswritten script produced a singular column that smashed everything together. Fixing it meant trial-and-error, instruction rephrasing, visual feedback, and often settling for what worked instead of what was ideal.

This midstream burst of momentum—between the wreckage of the first attempt and the fresh start of the second—revealed something important: some of the best progress came when I stopped trying to do everything in one place. Two tools, two jobs. Divide, simplify, survive.

### Generate Script: The Straightforward One

At first, things went surprisingly well. The AI and I covered a lot of ground quickly—especially with the generate script. It was direct, relatively clean, and once finalized, I used it to process three full articles without issue. The data looked sound, and the structure held.

### Compare Script: A Fractured Saga

But what I hadn’t accounted for was how fragile that early success would be once the AI had to carry logic across multiple sessions.

The compare script—intended to make sense of the output from the generate script—unraveled version by version. Version 2 was stable. Version 3 restructured the output unexpectedly. Version 4 hardcoded assumptions and collapsed flexibility. Version 5, despite presenting as a polished solution, dropped rows silently and pointed to phantom files. Even worse, it lost two core functions entirely. Neither I nor the AI noticed at the time, so I saved and handed back a broken script. In the next session, the AI kept referencing those now-missing functions and insisted I import them from a module that no longer existed.

What followed was a frustrating cycle: I asked for inline logic; it kept reverting to imports. I clarified the structure; it invented missing outputs. And somewhere in all of this, a simple renaming triggered regressions I spent hours untangling.

Meanwhile, because I was carrying code across sessions, the AI began treating me like a Python developer. It started suggesting bash commands to run scripts, complete with environment setup instructions—despite knowing I wasn’t running these scripts directly.

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

# Appendix: Timeline and Conversation Summary

## 🗓️ Timeline of Events

### 1. Initial Efforts (Early JSON Framework Attempt)
- **Goal**: Build an ethical reporting system using JSON to measure deltas between article stages.
- **Approach**: Started from a preexisting script; expanded it with updated models.
- **Symptoms**: Inconsistent stage comparisons, visualizations breaking, massive bloat (11,000+ chars).
- **Outcome**: Framework collapsed under its own complexity. Abandoned.

### 2. Intermediate Night Session (Aha Moment)
- **Time**: ~2:30 a.m.
- **Insight**: Realized the JSON structure failed only with full article data.
- **Change**: Switched to running parallel model sessions, separating logic and visual tasks.
- **Outcome**: Clean slate with minimal assumptions.

### 3. Second Attempt: Python Rewrite Begins
- **Reason**: XML hit context limits. Claude suggested Python.
- **Constraint**: You don’t read Python—this became a trust experiment.
- **Setup**: Two scripts—generate (metrics) and compare (aggregation).

### 4. Generate Script Stabilizes
- **Progress**: Script ran 3 articles cleanly.
- **Observation**: Structure held; less issue compared to compare script.

### 5. Compare Script Chaos (Versions 2–5)
- **v2**: Stable.
- **v3**: Unexpected structure.
- **v4**: Hardcoded assumptions.
- **v5**: Silent data drops, missing functions, phantom imports.
- **Outcome**: Final version ran cleanly, but markdown was dropped in favor of stable data.

### 6. Ethical Reporting Improves, Markdown Doesn’t
- **Visualization Failures**: Claude’s spacing issues; ChatGPT more usable.
- **Tradeoff**: You let markdown go to prioritize metrics.
- **AI Misfire**: Included `RunID` in average totals, breaking results.

### 7. Reflective Consolidation
- **Realization**: This wasn’t about scripting—it was about orchestrating trust across models.
- **Framing**: Started treating AI like teammates, not tools.

## 📄 Conversation Summary

### Style and Writing Setup
- Provided reference files to match tone (not content).
- Goal: Honest, witty, transparent storytelling about working with AI.

### Script Troubles
- Provided early and late versions of both `generate` and `compare` scripts.
- Scripts regressed, lost functions, misinterpreted file changes.

### Implementation Refinement
- Emphasized AI's assumptions about CLI usage.
- Trimmed redundancy, added intentional wit.
- Rewrote context to split “First Attempt” vs “Pivot to Python.”
- Used subheadings in “Process” for better flow.

### Timeline Recap
| Phase | Description | Outcome |
|-------|-------------|---------|
| **JSON Framework** | Token-optimized logic, collapsed under real data | Abandoned |
| **2:30 a.m. Reset** | Realized context loss and fragmentation | Pivot to Python |
| **Generate Script** | Built successfully, 3 articles processed | Stable |
| **Compare Script (v2–v5)** | Multiple regressions, data loss, import issues | Eventually stabilized |
| **Markdown + Charts** | Visualization output unreliable | Split tools by task |
| **Current State** | Metrics solid, charts and summaries next | Part 2 focus |

