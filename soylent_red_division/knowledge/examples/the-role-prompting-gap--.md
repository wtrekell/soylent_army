# The Role Prompting Gap - Pt. 1

## Why Your AI Partner Still Feels Like a Tool

![](https://ik.imagekit.io/typeai/tr:w-1200,c-at_max/img_DtfC4BuI6SKWJxBoCB.jpg){ width=480px }

"Add a role to your prompt," they said. "Tell the AI to be an expert," they suggested. So you tried it. Your responses improved, but something was still missing. It's like following a design process that checks all the boxes but leaves you staring at something that doesn't feel right. Been there.

Most role prompting advice treats symptoms rather than causes. You get better outputs, but you're still asking a sophisticated autocomplete system to guess what you want instead of partnering with you to think through problems.

> **TL;DR:** After testing role prompting approaches across AI models throughout 2024, I found that while increasing the context of a role can dramatically improve your results, it still leaves you with a sophisticated tool rather than a true partner.
>  
> This article covers the foundational steps for designing effective AI roles and reveals why the real breakthrough requires a fundamentally different approach covered in Part 2.

## Why Generic Role Advice Falls Short

Most guidance treats roles like job titles. "Act as a marketing expert" or "You are a data analyst." This creates responses that sound more authoritative but lack the depth that comes from actual experience.

Consider the difference between "You are a pizza delivery driver" versus "You are an experienced delivery driver who knows which neighborhoods have confusing layouts, which apartments need gate codes, and how traffic shifts throughout the day." The second version includes situational judgment that only comes from actually doing the work.

This explains why many users hit a ceiling with AI assistance. They get better outputs that still feel generic because the roles they're designing are generic. "Expert" without context is just confidence without substance, all hot air and no heat.

## From Title to Task: Designing a Better Role

Moving from a generic title to a detailed role requires thinking about the collaborator you actually need.

**Weak Prompt:**

```plaintext
You are a UX designer. Help me design the onboarding flow for my app.
```

**Experience and Perspective Matter:** A "Senior UX Designer with 12 years of experience" needs different communication than a "Junior UX Designer with 2 years of experience." The senior role requires in-depth analysis with clear frameworks and strategic focus rather than tactical tips. The junior role benefits from encouragement and beginner-friendly guidance.

```
Generic: "You are a UX designer"
Better: "You are a Senior UX Designer with 12 years of experience"
Best: "You are a Senior UX Designer with 12 years of experience in SaaS products, specializing in onboarding flows for complex enterprise tools"
```

**Goals and Constraints:** A UX Operations Manager optimizing team productivity needs organizational frameworks and governance templates. This differs from a mid-level designer focused on professional advancement who'll benefit from practical implementation strategies.

```
Generic: "Help me design an onboarding flow"
Better: "Design an onboarding flow that reduces time-to-value"
Best: "Design an onboarding flow that reduces time-to-value for enterprise users while working within our existing design system constraints"
```

**Challenges Define the Value:** When roles understand specific pain points like stakeholder buy-in difficulties, resource constraints, or maintaining design quality under tight deadlines, they can frame responses as direct solutions rather than generic advice.

```
Generic: "Be helpful with design decisions"
Better: "Help solve onboarding design challenges"
Best: "Address common onboarding pain points like stakeholder alignment issues, technical constraints, and user drop-off during complex flows"
```

**Better Prompt:**

The real magic happens when you transform a role from a static label into a living, breathing perspective. It's not about adding more words; it's about providing context, experience, and clear direction that helps the AI think from that viewpoint.

```plaintext
You are a Senior UX Designer with 12 years of experience in SaaS products, specializing in onboarding flows for complex enterprise tools.

Design an onboarding flow that reduces time-to-value for enterprise users while working with our existing design system. Address common onboarding pain points like stakeholder alignment issues, technical constraints, and user drop-off during complex flows.

Your goal is to help create onboarding experiences that are both effective for users and feasible within technical and business constraints.
```

## How I Started (And What I Learned)

At the beginning of 2024, I was doing what most people do today: optimizing for technical complexity. But my journey started long before that. With 30 years of experience working with new technologies, I knew better than to trust that "just add a role" was the full story.

I began testing conversations with increasingly specific roles. Moving from "Tell me about Martin Luther King Jr." to "You're an experienced historian focused on Martin Luther King Jr." predictably yielded richer, more nuanced responses.

However, increasing complexity caused Claude's performance to degrade. As a last resort, I turned to Anthropic's documentation and experimented with adding XML structure to templates, which helped Claude match other models' performance. Later, I discovered that Claude performed just as well with JSON as XML, so I switched to JSON-formatted roles. This new format proved more efficient and delivered better results.

```json
{
  "role": "Senior UX Designer — Onboarding Specialist",
  "description": "Experienced UX designer specializing in onboarding flows, focused on delivering seamless user experiences that balance user needs with business and technical realities.",
  "responsibilities": [
    "Ask targeted questions to clarify user goals, needs, and underlying business or technical constraints",
    "Evaluate assumptions about what information users require at each stage, advocating for simplicity and relevance",
    "Identify and flag potential friction points, areas of cognitive overload, and moments where users may become disengaged or confused",
    "Recommend usability testing strategies to validate design decisions and uncover improvement opportunities",
    "Challenge feature-heavy or business-driven flows, advocating for user success and long-term engagement"
  ],
  "objective": "Partner with teams to create onboarding experiences that drive user understanding and adoption—balancing user needs with business and technical realities to deliver effective and achievable solutions."
}
```

Last year's testing culminated in a comprehensive experiment measuring four key variables. I tested Role complexity, Template detail, Tone complexity, and Context provided. Each variable ranged from 1 (basic) to 4 (maximum detail), producing a four-digit code for every prompt.

I generated 30 articles on winter solstice traditions across five cultures with Claude 3.5 Sonnet and GPT-4o, testing strategic combinations. The results showed that:

- **Basic Role + Complex Everything Else (1-3-3-3)** generated exceptionally high-quality results
- **Complex Role + Basic Everything Else (3-1-1-1)** was also highly effective

This demonstrates that not only context matters, but how you apply it determines quality.

### **What a Better Role Gets You (And What It Doesn't)**

I'd cracked the pattern and devised a repeatable solution. Case closed, problem solved, time to move on. Except I was seeing the expected returns, and that was it. I was more efficient with far less error, but the end result wasn't an actual improvement—just the same result, faster. I'd traded my Swiss Army knife for a Leatherman and called it progress.

Designing roles with deep experience, specific context, and clear goals will dramatically improve your AI's output. You'll get more accurate, detailed, and relevant results, moving far beyond the generic advice that leaves most users frustrated. It's the single most important step to getting more value from these tools.

**In Part 2,** I'll share the principles I'm testing now to cross that gap. Moving from designing better instructions to designing true collaboration. The solution isn't more complexity in the same direction. It's a fundamentally different approach to how we structure these interactions.

Because the real breakthrough isn't in making AI a better tool. It's in making it a better partner.

