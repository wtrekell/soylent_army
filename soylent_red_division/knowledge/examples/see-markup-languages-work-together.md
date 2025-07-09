# See Markup Languages Work Together

## A Demonstration From Research to Draft

![](https://ik.imagekit.io/typeai/tr:w-1200,c-at_max/img_1t301qaHsNEcfp696A.jpg){ width=480px }

Structure makes a measurable difference in AI responses. I've simplified these prompts so you can test them yourself and see how markup languages change the quality of what you get back. These aren't prompts I'd actually use in practice. They're here to show how a complex workflow might function using **XML for data mining** → **JSON for data refinement** → **Markdown for draft creation**.

## Step 1: XML Data Mining

Here's a basic XML prompt to conduct research for this article:

```
<research_workflow>
  <objective>Gather comprehensive data for blog post about markup languages in AI prompting</objective>
 
  <step number="1">
    <action>Research current markup language usage in AI</action>
    <focus>Practical applications, not theoretical concepts</focus>
    <output>List of 8-10 real use cases with specific examples</output>
  </step>
 
  <step number="2">
    <action>Identify key benefits and challenges</action>
    <requirements>
      <requirement>Focus on UX designer perspective</requirement>
      <requirement>Include token efficiency considerations</requirement>
      <requirement>Address learning curve concerns</requirement>
    </requirements>
    <output>Structured comparison of advantages vs obstacles</output>
  </step>
 
  <step number="3">
    <action>Collect implementation examples</action>
    <criteria>
      <criterion>Beginner-friendly starting points</criterion>
      <criterion>Progressive complexity examples</criterion>
      <criterion>Common mistake patterns</criterion>
    </criteria>
    <output>
      <item>Basic template for each format</item>
      <item>Real-world application scenarios</item>
      <item>Troubleshooting guidance</item>
    </output>
  </step>
 
  <step number="4">
    <action>Synthesize decision framework</action>
    <focus>When to choose which format and why</focus>
    <output>Clear decision tree with practical criteria</output>
  </step>
</research_workflow>
```

You can see how this XML structure organizes the AI's thinking through explicit tags that prevent mixing up requirements with examples. Some models might start writing the blog post mentioned in the objective instead of doing research. That's fine since the structure still gives you consistent, organized output to work with.

**Save whatever output you get** even if it's not perfect. You'll need it for Step 2.

## Step 2: JSON Data Refinement

Take the output from Step 1 and use this JSON prompt to refine it into organized, human-readable insights. You can continue in the same session or start a fresh one.

Replace "**PASTE THE XML OUTPUT FROM STEP 1 HERE**" with your actual results.

> **Claude users:** Your XML output will likely be added as an attachment. Simply replace the paste instruction with "**Attached**" to avoid confusion.

```
{
  "content_refinement": {
    "objective": "Transform raw research into organized insights for UX designers",
    "input_data": "PASTE THE XML OUTPUT FROM STEP 1 HERE",
    "constraints": [
      "Focus on web-based AI tools only - no CLI or API information",
      "Target consumer AI interfaces like ChatGPT, Claude, etc.",
      "Exclude technical implementation details"
    ],
    "refinement_goals": [
      "Eliminate redundancy and organize by theme",
      "Prioritize information by practical importance",
      "Structure insights for logical article flow",
      "Identify compelling examples and quotes"
    ],
    "output_structure": {
      "key_insights": {
        "format": "3-5 main takeaways with supporting evidence",
        "style": "Clear, actionable statements"
      },
      "practical_examples": {
        "format": "Specific scenarios with before/after comparisons",
        "focus": "Real implementation challenges and solutions"
      },
      "decision_criteria": {
        "format": "Situational guidance for format selection",
        "style": "IF/THEN logic with concrete triggers"
      },
      "implementation_roadmap": {
        "format": "Step-by-step progression for beginners",
        "style": "Actionable next steps with success metrics"
      }
    },
    "quality_criteria": {
      "relevance": "Focus on UX designer workflows",
      "actionability": "Include specific tools and techniques",
      "clarity": "Avoid jargon, explain technical concepts simply"
    }
  }
}
```

Notice how JSON guides the AI to separate insights from examples from criteria. That organized structure makes Step 3 possible. **Save this refined output** for the final step.

## Step 3: Markdown Draft Creation

Use this Markdown structure to create a publication-ready draft. You can continue in the same session or start fresh.

Replace "**PASTE YOUR REFINED JSON OUTPUT FROM STEP 2 HERE**" with your refined info.

```
# Article Creation Task

## Source Material
PASTE YOUR REFINED JSON OUTPUT FROM STEP 2 HERE

## Objective
Transform the research insights above into a compelling blog post about markup languages for AI prompting

## Content Constraints
- Focus on web-based AI interfaces only
- Exclude CLI tools, API implementations, or technical setup
- Target consumer AI tools (ChatGPT, Claude, Gemini, etc.)

## Target Audience
UX designers with 2-5 years experience who are curious about AI integration

## Article Requirements
- **Length**: 1,200-1,500 words
- **Tone**: Practical educator sharing real experience
- **Structure**: Problem → Solution → Implementation → Next Steps
- **Examples**: Include specific code snippets and real scenarios

## Required Sections
1. **Hook**: Open with a relatable problem scenario
2. **Context**: Why markup matters for AI communication
3. **Comparison**: When to use XML vs JSON vs Markdown
4. **Implementation**: Step-by-step getting started guide
5. **Decision Framework**: Clear criteria for format selection
6. **Next Steps**: Actionable recommendations for readers

## Success Criteria
- Readers can immediately apply one technique after reading
- Decision framework helps them choose the right approach
- Examples are copy-pasteable and immediately useful
- Tone remains encouraging and practical throughout

## Output Format
Complete draft article ready for human editing and fact-checking
```

## Real Results: What Actually Happened

I tested this exact workflow across Claude 3.5 Sonnet, Gemini Pro, and ChatGPT-4o using the same prompts in fresh sessions. Here's what each model actually produced with no cherry-picking, just the first results from each.

- **Claude 4 Sonnet:** The UX Designer's Guide to Markup Languages
- **Gemini 2.5 Flash:** Tired of Generic AI Answers?
- **ChatGPT-4o:** Speak AI Fluently

These are the actual outputs—some better than others, all different in their own ways. See for yourself how structured prompts perform across the AI tools you're likely using.

## What You've Just Accomplished

You've experienced the complete markup progression:

1. **XML structured your thinking** and gathered comprehensive research
2. **JSON organized your insights** and made them human-readable
3. **Markdown transformed insights into content** ready for publication

This demonstrates structured prompting in practice. Each format serves its specific purpose in the content creation pipeline.

## Beyond This Demonstration

This three-step process works for research-to-publication workflows, but it's not universal. In reality, each of these prompts could've been written in Markdown (though I'd still choose JSON for Step 2's data transformation). The different formats here are primarily for demonstration.

The point isn't to always use this exact sequence. It's to see how each format serves different purposes in content workflows. Real implementations adapt based on what you're trying to accomplish and how complex your requirements are.

## Try It With Your Own Content

The beauty of this workflow is its flexibility. Replace the markup research topic with any subject you need to write about:

- **User research synthesis** - Use JSON/XML for data organization
- **Product feature documentation** - Markdown for clear, readable guides
- **Team process improvements** - Markdown/JSON for structured proposals
- **Design system guidelines** - Markdown/JSON for comprehensive documentation

*This is structured prompting in practice. What will you write about next?*