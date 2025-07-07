from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
import json
import os
from datetime import datetime


class BrandStyleGuideInput(BaseModel):
    """Input schema for BrandStyleGuideTool."""
    query: str = Field(..., description="Query about brand guidelines, voice, or style requirements")


class BrandStyleGuideTool(BaseTool):
    name: str = "Brand Style Guide"
    description: str = (
        "Access brand guidelines, voice, tone, and style requirements. "
        "Use this tool to ensure content aligns with brand standards and messaging."
    )
    args_schema: Type[BaseModel] = BrandStyleGuideInput

    def _run(self, query: str) -> str:
        """Retrieve brand guidelines and style information."""
        try:
            # Check for brand guidelines in knowledge folder
            knowledge_path = "/Users/williamtrekell/Documents/git_repos/soylent_army/soylent_red/knowledge"
            brand_file = os.path.join(knowledge_path, "brand_guidelines.md")
            
            if os.path.exists(brand_file):
                with open(brand_file, 'r', encoding='utf-8') as f:
                    guidelines = f.read()
                return f"Brand Guidelines:\n{guidelines}"
            else:
                # Default brand guidelines template
                return """Default Brand Guidelines:
                
Voice & Tone:
- Professional yet approachable
- Authoritative but not condescending
- Clear and concise communication
- Value-driven messaging

Writing Style:
- Use active voice
- Keep sentences clear and concise
- Include relevant examples and data
- Structure content with clear headings
- Maintain consistent terminology

Content Standards:
- Always provide actionable insights
- Include credible sources and citations
- Focus on reader value and benefits
- Use compelling headlines and introductions
- End with clear takeaways or calls-to-action

Format Requirements:
- Use proper markdown formatting
- Include relevant subheadings (H2, H3)
- Break up text with bullet points and lists
- Optimize for readability and engagement"""
                
        except Exception as e:
            return f"Error accessing brand guidelines: {str(e)}"


class WebResearchInput(BaseModel):
    """Input schema for WebResearchTool."""
    topic: str = Field(..., description="Topic to research")
    focus_area: Optional[str] = Field(None, description="Specific focus area or angle for research")


class WebResearchTool(BaseTool):
    name: str = "Web Research"
    description: str = (
        "Conduct comprehensive web research on topics to gather current information, "
        "trends, statistics, and insights for content creation."
    )
    args_schema: Type[BaseModel] = WebResearchInput

    def _run(self, topic: str, focus_area: Optional[str] = None) -> str:
        """Perform web research on the given topic."""
        try:
            # This is a simplified research tool
            # In production, you would integrate with actual search APIs
            research_query = f"{topic}"
            if focus_area:
                research_query += f" {focus_area}"
                
            return f"""Research Results for: {topic}
            
Focus Area: {focus_area if focus_area else 'General overview'}

Key Findings:
- Current market trends and developments
- Recent industry reports and statistics  
- Expert opinions and insights
- Emerging themes and topics
- Competitive landscape analysis

Research Sources:
- Industry publications and reports
- Expert interviews and quotes
- Statistical databases
- News articles and press releases
- Academic studies and research papers

Recommended Content Angles:
- Latest trends and innovations
- Data-driven insights and analysis
- Expert perspectives and commentary
- Practical applications and case studies
- Future predictions and implications

Note: This is a template response. In production, integrate with actual search APIs like Google Search API, Bing Search API, or specialized research databases."""
            
        except Exception as e:
            return f"Error conducting research: {str(e)}"


class SEOAnalysisInput(BaseModel):
    """Input schema for SEOAnalysisTool."""
    content: str = Field(..., description="Content to analyze for SEO optimization")
    target_keywords: Optional[str] = Field(None, description="Target keywords for optimization")


class SEOAnalysisTool(BaseTool):
    name: str = "SEO Analysis"
    description: str = (
        "Analyze content for SEO optimization opportunities including keyword density, "
        "content structure, and search engine best practices."
    )
    args_schema: Type[BaseModel] = SEOAnalysisInput

    def _run(self, content: str, target_keywords: Optional[str] = None) -> str:
        """Analyze content for SEO optimization."""
        try:
            word_count = len(content.split())
            
            # Basic SEO analysis
            has_h1 = "# " in content
            has_h2 = "## " in content
            has_h3 = "### " in content
            
            # Check for target keywords if provided
            keyword_analysis = ""
            if target_keywords:
                keywords = [kw.strip().lower() for kw in target_keywords.split(",")]
                content_lower = content.lower()
                keyword_density = {}
                
                for keyword in keywords:
                    count = content_lower.count(keyword)
                    density = (count / word_count) * 100 if word_count > 0 else 0
                    keyword_density[keyword] = {"count": count, "density": density}
                
                keyword_analysis = f"""
Keyword Analysis:
{chr(10).join([f"- '{kw}': {data['count']} occurrences ({data['density']:.1f}% density)" 
               for kw, data in keyword_density.items()])}
"""

            return f"""SEO Analysis Report:

Content Statistics:
- Word count: {word_count}
- Has H1 header: {has_h1}
- Has H2 headers: {has_h2}
- Has H3 headers: {has_h3}

{keyword_analysis}

SEO Recommendations:
- Ensure headline is compelling and includes target keywords
- Use descriptive subheadings (H2, H3) for better structure
- Maintain keyword density between 1-3% for target keywords
- Include meta description (150-160 characters)
- Add internal and external links where relevant
- Optimize for featured snippets with clear, concise answers
- Ensure mobile-friendly formatting
- Include relevant images with alt text

Newsletter-Specific SEO:
- Optimize subject line for email deliverability
- Use clear, scannable formatting
- Include social sharing buttons
- Optimize for search within newsletter platforms"""
            
        except Exception as e:
            return f"Error analyzing content for SEO: {str(e)}"


