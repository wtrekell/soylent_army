#!/usr/bin/env python3
"""
AI Writing Process Analyzer
Analyzes text changes across writing stages to provide transparency metrics
"""

import difflib
import re
from collections import Counter
import statistics
import json
from datetime import datetime
import os

class WritingAnalyzer:
    def __init__(self):
        self.stages = {
            'stage2_draft': None,
            'stage3_refined': None,
            'stage4_edited': None,
            'stage5_final': None
        }
        
    def load_text_file(self, filepath, stage):
        """Load a text file for a specific stage"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.stages[stage] = f.read()
            print(f"✓ Loaded {stage}: {os.path.basename(filepath)}")
        except Exception as e:
            print(f"✗ Error loading {filepath}: {e}")
            
    def load_text_string(self, text, stage):
        """Load text directly as a string"""
        self.stages[stage] = text
        print(f"✓ Loaded {stage} from string input")
    
    def analyze_changes(self, text1, text2, stage_name):
        """Analyze changes between two versions of text"""
        if not text1 or not text2:
            return None
            
        # Tokenize into words
        words1 = re.findall(r'\b\w+\b', text1.lower())
        words2 = re.findall(r'\b\w+\b', text2.lower())
        
        # Sentence splitting
        sentences1 = re.split(r'[.!?]+', text1)
        sentences2 = re.split(r'[.!?]+', text2)
        
        # Calculate similarity using difflib
        seq_matcher = difflib.SequenceMatcher(None, text1, text2)
        similarity_ratio = seq_matcher.ratio()
        
        # Get actual changes
        changes = list(seq_matcher.get_opcodes())
        
        # Count changes by type
        insertions = sum(1 for tag, _, _, _, _ in changes if tag == 'insert')
        deletions = sum(1 for tag, _, _, _, _ in changes if tag == 'delete')
        replacements = sum(1 for tag, _, _, _, _ in changes if tag == 'replace')
        
        # Calculate word-level changes
        word_matcher = difflib.SequenceMatcher(None, words1, words2)
        word_changes = list(word_matcher.get_opcodes())
        
        added_words = []
        removed_words = []
        
        for tag, i1, i2, j1, j2 in word_changes:
            if tag == 'insert':
                added_words.extend(words2[j1:j2])
            elif tag == 'delete':
                removed_words.extend(words1[i1:i2])
            elif tag == 'replace':
                removed_words.extend(words1[i1:i2])
                added_words.extend(words2[j1:j2])
        
        # Semantic analysis - vocabulary changes
        vocab1 = set(words1)
        vocab2 = set(words2)
        new_vocabulary = vocab2 - vocab1
        removed_vocabulary = vocab1 - vocab2
        
        # Readability metrics
        avg_sentence_len1 = statistics.mean([len(s.split()) for s in sentences1 if s.strip()])
        avg_sentence_len2 = statistics.mean([len(s.split()) for s in sentences2 if s.strip()])
        
        # Structure analysis
        paragraphs1 = text1.split('\n\n')
        paragraphs2 = text2.split('\n\n')
        
        return {
            'stage': stage_name,
            'character_count': {
                'before': len(text1),
                'after': len(text2),
                'change': len(text2) - len(text1),
                'change_percent': ((len(text2) - len(text1)) / len(text1) * 100) if len(text1) > 0 else 0
            },
            'word_count': {
                'before': len(words1),
                'after': len(words2),
                'change': len(words2) - len(words1),
                'change_percent': ((len(words2) - len(words1)) / len(words1) * 100) if len(words1) > 0 else 0
            },
            'similarity_score': round(similarity_ratio * 100, 2),
            'change_operations': {
                'insertions': insertions,
                'deletions': deletions,
                'replacements': replacements,
                'total': insertions + deletions + replacements
            },
            'word_level_changes': {
                'added': len(added_words),
                'removed': len(removed_words),
                'most_added': Counter(added_words).most_common(5),
                'most_removed': Counter(removed_words).most_common(5)
            },
            'vocabulary': {
                'new_unique_words': len(new_vocabulary),
                'removed_unique_words': len(removed_vocabulary),
                'vocabulary_before': len(vocab1),
                'vocabulary_after': len(vocab2)
            },
            'structure': {
                'paragraphs_before': len([p for p in paragraphs1 if p.strip()]),
                'paragraphs_after': len([p for p in paragraphs2 if p.strip()]),
                'avg_sentence_length_before': round(avg_sentence_len1, 1),
                'avg_sentence_length_after': round(avg_sentence_len2, 1)
            }
        }
    
    def analyze_semantic_shift(self, text1, text2):
        """Analyze semantic changes between versions"""
        # Extract key themes (simplified - you could use more sophisticated NLP here)
        def extract_themes(text):
            words = re.findall(r'\b\w+\b', text.lower())
            # Filter out common words (simplified stopwords)
            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'been', 'be',
                        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
                        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their'}
            
            meaningful_words = [w for w in words if w not in stopwords and len(w) > 3]
            return Counter(meaningful_words).most_common(10)
        
        themes1 = extract_themes(text1)
        themes2 = extract_themes(text2)
        
        # Find theme shifts
        themes_dict1 = dict(themes1)
        themes_dict2 = dict(themes2)
        
        emerging_themes = [(word, count) for word, count in themes2 
                          if word not in themes_dict1 or themes_dict2[word] > themes_dict1.get(word, 0) * 1.5]
        
        diminishing_themes = [(word, themes_dict1[word]) for word, _ in themes1 
                             if word not in themes_dict2 or themes_dict1[word] > themes_dict2.get(word, 0) * 1.5]
        
        return {
            'top_themes_before': themes1[:5],
            'top_themes_after': themes2[:5],
            'emerging_themes': emerging_themes[:5],
            'diminishing_themes': diminishing_themes[:5]
        }
    
    def generate_report(self, project_name="Untitled"):
        """Generate comprehensive analysis report"""
        print("\n" + "="*60)
        print(f"AI WRITING PROCESS ANALYSIS REPORT")
        print(f"Project: {project_name}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        results = {
            'project': project_name,
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }
        
        # Analyze each transition
        transitions = [
            ('stage2_draft', 'stage3_refined', 'Stage 2→3: Draft to Refined'),
            ('stage3_refined', 'stage4_edited', 'Stage 3→4: Refined to Edited'),
            ('stage4_edited', 'stage5_final', 'Stage 4→5: Edited to Final')
        ]
        
        for before_key, after_key, label in transitions:
            if self.stages[before_key] and self.stages[after_key]:
                print(f"\n{label}")
                print("-" * len(label))
                
                analysis = self.analyze_changes(
                    self.stages[before_key], 
                    self.stages[after_key], 
                    label
                )
                
                semantic_shift = self.analyze_semantic_shift(
                    self.stages[before_key], 
                    self.stages[after_key]
                )
                
                analysis['semantic_shift'] = semantic_shift
                results['stages'][label] = analysis
                
                # Print summary
                print(f"Similarity: {analysis['similarity_score']}%")
                print(f"Word count: {analysis['word_count']['before']} → {analysis['word_count']['after']} ({analysis['word_count']['change_percent']:+.1f}%)")
                print(f"Changes: {analysis['change_operations']['total']} operations")
                print(f"New vocabulary: {analysis['vocabulary']['new_unique_words']} words")
                
                if semantic_shift['emerging_themes']:
                    print(f"Emerging themes: {', '.join([w for w, _ in semantic_shift['emerging_themes'][:3]])}")
        
        # Overall analysis
        if self.stages['stage2_draft'] and self.stages['stage5_final']:
            print("\n" + "="*60)
            print("OVERALL TRANSFORMATION (Draft → Final)")
            print("="*60)
            
            overall = self.analyze_changes(
                self.stages['stage2_draft'], 
                self.stages['stage5_final'], 
                'Overall'
            )
            
            results['overall'] = overall
            
            print(f"\nContent retention: {overall['similarity_score']}%")
            print(f"Word count change: {overall['word_count']['change_percent']:+.1f}%")
            print(f"Vocabulary expansion: {overall['vocabulary']['vocabulary_before']} → {overall['vocabulary']['vocabulary_after']} unique words")
            
            # AI contribution estimate
            ai_contribution = 100 - overall['similarity_score']
            print(f"\nEstimated AI contribution: ~{ai_contribution:.1f}% of content transformed")
            
            # Generate transparency statement
            print("\n" + "-"*60)
            print("SUGGESTED TRANSPARENCY STATEMENT:")
            print("-"*60)
            print(f"This article underwent AI-assisted editing across 4 stages. ")
            print(f"Analysis shows {overall['similarity_score']}% similarity between ")
            print(f"initial AI draft and final human-edited version, with ")
            print(f"{overall['word_count']['change_percent']:+.1f}% change in length and ")
            print(f"{overall['vocabulary']['new_unique_words']} new unique terms introduced.")
        
        # Save detailed results
        with open(f"{project_name}_analysis_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n✓ Detailed results saved to: {project_name}_analysis_results.json")
        
        return results

def main():
    """Main function for command-line usage"""
    print("AI Writing Process Analyzer")
    print("==========================\n")
    
    analyzer = WritingAnalyzer()
    
    # Get project name
    project_name = input("Enter project name: ").strip() or "Untitled"
    
    print("\nYou can either:")
    print("1. Load text files (one for each stage)")
    print("2. Paste text directly")
    
    method = input("\nChoose method (1 or 2): ").strip()
    
    stages = [
        ('stage2_draft', 'Stage 2 - Initial AI Draft'),
        ('stage3_refined', 'Stage 3 - AI-Refined Version'),
        ('stage4_edited', 'Stage 4 - Word Processor Edited'),
        ('stage5_final', 'Stage 5 - Final Human Edit')
    ]
    
    if method == '1':
        # File loading method
        for stage_key, stage_name in stages:
            filepath = input(f"\nPath to {stage_name} file (or press Enter to skip): ").strip()
            if filepath:
                analyzer.load_text_file(filepath, stage_key)
    else:
        # Direct paste method
        for stage_key, stage_name in stages:
            print(f"\nPaste {stage_name} (press Enter twice when done):")
            lines = []
            empty_count = 0
            while empty_count < 2:
                line = input()
                if not line:
                    empty_count += 1
                else:
                    empty_count = 0
                lines.append(line)
            
            text = '\n'.join(lines[:-2])  # Remove the two empty lines at the end
            if text.strip():
                analyzer.load_text_string(text, stage_key)
    
    # Generate report
    analyzer.generate_report(project_name)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()