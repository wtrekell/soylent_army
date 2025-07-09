# Engaging Experiment

## Hypothesis

AI can produce functional, reliable Python code for a metrics system outside my domain expertise—specifically, to compare and analyze document versions—without requiring me to debug or understand the underlying language.

## Background: The First Attempt

This was actually my second attempt at solving the problem.

The first try—several days deep and buried in tangled logic—was far messier, but in some ways, more ambitious. That version started with a preexisting script I'd been updating for months. After a hiatus, I dove back in with newer models, trying to push it forward. Early results were promising, but as I layered on structure and scope, the whole thing ballooned past 11,000 characters and collapsed under its own complexity.

I ran the gauntlet: ChatGPT, Claude, Gemini, Perplexity. I spun up dual sessions, cross-fed model feedback, and orchestrated an AI-powered peer review cycle more elaborate than anything I’ve seen in enterprise QA. It was fascinating—until it wasn’t. JSON structures were inconsistent, visualizations broke formatting across platforms, and everything groaned under the weight of trying to do too much in a single pass.

The fatal blow came when I began running real article data through what looked like a solid JSON framework. I had trimmed it for token efficiency, but stripped away too much context. Key stages like draft → refined → edited → final became ambiguous. Each run interpreted the workflow differently, leading to wildly divergent outputs.

When I asked for explanations, models provided wildly different rationales—some useful, some unreadable. At one point I had Claude and GPT analyzing each other's recommendations like digital consultants stuck in a loop. If that sounds excessive, it was. It also didn’t work.

Eventually, sometime between frustration and sleep deprivation, I realized I could either continue patching a framework that was actively working against me—or start clean, with a new strategy and minimal assumptions.

That’s what this second experiment became.

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

# Appendix: Timeline of Events

### 1. Initial Efforts (Early JSON Framework Attempt)
- **Goal**: Build an ethical reporting system using JSON to measure deltas between article stages (draft → refined → edited → final).
- **Approach**: Started with a preexisting JSON-based script, expanding it with updated models. Tried to make it token-efficient by stripping excess context.
- **Symptoms**: Wildly inconsistent numbers from runs. Claude and GPT compared one another’s output like dueling consultants. Attempts to restructure led to massive bloat (11,000+ characters).
- **Outcome**: Realized the framework was too fragile and unclear to maintain.

### 2. Intermediate Night Session (Aha Moment)
- **Time**: ~2:30 a.m.
- **Insight**: The JSON collapsed when run against full articles—not during design. You concluded it lacked the instruction specificity for real content.
- **Shift**: Decided to clean slate. Opened parallel sessions: One for running the code (ChatGPT browser), One for visualizations, One for writing/fixing logic (Claude).

### 3. Second Attempt: Python Rewrite Begins (Current Article Focus)
- **Reason**: XML hit its context ceiling. You asked Claude what format it would use—it said Python.
- **Constraint**: You don’t know Python, so this became an experiment in trusting the AI.
- **Setup**: A generate script to process deltas. A compare script to aggregate and report them.

### 4. Generate Script Stabilizes
- **Progress**: Generate script came together relatively easily. You were able to process 3 full articles with no issues. Data structure held.

### 5. Compare Script Chaos (Versions 2–5)
- **Version 2**: Baseline. Worked. **Version 3**: Restructured output unexpectedly. **Version 4**: Hardcoded assumptions, less flexibility. **Version 5**: Looked good—but silently dropped rows and linked to phantom files.

### 6. Ethical Reporting Improves, Markdown Doesn’t
- **Victory**: Compare script eventually delivered correct metrics. **Tradeoff**: You gave up on markdown formatting to just get usable data.

### 7. Visualization Complexity & Continued Refinement
- **Problem**: Chart rendering logic was fragile. A minor change could collapse multiple versions into one column.

### 8. Reflective Consolidation
- **Realization**: You weren’t doing AI-assisted coding—you were doing multi-model orchestration without knowing the language.

### Summary Table
| Phase | Description | Outcome |
| --- | --- | --- |
| **JSON Framework** | Token-optimized logic, collapsed under real data | Abandoned |
| **2:30 a.m. Reset** | Realized context loss and fragmentation | Pivot to Python |
| **Generate Script** | Built successfully, 3 articles processed | Stable |
| **Compare Script (v2–v5)** | Multiple regressions, data loss, import issues | Eventually stabilized |
| **Markdown + Charts** | Visualization output unreliable | Split tools by task |
| **Current State** | Metrics solid, charts and summaries next | Part 2 focus |