class ContentQualityInput(BaseModel):
    """Input schema for ContentQualityTool."""
    content: str = Field(..., description="Content to analyze for quality and readability")


class ContentQualityTool(BaseTool):
    name: str = "Content Quality Analysis"
    description: str = (
        "Analyze content for quality, readability, engagement factors, and publication standards. "
        "Provides recommendations for improvement."
    )
    args_schema: Type[BaseModel] = ContentQualityInput

    def _run(self, content: str) -> str:
        """Analyze content quality and readability."""
        try:
            lines = content.split('\n')
            paragraphs = [line for line in lines if line.strip() and not line.startswith('#')]
            sentences = []
            
            for paragraph in paragraphs:
                sentences.extend([s.strip() for s in paragraph.split('.') if s.strip()])
            
            word_count = len(content.split())
            sentence_count = len(sentences)
            paragraph_count = len(paragraphs)
            
            avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
            avg_sentences_per_paragraph = sentence_count / paragraph_count if paragraph_count > 0 else 0
            
            # Basic readability assessment
            readability_score = "Good"
            if avg_words_per_sentence > 25:
                readability_score = "Needs Improvement - Sentences too long"
            elif avg_words_per_sentence < 10:
                readability_score = "Needs Improvement - Sentences too short"
                
            return f"""Content Quality Analysis:

Structure Analysis:
- Word count: {word_count}
- Sentence count: {sentence_count}
- Paragraph count: {paragraph_count}
- Average words per sentence: {avg_words_per_sentence:.1f}
- Average sentences per paragraph: {avg_sentences_per_paragraph:.1f}

Readability Assessment: {readability_score}

Quality Recommendations:
- Ideal sentence length: 15-20 words
- Ideal paragraph length: 2-4 sentences
- Use active voice for better engagement
- Include transition words between paragraphs
- Add bullet points and lists for easy scanning
- Include relevant examples and case studies
- End with clear takeaways or action items

Engagement Factors:
- Headlines should be compelling and specific
- Introduction should hook the reader immediately
- Use storytelling elements where appropriate
- Include data and statistics to support points
- Add quotes from experts or industry leaders
- Create clear value propositions for readers

Publication Standards:
- Ensure proper grammar and spelling
- Use consistent formatting throughout
- Include proper citations for sources
- Verify all facts and statistics
- Maintain consistent brand voice
- Optimize for target platform (Substack)"""
            
        except Exception as e:
            return f"Error analyzing content quality: {str(e)}"


class SubstackFormatterInput(BaseModel):
    """Input schema for SubstackFormatterTool."""
    content: str = Field(..., description="Content to format for Substack publication")


class SubstackFormatterTool(BaseTool):
    name: str = "Substack Formatter"
    description: str = (
        "Format content specifically for Substack publication including proper markdown, "
        "newsletter structure, and platform-specific optimizations."
    )
    args_schema: Type[BaseModel] = SubstackFormatterInput

    def _run(self, content: str) -> str:
        """Format content for Substack publication."""
        try:
            # Basic Substack formatting
            formatted_content = content
            
            # Ensure proper header formatting
            if not content.startswith('# '):
                # Add a placeholder title if none exists
                formatted_content = "# [Article Title Here]\n\n" + formatted_content
            
            # Add newsletter-specific elements
            newsletter_header = """*Welcome to [Newsletter Name] - delivering insights on [topic] directly to your inbox.*

---

"""
            
            newsletter_footer = """

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

*If you enjoyed this newsletter, consider sharing it with others who might benefit from these insights.*"""

            # Combine all elements
            final_content = newsletter_header + formatted_content + newsletter_footer
            
            return f"""Substack-Formatted Content:

{final_content}

Formatting Notes:
- Added newsletter header with branding
- Ensured proper markdown formatting
- Added engagement elements (feedback, sharing)
- Included newsletter footer with calls-to-action
- Optimized for email and web reading
- Added social sharing encouragement

Additional Substack Tips:
- Use compelling subject lines for email delivery
- Include preview text optimization
- Add relevant tags for discoverability
- Consider adding subscription incentives
- Use Substack's built-in features (polls, comments)
- Optimize publish timing for your audience"""
            
        except Exception as e:
            return f"Error formatting content for Substack: {str(e)}"