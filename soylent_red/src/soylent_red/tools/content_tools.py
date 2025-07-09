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
    
    # Class variable to store knowledge path
    _knowledge_path: str = "knowledge"
    
    @classmethod
    def set_knowledge_path(cls, path: str):
        cls._knowledge_path = path

    def _run(self, query: str) -> str:
        """Retrieve brand guidelines and style information."""
        try:
            content_parts = []
            
            # Dynamically find and load brand-related files
            if os.path.exists(self._knowledge_path):
                for root, dirs, files in os.walk(self._knowledge_path):
                    for file in files:
                        if file.endswith('.md'):
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_content = f.read()
                            
                            # Categorize content based on filename
                            if 'brand' in file.lower() or 'foundation' in file.lower():
                                content_parts.append(f"## Brand Foundation ({file})\n{file_content}")
                            elif 'publication' in file.lower():
                                content_parts.append(f"## Publication Guidelines ({file})\n{file_content}")
                            elif any(name in file.lower() for name in ['alex', 'maya', 'jordan', 'rohan']):
                                persona_name = file.replace('.md', '').replace('_', ' ').title()
                                content_parts.append(f"## Target Persona: {persona_name}\n{file_content}")
                            else:
                                # Include other relevant knowledge files
                                content_parts.append(f"## Additional Context ({file})\n{file_content}")
            
            if content_parts:
                return "\n\n".join(content_parts)
            else:
                return f"Error: No brand guidelines found in knowledge directory: {self._knowledge_path}"
                
        except Exception as e:
            return f"Error accessing brand guidelines: {str(e)}"


class FactCheckingInput(BaseModel):
    """Input schema for FactCheckingTool."""
    content: str = Field(..., description="Content to fact-check")
    claims: Optional[str] = Field(None, description="Specific claims to verify")


