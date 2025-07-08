## When AI Brainstorming Became the Story

## An Experiment in Creative Collaboration

![](https://ik.imagekit.io/typeai/tr:w-1200,c-at_max/img_Yxo4vC4Rg3a0Ku0LJe.jpg){ width=480px }

Early last week, I was struggling to get a few AI agents to identify the need for a new agent, define it, and set it on a task. I got two talking and the third agent created, but the instructions on what it was expected to do got lost. That's a story for another time though.

While wrestling with those agents, I realized I'd been putting off planning a series of articles about practical AI use in office environments beyond single-task workflows.ar tasks. Rather than keep spinning my wheels hunting for the perfect topic, I pivoted. What if I made the *process* of AI-powered brainstorming the experiment itself?

## TL;DR

Using ChatGPT o3, I developed a comprehensive prompt using three creative frameworks, but had to negotiate for complete results when the AI initially provided arbitrary sampling instead of a comprehensive list. Testing the final prompt across several AI models revealed that two of the three converged on topics I'd recently been exploring and that had also appeared in recent Anthropic research.

## Oh GPT o3, Prompt me Please

I had ChatGPT o3 create a prompt which showed the process for using three creative frameworks to create article ideas. I specifically asked for a prompt that would have each AI give me *all* the results in one response to see if outputs would get mangled before I got started in earnest.

Unsurprisingly, o3 had decided to limit results to nine ideas. When I asked about it, the AI explained it was balancing "signal-to-noise." I explained the fundamental problem. The AI was making editorial decisions without showing its work, leaving me no way to evaluate the quality of the 9 I received against the options I'd never see.

> How am I to know if I was getting the best ideas, the worst ones, or just the first three that popped out?

The AI proposed a compromise: generate *all* the ideas first, score each on Trend Fit, Novelty, and Practical Impact, then rank them to surface the best performers. When I confirmed "That means it would have to provide all of them, show me the scores, and expand on the 9," it delivered a solution that satisfied my need for oversight without producing the brainstorming equivalent of "War & Peace." This approach offered transparent, scored ranking that moved from arbitrary sampling to deliberate selection. Oddly, I got a novel anyway. This is just the simplified outline:

---

- **Intro**: Brief role instruction for UX/product/service designers
- **Task Overview**: Step-by-step process for research, ideation, scoring, selection
- **Markdown Section 1**:
  - *Trends Snapshot*: Current UX/Product/Service-Design trends
  - *Idea Scorecard Table*: All 15 ideas with frameworks, principles, scores
- **Markdown Section 2**:
  - *Expanded Concepts*: Detailed expansion of nine winners
- **JSON Block**: Structured summary of winners with rank, id, scores
- **Formatting Rules**: Output format and presentation guidelines

*See the full Markdown and XML prompts*

---

The resulting prompt was comprehensive, to say the least. To reduce the risk of each AI wandering off in its own direction, I asked for it to XML-size the prompt and throw in some fries.

# The Brainstorming Storm

To ensure diverse and comprehensive ideas, I gave the AIs three distinct creative frameworks to work with. This approach provided scaffolding for their brainstorming and pushed them beyond surface-level suggestions.

**Tools and Versions:**

- ChatGPT o3 (initial prompt development)
- ChatGPT 4.1 (execution)
- Claude 4 Sonnet (execution)
- Gemini 2.5 Pro (execution)

### SCAMPER

SCAMPER is an acronym for seven creative thinking techniques that helps you expand ideas through targeted questions. It guides your brainstorming by asking specific questions about your concept or problem.

**SCAMPER Application**:

- **Substitute**: Replace traditional design approaches
- **Combine**: Merge separate design disciplines
- **Adapt**: Modify existing patterns for new contexts
- **Modify**: Scale or adjust current practices
- **Put to other uses**: Apply patterns to new domains
- **Eliminate**: Remove problematic elements
- **Reverse**: Invert traditional approaches

**Top SCAMPER Ideas from Each Model:**

```plaintext
Gemini 2.5 Pro
The Post-App Era: Substituting Apps with AI...       Substitute       27
Combine or Die: Merging Service & Product D...       Combine          25
Putting Ethics on Autopilot: Can We Elimina...       Eliminate        24

ChatGPT-4.1
AI-Driven Empathy Mapping                            Substitute       27
Sustainable Interaction Patterns                     Combine          25
AR Try-Before-You-Buy                                Substitute       24

Claude 4 Sonnet
Substitute Screens with Spatial Layers               Substitute       26
Combine Ethics with AI Tools                         Combine          25
Eliminate Dark Patterns Through Service Design       Eliminate        25
```

### Six Thinking Hats

Edward de Bono created the Six Thinking Hats framework to help teams examine decisions from multiple perspectives. Each “hat” represents a different thinking mode, forcing you to consider topics more holistically and give balanced consideration of a topic.

**Six Thinking Hats Application**:

- **White Hat** focuses on factual, data-driven analysis
- **Red Hat** explores emotional and intuitive responses
- **Black Hat** takes a critical, risk-focused approach
- **Yellow Hat** emphasizes optimistic, benefit-focused thinking
- **Green Hat** generates creative alternatives
- **Blue Hat** manages the overall process and maintains perspective

**Top Six Thinking Hats Ideas:**

```plaintext
Claude 3.5 Sonnet
Designing for Emotional AI Trust.                  Red Hat       25
The Business Case for Accessibility.               Yellow Hat    24
Sustainable Interaction Innovation.                Green Hat     23

Gemini 2.5 Pro
Beyond Brainstorms...                              Green Hat     28
The Optimist’s Guide to...                         Yellow Hat    25
A Pre-Mortem for Your...                           Black Hat     25

ChatGPT-4.1
De-Biasing Design Teams.                           Black Hat     26
AI Ideation Sprint.                                Green Hat     25
Calm Tech + UX.                                    Yellow Hat    23

```

### Lotus Blossom

The Lotus Blossom technique gives you a visual way to brainstorm that starts with one central theme and branches outward into related concepts. You place your core idea in the center of a 3x3 grid, then fill the surrounding squares with related sub-themes. This approach creates structured yet expansive exploration of your topic.

- **Central theme**: Core design challenge
- **Eight petals**: Related concepts branching from center
- **Secondary blooms**: Each petal becomes new center
- **Systematic expansion**: Comprehensive topic exploration

**Top Lotus Blossom Ideas:**

```
Gemini 2.5 Pro
Your Next Interface Isn't a Screen                   Central Petal    27
From Data Points to Life Paths: Desig...             Branch Petal     26
The Zero-Waste UI: A Manifesto for Sus...            Branch Petal     22

ChatGPT-4.1
Immersive 3D Navigation                              Branch Petal     27
Micro-interaction Toolkit                            Branch Petal     26
Ethical Data Flows                                   Branch Petal     25

Claude 3.5 Sonnet
Proactive Design: The Central Bloom                  Central Petal    26
Zero-Waste Digital Petal                             Branch Petal     24
Strategic Research Petal                             Branch Petal     23
```

## The Unexpected Convergence

The most surprising part? Two of the three models landed on a topic I've been exploring recently while working with agent AI systems. Interestingly, this same concept appeared in a recent Anthropic post.

After three rounds of scoring, each AI platform selected its champion. ChatGPT o1 and Gemini 2.5 Pro both crowned "**The Conductor: Orchestrating Human & AI Design Teams**" as the winner—a Six Thinking Hats Blue Hat concept focused on managing hybrid human-AI design workflows. Claude 4 Sonnet chose "**The Post-App Era: Substituting Apps with AI Agents**," a SCAMPER concept about replacing traditional applications with conversational AI.

The irony isn't lost on me: I started this experiment because I was creatively stuck, let AI help me brainstorm, and ended up with AIs telling me the biggest challenge is figuring out who should be in charge of the creative process. Perhaps that's the real insight—the future isn't about choosing between human or AI leadership, but learning when to conduct and when to play in the ensemble.

## Resources

**Keep Learning!**

- [SCAMPER Design Framework](https://www.perplexity.ai/page/scamper-design-framework-40setAC9Rm.c9rVa507_fQ)
- [Six Thinking Hats Framework](https://www.perplexity.ai/page/six-thinking-hats-framework-uxqP48DmS6yS5nv7dhVmMA)
- [Lotus Blossom Ideation Framework](https://www.perplexity.ai/page/lotus-blossom-ideation-framewo-hkI5xcHUS2i8lDKtsxet1A)

**Topical Links:**

- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system)
- [Wikipedia: Edward de Bono](https://en.wikipedia.org/wiki/Edward_de_Bono)

**Project Files:**

- **Experiment Transcripts:** \[brainstorming-sessions.zip]

*A note on the session transcripts: Given how quickly AI models evolve, the specific outputs and behaviors documented in these chat sessions are already losing relevance and will continue to do so as models get updated and new ones emerge. However, the underlying creative frameworks—SCAMPER, Six Thinking Hats, and Lotus Blossom will surely endure.*

## Appendix

```plaintext
You are a research assistant for UX, product, and service designers.

**Task overview (do ALL steps, then answer once):**

1. **Quick scan:** Search the web for the most current topics, pain points, and emerging trends in UX, product, and service design (use any browser/search tool available).

2. **Ideation:** Using what you just learned, brainstorm **15 article concepts**—**five per framework**:  
   - **SCAMPER** (draw from its seven verbs)  
   - **Six Thinking Hats**  
   - **Lotus Blossom** (start with a central UX theme and branch)  
   For every idea, give:  
   - A catchy **title**  
   - A 1-to-2 sentence **summary**  
   - The **specific principle** (e.g., “SCAMPER – Combine”)

3. **Score & rank:** For all 15 ideas, assign a 0-10 score for each of:  
   - **Trend Fit** (relevance to the trends you found)  
   - **Novelty** (freshness vs. what’s already out there)  
   - **Practical Impact** (how actionable it is for designers)  
   Add them for a **Total Score**.  
   **Sort ideas within each framework by Total Score (highest→lowest).**

4. **Select winners:** Take the **top three ideas in each framework** (9 winners total).

5. **Expand winners:** For each of the nine winners, provide a concise expansion with:  
   - **Who it helps most** (target reader)  
   - **3-4 takeaway bullets** (what they’ll learn/act on)  
   - **Suggested visual or example** to include in the article

6. **Output everything in ONE response** using **all three sections below, in this order, and nothing else.**

---

### Markdown section (1 + 2 + 3)

## Current UX/Product/Service-Design Trends (snapshot)
- AI-driven personalization
- Accessibility as a baseline requirement
- Micro-interactions for user delight
- …

## Idea Scorecard (all 15)

| # | Title                        | Summary                                                          | Framework        | Principle    | Trend Fit | Novelty | Impact | **Total** |
|---|------------------------------|------------------------------------------------------------------|------------------|--------------|-----------|---------|--------|-----------|
| 1 | The Frictionless Feedback Loop | Techniques for creating seamless in-app feedback channels.        | SCAMPER          | Substitute   | 9         | 9       | 8      | **26**    |
| 2 | …                            | …                                                                | SCAMPER          | …            | …         | …       | …      | …         |
| … |                              |                                                                  |                  |              |           |         |        |           |

---

### Markdown section (4 + 5 – Expanded Concepts)

## Expanded Concepts (Top 9)

### The Frictionless Feedback Loop — SCAMPER • Substitute
**Who it helps most:** Product managers and UX researchers in SaaS  
**Key takeaways:**  
- Embed feedback directly into product touchpoints  
- Reduce user drop-off with intuitive, one-tap surveys  
- Analyze and act on qualitative data in real time  
**Suggested visual:** Annotated flow diagram of an in-app feedback journey

### …

---

### JSON block (6)

{
  "best_ideas": [
    { "rank": 1, "id": 1, "title": "The Frictionless Feedback Loop", "framework": "SCAMPER", "principle": "Substitute", "total": 26 },
    ...
  ]
}

---

**Formatting rules**

- Present the two Markdown sections **exactly** as shown, followed by the raw JSON block (no backticks around the JSON).
- The **Idea Scorecard table must list all 15 ideas** with their scores.
- In **Expanded Concepts**, list **only the nine winners** in the order SCAMPER → Six Hats → Lotus Blossom (highest-scoring first within each framework).
- Use the table’s **#** as the `id` field in JSON so each winner is traceable.
- Respond **once**—no partial outputs.
- Follow this structure precisely; any deviation is an error.

```

```plaintext
<?xml version="1.0" encoding="UTF-8"?>
<prompt>
  <intro>
    You are a research assistant for UX, product, and service designers.
  </intro>

  <taskOverview>
    <step order="1">
      Quick scan: Search the web for the most current topics, pain points, and emerging trends in UX, product, and service design (use any browser/search tool available).
    </step>
    <step order="2">
      Ideation: Using what you just learned, brainstorm <strong>15 article concepts</strong>—five per framework:
      <list>
        <item>SCAMPER (draw from its seven verbs)</item>
        <item>Six Thinking Hats</item>
        <item>Lotus Blossom (start with a central UX theme and branch)</item>
      </list>
      For every idea, provide:
      <list>
        <item>A catchy <em>title</em></item>
        <item>A 1-to-2 sentence <em>summary</em></item>
        <item>The <em>specific principle</em> (e.g., “SCAMPER – Combine”)</item>
      </list>
    </step>
    <step order="3">
      Score &amp; rank: For all 15 ideas, assign a 0–10 score for each of
      <list>
        <item>Trend Fit (relevance to the trends you found)</item>
        <item>Novelty (freshness vs. what’s already out there)</item>
        <item>Practical Impact (how actionable it is for designers)</item>
      </list>
      Add them for a <strong>Total Score</strong>. Sort ideas <em>within each framework</em> by Total Score (highest → lowest).
    </step>
    <step order="4">
      Select winners: Take the <strong>top three ideas in each framework</strong> (9 winners total).
    </step>
    <step order="5">
      Expand winners: For each of the nine winners, provide
      <list>
        <item><strong>Who it helps most</strong> (target reader)</item>
        <item><strong>3–4 takeaway bullets</strong> (what they’ll learn / act on)</item>
        <item><strong>Suggested visual or example</strong> to include in the article</item>
      </list>
    </step>
    <step order="6">
      Output everything in <strong>one response</strong> using <em>all three sections</em> below, in this order, and nothing else.
    </step>
  </taskOverview>

  <markdownTemplates>
    <section name="TrendsAndScorecard"><![CDATA[
## Current UX/Product/Service-Design Trends (snapshot)
- {Trend 1}
- {Trend 2}
- {Trend 3}
- …

## Idea Scorecard (all 15)

| # | Title | Summary | Framework | Principle | Trend Fit | Novelty | Impact | **Total** |
|---|-------|---------|-----------|-----------|-----------|---------|--------|---------|
| 1 | … | … | SCAMPER | Substitute | 9 | 8 | 7 | **24** |
| 2 | … | … | SCAMPER | Combine | 8 | 9 | 6 | **23** |
| … |   |   |         |           |   |   |   |       |
    ]]></section>

    <section name="ExpandedConcepts"><![CDATA[
## Expanded Concepts (Top 9)

### {Title of Winner 1} — SCAMPER • Substitute
**Who it helps most:** {Target reader}  
**Key takeaways:**  
- Bullet 1  
- Bullet 2  
- Bullet 3  
**Suggested visual:** {Visual/exercise/example}

### {Title of Winner 2} — SCAMPER • …  
…
    ]]></section>
  </markdownTemplates>

  <jsonTemplate><![CDATA[
{
  "best_ideas": [
    { "rank": 1, "id": 3,  "title": "…", "framework": "SCAMPER",        "principle": "Substitute", "total": 24 },
    { "rank": 2, "id": 6,  "title": "…", "framework": "Six Thinking Hats", "principle": "Green Hat",  "total": 23 },
    { "rank": 3, "id": 11, "title": "…", "framework": "Lotus Blossom",  "principle": "Petal X",    "total": 22 },
    { "rank": 4, "id": 7,  "title": "…", "framework": "Six Thinking Hats", "principle": "Yellow Hat", "total": 22 },
    { "rank": 5, "id": 1,  "title": "…", "framework": "SCAMPER",        "principle": "Combine",    "total": 21 }
  ]
}
    ]]></jsonTemplate>

  <formattingRules>
    <rule>Present the two Markdown sections exactly as shown, followed by the raw JSON block (no backticks around the JSON).</rule>
    <rule>The Idea Scorecard table must list all 15 ideas with their scores.</rule>
    <rule>In <em>Expanded Concepts</em>, list only the nine winners in the order SCAMPER → Six Thinking Hats → Lotus Blossom (highest-scoring first within each framework).</rule>
    <rule>Use the table’s <code>#</code> as the <code>id</code> field in JSON so each winner is traceable.</rule>
    <rule>Respond once—no partial outputs.</rule>
    <rule>Follow this structure precisely; any deviation is an error.</rule>
  </formattingRules>
</prompt>

```