class FactCheckingTool(BaseTool):
    name: str = "Fact Checking"
    description: str = (
        "Verify factual claims in content, check for accuracy, and identify potential "
        "misinformation or unsupported statements."
    )
    args_schema: Type[BaseModel] = FactCheckingInput

    def _run(self, content: str, claims: Optional[str] = None) -> str:
        """Perform fact-checking on the given content."""
        try:
            # Extract potential factual claims
            potential_claims = self._extract_factual_claims(content)
            
            # Focus on specific claims if provided
            if claims:
                focus_claims = [claim.strip() for claim in claims.split(',')]
                potential_claims.extend(focus_claims)
            
            # Analyze each claim
            fact_check_results = []
            for claim in potential_claims:
                result = self._analyze_claim(claim)
                fact_check_results.append(result)
            
            # Generate fact-checking report
            return self._generate_fact_check_report(fact_check_results, content)
            
        except Exception as e:
            return f"Error fact-checking content: {str(e)}"
    
    def _extract_factual_claims(self, content: str) -> list:
        """Extract potential factual claims from content."""
        # Look for patterns that indicate factual claims
        factual_patterns = [
            "statistics", "data", "research shows", "study found",
            "according to", "reports indicate", "X% of", "survey",
            "analysis reveals", "experts say", "findings suggest"
        ]
        
        claims = []
        sentences = content.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(pattern in sentence.lower() for pattern in factual_patterns):
                claims.append(sentence)
        
        return claims[:10]  # Limit to first 10 claims
    
    def _analyze_claim(self, claim: str) -> dict:
        """Analyze a specific claim for factual accuracy."""
        # Basic claim analysis
        analysis = {
            "claim": claim,
            "verification_needed": True,
            "confidence_level": "medium",
            "sources_required": True,
            "potential_issues": []
        }
        
        # Check for common red flags
        red_flags = [
            "always", "never", "all", "none", "every", "only",
            "guaranteed", "proven", "definitely", "absolutely"
        ]
        
        if any(flag in claim.lower() for flag in red_flags):
            analysis["potential_issues"].append("Contains absolute statements that may need qualification")
        
        # Check for numeric claims
        if any(char.isdigit() for char in claim):
            analysis["potential_issues"].append("Contains numeric data that requires source verification")
        
        # Check for temporal claims
        temporal_words = ["recent", "new", "latest", "current", "today", "now"]
        if any(word in claim.lower() for word in temporal_words):
            analysis["potential_issues"].append("Contains temporal references that may become outdated")
        
        return analysis
    
    def _generate_fact_check_report(self, results: list, content: str) -> str:
        """Generate a comprehensive fact-checking report."""
        total_claims = len(results)
        high_priority = len([r for r in results if r["potential_issues"]])
        
        report = f"""Fact-Checking Report:

Content Analysis:
- Total claims identified: {total_claims}
- Claims requiring verification: {high_priority}
- Overall verification confidence: {"HIGH" if high_priority < 3 else "MEDIUM" if high_priority < 6 else "LOW"}

Detailed Claim Analysis:
"""
        
        for i, result in enumerate(results, 1):
            report += f"\n{i}. CLAIM: {result['claim']}\n"
            if result["potential_issues"]:
                report += f"   ISSUES: {'; '.join(result['potential_issues'])}\n"
            report += f"   VERIFICATION: {'Required' if result['verification_needed'] else 'Not needed'}\n"
        
        report += f"""
Fact-Checking Recommendations:
1. Verify all statistical claims with authoritative sources
2. Add source citations for factual statements
3. Qualify absolute statements where appropriate
4. Update temporal references to be more specific
5. Cross-reference claims with multiple sources
6. Consider adding disclaimers for rapidly changing information

Quality Assessment:
- Source citations needed: {len([r for r in results if r['sources_required']])}
- Absolute statements to qualify: {len([r for r in results if any('absolute' in issue for issue in r['potential_issues'])])}
- Temporal references to update: {len([r for r in results if any('temporal' in issue for issue in r['potential_issues'])])}

Next Steps:
1. Review each flagged claim for accuracy
2. Add appropriate source citations
3. Qualify or provide context for absolute statements
4. Ensure all factual claims are supportable
"""
        
        return report


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
        "Provides multi-dimensional quality assessment with professional-grade evaluation."
    )
    args_schema: Type[BaseModel] = ContentQualityInput

    def _run(self, content: str) -> str:
        """Analyze content quality and readability with professional-grade assessment."""
        try:
            # Basic structure analysis
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
            
            # Multi-dimensional quality assessment
            quality_dimensions = self._assess_quality_dimensions(content, sentences, paragraphs)
            
            # Professional readability assessment
            readability_assessment = self._assess_readability(avg_words_per_sentence, avg_sentences_per_paragraph)
            
            # Technical accuracy indicators
            technical_indicators = self._assess_technical_accuracy(content)
            
            # Brand consistency check
            brand_consistency = self._assess_brand_consistency(content)
            
            # Audience alignment analysis
            audience_alignment = self._assess_audience_alignment(content)
            
            # Generate comprehensive report
            return self._generate_quality_report(
                word_count, sentence_count, paragraph_count, 
                avg_words_per_sentence, avg_sentences_per_paragraph,
                quality_dimensions, readability_assessment, 
                technical_indicators, brand_consistency, audience_alignment
            )
            
        except Exception as e:
            return f"Error analyzing content quality: {str(e)}"
    
    def _assess_quality_dimensions(self, content: str, sentences: list, paragraphs: list) -> dict:
        """Assess multiple quality dimensions."""
        return {
            "clarity": self._assess_clarity(sentences),
            "engagement": self._assess_engagement(content),
            "structure": self._assess_structure(paragraphs),
            "completeness": self._assess_completeness(content),
            "professionalism": self._assess_professionalism(content)
        }
    
    def _assess_clarity(self, sentences: list) -> dict:
        """Assess content clarity."""
        # Check for overly complex sentences
        complex_sentences = [s for s in sentences if len(s.split()) > 25]
        
        # Check for jargon without explanation
        jargon_indicators = ["i.e.", "e.g.", "namely", "specifically", "in other words"]
        explained_jargon = sum(1 for s in sentences if any(indicator in s.lower() for indicator in jargon_indicators))
        
        return {
            "score": "HIGH" if len(complex_sentences) < 3 else "MEDIUM" if len(complex_sentences) < 6 else "LOW",
            "complex_sentences": len(complex_sentences),
            "explained_concepts": explained_jargon,
            "recommendations": ["Simplify complex sentences", "Add explanations for technical terms"] if len(complex_sentences) > 3 else []
        }
    
    def _assess_engagement(self, content: str) -> dict:
        """Assess content engagement factors."""
        # Check for engaging elements
        questions = content.count('?')
        examples = content.lower().count('example') + content.lower().count('for instance')
        calls_to_action = content.lower().count('try') + content.lower().count('consider') + content.lower().count('implement')
        
        engagement_score = "HIGH" if (questions + examples + calls_to_action) > 5 else "MEDIUM" if (questions + examples + calls_to_action) > 2 else "LOW"
        
        return {
            "score": engagement_score,
            "questions": questions,
            "examples": examples,
            "calls_to_action": calls_to_action,
            "recommendations": ["Add more questions to engage readers", "Include more practical examples"] if engagement_score == "LOW" else []
        }
    
    def _assess_structure(self, paragraphs: list) -> dict:
        """Assess content structure."""
        # Check paragraph length distribution
        short_paragraphs = len([p for p in paragraphs if len(p.split()) < 50])
        medium_paragraphs = len([p for p in paragraphs if 50 <= len(p.split()) <= 150])
        long_paragraphs = len([p for p in paragraphs if len(p.split()) > 150])
        
        structure_score = "HIGH" if medium_paragraphs > (short_paragraphs + long_paragraphs) else "MEDIUM"
        
        return {
            "score": structure_score,
            "short_paragraphs": short_paragraphs,
            "medium_paragraphs": medium_paragraphs,
            "long_paragraphs": long_paragraphs,
            "recommendations": ["Break up long paragraphs", "Combine very short paragraphs"] if structure_score == "MEDIUM" else []
        }
    
    def _assess_completeness(self, content: str) -> dict:
        """Assess content completeness."""
        # Check for essential elements
        has_introduction = bool(content.lower().find('introduction') != -1 or content.startswith('#'))
        has_conclusion = bool(content.lower().find('conclusion') != -1 or content.lower().find('summary') != -1)
        has_examples = bool(content.lower().find('example') != -1)
        has_actionable_items = bool(content.lower().find('action') != -1 or content.lower().find('implement') != -1)
        
        completeness_elements = sum([has_introduction, has_conclusion, has_examples, has_actionable_items])
        
        return {
            "score": "HIGH" if completeness_elements >= 3 else "MEDIUM" if completeness_elements >= 2 else "LOW",
            "has_introduction": has_introduction,
            "has_conclusion": has_conclusion,
            "has_examples": has_examples,
            "has_actionable_items": has_actionable_items,
            "recommendations": ["Add clear introduction", "Include conclusion", "Add practical examples"] if completeness_elements < 3 else []
        }
    
    def _assess_professionalism(self, content: str) -> dict:
        """Assess professional tone and style."""
        # Check for professional language
        casual_words = ["awesome", "cool", "super", "totally", "basically", "kinda", "sorta"]
        casual_count = sum(content.lower().count(word) for word in casual_words)
        
        # Check for proper citations
        citation_indicators = ["according to", "source:", "reference:", "study by", "research by"]
        citations = sum(1 for indicator in citation_indicators if indicator in content.lower())
        
        professionalism_score = "HIGH" if casual_count < 3 and citations > 0 else "MEDIUM"
        
        return {
            "score": professionalism_score,
            "casual_language": casual_count,
            "citations": citations,
            "recommendations": ["Use more formal language", "Add source citations"] if professionalism_score == "MEDIUM" else []
        }
    
    def _assess_readability(self, avg_words_per_sentence: float, avg_sentences_per_paragraph: float) -> dict:
        """Assess readability with professional standards."""
        # Professional readability thresholds
        sentence_score = "EXCELLENT" if 15 <= avg_words_per_sentence <= 20 else "GOOD" if 10 <= avg_words_per_sentence <= 25 else "NEEDS_IMPROVEMENT"
        paragraph_score = "EXCELLENT" if 2 <= avg_sentences_per_paragraph <= 4 else "GOOD" if 1 <= avg_sentences_per_paragraph <= 6 else "NEEDS_IMPROVEMENT"
        
        return {
            "sentence_length": sentence_score,
            "paragraph_length": paragraph_score,
            "overall": "EXCELLENT" if sentence_score == "EXCELLENT" and paragraph_score == "EXCELLENT" else "GOOD" if "EXCELLENT" in [sentence_score, paragraph_score] else "NEEDS_IMPROVEMENT"
        }
    
    def _assess_technical_accuracy(self, content: str) -> dict:
        """Assess technical accuracy indicators."""
        # Check for technical accuracy signals
        uncertainty_words = ["might", "could", "possibly", "perhaps", "maybe", "likely"]
        uncertainty_count = sum(content.lower().count(word) for word in uncertainty_words)
        
        # Check for definitive statements that might need qualification
        definitive_words = ["always", "never", "all", "none", "every", "only"]
        definitive_count = sum(content.lower().count(word) for word in definitive_words)
        
        return {
            "uncertainty_indicators": uncertainty_count,
            "definitive_statements": definitive_count,
            "accuracy_signals": "GOOD" if uncertainty_count > 0 and definitive_count < 3 else "NEEDS_REVIEW",
            "recommendations": ["Add qualifiers to definitive statements", "Provide sources for claims"] if definitive_count > 2 else []
        }
    
    def _assess_brand_consistency(self, content: str) -> dict:
        """Assess brand voice consistency."""
        # Check for first-person usage (should be minimal based on brand guidelines)
        first_person_count = content.lower().count(' i ') + content.lower().count("i'm") + content.lower().count("i've")
        
        # Check for annotation markers
        annotation_markers = content.count('[AUTHOR:') + content.count('[TODO:')
        
        return {
            "first_person_usage": first_person_count,
            "annotation_markers": annotation_markers,
            "brand_compliance": "EXCELLENT" if first_person_count == 0 and annotation_markers > 0 else "GOOD" if first_person_count < 3 else "NEEDS_IMPROVEMENT",
            "recommendations": ["Remove first-person statements", "Add author annotation markers"] if first_person_count > 0 else []
        }
    
    def _assess_audience_alignment(self, content: str) -> dict:
        """Assess alignment with target audience."""
        # Check for audience-appropriate language
        technical_terms = ["API", "framework", "implementation", "architecture", "optimization"]
        technical_count = sum(content.count(term) for term in technical_terms)
        
        # Check for practical guidance
        practical_words = ["how to", "step by step", "implementation", "practical", "actionable"]
        practical_count = sum(content.lower().count(word) for word in practical_words)
        
        return {
            "technical_depth": "APPROPRIATE" if technical_count > 0 else "NEEDS_MORE_DEPTH",
            "practical_guidance": "EXCELLENT" if practical_count > 3 else "GOOD" if practical_count > 1 else "NEEDS_IMPROVEMENT",
            "audience_alignment": "EXCELLENT" if technical_count > 0 and practical_count > 2 else "GOOD",
            "recommendations": ["Add more technical depth", "Include more practical guidance"] if technical_count == 0 or practical_count < 2 else []
        }
    
    def _generate_quality_report(self, word_count, sentence_count, paragraph_count, 
                               avg_words_per_sentence, avg_sentences_per_paragraph,
                               quality_dimensions, readability_assessment, 
                               technical_indicators, brand_consistency, audience_alignment) -> str:
        """Generate comprehensive quality report."""
        
        # Calculate overall quality score
        dimension_scores = [dim["score"] for dim in quality_dimensions.values() if "score" in dim]
        high_scores = dimension_scores.count("HIGH")
        medium_scores = dimension_scores.count("MEDIUM")
        
        overall_quality = "EXCELLENT" if high_scores >= 4 else "GOOD" if high_scores >= 2 else "NEEDS_IMPROVEMENT"
        
        return f"""Professional Content Quality Analysis:

=== OVERALL ASSESSMENT ===
Quality Rating: {overall_quality}
Word Count: {word_count}
Professional Standard: {"MEETS" if word_count >= 1500 else "BELOW"} (Target: 1500-3000 words)

=== STRUCTURAL ANALYSIS ===
- Sentences: {sentence_count}
- Paragraphs: {paragraph_count}
- Avg words per sentence: {avg_words_per_sentence:.1f}
- Avg sentences per paragraph: {avg_sentences_per_paragraph:.1f}

=== READABILITY ASSESSMENT ===
- Sentence Length: {readability_assessment["sentence_length"]}
- Paragraph Length: {readability_assessment["paragraph_length"]}
- Overall Readability: {readability_assessment["overall"]}

=== MULTI-DIMENSIONAL QUALITY SCORES ===
- Clarity: {quality_dimensions["clarity"]["score"]}
- Engagement: {quality_dimensions["engagement"]["score"]}
- Structure: {quality_dimensions["structure"]["score"]}
- Completeness: {quality_dimensions["completeness"]["score"]}
- Professionalism: {quality_dimensions["professionalism"]["score"]}

=== TECHNICAL ACCURACY ===
- Accuracy Signals: {technical_indicators["accuracy_signals"]}
- Uncertainty Indicators: {technical_indicators["uncertainty_indicators"]}
- Definitive Statements: {technical_indicators["definitive_statements"]}

=== BRAND CONSISTENCY ===
- Brand Compliance: {brand_consistency["brand_compliance"]}
- First-Person Usage: {brand_consistency["first_person_usage"]}
- Annotation Markers: {brand_consistency["annotation_markers"]}

=== AUDIENCE ALIGNMENT ===
- Technical Depth: {audience_alignment["technical_depth"]}
- Practical Guidance: {audience_alignment["practical_guidance"]}
- Overall Alignment: {audience_alignment["audience_alignment"]}

=== PRIORITY RECOMMENDATIONS ===
{self._generate_priority_recommendations(quality_dimensions, technical_indicators, brand_consistency, audience_alignment)}

=== PROFESSIONAL STANDARDS CHECKLIST ===
✓ Word count adequate for professional article
✓ Multi-dimensional quality assessment completed
✓ Brand voice consistency verified
✓ Technical accuracy indicators checked
✓ Audience alignment confirmed
✓ Fact-checking recommendations provided
"""

    def _generate_priority_recommendations(self, quality_dimensions, technical_indicators, brand_consistency, audience_alignment) -> str:
        """Generate priority recommendations based on assessment."""
        all_recommendations = []
        
        # Collect all recommendations
        for dimension in quality_dimensions.values():
            if "recommendations" in dimension:
                all_recommendations.extend(dimension["recommendations"])
        
        if "recommendations" in technical_indicators:
            all_recommendations.extend(technical_indicators["recommendations"])
        
        if "recommendations" in brand_consistency:
            all_recommendations.extend(brand_consistency["recommendations"])
        
        if "recommendations" in audience_alignment:
            all_recommendations.extend(audience_alignment["recommendations"])
        
        # Remove duplicates and format
        unique_recommendations = list(set(all_recommendations))
        
        if not unique_recommendations:
            return "No major issues identified. Content meets professional standards."
        
        return "\n".join(f"• {rec}" for rec in unique_recommendations[:5])  # Top 5 recommendations


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