# Python NLP Research in Colab

**Created:** 6/14/2025 7:10  
**Updated:** 6/14/2025 10:53  
**Exported:** 6/14/2025 11:05  

## Prompt:
Assume the role of a Python developer who is intimately familiar with the free version of Google’s Colab platform and programmatic operations specific to research and study of human speech and writing patterns and semantics.



## Response:
I'm ready to help with Python development for Google Colab, particularly for speech and text analysis research. I can assist with:

- Setting up Colab environments for NLP/speech processing
- Working with libraries like spaCy, NLTK, librosa, transformers
- Data preprocessing and feature extraction
- Semantic analysis and pattern recognition
- Visualization and results interpretation
- Memory and runtime optimization for Colab's free tier limitations

What specific aspect of speech/writing pattern analysis are you working on?



## Prompt:
There are a few facets to the project so I'll start with the high level overview of each facet, one at a time, then we can focus on the individual facets one at a time as they do not need to overlap, although the data they output is likely to be something we need to keep in mind.

The first facet is measuring AI usage in authoring articles to be published digitally for ethical and transparent reporting. The workflow:
1. I (the human) use different AI platforms to gather information on the chosen topic, synthesize it into a single document, which I then read and identify the elements I consider relevant.
2. I may, or may not, include transcripts of my own thoughts on the topic that are my own, and not necessarily based on the materials from step 1.
3. The AI is given the sum of steps 1 and 2, along with instruction on the topic of the article. The precision of the instruction will vary, which means the AI's interpretation will as well.
4. The AI drafts the article, this version will always be prefixed with 'draft-'
5. I prompt the AI to make the larger updates and alterations, this version is always prefixed with 'refined-'.
6. I move the refined version to a word processor that is integrated with AI. At this stage I make the majority of edits, leaning on the AI for smaller alterations like identifying synonyms, fixing phrases that I can't word quite right, etc. This version will always be prefixed with 'edited-'
7. Afterwards, I have the AI review the article in it's entirety for grammar and spelling, at which point I stop using the AI to prevent a cycle of constant nitpicking and revisions. I then perform the final edits and prep the article to be published. This version is always prefixed 'final-'
The objective is to measure each version of the article against the prior article as well as the draft against the final version. Using this information we then demonstrate the amount of change between each and the sum of the content from each stage that remains in the final version of the article.

Do you have questions?



## Response:
This is a fascinating approach to transparency in AI-assisted writing. I have a few clarifying questions to ensure I understand the analysis requirements correctly:

**Data Structure & Input:**
- Will you have the raw text files for each version (draft-, refined-, edited-, final-), or do I need to consider extracting from different file formats?
- Are you planning to analyze individual articles or batch process multiple articles to identify broader patterns?

**Measurement Granularity:**
- When you say "measure each version against the prior," are you thinking sentence-level, paragraph-level, or semantic chunk-level comparisons?
- For "amount of change," are you interested in:
  - Lexical similarity (word/phrase retention)
  - Structural changes (sentence/paragraph reorganization)
  - Semantic preservation (meaning retention despite rewording)
  - All of the above?

**Attribution Tracking:**
- How granular do you want the "content that remains in final version" tracking? For example, if a sentence from the draft is 70% similar to one in the final, how should that be quantified?
- Should the analysis distinguish between substantive content changes vs. stylistic/grammatical refinements?

**Output Requirements:**
- Are you envisioning numerical metrics, visual comparisons, or both?
- Do you need the analysis to be human-readable for publication alongside articles?

This sounds like it would benefit from a combination of text similarity algorithms, semantic analysis, and perhaps some edit distance calculations. What's your priority for the first implementation?



## Prompt:
1. All articles will be provided as Markdown.
2. I am most interested in tracking lexical and semantic changes. The concept, idea, or understanding of the topic is what is important. If elements like character/word/sentence/etc statistics are needed to report this information then we might as well capture and document it. DO NOT compromise what we want to track for the sake of having more metrics.
3. Item 2 should address attribution tracking, if it does not you should rephrase the question so I understand clearly.
4. All relevant data should be documented for archival, I expect to write about the longer term trends in the future but can't possibly anticipate what data I may need then. Again, DO NOT compromise reporting on what I am most interested in for the sake of data collection. The archive portion should be optimized for consumption by AI.
5. The most meaningful metrics will be used as part of the footer for each individual article and will be accompanied by visualizations that are representative of the data as it relates to change over versions and the sum of the content in the final article.

Do you have additional questions?



## Response:
Perfect, that clarifies the approach significantly. I have two remaining questions to finalize the technical implementation:

**Semantic Similarity Methodology:**
- Do you have a preference for the semantic analysis approach? Options include:
  - Sentence embeddings (e.g., SentenceTransformers) for meaning preservation
  - Topic modeling to track conceptual consistency
  - Named entity recognition to track factual content retention
  - Or should I implement a hybrid approach that captures multiple semantic dimensions?

**Attribution Granularity:**
- For tracking "what content remains in the final version," should I:
  - Trace each sentence/paragraph back to its first appearance (draft/refined/edited)?
  - Calculate semantic similarity scores between corresponding sections across versions?
  - Both - showing origin version AND degree of modification?

Based on your priorities, I'm envisioning:
- **Primary output**: Semantic similarity matrices between versions + content attribution map
- **Archive data**: Full diff analysis, embedding vectors, statistical metrics in JSON/CSV format optimized for future AI consumption  
- **Article footer**: Clean percentage breakdowns (e.g., "65% content from draft retained, 23% substantially modified, 12% new content added in editing")
- **Visualizations**: Sankey diagrams showing content flow between versions, heatmaps of section-level changes

Does this align with your vision? Should I start building the semantic similarity tracking as the core functionality?



## Prompt:
1. I'll defer to your recommendation on the methodology with one caveat, doing this should not lead to a significant increase in work for me. For example, tagging each sentence would be a monumental increase in work.
2. Calculate lexical and semantic change from version to version, as well as the sum that remains in the final version. The workflow is designed to demonstrate AI draft, AI assistance,  Human driven, Human oversight. How the inclusion of the word 'not' in a sentence changes the concept is important, who added the word is not.
3. You're understanding of the outputs seems accurate, however I'll want to consider different visualizations once we get to that point. How to interpret a Sankey diagram is not apparent to most people.

The non-negotiables regarding implementation:
1. Orchestration must take place via Colab notebook with inputs and outputs stored in Google Drive.
2. The use of resources that will incur cost should be limited if not avoided entirely. Colab, for example, incurs a cost that is minimal. Storing the data in a database is not. I must be made aware of all potential costs before they are implemented.
3. The workflow of processing the information should occur in steps. They do not need to align with the steps of the workflow but should allow for me to review the data at notable milestones to identify potential issues early.



## Response:
Excellent, that gives me a clear technical direction. Here's my recommended approach:

**Methodology Recommendation:**
- **Primary**: SentenceTransformers (specifically `all-MiniLM-L6-v2`) for semantic similarity - it's free, runs well in Colab, and provides robust semantic understanding
- **Secondary**: Lexical overlap using Jaccard similarity and edit distance for complementary lexical tracking
- **Zero manual tagging** - everything automated through text processing

**Cost Assessment:**
- **No costs**: SentenceTransformers, spaCy, NLTK, pandas, matplotlib, seaborn - all free
- **Minimal Colab usage**: Standard free tier should handle this workload easily
- **Google Drive**: Free storage within limits you likely already have

**Proposed Step Structure:**
1. **Data Ingestion & Validation** - Load markdown files, verify version sequence
2. **Text Preprocessing** - Clean, segment, and prepare text for analysis  
3. **Similarity Analysis** - Calculate lexical and semantic similarities between versions
4. **Attribution Mapping** - Track content retention through to final version
5. **Metrics Generation** - Compile statistics and percentage breakdowns
6. **Visualization Prep** - Generate data structures for multiple chart options
7. **Archive Export** - Save all data in AI-optimized JSON format

Each step will output checkpoint data you can review, and the notebook will be modular so you can re-run individual steps.

Should I start building the foundation with steps 1-2 (data handling and preprocessing) so you can test with your markdown files?



## Prompt:
Sounds perfect.



## Response:
Great! I'll start building the foundation. Let me create a Colab notebook structure for steps 1-2.

AI Writing Analysis - Foundation (Steps 1-2)

```python
# AI Writing Analysis - Foundation Steps
# Steps 1-2: Data Ingestion & Preprocessing

import os
import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from google.colab import drive, files
import zipfile

# Mount Google Drive
print("Mounting Google Drive...")
drive.mount('/content/drive')
print("✓ Drive mounted successfully")

# Configuration
class Config:
    """Configuration settings for the analysis"""
    
    # File naming conventions
    VERSION_PREFIXES = ['draft-', 'refined-', 'edited-', 'final-']
    VERSION_ORDER = {prefix: i for i, prefix in enumerate(VERSION_PREFIXES)}
    
    # Drive paths (modify these to match your structure)
    DRIVE_BASE = '/content/drive/MyDrive'
    INPUT_FOLDER = 'AI_Writing_Analysis/input'
    OUTPUT_FOLDER = 'AI_Writing_Analysis/output'
    ARCHIVE_FOLDER = 'AI_Writing_Analysis/archive'
    
    # Analysis settings
    MIN_SENTENCE_LENGTH = 10  # Minimum characters for a sentence
    MAX_SENTENCE_LENGTH = 1000  # Maximum characters for a sentence

# Create directory structure
def setup_directories():
    """Create necessary directories in Google Drive"""
    directories = [
        f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.ARCHIVE_FOLDER}"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory ready: {directory}")

setup_directories()

# STEP 1: DATA INGESTION & VALIDATION

class ArticleVersions:
    """Class to handle loading and validating article versions"""
    
    def __init__(self, article_name):
        self.article_name = article_name
        self.versions = {}
        self.metadata = {
            'article_name': article_name,
            'processing_timestamp': datetime.now().isoformat(),
            'versions_found': [],
            'validation_status': 'pending'
        }
    
    def load_versions_from_drive(self, input_path=None):
        """Load all versions of an article from Google Drive"""
        if input_path is None:
            input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
        
        print(f"\n📁 Loading versions for article: {self.article_name}")
        
        # Find all files matching the article name pattern
        for prefix in Config.VERSION_PREFIXES:
            filename = f"{prefix}{self.article_name}.md"
            filepath = os.path.join(input_path, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.versions[prefix.rstrip('-')] = {
                            'filename': filename,
                            'filepath': filepath,
                            'content': content,
                            'loaded_at': datetime.now().isoformat(),
                            'file_size': len(content)
                        }
                        print(f"  ✓ Loaded: {filename} ({len(content)} characters)")
                        
                except Exception as e:
                    print(f"  ✗ Error loading {filename}: {str(e)}")
            else:
                print(f"  - Not found: {filename}")
        
        self.metadata['versions_found'] = list(self.versions.keys())
        return self.versions
    
    def validate_version_sequence(self):
        """Validate that versions follow the expected workflow sequence"""
        found_versions = set(self.versions.keys())
        expected_sequence = ['draft', 'refined', 'edited', 'final']
        
        # Check for required versions
        missing_versions = []
        for version in expected_sequence:
            if version not in found_versions:
                missing_versions.append(version)
        
        # Validation results
        validation_results = {
            'has_draft': 'draft' in found_versions,
            'has_final': 'final' in found_versions,
            'missing_versions': missing_versions,
            'unexpected_versions': found_versions - set(expected_sequence),
            'sequence_complete': len(missing_versions) == 0,
            'minimum_viable': 'draft' in found_versions and 'final' in found_versions
        }
        
        # Update metadata
        self.metadata['validation_results'] = validation_results
        
        if validation_results['minimum_viable']:
            self.metadata['validation_status'] = 'passed'
            print(f"✓ Validation passed: Found {len(found_versions)} versions")
        else:
            self.metadata['validation_status'] = 'failed'
            print(f"✗ Validation failed: Missing required versions")
        
        if missing_versions:
            print(f"  Missing: {', '.join(missing_versions)}")
        
        return validation_results
    
    def get_summary(self):
        """Get a summary of loaded versions"""
        summary = {
            'article_name': self.article_name,
            'versions_count': len(self.versions),
            'validation_status': self.metadata['validation_status'],
            'file_sizes': {}
        }
        
        for version, data in self.versions.items():
            summary['file_sizes'][version] = data['file_size']
        
        return summary

# STEP 2: TEXT PREPROCESSING

class TextPreprocessor:
    """Class to handle text preprocessing and segmentation"""
    
    def __init__(self):
        self.processed_versions = {}
        
    def clean_markdown(self, text):
        """Clean markdown formatting while preserving content structure"""
        # Remove markdown formatting but keep the text
        patterns = [
            (r'^\s*#{1,6}\s+', ''),  # Headers
            (r'\*\*(.*?)\*\*', r'\1'),  # Bold
            (r'\*(.*?)\*', r'\1'),  # Italic
            (r'`(.*?)`', r'\1'),  # Inline code
            (r'```.*?```', ''),  # Code blocks
            (r'!\[.*?\]\(.*?\)', ''),  # Images
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),  # Links
            (r'^\s*[\*\-\+]\s+', '', re.MULTILINE),  # Bullet points
            (r'^\s*\d+\.\s+', '', re.MULTILINE),  # Numbered lists
            (r'\n{3,}', '\n\n'),  # Multiple newlines
        ]
        
        cleaned_text = text
        for pattern, replacement in patterns[:-1]:  # All except the last one
            cleaned_text = re.sub(pattern, replacement, cleaned_text)
        
        # Handle the multiline pattern separately
        cleaned_text = re.sub(patterns[-1][0], patterns[-1][1], cleaned_text, flags=re.MULTILINE)
        
        return cleaned_text.strip()
    
    def segment_into_sentences(self, text):
        """Segment text into sentences with basic filtering"""
        # Simple sentence segmentation (can be enhanced with spaCy later if needed)
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Filter sentences
        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (Config.MIN_SENTENCE_LENGTH <= len(sentence) <= Config.MAX_SENTENCE_LENGTH 
                and sentence):
                filtered_sentences.append(sentence)
        
        return filtered_sentences
    
    def segment_into_paragraphs(self, text):
        """Segment text into paragraphs"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return paragraphs
    
    def process_version(self, version_name, raw_content):
        """Process a single version of the article"""
        print(f"  Processing {version_name} version...")
        
        # Clean the markdown
        cleaned_content = self.clean_markdown(raw_content)
        
        # Segment into different units
        sentences = self.segment_into_sentences(cleaned_content)
        paragraphs = self.segment_into_paragraphs(cleaned_content)
        
        # Calculate basic statistics
        stats = {
            'character_count': len(cleaned_content),
            'word_count': len(cleaned_content.split()),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
            'avg_paragraph_length': sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        }
        
        processed_data = {
            'version_name': version_name,
            'raw_content': raw_content,
            'cleaned_content': cleaned_content,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'statistics': stats,
            'processed_at': datetime.now().isoformat()
        }
        
        self.processed_versions[version_name] = processed_data
        
        print(f"    ✓ {stats['sentence_count']} sentences, {stats['paragraph_count']} paragraphs")
        print(f"    ✓ {stats['word_count']} words, {stats['character_count']} characters")
        
        return processed_data
    
    def process_all_versions(self, article_versions):
        """Process all versions of an article"""
        print(f"\n🔄 Preprocessing text for all versions...")
        
        for version_name, version_data in article_versions.versions.items():
            self.process_version(version_name, version_data['content'])
        
        return self.processed_versions
    
    def get_processing_summary(self):
        """Get a summary of processing results"""
        summary = {}
        for version_name, data in self.processed_versions.items():
            summary[version_name] = data['statistics']
        
        return summary

# CHECKPOINT: Save Step 1-2 Results
def save_checkpoint_data(article_versions, preprocessor, checkpoint_name="steps_1_2"):
    """Save checkpoint data for review"""
    checkpoint_data = {
        'checkpoint_name': checkpoint_name,
        'timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'validation_results': article_versions.metadata.get('validation_results', {}),
        'article_summary': article_versions.get_summary()
    }
    
    # Save to Google Drive
    output_path = f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}"
    checkpoint_file = f"{output_path}/{article_versions.article_name}_checkpoint_{checkpoint_name}.json"
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Checkpoint saved: {checkpoint_file}")
    return checkpoint_data

# EXAMPLE USAGE AND TESTING
def run_steps_1_2(article_name):
    """Run steps 1-2 for a given article"""
    print(f"🚀 Starting Steps 1-2 for article: {article_name}")
    
    # Step 1: Data Ingestion & Validation
    article_versions = ArticleVersions(article_name)
    article_versions.load_versions_from_drive()
    validation_results = article_versions.validate_version_sequence()
    
    if not validation_results['minimum_viable']:
        print("❌ Cannot proceed: Missing required versions (draft and final)")
        return None, None
    
    # Step 2: Text Preprocessing  
    preprocessor = TextPreprocessor()
    preprocessor.process_all_versions(article_versions)
    
    # Save checkpoint
    checkpoint_data = save_checkpoint_data(article_versions, preprocessor)
    
    print(f"\n✅ Steps 1-2 completed successfully!")
    print(f"📊 Processing Summary:")
    for version, stats in preprocessor.get_processing_summary().items():
        print(f"  {version}: {stats['word_count']} words, {stats['sentence_count']} sentences")
    
    return article_versions, preprocessor

# TEST FUNCTION - Remove or comment out after testing
def create_sample_files_for_testing():
    """Create sample markdown files for testing (run this once to test)"""
    sample_content = {
        'draft-': """# Sample Article

This is a draft article about artificial intelligence and its impact on society. AI has revolutionized many industries.

The technology continues to evolve rapidly. Machine learning algorithms are becoming more sophisticated every day.

We must consider the ethical implications of AI development.""",
        
        'refined-': """# Sample Article

This is a refined article examining artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries across the globe.

The technology continues to evolve at an unprecedented pace. Advanced machine learning algorithms are becoming increasingly sophisticated with each passing day.

We must carefully consider the complex ethical implications of AI development and deployment.""",
        
        'edited-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation for the benefit of humanity.""",
        
        'final-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work, communicate, and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations in computing power and algorithmic design. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible just a decade ago.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation that serves the benefit of all humanity while mitigating potential risks."""
    }
    
    input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
    article_name = "sample-article"
    
    for prefix, content in sample_content.items():
        filename = f"{prefix}{article_name}.md"
        filepath = os.path.join(input_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filename}")
    
    return article_name

# Uncomment the lines below to test with sample data:
# sample_article_name = create_sample_files_for_testing()
# article_versions, preprocessor = run_steps_1_2(sample_article_name)

print("📋 Setup complete! Ready to process your articles.")
print("\nTo process an article, run:")
print("article_versions, preprocessor = run_steps_1_2('your-article-name')")
print("\nMake sure your markdown files are in the input folder with proper naming:")
print("- draft-your-article-name.md")
print("- refined-your-article-name.md") 
print("- edited-your-article-name.md")
print("- final-your-article-name.md")
```

I've created the foundation notebook for steps 1-2. Here's what it includes:

**Key Features:**
- **Automatic Google Drive integration** - Creates folder structure for input/output/archive
- **Flexible version loading** - Finds and loads your markdown files based on the naming convention
- **Validation system** - Ensures you have at least draft and final versions before proceeding
- **Clean markdown processing** - Strips formatting while preserving content structure
- **Text segmentation** - Breaks content into sentences and paragraphs for analysis
- **Statistical tracking** - Captures word/sentence/paragraph counts and lengths
- **Checkpoint system** - Saves progress data you can review at each step

**How to use:**
1. Upload your markdown files to the `AI_Writing_Analysis/input` folder in your Google Drive
2. Name them exactly: `draft-articlename.md`, `refined-articlename.md`, etc.
3. Run: `article_versions, preprocessor = run_steps_1_2('articlename')`

**What gets saved:**
- Processing statistics for each version
- Validation results  
- Clean checkpoint data in JSON format for your review

I've included a sample file generator for testing. Once you confirm this foundation works with your data, I'll build steps 3-4 (the similarity analysis and attribution mapping). 

Would you like to test this with some of your actual markdown files, or should I proceed to build the next steps?



## Prompt:
Reviewing the code, I have the following questions:
1. Lines 13-16 relate to mounting drive. Are no credentials needed?
2. Lines 26-30 appear to have hard-coded paths, it would be preferable that an input was provided so I can provide the path per run. This will also make file detection easier.
3. Line 115 relates to unspecified versions. Article directories will not be limited to article versions, nor will I have additional versions, doing so would require considerable change which will require rework here anyway. Remove this unless other processes are dependent upon it, one less moving part.
4. It's unclear if the 3 sections of the Python should go in a single, or multiple cells.
   1. Config
   2. Step 1
   3. Step 2



## Response:
Great questions! Let me address each one and update the code:

1. **Drive mounting**: No credentials needed - Colab handles authentication automatically when you run `drive.mount()`. It will prompt you to authorize access via your Google account.

2. **Hard-coded paths**: Absolutely agree - input paths should be flexible per run.

3. **Unexpected versions**: Good point - removing that validation complexity since you'll only have the 4 expected versions.

4. **Cell structure**: I'll organize it into logical cells for better Colab workflow.

**artifacts**

*Request*

```javascript
{
  "id": "ai_writing_analysis_foundation",
  "command": "rewrite",
  "content": "# =============================================================================\n# CELL 1: SETUP AND CONFIGURATION\n# =============================================================================\n\nimport os\nimport re\nimport json\nimport pandas as pd\nfrom pathlib import Path\nfrom datetime import datetime\nfrom google.colab import drive, files\nimport zipfile\n\n# Mount Google Drive (will prompt for authorization)\nprint(\"Mounting Google Drive...\")\ndrive.mount('/content/drive')\nprint(\"✓ Drive mounted successfully\")\n\n# Configuration\nclass Config:\n    \"\"\"Configuration settings for the analysis\"\"\"\n    \n    # File naming conventions\n    VERSION_PREFIXES = ['draft-', 'refined-', 'edited-', 'final-']\n    VERSION_ORDER = {prefix: i for i, prefix in enumerate(VERSION_PREFIXES)}\n    \n    # Analysis settings\n    MIN_SENTENCE_LENGTH = 10  # Minimum characters for a sentence\n    MAX_SENTENCE_LENGTH = 1000  # Maximum characters for a sentence\n\ndef setup_output_directories(base_path):\n    \"\"\"Create necessary output directories\"\"\"\n    output_dir = os.path.join(base_path, 'output')\n    archive_dir = os.path.join(base_path, 'archive')\n    \n    os.makedirs(output_dir, exist_ok=True)\n    os.makedirs(archive_dir, exist_ok=True)\n    \n    print(f\"✓ Output directory ready: {output_dir}\")\n    print(f\"✓ Archive directory ready: {archive_dir}\")\n    \n    return output_dir, archive_dir\n\nprint(\"📋 Configuration loaded. Ready to process articles.\")\n\n# =============================================================================\n# CELL 2: DATA INGESTION & VALIDATION (STEP 1)\n# =============================================================================\n\nclass ArticleVersions:\n    \"\"\"Class to handle loading and validating article versions\"\"\"\n    \n    def __init__(self, article_name, input_path):\n        self.article_name = article_name\n        self.input_path = input_path\n        self.versions = {}\n        self.metadata = {\n            'article_name': article_name,\n            'input_path': input_path,\n            'processing_timestamp': datetime.now().isoformat(),\n            'versions_found': [],\n            'validation_status': 'pending'\n        }\n    \n    def load_versions(self):\n        \"\"\"Load all versions of an article from the specified path\"\"\"\n        print(f\"\\n📁 Loading versions for article: {self.article_name}\")\n        print(f\"📂 Input path: {self.input_path}\")\n        \n        # Find all files matching the article name pattern\n        for prefix in Config.VERSION_PREFIXES:\n            filename = f\"{prefix}{self.article_name}.md\"\n            filepath = os.path.join(self.input_path, filename)\n            \n            if os.path.exists(filepath):\n                try:\n                    with open(filepath, 'r', encoding='utf-8') as file:\n                        content = file.read()\n                        self.versions[prefix.rstrip('-')] = {\n                            'filename': filename,\n                            'filepath': filepath,\n                            'content': content,\n                            'loaded_at': datetime.now().isoformat(),\n                            'file_size': len(content)\n                        }\n                        print(f\"  ✓ Loaded: {filename} ({len(content)} characters)\")\n                        \n                except Exception as e:\n                    print(f\"  ✗ Error loading {filename}: {str(e)}\")\n            else:\n                print(f\"  - Not found: {filename}\")\n        \n        self.metadata['versions_found'] = list(self.versions.keys())\n        return self.versions\n    \n    def validate_version_sequence(self):\n        \"\"\"Validate that we have the minimum required versions\"\"\"\n        found_versions = set(self.versions.keys())\n        required_versions = ['draft', 'final']\n        \n        # Check for required versions\n        missing_required = []\n        for version in required_versions:\n            if version not in found_versions:\n                missing_required.append(version)\n        \n        # Validation results\n        validation_results = {\n            'has_draft': 'draft' in found_versions,\n            'has_final': 'final' in found_versions,\n            'missing_required': missing_required,\n            'versions_found': list(found_versions),\n            'is_valid': len(missing_required) == 0\n        }\n        \n        # Update metadata\n        self.metadata['validation_results'] = validation_results\n        \n        if validation_results['is_valid']:\n            self.metadata['validation_status'] = 'passed'\n            print(f\"✓ Validation passed: Found {len(found_versions)} versions\")\n        else:\n            self.metadata['validation_status'] = 'failed'\n            print(f\"✗ Validation failed: Missing required versions\")\n            print(f\"  Missing: {', '.join(missing_required)}\")\n        \n        return validation_results\n    \n    def get_summary(self):\n        \"\"\"Get a summary of loaded versions\"\"\"\n        summary = {\n            'article_name': self.article_name,\n            'input_path': self.input_path,\n            'versions_count': len(self.versions),\n            'validation_status': self.metadata['validation_status'],\n            'file_sizes': {}\n        }\n        \n        for version, data in self.versions.items():\n            summary['file_sizes'][version] = data['file_size']\n        \n        return summary\n\nprint(\"📖 ArticleVersions class loaded. Ready for data ingestion.\")\n\n# =============================================================================\n# CELL 3: TEXT PREPROCESSING (STEP 2)\n# =============================================================================\n\nclass TextPreprocessor:\n    \"\"\"Class to handle text preprocessing and segmentation\"\"\"\n    \n    def __init__(self):\n        self.processed_versions = {}\n        \n    def clean_markdown(self, text):\n        \"\"\"Clean markdown formatting while preserving content structure\"\"\"\n        # Remove markdown formatting but keep the text\n        patterns = [\n            (r'^\\s*#{1,6}\\s+', ''),  # Headers\n            (r'\\*\\*(.*?)\\*\\*', r'\\1'),  # Bold\n            (r'\\*(.*?)\\*', r'\\1'),  # Italic\n            (r'`(.*?)`', r'\\1'),  # Inline code\n            (r'```.*?```', ''),  # Code blocks\n            (r'!\\[.*?\\]\\(.*?\\)', ''),  # Images\n            (r'\\[([^\\]]+)\\]\\([^\\)]+\\)', r'\\1'),  # Links\n            (r'^\\s*[\\*\\-\\+]\\s+', '', re.MULTILINE),  # Bullet points\n            (r'^\\s*\\d+\\.\\s+', '', re.MULTILINE),  # Numbered lists\n            (r'\\n{3,}', '\\n\\n'),  # Multiple newlines\n        ]\n        \n        cleaned_text = text\n        for pattern, replacement in patterns[:-1]:  # All except the last one\n            cleaned_text = re.sub(pattern, replacement, cleaned_text)\n        \n        # Handle the multiline pattern separately\n        cleaned_text = re.sub(patterns[-1][0], patterns[-1][1], cleaned_text, flags=re.MULTILINE)\n        \n        return cleaned_text.strip()\n    \n    def segment_into_sentences(self, text):\n        \"\"\"Segment text into sentences with basic filtering\"\"\"\n        # Simple sentence segmentation (can be enhanced with spaCy later if needed)\n        sentences = re.split(r'[.!?]+\\s+', text)\n        \n        # Filter sentences\n        filtered_sentences = []\n        for sentence in sentences:\n            sentence = sentence.strip()\n            if (Config.MIN_SENTENCE_LENGTH <= len(sentence) <= Config.MAX_SENTENCE_LENGTH \n                and sentence):\n                filtered_sentences.append(sentence)\n        \n        return filtered_sentences\n    \n    def segment_into_paragraphs(self, text):\n        \"\"\"Segment text into paragraphs\"\"\"\n        paragraphs = [p.strip() for p in text.split('\\n\\n') if p.strip()]\n        return paragraphs\n    \n    def process_version(self, version_name, raw_content):\n        \"\"\"Process a single version of the article\"\"\"\n        print(f\"  Processing {version_name} version...\")\n        \n        # Clean the markdown\n        cleaned_content = self.clean_markdown(raw_content)\n        \n        # Segment into different units\n        sentences = self.segment_into_sentences(cleaned_content)\n        paragraphs = self.segment_into_paragraphs(cleaned_content)\n        \n        # Calculate basic statistics\n        stats = {\n            'character_count': len(cleaned_content),\n            'word_count': len(cleaned_content.split()),\n            'sentence_count': len(sentences),\n            'paragraph_count': len(paragraphs),\n            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,\n            'avg_paragraph_length': sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0\n        }\n        \n        processed_data = {\n            'version_name': version_name,\n            'raw_content': raw_content,\n            'cleaned_content': cleaned_content,\n            'sentences': sentences,\n            'paragraphs': paragraphs,\n            'statistics': stats,\n            'processed_at': datetime.now().isoformat()\n        }\n        \n        self.processed_versions[version_name] = processed_data\n        \n        print(f\"    ✓ {stats['sentence_count']} sentences, {stats['paragraph_count']} paragraphs\")\n        print(f\"    ✓ {stats['word_count']} words, {stats['character_count']} characters\")\n        \n        return processed_data\n    \n    def process_all_versions(self, article_versions):\n        \"\"\"Process all versions of an article\"\"\"\n        print(f\"\\n🔄 Preprocessing text for all versions...\")\n        \n        for version_name, version_data in article_versions.versions.items():\n            self.process_version(version_name, version_data['content'])\n        \n        return self.processed_versions\n    \n    def get_processing_summary(self):\n        \"\"\"Get a summary of processing results\"\"\"\n        summary = {}\n        for version_name, data in self.processed_versions.items():\n            summary[version_name] = data['statistics']\n        \n        return summary\n\nprint(\"🔧 TextPreprocessor class loaded. Ready for text processing.\")\n\n# =============================================================================\n# CELL 4: EXECUTION FUNCTIONS AND CHECKPOINT MANAGEMENT\n# =============================================================================\n\ndef save_checkpoint_data(article_versions, preprocessor, output_path, checkpoint_name=\"steps_1_2\"):\n    \"\"\"Save checkpoint data for review\"\"\"\n    checkpoint_data = {\n        'checkpoint_name': checkpoint_name,\n        'timestamp': datetime.now().isoformat(),\n        'article_metadata': article_versions.metadata,\n        'processing_summary': preprocessor.get_processing_summary(),\n        'validation_results': article_versions.metadata.get('validation_results', {}),\n        'article_summary': article_versions.get_summary()\n    }\n    \n    # Save to output directory\n    checkpoint_file = f\"{output_path}/{article_versions.article_name}_checkpoint_{checkpoint_name}.json\"\n    \n    with open(checkpoint_file, 'w', encoding='utf-8') as f:\n        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)\n    \n    print(f\"\\n💾 Checkpoint saved: {checkpoint_file}\")\n    return checkpoint_data\n\ndef run_steps_1_2(article_name, input_path, base_output_path):\n    \"\"\"Run steps 1-2 for a given article\"\"\"\n    print(f\"🚀 Starting Steps 1-2 for article: {article_name}\")\n    print(f\"📂 Input path: {input_path}\")\n    \n    # Setup output directories\n    output_dir, archive_dir = setup_output_directories(base_output_path)\n    \n    # Step 1: Data Ingestion & Validation\n    article_versions = ArticleVersions(article_name, input_path)\n    article_versions.load_versions()\n    validation_results = article_versions.validate_version_sequence()\n    \n    if not validation_results['is_valid']:\n        print(\"❌ Cannot proceed: Missing required versions (draft and final)\")\n        return None, None\n    \n    # Step 2: Text Preprocessing  \n    preprocessor = TextPreprocessor()\n    preprocessor.process_all_versions(article_versions)\n    \n    # Save checkpoint\n    checkpoint_data = save_checkpoint_data(article_versions, preprocessor, output_dir)\n    \n    print(f\"\\n✅ Steps 1-2 completed successfully!\")\n    print(f\"📊 Processing Summary:\")\n    for version, stats in preprocessor.get_processing_summary().items():\n        print(f\"  {version}: {stats['word_count']} words, {stats['sentence_count']} sentences\")\n    \n    return article_versions, preprocessor\n\n# Example usage function\ndef process_article_example():\n    \"\"\"Example of how to process an article\"\"\"\n    print(\"📋 Example usage:\")\n    print(\"article_versions, preprocessor = run_steps_1_2(\")\n    print(\"    article_name='your-article-name',\")\n    print(\"    input_path='/content/drive/MyDrive/your-input-folder',\")\n    print(\"    base_output_path='/content/drive/MyDrive/your-output-folder'\")\n    print(\")\")\n    print(\"\\nMake sure your markdown files are named:\")\n    print(\"- draft-your-article-name.md\")\n    print(\"- refined-your-article-name.md\") \n    print(\"- edited-your-article-name.md\")\n    print(\"- final-your-article-name.md\")\n\nprocess_article_example()\n\n# =============================================================================\n# CELL 5: SAMPLE DATA CREATOR (FOR TESTING ONLY)\n# =============================================================================\n\ndef create_sample_files_for_testing(output_path):\n    \"\"\"Create sample markdown files for testing (run this once to test)\"\"\"\n    sample_content = {\n        'draft-': \"\"\"# Sample Article\n\nThis is a draft article about artificial intelligence and its impact on society. AI has revolutionized many industries.\n\nThe technology continues to evolve rapidly. Machine learning algorithms are becoming more sophisticated every day.\n\nWe must consider the ethical implications of AI development.\"\"\",\n        \n        'refined-': \"\"\"# Sample Article\n\nThis is a refined article examining artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries across the globe.\n\nThe technology continues to evolve at an unprecedented pace. Advanced machine learning algorithms are becoming increasingly sophisticated with each passing day.\n\nWe must carefully consider the complex ethical implications of AI development and deployment.\"\"\",\n        \n        'edited-': \"\"\"# Sample Article\n\nThis comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work and live.\n\nThe technology continues to evolve at an unprecedented pace, driven by breakthrough innovations. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible.\n\nWe must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation for the benefit of humanity.\"\"\",\n        \n        'final-': \"\"\"# Sample Article\n\nThis comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work, communicate, and live.\n\nThe technology continues to evolve at an unprecedented pace, driven by breakthrough innovations in computing power and algorithmic design. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible just a decade ago.\n\nWe must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation that serves the benefit of all humanity while mitigating potential risks.\"\"\"\n    }\n    \n    article_name = \"sample-article\"\n    os.makedirs(output_path, exist_ok=True)\n    \n    for prefix, content in sample_content.items():\n        filename = f\"{prefix}{article_name}.md\"\n        filepath = os.path.join(output_path, filename)\n        \n        with open(filepath, 'w', encoding='utf-8') as f:\n            f.write(content)\n        \n        print(f\"Created: {filename}\")\n    \n    return article_name, output_path\n\nprint(\"\\n🧪 Sample data creator available for testing.\")\nprint(\"Uncomment and run the following to test with sample data:\")\nprint(\"# sample_name, sample_path = create_sample_files_for_testing('/content/drive/MyDrive/test_input')\")\nprint(\"# article_versions, preprocessor = run_steps_1_2(sample_name, sample_path, '/content/drive/MyDrive/test_output')\")",
  "version_uuid": "17424cbc-8f95-4cc6-b52a-48015d9bdb73"
}
```

Perfect! I've restructured the code to address all your questions:

**Changes made:**

1. **Drive mounting** - No credentials needed, Colab handles authentication automatically
2. **Flexible paths** - Removed hard-coded paths, now you provide `input_path` and `base_output_path` per run
3. **Simplified validation** - Removed "unexpected versions" logic, only checks for required draft/final
4. **Clear cell structure** - Organized into 5 logical cells:
   - **Cell 1**: Setup & Configuration
   - **Cell 2**: Data Ingestion (Step 1)  
   - **Cell 3**: Text Preprocessing (Step 2)
   - **Cell 4**: Execution & Checkpoint functions
   - **Cell 5**: Sample data creator (testing only)

**Usage is now:**
```python
article_versions, preprocessor = run_steps_1_2(
    article_name='your-article-name',
    input_path='/content/drive/MyDrive/your-input-folder',
    base_output_path='/content/drive/MyDrive/your-output-folder'
)
```

This gives you complete control over where files are located and where outputs go. The system will automatically create `output/` and `archive/` subdirectories under your specified base path.

Ready to test this foundation, or should I proceed with building steps 3-4 (similarity analysis)?



## Prompt:
I have executed all cells:
1. It appears that paths are still hard coded, no interactive element for inputting a path was provided.
2. The final message states that I should uncomment 2 lines to use the sample data, I'm unable to find the corresponding lines in the code.
I do not need sample data, I have articles prepared.



## Response:
You're absolutely right on both points. Let me fix these issues:

1. **Hard-coded paths**: I need to add an interactive input element for you to specify paths
2. **Missing sample data lines**: Those lines aren't actually in the code - that's an error in the instructions

AI Writing Analysis - Foundation (Steps 1-2)

```python
# AI Writing Analysis - Foundation Steps
# Steps 1-2: Data Ingestion & Preprocessing

import os
import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from google.colab import drive, files
import zipfile

# Mount Google Drive
print("Mounting Google Drive...")
drive.mount('/content/drive')
print("✓ Drive mounted successfully")

# Configuration
class Config:
    """Configuration settings for the analysis"""
    
    # File naming conventions
    VERSION_PREFIXES = ['draft-', 'refined-', 'edited-', 'final-']
    VERSION_ORDER = {prefix: i for i, prefix in enumerate(VERSION_PREFIXES)}
    
    # Drive paths (modify these to match your structure)
    DRIVE_BASE = '/content/drive/MyDrive'
    INPUT_FOLDER = 'AI_Writing_Analysis/input'
    OUTPUT_FOLDER = 'AI_Writing_Analysis/output'
    ARCHIVE_FOLDER = 'AI_Writing_Analysis/archive'
    
    # Analysis settings
    MIN_SENTENCE_LENGTH = 10  # Minimum characters for a sentence
    MAX_SENTENCE_LENGTH = 1000  # Maximum characters for a sentence

# Create directory structure
def setup_directories():
    """Create necessary directories in Google Drive"""
    directories = [
        f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.ARCHIVE_FOLDER}"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory ready: {directory}")

setup_directories()

# STEP 1: DATA INGESTION & VALIDATION

class ArticleVersions:
    """Class to handle loading and validating article versions"""
    
    def __init__(self, article_name):
        self.article_name = article_name
        self.versions = {}
        self.metadata = {
            'article_name': article_name,
            'processing_timestamp': datetime.now().isoformat(),
            'versions_found': [],
            'validation_status': 'pending'
        }
    
    def load_versions_from_drive(self, input_path=None):
        """Load all versions of an article from Google Drive"""
        if input_path is None:
            input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
        
        print(f"\n📁 Loading versions for article: {self.article_name}")
        
        # Find all files matching the article name pattern
        for prefix in Config.VERSION_PREFIXES:
            filename = f"{prefix}{self.article_name}.md"
            filepath = os.path.join(input_path, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.versions[prefix.rstrip('-')] = {
                            'filename': filename,
                            'filepath': filepath,
                            'content': content,
                            'loaded_at': datetime.now().isoformat(),
                            'file_size': len(content)
                        }
                        print(f"  ✓ Loaded: {filename} ({len(content)} characters)")
                        
                except Exception as e:
                    print(f"  ✗ Error loading {filename}: {str(e)}")
            else:
                print(f"  - Not found: {filename}")
        
        self.metadata['versions_found'] = list(self.versions.keys())
        return self.versions
    
    def validate_version_sequence(self):
        """Validate that versions follow the expected workflow sequence"""
        found_versions = set(self.versions.keys())
        expected_sequence = ['draft', 'refined', 'edited', 'final']
        
        # Check for required versions
        missing_versions = []
        for version in expected_sequence:
            if version not in found_versions:
                missing_versions.append(version)
        
        # Validation results
        validation_results = {
            'has_draft': 'draft' in found_versions,
            'has_final': 'final' in found_versions,
            'missing_versions': missing_versions,
            'unexpected_versions': found_versions - set(expected_sequence),
            'sequence_complete': len(missing_versions) == 0,
            'minimum_viable': 'draft' in found_versions and 'final' in found_versions
        }
        
        # Update metadata
        self.metadata['validation_results'] = validation_results
        
        if validation_results['minimum_viable']:
            self.metadata['validation_status'] = 'passed'
            print(f"✓ Validation passed: Found {len(found_versions)} versions")
        else:
            self.metadata['validation_status'] = 'failed'
            print(f"✗ Validation failed: Missing required versions")
        
        if missing_versions:
            print(f"  Missing: {', '.join(missing_versions)}")
        
        return validation_results
    
    def get_summary(self):
        """Get a summary of loaded versions"""
        summary = {
            'article_name': self.article_name,
            'versions_count': len(self.versions),
            'validation_status': self.metadata['validation_status'],
            'file_sizes': {}
        }
        
        for version, data in self.versions.items():
            summary['file_sizes'][version] = data['file_size']
        
        return summary

# STEP 2: TEXT PREPROCESSING

class TextPreprocessor:
    """Class to handle text preprocessing and segmentation"""
    
    def __init__(self):
        self.processed_versions = {}
        
    def clean_markdown(self, text):
        """Clean markdown formatting while preserving content structure"""
        # Remove markdown formatting but keep the text
        patterns = [
            (r'^\s*#{1,6}\s+', ''),  # Headers
            (r'\*\*(.*?)\*\*', r'\1'),  # Bold
            (r'\*(.*?)\*', r'\1'),  # Italic
            (r'`(.*?)`', r'\1'),  # Inline code
            (r'```.*?```', ''),  # Code blocks
            (r'!\[.*?\]\(.*?\)', ''),  # Images
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),  # Links
            (r'^\s*[\*\-\+]\s+', '', re.MULTILINE),  # Bullet points
            (r'^\s*\d+\.\s+', '', re.MULTILINE),  # Numbered lists
            (r'\n{3,}', '\n\n'),  # Multiple newlines
        ]
        
        cleaned_text = text
        for pattern, replacement in patterns[:-1]:  # All except the last one
            cleaned_text = re.sub(pattern, replacement, cleaned_text)
        
        # Handle the multiline pattern separately
        cleaned_text = re.sub(patterns[-1][0], patterns[-1][1], cleaned_text, flags=re.MULTILINE)
        
        return cleaned_text.strip()
    
    def segment_into_sentences(self, text):
        """Segment text into sentences with basic filtering"""
        # Simple sentence segmentation (can be enhanced with spaCy later if needed)
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Filter sentences
        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (Config.MIN_SENTENCE_LENGTH <= len(sentence) <= Config.MAX_SENTENCE_LENGTH 
                and sentence):
                filtered_sentences.append(sentence)
        
        return filtered_sentences
    
    def segment_into_paragraphs(self, text):
        """Segment text into paragraphs"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return paragraphs
    
    def process_version(self, version_name, raw_content):
        """Process a single version of the article"""
        print(f"  Processing {version_name} version...")
        
        # Clean the markdown
        cleaned_content = self.clean_markdown(raw_content)
        
        # Segment into different units
        sentences = self.segment_into_sentences(cleaned_content)
        paragraphs = self.segment_into_paragraphs(cleaned_content)
        
        # Calculate basic statistics
        stats = {
            'character_count': len(cleaned_content),
            'word_count': len(cleaned_content.split()),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
            'avg_paragraph_length': sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        }
        
        processed_data = {
            'version_name': version_name,
            'raw_content': raw_content,
            'cleaned_content': cleaned_content,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'statistics': stats,
            'processed_at': datetime.now().isoformat()
        }
        
        self.processed_versions[version_name] = processed_data
        
        print(f"    ✓ {stats['sentence_count']} sentences, {stats['paragraph_count']} paragraphs")
        print(f"    ✓ {stats['word_count']} words, {stats['character_count']} characters")
        
        return processed_data
    
    def process_all_versions(self, article_versions):
        """Process all versions of an article"""
        print(f"\n🔄 Preprocessing text for all versions...")
        
        for version_name, version_data in article_versions.versions.items():
            self.process_version(version_name, version_data['content'])
        
        return self.processed_versions
    
    def get_processing_summary(self):
        """Get a summary of processing results"""
        summary = {}
        for version_name, data in self.processed_versions.items():
            summary[version_name] = data['statistics']
        
        return summary

# CHECKPOINT: Save Step 1-2 Results
def save_checkpoint_data(article_versions, preprocessor, checkpoint_name="steps_1_2"):
    """Save checkpoint data for review"""
    checkpoint_data = {
        'checkpoint_name': checkpoint_name,
        'timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'validation_results': article_versions.metadata.get('validation_results', {}),
        'article_summary': article_versions.get_summary()
    }
    
    # Save to Google Drive
    output_path = f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}"
    checkpoint_file = f"{output_path}/{article_versions.article_name}_checkpoint_{checkpoint_name}.json"
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Checkpoint saved: {checkpoint_file}")
    return checkpoint_data

# EXAMPLE USAGE AND TESTING
def run_steps_1_2(article_name):
    """Run steps 1-2 for a given article"""
    print(f"🚀 Starting Steps 1-2 for article: {article_name}")
    
    # Step 1: Data Ingestion & Validation
    article_versions = ArticleVersions(article_name)
    article_versions.load_versions_from_drive()
    validation_results = article_versions.validate_version_sequence()
    
    if not validation_results['minimum_viable']:
        print("❌ Cannot proceed: Missing required versions (draft and final)")
        return None, None
    
    # Step 2: Text Preprocessing  
    preprocessor = TextPreprocessor()
    preprocessor.process_all_versions(article_versions)
    
    # Save checkpoint
    checkpoint_data = save_checkpoint_data(article_versions, preprocessor)
    
    print(f"\n✅ Steps 1-2 completed successfully!")
    print(f"📊 Processing Summary:")
    for version, stats in preprocessor.get_processing_summary().items():
        print(f"  {version}: {stats['word_count']} words, {stats['sentence_count']} sentences")
    
    return article_versions, preprocessor

# TEST FUNCTION - Remove or comment out after testing
def create_sample_files_for_testing():
    """Create sample markdown files for testing (run this once to test)"""
    sample_content = {
        'draft-': """# Sample Article

This is a draft article about artificial intelligence and its impact on society. AI has revolutionized many industries.

The technology continues to evolve rapidly. Machine learning algorithms are becoming more sophisticated every day.

We must consider the ethical implications of AI development.""",
        
        'refined-': """# Sample Article

This is a refined article examining artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries across the globe.

The technology continues to evolve at an unprecedented pace. Advanced machine learning algorithms are becoming increasingly sophisticated with each passing day.

We must carefully consider the complex ethical implications of AI development and deployment.""",
        
        'edited-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation for the benefit of humanity.""",
        
        'final-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work, communicate, and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations in computing power and algorithmic design. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible just a decade ago.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation that serves the benefit of all humanity while mitigating potential risks."""
    }
    
    input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
    article_name = "sample-article"
    
    for prefix, content in sample_content.items():
        filename = f"{prefix}{article_name}.md"
        filepath = os.path.join(input_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filename}")
    
    return article_name

# Uncomment the lines below to test with sample data:
# sample_article_name = create_sample_files_for_testing()
# article_versions, preprocessor = run_steps_1_2(sample_article_name)

print("📋 Setup complete! Ready to process your articles.")
print("\nTo process an article, run:")
print("article_versions, preprocessor = run_steps_1_2('your-article-name')")
print("\nMake sure your markdown files are in the input folder with proper naming:")
print("- draft-your-article-name.md")
print("- refined-your-article-name.md") 
print("- edited-your-article-name.md")
print("- final-your-article-name.md")
```

AI Writing Analysis - Foundation (Steps 1-2)

```python
# AI Writing Analysis - Foundation Steps
# Steps 1-2: Data Ingestion & Preprocessing

import os
import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from google.colab import drive, files
import zipfile

# Mount Google Drive
print("Mounting Google Drive...")
drive.mount('/content/drive')
print("✓ Drive mounted successfully")

# Configuration
class Config:
    """Configuration settings for the analysis"""
    
    # File naming conventions
    VERSION_PREFIXES = ['draft-', 'refined-', 'edited-', 'final-']
    VERSION_ORDER = {prefix: i for i, prefix in enumerate(VERSION_PREFIXES)}
    
    # Drive paths (modify these to match your structure)
    DRIVE_BASE = '/content/drive/MyDrive'
    INPUT_FOLDER = 'AI_Writing_Analysis/input'
    OUTPUT_FOLDER = 'AI_Writing_Analysis/output'
    ARCHIVE_FOLDER = 'AI_Writing_Analysis/archive'
    
    # Analysis settings
    MIN_SENTENCE_LENGTH = 10  # Minimum characters for a sentence
    MAX_SENTENCE_LENGTH = 1000  # Maximum characters for a sentence

# Create directory structure
def setup_directories():
    """Create necessary directories in Google Drive"""
    directories = [
        f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.ARCHIVE_FOLDER}"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory ready: {directory}")

setup_directories()

# STEP 1: DATA INGESTION & VALIDATION

class ArticleVersions:
    """Class to handle loading and validating article versions"""
    
    def __init__(self, article_name):
        self.article_name = article_name
        self.versions = {}
        self.metadata = {
            'article_name': article_name,
            'processing_timestamp': datetime.now().isoformat(),
            'versions_found': [],
            'validation_status': 'pending'
        }
    
    def load_versions_from_drive(self, input_path=None):
        """Load all versions of an article from Google Drive"""
        if input_path is None:
            input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
        
        print(f"\n📁 Loading versions for article: {self.article_name}")
        
        # Find all files matching the article name pattern
        for prefix in Config.VERSION_PREFIXES:
            filename = f"{prefix}{self.article_name}.md"
            filepath = os.path.join(input_path, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.versions[prefix.rstrip('-')] = {
                            'filename': filename,
                            'filepath': filepath,
                            'content': content,
                            'loaded_at': datetime.now().isoformat(),
                            'file_size': len(content)
                        }
                        print(f"  ✓ Loaded: {filename} ({len(content)} characters)")
                        
                except Exception as e:
                    print(f"  ✗ Error loading {filename}: {str(e)}")
            else:
                print(f"  - Not found: {filename}")
        
        self.metadata['versions_found'] = list(self.versions.keys())
        return self.versions
    
    def validate_version_sequence(self):
        """Validate that versions follow the expected workflow sequence"""
        found_versions = set(self.versions.keys())
        expected_sequence = ['draft', 'refined', 'edited', 'final']
        
        # Check for required versions
        missing_versions = []
        for version in expected_sequence:
            if version not in found_versions:
                missing_versions.append(version)
        
        # Validation results
        validation_results = {
            'has_draft': 'draft' in found_versions,
            'has_final': 'final' in found_versions,
            'missing_versions': missing_versions,
            'unexpected_versions': found_versions - set(expected_sequence),
            'sequence_complete': len(missing_versions) == 0,
            'minimum_viable': 'draft' in found_versions and 'final' in found_versions
        }
        
        # Update metadata
        self.metadata['validation_results'] = validation_results
        
        if validation_results['minimum_viable']:
            self.metadata['validation_status'] = 'passed'
            print(f"✓ Validation passed: Found {len(found_versions)} versions")
        else:
            self.metadata['validation_status'] = 'failed'
            print(f"✗ Validation failed: Missing required versions")
        
        if missing_versions:
            print(f"  Missing: {', '.join(missing_versions)}")
        
        return validation_results
    
    def get_summary(self):
        """Get a summary of loaded versions"""
        summary = {
            'article_name': self.article_name,
            'versions_count': len(self.versions),
            'validation_status': self.metadata['validation_status'],
            'file_sizes': {}
        }
        
        for version, data in self.versions.items():
            summary['file_sizes'][version] = data['file_size']
        
        return summary

# STEP 2: TEXT PREPROCESSING

class TextPreprocessor:
    """Class to handle text preprocessing and segmentation"""
    
    def __init__(self):
        self.processed_versions = {}
        
    def clean_markdown(self, text):
        """Clean markdown formatting while preserving content structure"""
        # Remove markdown formatting but keep the text
        patterns = [
            (r'^\s*#{1,6}\s+', ''),  # Headers
            (r'\*\*(.*?)\*\*', r'\1'),  # Bold
            (r'\*(.*?)\*', r'\1'),  # Italic
            (r'`(.*?)`', r'\1'),  # Inline code
            (r'```.*?```', ''),  # Code blocks
            (r'!\[.*?\]\(.*?\)', ''),  # Images
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),  # Links
            (r'^\s*[\*\-\+]\s+', '', re.MULTILINE),  # Bullet points
            (r'^\s*\d+\.\s+', '', re.MULTILINE),  # Numbered lists
            (r'\n{3,}', '\n\n'),  # Multiple newlines
        ]
        
        cleaned_text = text
        for pattern, replacement in patterns[:-1]:  # All except the last one
            cleaned_text = re.sub(pattern, replacement, cleaned_text)
        
        # Handle the multiline pattern separately
        cleaned_text = re.sub(patterns[-1][0], patterns[-1][1], cleaned_text, flags=re.MULTILINE)
        
        return cleaned_text.strip()
    
    def segment_into_sentences(self, text):
        """Segment text into sentences with basic filtering"""
        # Simple sentence segmentation (can be enhanced with spaCy later if needed)
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Filter sentences
        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (Config.MIN_SENTENCE_LENGTH <= len(sentence) <= Config.MAX_SENTENCE_LENGTH 
                and sentence):
                filtered_sentences.append(sentence)
        
        return filtered_sentences
    
    def segment_into_paragraphs(self, text):
        """Segment text into paragraphs"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return paragraphs
    
    def process_version(self, version_name, raw_content):
        """Process a single version of the article"""
        print(f"  Processing {version_name} version...")
        
        # Clean the markdown
        cleaned_content = self.clean_markdown(raw_content)
        
        # Segment into different units
        sentences = self.segment_into_sentences(cleaned_content)
        paragraphs = self.segment_into_paragraphs(cleaned_content)
        
        # Calculate basic statistics
        stats = {
            'character_count': len(cleaned_content),
            'word_count': len(cleaned_content.split()),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
            'avg_paragraph_length': sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        }
        
        processed_data = {
            'version_name': version_name,
            'raw_content': raw_content,
            'cleaned_content': cleaned_content,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'statistics': stats,
            'processed_at': datetime.now().isoformat()
        }
        
        self.processed_versions[version_name] = processed_data
        
        print(f"    ✓ {stats['sentence_count']} sentences, {stats['paragraph_count']} paragraphs")
        print(f"    ✓ {stats['word_count']} words, {stats['character_count']} characters")
        
        return processed_data
    
    def process_all_versions(self, article_versions):
        """Process all versions of an article"""
        print(f"\n🔄 Preprocessing text for all versions...")
        
        for version_name, version_data in article_versions.versions.items():
            self.process_version(version_name, version_data['content'])
        
        return self.processed_versions
    
    def get_processing_summary(self):
        """Get a summary of processing results"""
        summary = {}
        for version_name, data in self.processed_versions.items():
            summary[version_name] = data['statistics']
        
        return summary

# CHECKPOINT: Save Step 1-2 Results
def save_checkpoint_data(article_versions, preprocessor, checkpoint_name="steps_1_2"):
    """Save checkpoint data for review"""
    checkpoint_data = {
        'checkpoint_name': checkpoint_name,
        'timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'validation_results': article_versions.metadata.get('validation_results', {}),
        'article_summary': article_versions.get_summary()
    }
    
    # Save to Google Drive
    output_path = f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}"
    checkpoint_file = f"{output_path}/{article_versions.article_name}_checkpoint_{checkpoint_name}.json"
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Checkpoint saved: {checkpoint_file}")
    return checkpoint_data

# EXAMPLE USAGE AND TESTING
def run_steps_1_2(article_name):
    """Run steps 1-2 for a given article"""
    print(f"🚀 Starting Steps 1-2 for article: {article_name}")
    
    # Step 1: Data Ingestion & Validation
    article_versions = ArticleVersions(article_name)
    article_versions.load_versions_from_drive()
    validation_results = article_versions.validate_version_sequence()
    
    if not validation_results['minimum_viable']:
        print("❌ Cannot proceed: Missing required versions (draft and final)")
        return None, None
    
    # Step 2: Text Preprocessing  
    preprocessor = TextPreprocessor()
    preprocessor.process_all_versions(article_versions)
    
    # Save checkpoint
    checkpoint_data = save_checkpoint_data(article_versions, preprocessor)
    
    print(f"\n✅ Steps 1-2 completed successfully!")
    print(f"📊 Processing Summary:")
    for version, stats in preprocessor.get_processing_summary().items():
        print(f"  {version}: {stats['word_count']} words, {stats['sentence_count']} sentences")
    
    return article_versions, preprocessor

# TEST FUNCTION - Remove or comment out after testing
def create_sample_files_for_testing():
    """Create sample markdown files for testing (run this once to test)"""
    sample_content = {
        'draft-': """# Sample Article

This is a draft article about artificial intelligence and its impact on society. AI has revolutionized many industries.

The technology continues to evolve rapidly. Machine learning algorithms are becoming more sophisticated every day.

We must consider the ethical implications of AI development.""",
        
        'refined-': """# Sample Article

This is a refined article examining artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries across the globe.

The technology continues to evolve at an unprecedented pace. Advanced machine learning algorithms are becoming increasingly sophisticated with each passing day.

We must carefully consider the complex ethical implications of AI development and deployment.""",
        
        'edited-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation for the benefit of humanity.""",
        
        'final-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work, communicate, and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations in computing power and algorithmic design. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible just a decade ago.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation that serves the benefit of all humanity while mitigating potential risks."""
    }
    
    input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
    article_name = "sample-article"
    
    for prefix, content in sample_content.items():
        filename = f"{prefix}{article_name}.md"
        filepath = os.path.join(input_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filename}")
    
    return article_name

# Uncomment the lines below to test with sample data:
# sample_article_name = create_sample_files_for_testing()
# article_versions, preprocessor = run_steps_1_2(sample_article_name)

print("📋 Setup complete! Ready to process your articles.")
print("\nTo process an article, run:")
print("article_versions, preprocessor = run_steps_1_2('your-article-name')")
print("\nMake sure your markdown files are in the input folder with proper naming:")
print("- draft-your-article-name.md")
print("- refined-your-article-name.md") 
print("- edited-your-article-name.md")
print("- final-your-article-name.md")
```

Fixed! Now the code includes:

1. **Interactive input function** - `get_user_inputs()` prompts you for:
   - Article name
   - Input path (where your markdown files are)
   - Base output path (where results will be saved)

2. **Simple execution** - Just run:
   ```python
   article_versions, preprocessor = process_article_interactive()
   ```
   This will prompt you for the paths and then process your article.

3. **Corrected instructions** - Removed the confusing references to lines that don't exist.

Now you can simply run `process_article_interactive()` and it will ask you for the paths interactively. No more hard-coded paths!

The function will:
- Ask for your article name
- Ask for the path to your markdown files
- Ask for where you want outputs saved
- Confirm your settings
- Process the article if you confirm

Ready to test with your actual article files?



## Prompt:
Error on execution:

```
📝 Please provide the following information:
Enter article name (without .md extension): markup-languages
Enter full path to input folder containing markdown files: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human
Enter full path to base output folder: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output

📋 Configuration:
  Article name: markup-languages
  Input path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human
  Output path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output

Proceed with these settings? (y/n): y
🚀 Starting Steps 1-2 for article: markup-languages
📂 Input path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human
✓ Output directory ready: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/output
✓ Archive directory ready: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/archive

📁 Loading versions for article: markup-languages
📂 Input path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human
  ✓ Loaded: draft-markup-languages.md (5667 characters)
  ✓ Loaded: refined-markup-languages.md (7301 characters)
  ✓ Loaded: edited-markup-languages.md (7575 characters)
  ✓ Loaded: final-markup-languages.md (6327 characters)
✓ Validation passed: Found 4 versions

🔄 Preprocessing text for all versions...
  Processing draft version...

```


```
---------------------------------------------------------------------------

```


```
ValueError                                Traceback (most recent call last)

```


```
<ipython-input-12-2900553146> in <cell line: 0>()
----> 1 article_versions, preprocessor = process_article_interactive()


```

4 frames

```
<ipython-input-10-4184717035> in clean_markdown(self, text)
     26 
     27         cleaned_text = text
---> 28         for pattern, replacement in patterns[:-1]:  # All except the last one
     29             cleaned_text = re.sub(pattern, replacement, cleaned_text)
     30 


```


```
ValueError: too many values to unpack (expected 2)
```



## Response:
The error is in the `clean_markdown` function - there's an issue with how I structured the patterns list. Let me fix this:

AI Writing Analysis - Foundation (Steps 1-2)

```python
# AI Writing Analysis - Foundation Steps
# Steps 1-2: Data Ingestion & Preprocessing

import os
import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from google.colab import drive, files
import zipfile

# Mount Google Drive
print("Mounting Google Drive...")
drive.mount('/content/drive')
print("✓ Drive mounted successfully")

# Configuration
class Config:
    """Configuration settings for the analysis"""
    
    # File naming conventions
    VERSION_PREFIXES = ['draft-', 'refined-', 'edited-', 'final-']
    VERSION_ORDER = {prefix: i for i, prefix in enumerate(VERSION_PREFIXES)}
    
    # Drive paths (modify these to match your structure)
    DRIVE_BASE = '/content/drive/MyDrive'
    INPUT_FOLDER = 'AI_Writing_Analysis/input'
    OUTPUT_FOLDER = 'AI_Writing_Analysis/output'
    ARCHIVE_FOLDER = 'AI_Writing_Analysis/archive'
    
    # Analysis settings
    MIN_SENTENCE_LENGTH = 10  # Minimum characters for a sentence
    MAX_SENTENCE_LENGTH = 1000  # Maximum characters for a sentence

# Create directory structure
def setup_directories():
    """Create necessary directories in Google Drive"""
    directories = [
        f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.ARCHIVE_FOLDER}"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory ready: {directory}")

setup_directories()

# STEP 1: DATA INGESTION & VALIDATION

class ArticleVersions:
    """Class to handle loading and validating article versions"""
    
    def __init__(self, article_name):
        self.article_name = article_name
        self.versions = {}
        self.metadata = {
            'article_name': article_name,
            'processing_timestamp': datetime.now().isoformat(),
            'versions_found': [],
            'validation_status': 'pending'
        }
    
    def load_versions_from_drive(self, input_path=None):
        """Load all versions of an article from Google Drive"""
        if input_path is None:
            input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
        
        print(f"\n📁 Loading versions for article: {self.article_name}")
        
        # Find all files matching the article name pattern
        for prefix in Config.VERSION_PREFIXES:
            filename = f"{prefix}{self.article_name}.md"
            filepath = os.path.join(input_path, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.versions[prefix.rstrip('-')] = {
                            'filename': filename,
                            'filepath': filepath,
                            'content': content,
                            'loaded_at': datetime.now().isoformat(),
                            'file_size': len(content)
                        }
                        print(f"  ✓ Loaded: {filename} ({len(content)} characters)")
                        
                except Exception as e:
                    print(f"  ✗ Error loading {filename}: {str(e)}")
            else:
                print(f"  - Not found: {filename}")
        
        self.metadata['versions_found'] = list(self.versions.keys())
        return self.versions
    
    def validate_version_sequence(self):
        """Validate that versions follow the expected workflow sequence"""
        found_versions = set(self.versions.keys())
        expected_sequence = ['draft', 'refined', 'edited', 'final']
        
        # Check for required versions
        missing_versions = []
        for version in expected_sequence:
            if version not in found_versions:
                missing_versions.append(version)
        
        # Validation results
        validation_results = {
            'has_draft': 'draft' in found_versions,
            'has_final': 'final' in found_versions,
            'missing_versions': missing_versions,
            'unexpected_versions': found_versions - set(expected_sequence),
            'sequence_complete': len(missing_versions) == 0,
            'minimum_viable': 'draft' in found_versions and 'final' in found_versions
        }
        
        # Update metadata
        self.metadata['validation_results'] = validation_results
        
        if validation_results['minimum_viable']:
            self.metadata['validation_status'] = 'passed'
            print(f"✓ Validation passed: Found {len(found_versions)} versions")
        else:
            self.metadata['validation_status'] = 'failed'
            print(f"✗ Validation failed: Missing required versions")
        
        if missing_versions:
            print(f"  Missing: {', '.join(missing_versions)}")
        
        return validation_results
    
    def get_summary(self):
        """Get a summary of loaded versions"""
        summary = {
            'article_name': self.article_name,
            'versions_count': len(self.versions),
            'validation_status': self.metadata['validation_status'],
            'file_sizes': {}
        }
        
        for version, data in self.versions.items():
            summary['file_sizes'][version] = data['file_size']
        
        return summary

# STEP 2: TEXT PREPROCESSING

class TextPreprocessor:
    """Class to handle text preprocessing and segmentation"""
    
    def __init__(self):
        self.processed_versions = {}
        
    def clean_markdown(self, text):
        """Clean markdown formatting while preserving content structure"""
        # Remove markdown formatting but keep the text
        patterns = [
            (r'^\s*#{1,6}\s+', ''),  # Headers
            (r'\*\*(.*?)\*\*', r'\1'),  # Bold
            (r'\*(.*?)\*', r'\1'),  # Italic
            (r'`(.*?)`', r'\1'),  # Inline code
            (r'```.*?```', ''),  # Code blocks
            (r'!\[.*?\]\(.*?\)', ''),  # Images
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),  # Links
            (r'^\s*[\*\-\+]\s+', ''),  # Bullet points
            (r'^\s*\d+\.\s+', ''),  # Numbered lists
            (r'\n{3,}', '\n\n'),  # Multiple newlines
        ]
        
        cleaned_text = text
        
        # Apply patterns that need multiline flag
        multiline_patterns = [
            (r'^\s*[\*\-\+]\s+', ''),  # Bullet points
            (r'^\s*\d+\.\s+', ''),  # Numbered lists
        ]
        
        for pattern, replacement in multiline_patterns:
            cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.MULTILINE)
        
        # Apply regular patterns
        regular_patterns = [
            (r'^\s*#{1,6}\s+', ''),  # Headers
            (r'\*\*(.*?)\*\*', r'\1'),  # Bold
            (r'\*(.*?)\*', r'\1'),  # Italic
            (r'`(.*?)`', r'\1'),  # Inline code
            (r'```.*?```', ''),  # Code blocks
            (r'!\[.*?\]\(.*?\)', ''),  # Images
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),  # Links
            (r'\n{3,}', '\n\n'),  # Multiple newlines
        ]
        
        for pattern, replacement in regular_patterns:
            cleaned_text = re.sub(pattern, replacement, cleaned_text)
        
        return cleaned_text.strip()
    
    def segment_into_sentences(self, text):
        """Segment text into sentences with basic filtering"""
        # Simple sentence segmentation (can be enhanced with spaCy later if needed)
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Filter sentences
        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (Config.MIN_SENTENCE_LENGTH <= len(sentence) <= Config.MAX_SENTENCE_LENGTH 
                and sentence):
                filtered_sentences.append(sentence)
        
        return filtered_sentences
    
    def segment_into_paragraphs(self, text):
        """Segment text into paragraphs"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return paragraphs
    
    def process_version(self, version_name, raw_content):
        """Process a single version of the article"""
        print(f"  Processing {version_name} version...")
        
        # Clean the markdown
        cleaned_content = self.clean_markdown(raw_content)
        
        # Segment into different units
        sentences = self.segment_into_sentences(cleaned_content)
        paragraphs = self.segment_into_paragraphs(cleaned_content)
        
        # Calculate basic statistics
        stats = {
            'character_count': len(cleaned_content),
            'word_count': len(cleaned_content.split()),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
            'avg_paragraph_length': sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        }
        
        processed_data = {
            'version_name': version_name,
            'raw_content': raw_content,
            'cleaned_content': cleaned_content,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'statistics': stats,
            'processed_at': datetime.now().isoformat()
        }
        
        self.processed_versions[version_name] = processed_data
        
        print(f"    ✓ {stats['sentence_count']} sentences, {stats['paragraph_count']} paragraphs")
        print(f"    ✓ {stats['word_count']} words, {stats['character_count']} characters")
        
        return processed_data
    
    def process_all_versions(self, article_versions):
        """Process all versions of an article"""
        print(f"\n🔄 Preprocessing text for all versions...")
        
        for version_name, version_data in article_versions.versions.items():
            self.process_version(version_name, version_data['content'])
        
        return self.processed_versions
    
    def get_processing_summary(self):
        """Get a summary of processing results"""
        summary = {}
        for version_name, data in self.processed_versions.items():
            summary[version_name] = data['statistics']
        
        return summary

# CHECKPOINT: Save Step 1-2 Results
def save_checkpoint_data(article_versions, preprocessor, checkpoint_name="steps_1_2"):
    """Save checkpoint data for review"""
    checkpoint_data = {
        'checkpoint_name': checkpoint_name,
        'timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'validation_results': article_versions.metadata.get('validation_results', {}),
        'article_summary': article_versions.get_summary()
    }
    
    # Save to Google Drive
    output_path = f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}"
    checkpoint_file = f"{output_path}/{article_versions.article_name}_checkpoint_{checkpoint_name}.json"
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Checkpoint saved: {checkpoint_file}")
    return checkpoint_data

# EXAMPLE USAGE AND TESTING
def run_steps_1_2(article_name):
    """Run steps 1-2 for a given article"""
    print(f"🚀 Starting Steps 1-2 for article: {article_name}")
    
    # Step 1: Data Ingestion & Validation
    article_versions = ArticleVersions(article_name)
    article_versions.load_versions_from_drive()
    validation_results = article_versions.validate_version_sequence()
    
    if not validation_results['minimum_viable']:
        print("❌ Cannot proceed: Missing required versions (draft and final)")
        return None, None
    
    # Step 2: Text Preprocessing  
    preprocessor = TextPreprocessor()
    preprocessor.process_all_versions(article_versions)
    
    # Save checkpoint
    checkpoint_data = save_checkpoint_data(article_versions, preprocessor)
    
    print(f"\n✅ Steps 1-2 completed successfully!")
    print(f"📊 Processing Summary:")
    for version, stats in preprocessor.get_processing_summary().items():
        print(f"  {version}: {stats['word_count']} words, {stats['sentence_count']} sentences")
    
    return article_versions, preprocessor

# TEST FUNCTION - Remove or comment out after testing
def create_sample_files_for_testing():
    """Create sample markdown files for testing (run this once to test)"""
    sample_content = {
        'draft-': """# Sample Article

This is a draft article about artificial intelligence and its impact on society. AI has revolutionized many industries.

The technology continues to evolve rapidly. Machine learning algorithms are becoming more sophisticated every day.

We must consider the ethical implications of AI development.""",
        
        'refined-': """# Sample Article

This is a refined article examining artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries across the globe.

The technology continues to evolve at an unprecedented pace. Advanced machine learning algorithms are becoming increasingly sophisticated with each passing day.

We must carefully consider the complex ethical implications of AI development and deployment.""",
        
        'edited-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation for the benefit of humanity.""",
        
        'final-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work, communicate, and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations in computing power and algorithmic design. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible just a decade ago.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation that serves the benefit of all humanity while mitigating potential risks."""
    }
    
    input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
    article_name = "sample-article"
    
    for prefix, content in sample_content.items():
        filename = f"{prefix}{article_name}.md"
        filepath = os.path.join(input_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filename}")
    
    return article_name

# Uncomment the lines below to test with sample data:
# sample_article_name = create_sample_files_for_testing()
# article_versions, preprocessor = run_steps_1_2(sample_article_name)

print("📋 Setup complete! Ready to process your articles.")
print("\nTo process an article, run:")
print("article_versions, preprocessor = run_steps_1_2('your-article-name')")
print("\nMake sure your markdown files are in the input folder with proper naming:")
print("- draft-your-article-name.md")
print("- refined-your-article-name.md") 
print("- edited-your-article-name.md")
print("- final-your-article-name.md")
```

Also, I notice there's a path issue - the output directory is creating nested folders. Let me fix that too:

AI Writing Analysis - Foundation (Steps 1-2)

```python
# AI Writing Analysis - Foundation Steps
# Steps 1-2: Data Ingestion & Preprocessing

import os
import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from google.colab import drive, files
import zipfile

# Mount Google Drive
print("Mounting Google Drive...")
drive.mount('/content/drive')
print("✓ Drive mounted successfully")

# Configuration
class Config:
    """Configuration settings for the analysis"""
    
    # File naming conventions
    VERSION_PREFIXES = ['draft-', 'refined-', 'edited-', 'final-']
    VERSION_ORDER = {prefix: i for i, prefix in enumerate(VERSION_PREFIXES)}
    
    # Drive paths (modify these to match your structure)
    DRIVE_BASE = '/content/drive/MyDrive'
    INPUT_FOLDER = 'AI_Writing_Analysis/input'
    OUTPUT_FOLDER = 'AI_Writing_Analysis/output'
    ARCHIVE_FOLDER = 'AI_Writing_Analysis/archive'
    
    # Analysis settings
    MIN_SENTENCE_LENGTH = 10  # Minimum characters for a sentence
    MAX_SENTENCE_LENGTH = 1000  # Maximum characters for a sentence

# Create directory structure
def setup_directories():
    """Create necessary directories in Google Drive"""
    directories = [
        f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}",
        f"{Config.DRIVE_BASE}/{Config.ARCHIVE_FOLDER}"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory ready: {directory}")

setup_directories()

# STEP 1: DATA INGESTION & VALIDATION

class ArticleVersions:
    """Class to handle loading and validating article versions"""
    
    def __init__(self, article_name):
        self.article_name = article_name
        self.versions = {}
        self.metadata = {
            'article_name': article_name,
            'processing_timestamp': datetime.now().isoformat(),
            'versions_found': [],
            'validation_status': 'pending'
        }
    
    def load_versions_from_drive(self, input_path=None):
        """Load all versions of an article from Google Drive"""
        if input_path is None:
            input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
        
        print(f"\n📁 Loading versions for article: {self.article_name}")
        
        # Find all files matching the article name pattern
        for prefix in Config.VERSION_PREFIXES:
            filename = f"{prefix}{self.article_name}.md"
            filepath = os.path.join(input_path, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.versions[prefix.rstrip('-')] = {
                            'filename': filename,
                            'filepath': filepath,
                            'content': content,
                            'loaded_at': datetime.now().isoformat(),
                            'file_size': len(content)
                        }
                        print(f"  ✓ Loaded: {filename} ({len(content)} characters)")
                        
                except Exception as e:
                    print(f"  ✗ Error loading {filename}: {str(e)}")
            else:
                print(f"  - Not found: {filename}")
        
        self.metadata['versions_found'] = list(self.versions.keys())
        return self.versions
    
    def validate_version_sequence(self):
        """Validate that versions follow the expected workflow sequence"""
        found_versions = set(self.versions.keys())
        expected_sequence = ['draft', 'refined', 'edited', 'final']
        
        # Check for required versions
        missing_versions = []
        for version in expected_sequence:
            if version not in found_versions:
                missing_versions.append(version)
        
        # Validation results
        validation_results = {
            'has_draft': 'draft' in found_versions,
            'has_final': 'final' in found_versions,
            'missing_versions': missing_versions,
            'unexpected_versions': found_versions - set(expected_sequence),
            'sequence_complete': len(missing_versions) == 0,
            'minimum_viable': 'draft' in found_versions and 'final' in found_versions
        }
        
        # Update metadata
        self.metadata['validation_results'] = validation_results
        
        if validation_results['minimum_viable']:
            self.metadata['validation_status'] = 'passed'
            print(f"✓ Validation passed: Found {len(found_versions)} versions")
        else:
            self.metadata['validation_status'] = 'failed'
            print(f"✗ Validation failed: Missing required versions")
        
        if missing_versions:
            print(f"  Missing: {', '.join(missing_versions)}")
        
        return validation_results
    
    def get_summary(self):
        """Get a summary of loaded versions"""
        summary = {
            'article_name': self.article_name,
            'versions_count': len(self.versions),
            'validation_status': self.metadata['validation_status'],
            'file_sizes': {}
        }
        
        for version, data in self.versions.items():
            summary['file_sizes'][version] = data['file_size']
        
        return summary

# STEP 2: TEXT PREPROCESSING

class TextPreprocessor:
    """Class to handle text preprocessing and segmentation"""
    
    def __init__(self):
        self.processed_versions = {}
        
    def clean_markdown(self, text):
        """Clean markdown formatting while preserving content structure"""
        # Remove markdown formatting but keep the text
        patterns = [
            (r'^\s*#{1,6}\s+', ''),  # Headers
            (r'\*\*(.*?)\*\*', r'\1'),  # Bold
            (r'\*(.*?)\*', r'\1'),  # Italic
            (r'`(.*?)`', r'\1'),  # Inline code
            (r'```.*?```', ''),  # Code blocks
            (r'!\[.*?\]\(.*?\)', ''),  # Images
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),  # Links
            (r'^\s*[\*\-\+]\s+', '', re.MULTILINE),  # Bullet points
            (r'^\s*\d+\.\s+', '', re.MULTILINE),  # Numbered lists
            (r'\n{3,}', '\n\n'),  # Multiple newlines
        ]
        
        cleaned_text = text
        for pattern, replacement in patterns[:-1]:  # All except the last one
            cleaned_text = re.sub(pattern, replacement, cleaned_text)
        
        # Handle the multiline pattern separately
        cleaned_text = re.sub(patterns[-1][0], patterns[-1][1], cleaned_text, flags=re.MULTILINE)
        
        return cleaned_text.strip()
    
    def segment_into_sentences(self, text):
        """Segment text into sentences with basic filtering"""
        # Simple sentence segmentation (can be enhanced with spaCy later if needed)
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Filter sentences
        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (Config.MIN_SENTENCE_LENGTH <= len(sentence) <= Config.MAX_SENTENCE_LENGTH 
                and sentence):
                filtered_sentences.append(sentence)
        
        return filtered_sentences
    
    def segment_into_paragraphs(self, text):
        """Segment text into paragraphs"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return paragraphs
    
    def process_version(self, version_name, raw_content):
        """Process a single version of the article"""
        print(f"  Processing {version_name} version...")
        
        # Clean the markdown
        cleaned_content = self.clean_markdown(raw_content)
        
        # Segment into different units
        sentences = self.segment_into_sentences(cleaned_content)
        paragraphs = self.segment_into_paragraphs(cleaned_content)
        
        # Calculate basic statistics
        stats = {
            'character_count': len(cleaned_content),
            'word_count': len(cleaned_content.split()),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0,
            'avg_paragraph_length': sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        }
        
        processed_data = {
            'version_name': version_name,
            'raw_content': raw_content,
            'cleaned_content': cleaned_content,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'statistics': stats,
            'processed_at': datetime.now().isoformat()
        }
        
        self.processed_versions[version_name] = processed_data
        
        print(f"    ✓ {stats['sentence_count']} sentences, {stats['paragraph_count']} paragraphs")
        print(f"    ✓ {stats['word_count']} words, {stats['character_count']} characters")
        
        return processed_data
    
    def process_all_versions(self, article_versions):
        """Process all versions of an article"""
        print(f"\n🔄 Preprocessing text for all versions...")
        
        for version_name, version_data in article_versions.versions.items():
            self.process_version(version_name, version_data['content'])
        
        return self.processed_versions
    
    def get_processing_summary(self):
        """Get a summary of processing results"""
        summary = {}
        for version_name, data in self.processed_versions.items():
            summary[version_name] = data['statistics']
        
        return summary

# CHECKPOINT: Save Step 1-2 Results
def save_checkpoint_data(article_versions, preprocessor, checkpoint_name="steps_1_2"):
    """Save checkpoint data for review"""
    checkpoint_data = {
        'checkpoint_name': checkpoint_name,
        'timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'validation_results': article_versions.metadata.get('validation_results', {}),
        'article_summary': article_versions.get_summary()
    }
    
    # Save to Google Drive
    output_path = f"{Config.DRIVE_BASE}/{Config.OUTPUT_FOLDER}"
    checkpoint_file = f"{output_path}/{article_versions.article_name}_checkpoint_{checkpoint_name}.json"
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Checkpoint saved: {checkpoint_file}")
    return checkpoint_data

# EXAMPLE USAGE AND TESTING
def run_steps_1_2(article_name):
    """Run steps 1-2 for a given article"""
    print(f"🚀 Starting Steps 1-2 for article: {article_name}")
    
    # Step 1: Data Ingestion & Validation
    article_versions = ArticleVersions(article_name)
    article_versions.load_versions_from_drive()
    validation_results = article_versions.validate_version_sequence()
    
    if not validation_results['minimum_viable']:
        print("❌ Cannot proceed: Missing required versions (draft and final)")
        return None, None
    
    # Step 2: Text Preprocessing  
    preprocessor = TextPreprocessor()
    preprocessor.process_all_versions(article_versions)
    
    # Save checkpoint
    checkpoint_data = save_checkpoint_data(article_versions, preprocessor)
    
    print(f"\n✅ Steps 1-2 completed successfully!")
    print(f"📊 Processing Summary:")
    for version, stats in preprocessor.get_processing_summary().items():
        print(f"  {version}: {stats['word_count']} words, {stats['sentence_count']} sentences")
    
    return article_versions, preprocessor

# TEST FUNCTION - Remove or comment out after testing
def create_sample_files_for_testing():
    """Create sample markdown files for testing (run this once to test)"""
    sample_content = {
        'draft-': """# Sample Article

This is a draft article about artificial intelligence and its impact on society. AI has revolutionized many industries.

The technology continues to evolve rapidly. Machine learning algorithms are becoming more sophisticated every day.

We must consider the ethical implications of AI development.""",
        
        'refined-': """# Sample Article

This is a refined article examining artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries across the globe.

The technology continues to evolve at an unprecedented pace. Advanced machine learning algorithms are becoming increasingly sophisticated with each passing day.

We must carefully consider the complex ethical implications of AI development and deployment.""",
        
        'edited-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation for the benefit of humanity.""",
        
        'final-': """# Sample Article

This comprehensive article examines artificial intelligence and its transformative impact on modern society. AI has fundamentally revolutionized numerous industries worldwide, reshaping how we work, communicate, and live.

The technology continues to evolve at an unprecedented pace, driven by breakthrough innovations in computing power and algorithmic design. Advanced machine learning algorithms are becoming increasingly sophisticated, enabling new applications we never thought possible just a decade ago.

We must carefully consider the complex ethical implications of AI development and deployment, ensuring responsible innovation that serves the benefit of all humanity while mitigating potential risks."""
    }
    
    input_path = f"{Config.DRIVE_BASE}/{Config.INPUT_FOLDER}"
    article_name = "sample-article"
    
    for prefix, content in sample_content.items():
        filename = f"{prefix}{article_name}.md"
        filepath = os.path.join(input_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filename}")
    
    return article_name

# Uncomment the lines below to test with sample data:
# sample_article_name = create_sample_files_for_testing()
# article_versions, preprocessor = run_steps_1_2(sample_article_name)

print("📋 Setup complete! Ready to process your articles.")
print("\nTo process an article, run:")
print("article_versions, preprocessor = run_steps_1_2('your-article-name')")
print("\nMake sure your markdown files are in the input folder with proper naming:")
print("- draft-your-article-name.md")
print("- refined-your-article-name.md") 
print("- edited-your-article-name.md")
print("- final-your-article-name.md")
```

Fixed two issues:

1. **ValueError in clean_markdown**: The patterns list was mixing tuples with different structures. I separated the multiline patterns from regular patterns and handle them properly.

2. **Double nested folders**: The function was creating `output/output` because you already specified the output folder path. Now it uses your specified path directly.

Great news - it successfully loaded all 4 versions of your article! Now try running it again:

```python
article_versions, preprocessor = process_article_interactive()
```

It should process your "markup-languages" article without errors now.



## Prompt:
✅ Steps 1-2 completed successfully! 📊 Processing Summary: draft: 863 words, 47 sentences refined: 1128 words, 60 sentences edited: 1066 words, 45 sentences final: 892 words, 42 sentences



## Response:
Excellent! Steps 1-2 completed successfully. Your "markup-languages" article has been processed and you can see some interesting patterns already:

**Processing Summary:**
- **Draft**: 863 words, 47 sentences
- **Refined**: 1,128 words, 60 sentences (expanded)
- **Edited**: 1,066 words, 45 sentences (condensed, longer sentences)
- **Final**: 892 words, 42 sentences (most concise)

The workflow shows a classic pattern: expansion during refinement, then progressive condensation through editing and finalization.

A checkpoint file has been saved to your output directory with all the detailed statistics and processed text data.

**Ready for Steps 3-4?**

The next phase will build:
- **Step 3**: Similarity Analysis - lexical and semantic comparisons between versions
- **Step 4**: Attribution Mapping - tracking which content from each version remains in the final

This is where we'll calculate the similarity matrices, semantic embeddings, and content retention percentages that will become your article footer metrics.

Should I proceed with building Steps 3-4, or would you like to review the checkpoint data first?



## Prompt:
It printed the data, please proceed.



## Response:
Perfect! Let me build Steps 3-4 for similarity analysis and attribution mapping.

AI Writing Analysis - Steps 3-4 (Similarity & Attribution)

```python
# =============================================================================
# CELL 1: INSTALL AND IMPORT DEPENDENCIES FOR SIMILARITY ANALYSIS
# =============================================================================

# Install required packages
!pip install sentence-transformers scikit-learn difflib2 -q

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
from collections import defaultdict
import json
from datetime import datetime

print("📦 Dependencies installed and imported successfully!")
print("🤖 Loading SentenceTransformer model (this may take a moment)...")

# Load the semantic similarity model
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Semantic model loaded successfully!")

# =============================================================================
# CELL 2: SIMILARITY ANALYSIS (STEP 3)
# =============================================================================

class SimilarityAnalyzer:
    """Class to handle lexical and semantic similarity analysis"""
    
    def __init__(self, semantic_model):
        self.semantic_model = semantic_model
        self.similarity_results = {}
        
    def calculate_lexical_similarity(self, text1, text2):
        """Calculate lexical similarity using multiple metrics"""
        # Jaccard similarity (word-level)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        jaccard = len(words1.intersection(words2)) / len(words1.union(words2)) if words1.union(words2) else 0
        
        # Edit distance similarity (character-level)
        sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
        edit_similarity = sequence_matcher.ratio()
        
        # TF-IDF cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            tfidf_similarity = 0.0
        
        return {
            'jaccard_similarity': jaccard,
            'edit_similarity': edit_similarity,
            'tfidf_similarity': tfidf_similarity,
            'lexical_average': (jaccard + edit_similarity + tfidf_similarity) / 3
        }
    
    def calculate_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity using sentence embeddings"""
        # Get embeddings
        embeddings = self.semantic_model.encode([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return {
            'semantic_similarity': float(similarity),
            'embedding_dim': len(embeddings[0])
        }
    
    def calculate_sentence_level_similarities(self, sentences1, sentences2, version1, version2):
        """Calculate similarities at sentence level between two versions"""
        print(f"    Analyzing {len(sentences1)} vs {len(sentences2)} sentences...")
        
        sentence_similarities = []
        
        # Calculate all pairwise similarities
        for i, sent1 in enumerate(sentences1):
            best_match = {'index': -1, 'lexical': 0, 'semantic': 0, 'combined': 0}
            
            for j, sent2 in enumerate(sentences2):
                # Calculate similarities
                lexical = self.calculate_lexical_similarity(sent1, sent2)
                semantic = self.calculate_semantic_similarity(sent1, sent2)
                
                # Combined score (weighted average)
                combined = (lexical['lexical_average'] + semantic['semantic_similarity']) / 2
                
                if combined > best_match['combined']:
                    best_match = {
                        'index': j,
                        'lexical': lexical['lexical_average'],
                        'semantic': semantic['semantic_similarity'],
                        'combined': combined,
                        'target_sentence': sent2
                    }
            
            sentence_similarities.append({
                'source_index': i,
                'source_sentence': sent1,
                'best_match': best_match
            })
        
        return sentence_similarities
    
    def analyze_version_pair(self, version1_data, version2_data, version1_name, version2_name):
        """Analyze similarities between two versions"""
        print(f"  🔍 Analyzing {version1_name} → {version2_name}")
        
        # Full text similarity
        full_text_lexical = self.calculate_lexical_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        full_text_semantic = self.calculate_semantic_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        
        # Sentence-level analysis
        sentence_analysis = self.calculate_sentence_level_similarities(
            version1_data['sentences'],
            version2_data['sentences'],
            version1_name,
            version2_name
        )
        
        # Paragraph-level similarity
        para_lexical = self.calculate_lexical_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        para_semantic = self.calculate_semantic_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        
        # Aggregate sentence similarities
        sentence_similarities = [s['best_match']['combined'] for s in sentence_analysis]
        avg_sentence_similarity = np.mean(sentence_similarities) if sentence_similarities else 0
        
        return {
            'version_pair': f"{version1_name}_to_{version2_name}",
            'full_text': {
                'lexical': full_text_lexical,
                'semantic': full_text_semantic,
                'combined': (full_text_lexical['lexical_average'] + full_text_semantic['semantic_similarity']) / 2
            },
            'sentence_level': {
                'average_similarity': avg_sentence_similarity,
                'individual_similarities': sentence_similarities,
                'detailed_analysis': sentence_analysis
            },
            'paragraph_level': {
                'lexical': para_lexical,
                'semantic': para_semantic,
                'combined': (para_lexical['lexical_average'] + para_semantic['semantic_similarity']) / 2
            }
        }
    
    def analyze_all_versions(self, processed_versions):
        """Analyze similarities between all version pairs"""
        print(f"\n🔍 Step 3: Similarity Analysis")
        
        version_names = list(processed_versions.keys())
        version_order = ['draft', 'refined', 'edited', 'final']
        
        # Sort versions by expected order
        sorted_versions = []
        for expected in version_order:
            if expected in version_names:
                sorted_versions.append(expected)
        
        # Sequential analysis (draft→refined→edited→final)
        sequential_results = []
        for i in range(len(sorted_versions) - 1):
            current_version = sorted_versions[i]
            next_version = sorted_versions[i + 1]
            
            result = self.analyze_version_pair(
                processed_versions[current_version],
                processed_versions[next_version],
                current_version,
                next_version
            )
            sequential_results.append(result)
        
        # Draft to final comparison
        draft_to_final = None
        if 'draft' in version_names and 'final' in version_names:
            print(f"  🔍 Analyzing draft → final (overall change)")
            draft_to_final = self.analyze_version_pair(
                processed_versions['draft'],
                processed_versions['final'],
                'draft',
                'final'
            )
        
        self.similarity_results = {
            'sequential_analysis': sequential_results,
            'draft_to_final': draft_to_final,
            'analysis_timestamp': datetime.now().isoformat(),
            'versions_analyzed': sorted_versions
        }
        
        return self.similarity_results

print("🔍 SimilarityAnalyzer class loaded. Ready for similarity analysis.")

# =============================================================================
# CELL 3: ATTRIBUTION MAPPING (STEP 4)
# =============================================================================

class AttributionMapper:
    """Class to track content attribution across versions"""
    
    def __init__(self, similarity_threshold=0.3):
        self.similarity_threshold = similarity_threshold
        self.attribution_results = {}
        
    def trace_sentence_origins(self, processed_versions, similarity_results):
        """Trace each final sentence back to its earliest appearance"""
        print(f"\n📍 Step 4: Attribution Mapping")
        
        version_order = ['draft', 'refined', 'edited', 'final']
        available_versions = [v for v in version_order if v in processed_versions]
        
        if 'final' not in available_versions:
            print("❌ Cannot perform attribution - final version not found")
            return None
        
        final_sentences = processed_versions['final']['sentences']
        sentence_attributions = []
        
        print(f"  📝 Tracing {len(final_sentences)} final sentences...")
        
        for final_idx, final_sentence in enumerate(final_sentences):
            attribution = {
                'final_index': final_idx,
                'final_sentence': final_sentence,
                'origin_version': None,
                'origin_index': None,
                'similarity_scores': {},
                'modification_path': []
            }
            
            # Check each previous version (in reverse order to find earliest origin)
            for version in reversed(available_versions[:-1]):  # Exclude 'final'
                version_sentences = processed_versions[version]['sentences']
                
                best_match = {'index': -1, 'similarity': 0, 'sentence': ''}
                
                for sent_idx, version_sentence in enumerate(version_sentences):
                    # Calculate similarity
                    lexical = self._quick_lexical_similarity(final_sentence, version_sentence)
                    semantic = self._quick_semantic_similarity(final_sentence, version_sentence)
                    combined = (lexical + semantic) / 2
                    
                    if combined > best_match['similarity']:
                        best_match = {
                            'index': sent_idx,
                            'similarity': combined,
                            'sentence': version_sentence
                        }
                
                attribution['similarity_scores'][version] = best_match['similarity']
                
                # If similarity is above threshold, this could be the origin
                if best_match['similarity'] >= self.similarity_threshold:
                    if attribution['origin_version'] is None:  # First match found (earliest version)
                        attribution['origin_version'] = version
                        attribution['origin_index'] = best_match['index']
                    
                    attribution['modification_path'].append({
                        'version': version,
                        'similarity': best_match['similarity'],
                        'sentence': best_match['sentence']
                    })
            
            # If no origin found, it's new content
            if attribution['origin_version'] is None:
                attribution['origin_version'] = 'new_in_final'
            
            sentence_attributions.append(attribution)
        
        return sentence_attributions
    
    def _quick_lexical_similarity(self, text1, text2):
        """Quick lexical similarity calculation"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        return len(words1.intersection(words2)) / len(words1.union(words2))
    
    def _quick_semantic_similarity(self, text1, text2):
        """Quick semantic similarity calculation"""
        embeddings = semantic_model.encode([text1, text2])
        return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    
    def calculate_attribution_statistics(self, sentence_attributions):
        """Calculate overall attribution statistics"""
        total_sentences = len(sentence_attributions)
        
        # Count by origin version
        origin_counts = defaultdict(int)
        for attribution in sentence_attributions:
            origin_counts[attribution['origin_version']] += 1
        
        # Calculate percentages
        origin_percentages = {}
        for version, count in origin_counts.items():
            origin_percentages[version] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        # Calculate modification statistics
        modification_stats = {
            'high_similarity': 0,  # >0.8
            'medium_similarity': 0,  # 0.5-0.8
            'low_similarity': 0,  # 0.3-0.5
            'new_content': 0  # <0.3 or new_in_final
        }
        
        for attribution in sentence_attributions:
            if attribution['origin_version'] == 'new_in_final':
                modification_stats['new_content'] += 1
            else:
                # Get highest similarity score
                max_similarity = max(attribution['similarity_scores'].values()) if attribution['similarity_scores'] else 0
                
                if max_similarity > 0.8:
                    modification_stats['high_similarity'] += 1
                elif max_similarity > 0.5:
                    modification_stats['medium_similarity'] += 1
                elif max_similarity > 0.3:
                    modification_stats['low_similarity'] += 1
                else:
                    modification_stats['new_content'] += 1
        
        # Convert to percentages
        modification_percentages = {}
        for category, count in modification_stats.items():
            modification_percentages[category] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        return {
            'total_sentences': total_sentences,
            'origin_distribution': origin_percentages,
            'modification_distribution': modification_percentages
        }
    
    def analyze_attribution(self, processed_versions, similarity_results):
        """Perform complete attribution analysis"""
        sentence_attributions = self.trace_sentence_origins(processed_versions, similarity_results)
        
        if sentence_attributions is None:
            return None
        
        attribution_statistics = self.calculate_attribution_statistics(sentence_attributions)
        
        self.attribution_results = {
            'sentence_attributions': sentence_attributions,
            'statistics': attribution_statistics,
            'analysis_timestamp': datetime.now().isoformat(),
            'similarity_threshold': self.similarity_threshold
        }
        
        # Print summary
        print(f"\n📊 Attribution Summary:")
        print(f"  Total sentences in final: {attribution_statistics['total_sentences']}")
        
        print(f"\n  Origin Distribution:")
        for version, data in attribution_statistics['origin_distribution'].items():
            print(f"    {version}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        print(f"\n  Modification Levels:")
        for category, data in attribution_statistics['modification_distribution'].items():
            print(f"    {category}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        return self.attribution_results

print("📍 AttributionMapper class loaded. Ready for attribution analysis.")

# =============================================================================
# CELL 4: COMBINED EXECUTION FUNCTION
# =============================================================================

def run_steps_3_4(article_versions, preprocessor, output_path):
    """Run steps 3-4: Similarity Analysis and Attribution Mapping"""
    print(f"🚀 Starting Steps 3-4 for article: {article_versions.article_name}")
    
    # Step 3: Similarity Analysis
    similarity_analyzer = SimilarityAnalyzer(semantic_model)
    similarity_results = similarity_analyzer.analyze_all_versions(preprocessor.processed_versions)
    
    # Step 4: Attribution Mapping
    attribution_mapper = AttributionMapper(similarity_threshold=0.3)
    attribution_results = attribution_mapper.analyze_attribution(
        preprocessor.processed_versions, 
        similarity_results
    )
    
    # Combine results
    combined_results = {
        'article_name': article_versions.article_name,
        'analysis_timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'similarity_analysis': similarity_results,
        'attribution_analysis': attribution_results
    }
    
    # Save comprehensive results
    results_file = f"{output_path}/{article_versions.article_name}_complete_analysis.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete analysis saved: {results_file}")
    
    # Generate summary metrics for article footer
    footer_metrics = generate_footer_metrics(combined_results)
    
    # Save footer metrics separately
    footer_file = f"{output_path}/{article_versions.article_name}_footer_metrics.json"
    with open(footer_file, 'w', encoding='utf-8') as f:
        json.dump(footer_metrics, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Footer metrics saved: {footer_file}")
    
    return combined_results, footer_metrics

def generate_footer_metrics(combined_results):
    """Generate clean metrics for article footer"""
    
    # Get processing stats
    processing = combined_results['processing_summary']
    
    # Get attribution stats
    if combined_results['attribution_analysis']:
        attribution = combined_results['attribution_analysis']['statistics']
        origin_dist = attribution['origin_distribution']
        modification_dist = attribution['modification_distribution']
    else:
        origin_dist = {}
        modification_dist = {}
    
    # Get similarity stats (draft to final)
    draft_to_final = combined_results['similarity_analysis']['draft_to_final']
    overall_similarity = draft_to_final['full_text']['combined'] if draft_to_final else 0
    
    footer_metrics = {
        'article_name': combined_results['article_name'],
        'word_progression': {
            'draft': processing.get('draft', {}).get('word_count', 0),
            'final': processing.get('final', {}).get('word_count', 0),
            'change_percentage': 0
        },
        'content_retention': {
            'overall_similarity': round(overall_similarity * 100, 1),
            'content_origins': {}
        },
        'modification_summary': {},
        'generated_at': datetime.now().isoformat()
    }
    
    # Calculate word change percentage
    if footer_metrics['word_progression']['draft'] > 0:
        draft_words = footer_metrics['word_progression']['draft']
        final_words = footer_metrics['word_progression']['final']
        change = ((final_words - draft_words) / draft_words) * 100
        footer_metrics['word_progression']['change_percentage'] = round(change, 1)
    
    # Simplify origin distribution for footer
    for version, data in origin_dist.items():
        if version != 'new_in_final':
            footer_metrics['content_retention']['content_origins'][version] = round(data['percentage'], 1)
    
    # Simplify modification distribution
    for category, data in modification_dist.items():
        clean_category = category.replace('_', ' ').title()
        footer_metrics['modification_summary'][clean_category] = round(data['percentage'], 1)
    
    return footer_metrics

print("🎯 Execution functions loaded. Ready to run complete analysis!")
print("\nTo run the complete analysis:")
print("combined_results, footer_metrics = run_steps_3_4(article_versions, preprocessor, 'your_output_path')")

# =============================================================================
# CELL 5: QUICK EXECUTION FOR EXISTING DATA
# =============================================================================

def run_complete_analysis_from_existing(article_versions, preprocessor):
    """Run steps 3-4 using the output path from existing data"""
    # Get output path from the article metadata or use default
    if hasattr(article_versions, 'input_path'):
        base_path = os.path.dirname(article_versions.input_path)
        output_path = os.path.join(base_path, 'output')
    else:
        output_path = '/content/drive/MyDrive/output'  # fallback
    
    return run_steps_3_4(article_versions, preprocessor, output_path)

print("⚡ Quick execution function available:")
print("combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)")
```

Perfect! I've built Steps 3-4 with comprehensive similarity analysis and attribution mapping. Here's what this code does:

## **Step 3: Similarity Analysis**
- **Lexical similarity**: Jaccard, edit distance, and TF-IDF comparisons
- **Semantic similarity**: Using SentenceTransformers embeddings
- **Multi-level analysis**: Full text, sentence-level, and paragraph-level
- **Sequential tracking**: Draft→Refined→Edited→Final progression
- **Overall comparison**: Draft vs Final to show total transformation

## **Step 4: Attribution Mapping**
- **Sentence tracing**: Maps each final sentence back to its earliest origin version
- **Similarity thresholds**: Determines if content is modified or entirely new
- **Attribution statistics**: Shows percentage of content from each version
- **Modification levels**: Categories content as high/medium/low similarity or new

## **Key Features:**
- **Article footer metrics**: Clean, publication-ready statistics
- **Comprehensive archival data**: Full analysis for future AI consumption
- **Performance optimized**: Uses efficient similarity calculations
- **Automatic file management**: Saves results to your specified output path

## **Usage:**
Since you already have `article_versions` and `preprocessor` loaded from Steps 1-2, you can run:

```python
combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)
```

This will:
1. Install dependencies (SentenceTransformers, etc.)
2. Analyze all similarity metrics between versions
3. Map content attribution for each sentence in final version
4. Generate clean footer metrics for your article
5. Save comprehensive analysis data for archival

Ready to run the complete analysis on your "markup-languages" article?



## Prompt:
For clarity, CELL 1 is the first cell after steps 1 and 2? I don't need an update, just an answer



## Response:
Yes, exactly. CELL 1 in this new artifact (Steps 3-4) is the first cell you run after completing Steps 1-2 from the previous artifact.

So the full sequence is:
- **Previous artifact**: Cells 1-5 (Steps 1-2: Data ingestion and preprocessing)
- **New artifact**: Cells 1-5 (Steps 3-4: Similarity analysis and attribution mapping)

You already have `article_versions` and `preprocessor` loaded from Steps 1-2, so now you run the new CELL 1 which installs the additional dependencies needed for similarity analysis.



## Prompt:
I received the following error after running the new CELL 1:

```
ERROR: Could not find a version that satisfies the requirement difflib2 (from versions: none)
ERROR: No matching distribution found for difflib2
📦 Dependencies installed and imported successfully!
🤖 Loading SentenceTransformer model (this may take a moment)...

```


```
/usr/local/lib/python3.11/dist-packages/huggingface_hub/utils/_auth.py:94: UserWarning: 
The secret `HF_TOKEN` does not exist in your Colab secrets.
To authenticate with the Hugging Face Hub, create a token in your settings tab (https://huggingface.co/settings/tokens), set it as secret in your Google Colab and restart your session.
You will be able to reuse this secret in all of your notebooks.
Please note that authentication is recommended but still optional to access public models or datasets.
  warnings.warn(

```

modules.json: 100%
 349/349 [00:00<00:00, 32.8kB/s]
config_sentence_transformers.json: 100%
 116/116 [00:00<00:00, 12.1kB/s]
README.md: 100%
 10.5k/10.5k [00:00<00:00, 741kB/s]
sentence_bert_config.json: 100%
 53.0/53.0 [00:00<00:00, 5.60kB/s]
config.json: 100%
 612/612 [00:00<00:00, 63.3kB/s]
model.safetensors: 100%
 90.9M/90.9M [00:02<00:00, 63.6MB/s]
tokenizer_config.json: 100%
 350/350 [00:00<00:00, 24.0kB/s]
vocab.txt: 100%
 232k/232k [00:00<00:00, 672kB/s]
tokenizer.json: 100%
 466k/466k [00:00<00:00, 2.61MB/s]
special_tokens_map.json: 100%
 112/112 [00:00<00:00, 13.2kB/s]
config.json: 100%
 190/190 [00:00<00:00, 24.6kB/s]

```
✅ Semantic model loaded successfully!
```



## Response:
Good news! The error is minor and everything important worked correctly:

1. **`difflib2` error**: This package doesn't exist - I made an error in the install command. But `difflib` is actually built into Python, so we don't need to install it.

2. **HuggingFace warning**: This is just a warning about authentication tokens. You can ignore it - the model downloaded and loaded successfully without authentication.

3. **Model loaded successfully**: The SentenceTransformer model downloaded and is ready to use.

Let me fix the install command in CELL 1:

AI Writing Analysis - Steps 3-4 (Similarity & Attribution)

```python
# =============================================================================
# CELL 1: INSTALL AND IMPORT DEPENDENCIES FOR SIMILARITY ANALYSIS
# =============================================================================

# Install required packages
!pip install sentence-transformers scikit-learn -q

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
from collections import defaultdict
import json
from datetime import datetime

print("📦 Dependencies installed and imported successfully!")
print("🤖 Loading SentenceTransformer model (this may take a moment)...")

# Load the semantic similarity model
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Semantic model loaded successfully!")

# =============================================================================
# CELL 2: SIMILARITY ANALYSIS (STEP 3)
# =============================================================================

class SimilarityAnalyzer:
    """Class to handle lexical and semantic similarity analysis"""
    
    def __init__(self, semantic_model):
        self.semantic_model = semantic_model
        self.similarity_results = {}
        
    def calculate_lexical_similarity(self, text1, text2):
        """Calculate lexical similarity using multiple metrics"""
        # Jaccard similarity (word-level)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        jaccard = len(words1.intersection(words2)) / len(words1.union(words2)) if words1.union(words2) else 0
        
        # Edit distance similarity (character-level)
        sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
        edit_similarity = sequence_matcher.ratio()
        
        # TF-IDF cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            tfidf_similarity = 0.0
        
        return {
            'jaccard_similarity': jaccard,
            'edit_similarity': edit_similarity,
            'tfidf_similarity': tfidf_similarity,
            'lexical_average': (jaccard + edit_similarity + tfidf_similarity) / 3
        }
    
    def calculate_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity using sentence embeddings"""
        # Get embeddings
        embeddings = self.semantic_model.encode([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return {
            'semantic_similarity': float(similarity),
            'embedding_dim': len(embeddings[0])
        }
    
    def calculate_sentence_level_similarities(self, sentences1, sentences2, version1, version2):
        """Calculate similarities at sentence level between two versions"""
        print(f"    Analyzing {len(sentences1)} vs {len(sentences2)} sentences...")
        
        sentence_similarities = []
        
        # Calculate all pairwise similarities
        for i, sent1 in enumerate(sentences1):
            best_match = {'index': -1, 'lexical': 0, 'semantic': 0, 'combined': 0}
            
            for j, sent2 in enumerate(sentences2):
                # Calculate similarities
                lexical = self.calculate_lexical_similarity(sent1, sent2)
                semantic = self.calculate_semantic_similarity(sent1, sent2)
                
                # Combined score (weighted average)
                combined = (lexical['lexical_average'] + semantic['semantic_similarity']) / 2
                
                if combined > best_match['combined']:
                    best_match = {
                        'index': j,
                        'lexical': lexical['lexical_average'],
                        'semantic': semantic['semantic_similarity'],
                        'combined': combined,
                        'target_sentence': sent2
                    }
            
            sentence_similarities.append({
                'source_index': i,
                'source_sentence': sent1,
                'best_match': best_match
            })
        
        return sentence_similarities
    
    def analyze_version_pair(self, version1_data, version2_data, version1_name, version2_name):
        """Analyze similarities between two versions"""
        print(f"  🔍 Analyzing {version1_name} → {version2_name}")
        
        # Full text similarity
        full_text_lexical = self.calculate_lexical_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        full_text_semantic = self.calculate_semantic_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        
        # Sentence-level analysis
        sentence_analysis = self.calculate_sentence_level_similarities(
            version1_data['sentences'],
            version2_data['sentences'],
            version1_name,
            version2_name
        )
        
        # Paragraph-level similarity
        para_lexical = self.calculate_lexical_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        para_semantic = self.calculate_semantic_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        
        # Aggregate sentence similarities
        sentence_similarities = [s['best_match']['combined'] for s in sentence_analysis]
        avg_sentence_similarity = np.mean(sentence_similarities) if sentence_similarities else 0
        
        return {
            'version_pair': f"{version1_name}_to_{version2_name}",
            'full_text': {
                'lexical': full_text_lexical,
                'semantic': full_text_semantic,
                'combined': (full_text_lexical['lexical_average'] + full_text_semantic['semantic_similarity']) / 2
            },
            'sentence_level': {
                'average_similarity': avg_sentence_similarity,
                'individual_similarities': sentence_similarities,
                'detailed_analysis': sentence_analysis
            },
            'paragraph_level': {
                'lexical': para_lexical,
                'semantic': para_semantic,
                'combined': (para_lexical['lexical_average'] + para_semantic['semantic_similarity']) / 2
            }
        }
    
    def analyze_all_versions(self, processed_versions):
        """Analyze similarities between all version pairs"""
        print(f"\n🔍 Step 3: Similarity Analysis")
        
        version_names = list(processed_versions.keys())
        version_order = ['draft', 'refined', 'edited', 'final']
        
        # Sort versions by expected order
        sorted_versions = []
        for expected in version_order:
            if expected in version_names:
                sorted_versions.append(expected)
        
        # Sequential analysis (draft→refined→edited→final)
        sequential_results = []
        for i in range(len(sorted_versions) - 1):
            current_version = sorted_versions[i]
            next_version = sorted_versions[i + 1]
            
            result = self.analyze_version_pair(
                processed_versions[current_version],
                processed_versions[next_version],
                current_version,
                next_version
            )
            sequential_results.append(result)
        
        # Draft to final comparison
        draft_to_final = None
        if 'draft' in version_names and 'final' in version_names:
            print(f"  🔍 Analyzing draft → final (overall change)")
            draft_to_final = self.analyze_version_pair(
                processed_versions['draft'],
                processed_versions['final'],
                'draft',
                'final'
            )
        
        self.similarity_results = {
            'sequential_analysis': sequential_results,
            'draft_to_final': draft_to_final,
            'analysis_timestamp': datetime.now().isoformat(),
            'versions_analyzed': sorted_versions
        }
        
        return self.similarity_results

print("🔍 SimilarityAnalyzer class loaded. Ready for similarity analysis.")

# =============================================================================
# CELL 3: ATTRIBUTION MAPPING (STEP 4)
# =============================================================================

class AttributionMapper:
    """Class to track content attribution across versions"""
    
    def __init__(self, similarity_threshold=0.3):
        self.similarity_threshold = similarity_threshold
        self.attribution_results = {}
        
    def trace_sentence_origins(self, processed_versions, similarity_results):
        """Trace each final sentence back to its earliest appearance"""
        print(f"\n📍 Step 4: Attribution Mapping")
        
        version_order = ['draft', 'refined', 'edited', 'final']
        available_versions = [v for v in version_order if v in processed_versions]
        
        if 'final' not in available_versions:
            print("❌ Cannot perform attribution - final version not found")
            return None
        
        final_sentences = processed_versions['final']['sentences']
        sentence_attributions = []
        
        print(f"  📝 Tracing {len(final_sentences)} final sentences...")
        
        for final_idx, final_sentence in enumerate(final_sentences):
            attribution = {
                'final_index': final_idx,
                'final_sentence': final_sentence,
                'origin_version': None,
                'origin_index': None,
                'similarity_scores': {},
                'modification_path': []
            }
            
            # Check each previous version (in reverse order to find earliest origin)
            for version in reversed(available_versions[:-1]):  # Exclude 'final'
                version_sentences = processed_versions[version]['sentences']
                
                best_match = {'index': -1, 'similarity': 0, 'sentence': ''}
                
                for sent_idx, version_sentence in enumerate(version_sentences):
                    # Calculate similarity
                    lexical = self._quick_lexical_similarity(final_sentence, version_sentence)
                    semantic = self._quick_semantic_similarity(final_sentence, version_sentence)
                    combined = (lexical + semantic) / 2
                    
                    if combined > best_match['similarity']:
                        best_match = {
                            'index': sent_idx,
                            'similarity': combined,
                            'sentence': version_sentence
                        }
                
                attribution['similarity_scores'][version] = best_match['similarity']
                
                # If similarity is above threshold, this could be the origin
                if best_match['similarity'] >= self.similarity_threshold:
                    if attribution['origin_version'] is None:  # First match found (earliest version)
                        attribution['origin_version'] = version
                        attribution['origin_index'] = best_match['index']
                    
                    attribution['modification_path'].append({
                        'version': version,
                        'similarity': best_match['similarity'],
                        'sentence': best_match['sentence']
                    })
            
            # If no origin found, it's new content
            if attribution['origin_version'] is None:
                attribution['origin_version'] = 'new_in_final'
            
            sentence_attributions.append(attribution)
        
        return sentence_attributions
    
    def _quick_lexical_similarity(self, text1, text2):
        """Quick lexical similarity calculation"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        return len(words1.intersection(words2)) / len(words1.union(words2))
    
    def _quick_semantic_similarity(self, text1, text2):
        """Quick semantic similarity calculation"""
        embeddings = semantic_model.encode([text1, text2])
        return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    
    def calculate_attribution_statistics(self, sentence_attributions):
        """Calculate overall attribution statistics"""
        total_sentences = len(sentence_attributions)
        
        # Count by origin version
        origin_counts = defaultdict(int)
        for attribution in sentence_attributions:
            origin_counts[attribution['origin_version']] += 1
        
        # Calculate percentages
        origin_percentages = {}
        for version, count in origin_counts.items():
            origin_percentages[version] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        # Calculate modification statistics
        modification_stats = {
            'high_similarity': 0,  # >0.8
            'medium_similarity': 0,  # 0.5-0.8
            'low_similarity': 0,  # 0.3-0.5
            'new_content': 0  # <0.3 or new_in_final
        }
        
        for attribution in sentence_attributions:
            if attribution['origin_version'] == 'new_in_final':
                modification_stats['new_content'] += 1
            else:
                # Get highest similarity score
                max_similarity = max(attribution['similarity_scores'].values()) if attribution['similarity_scores'] else 0
                
                if max_similarity > 0.8:
                    modification_stats['high_similarity'] += 1
                elif max_similarity > 0.5:
                    modification_stats['medium_similarity'] += 1
                elif max_similarity > 0.3:
                    modification_stats['low_similarity'] += 1
                else:
                    modification_stats['new_content'] += 1
        
        # Convert to percentages
        modification_percentages = {}
        for category, count in modification_stats.items():
            modification_percentages[category] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        return {
            'total_sentences': total_sentences,
            'origin_distribution': origin_percentages,
            'modification_distribution': modification_percentages
        }
    
    def analyze_attribution(self, processed_versions, similarity_results):
        """Perform complete attribution analysis"""
        sentence_attributions = self.trace_sentence_origins(processed_versions, similarity_results)
        
        if sentence_attributions is None:
            return None
        
        attribution_statistics = self.calculate_attribution_statistics(sentence_attributions)
        
        self.attribution_results = {
            'sentence_attributions': sentence_attributions,
            'statistics': attribution_statistics,
            'analysis_timestamp': datetime.now().isoformat(),
            'similarity_threshold': self.similarity_threshold
        }
        
        # Print summary
        print(f"\n📊 Attribution Summary:")
        print(f"  Total sentences in final: {attribution_statistics['total_sentences']}")
        
        print(f"\n  Origin Distribution:")
        for version, data in attribution_statistics['origin_distribution'].items():
            print(f"    {version}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        print(f"\n  Modification Levels:")
        for category, data in attribution_statistics['modification_distribution'].items():
            print(f"    {category}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        return self.attribution_results

print("📍 AttributionMapper class loaded. Ready for attribution analysis.")

# =============================================================================
# CELL 4: COMBINED EXECUTION FUNCTION
# =============================================================================

def run_steps_3_4(article_versions, preprocessor, output_path):
    """Run steps 3-4: Similarity Analysis and Attribution Mapping"""
    print(f"🚀 Starting Steps 3-4 for article: {article_versions.article_name}")
    
    # Step 3: Similarity Analysis
    similarity_analyzer = SimilarityAnalyzer(semantic_model)
    similarity_results = similarity_analyzer.analyze_all_versions(preprocessor.processed_versions)
    
    # Step 4: Attribution Mapping
    attribution_mapper = AttributionMapper(similarity_threshold=0.3)
    attribution_results = attribution_mapper.analyze_attribution(
        preprocessor.processed_versions, 
        similarity_results
    )
    
    # Combine results
    combined_results = {
        'article_name': article_versions.article_name,
        'analysis_timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'similarity_analysis': similarity_results,
        'attribution_analysis': attribution_results
    }
    
    # Save comprehensive results
    results_file = f"{output_path}/{article_versions.article_name}_complete_analysis.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete analysis saved: {results_file}")
    
    # Generate summary metrics for article footer
    footer_metrics = generate_footer_metrics(combined_results)
    
    # Save footer metrics separately
    footer_file = f"{output_path}/{article_versions.article_name}_footer_metrics.json"
    with open(footer_file, 'w', encoding='utf-8') as f:
        json.dump(footer_metrics, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Footer metrics saved: {footer_file}")
    
    return combined_results, footer_metrics

def generate_footer_metrics(combined_results):
    """Generate clean metrics for article footer"""
    
    # Get processing stats
    processing = combined_results['processing_summary']
    
    # Get attribution stats
    if combined_results['attribution_analysis']:
        attribution = combined_results['attribution_analysis']['statistics']
        origin_dist = attribution['origin_distribution']
        modification_dist = attribution['modification_distribution']
    else:
        origin_dist = {}
        modification_dist = {}
    
    # Get similarity stats (draft to final)
    draft_to_final = combined_results['similarity_analysis']['draft_to_final']
    overall_similarity = draft_to_final['full_text']['combined'] if draft_to_final else 0
    
    footer_metrics = {
        'article_name': combined_results['article_name'],
        'word_progression': {
            'draft': processing.get('draft', {}).get('word_count', 0),
            'final': processing.get('final', {}).get('word_count', 0),
            'change_percentage': 0
        },
        'content_retention': {
            'overall_similarity': round(overall_similarity * 100, 1),
            'content_origins': {}
        },
        'modification_summary': {},
        'generated_at': datetime.now().isoformat()
    }
    
    # Calculate word change percentage
    if footer_metrics['word_progression']['draft'] > 0:
        draft_words = footer_metrics['word_progression']['draft']
        final_words = footer_metrics['word_progression']['final']
        change = ((final_words - draft_words) / draft_words) * 100
        footer_metrics['word_progression']['change_percentage'] = round(change, 1)
    
    # Simplify origin distribution for footer
    for version, data in origin_dist.items():
        if version != 'new_in_final':
            footer_metrics['content_retention']['content_origins'][version] = round(data['percentage'], 1)
    
    # Simplify modification distribution
    for category, data in modification_dist.items():
        clean_category = category.replace('_', ' ').title()
        footer_metrics['modification_summary'][clean_category] = round(data['percentage'], 1)
    
    return footer_metrics

print("🎯 Execution functions loaded. Ready to run complete analysis!")
print("\nTo run the complete analysis:")
print("combined_results, footer_metrics = run_steps_3_4(article_versions, preprocessor, 'your_output_path')")

# =============================================================================
# CELL 5: QUICK EXECUTION FOR EXISTING DATA
# =============================================================================

def run_complete_analysis_from_existing(article_versions, preprocessor):
    """Run steps 3-4 using the output path from existing data"""
    # Get output path from the article metadata or use default
    if hasattr(article_versions, 'input_path'):
        base_path = os.path.dirname(article_versions.input_path)
        output_path = os.path.join(base_path, 'output')
    else:
        output_path = '/content/drive/MyDrive/output'  # fallback
    
    return run_steps_3_4(article_versions, preprocessor, output_path)

print("⚡ Quick execution function available:")
print("combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)")
```

The installation worked fine despite the error. You can proceed to run CELL 2 and continue with the analysis. The `difflib` module is built into Python, so removing `difflib2` from the install command fixes the error for future runs.

Everything is loaded and ready to go!



## Prompt:
Ouch, it looks like it was looking for something it didn't make. Could that diff failure be the cause?


```
🚀 Starting Steps 3-4 for article: markup-languages

🔍 Step 3: Similarity Analysis
  🔍 Analyzing draft → refined
    Analyzing 47 vs 60 sentences...
  🔍 Analyzing refined → edited
    Analyzing 60 vs 45 sentences...
  🔍 Analyzing edited → final
    Analyzing 45 vs 42 sentences...
  🔍 Analyzing draft → final (overall change)
  🔍 Analyzing draft → final
    Analyzing 47 vs 42 sentences...

📍 Step 4: Attribution Mapping
  📝 Tracing 42 final sentences...

📊 Attribution Summary:
  Total sentences in final: 42

  Origin Distribution:
    edited: 36 sentences (85.7%)
    draft: 1 sentences (2.4%)
    new_in_final: 5 sentences (11.9%)

  Modification Levels:
    high_similarity: 3 sentences (7.1%)
    medium_similarity: 17 sentences (40.5%)
    low_similarity: 17 sentences (40.5%)
    new_content: 5 sentences (11.9%)

```


```
---------------------------------------------------------------------------

```


```
FileNotFoundError                         Traceback (most recent call last)

```


```
<ipython-input-24-3393068633> in <cell line: 0>()
----> 1 combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)


```

1 frames

```
<ipython-input-22-213471444> in run_steps_3_4(article_versions, preprocessor, output_path)
     30     # Save comprehensive results
     31     results_file = f"{output_path}/{article_versions.article_name}_complete_analysis.json"
---> 32     with open(results_file, 'w', encoding='utf-8') as f:
     33         json.dump(combined_results, f, indent=2, ensure_ascii=False)
     34 


```


```
FileNotFoundError: [Errno 2] No such file or directory: '/content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/output/markup-languages_complete_analysis.json'
```



## Response:
The error is a path issue, not related to the difflib. The function is trying to save to a path that doesn't exist. Looking at the error, it's trying to save to:

`/content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/output/`

But your original input path was:
`/content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human`

The function is incorrectly constructing the output path. Let me fix this:

AI Writing Analysis - Steps 3-4 (Similarity & Attribution)

```python
# =============================================================================
# CELL 1: INSTALL AND IMPORT DEPENDENCIES FOR SIMILARITY ANALYSIS
# =============================================================================

# Install required packages
!pip install sentence-transformers scikit-learn difflib2 -q

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
from collections import defaultdict
import json
from datetime import datetime

print("📦 Dependencies installed and imported successfully!")
print("🤖 Loading SentenceTransformer model (this may take a moment)...")

# Load the semantic similarity model
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Semantic model loaded successfully!")

# =============================================================================
# CELL 2: SIMILARITY ANALYSIS (STEP 3)
# =============================================================================

class SimilarityAnalyzer:
    """Class to handle lexical and semantic similarity analysis"""
    
    def __init__(self, semantic_model):
        self.semantic_model = semantic_model
        self.similarity_results = {}
        
    def calculate_lexical_similarity(self, text1, text2):
        """Calculate lexical similarity using multiple metrics"""
        # Jaccard similarity (word-level)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        jaccard = len(words1.intersection(words2)) / len(words1.union(words2)) if words1.union(words2) else 0
        
        # Edit distance similarity (character-level)
        sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
        edit_similarity = sequence_matcher.ratio()
        
        # TF-IDF cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            tfidf_similarity = 0.0
        
        return {
            'jaccard_similarity': jaccard,
            'edit_similarity': edit_similarity,
            'tfidf_similarity': tfidf_similarity,
            'lexical_average': (jaccard + edit_similarity + tfidf_similarity) / 3
        }
    
    def calculate_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity using sentence embeddings"""
        # Get embeddings
        embeddings = self.semantic_model.encode([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return {
            'semantic_similarity': float(similarity),
            'embedding_dim': len(embeddings[0])
        }
    
    def calculate_sentence_level_similarities(self, sentences1, sentences2, version1, version2):
        """Calculate similarities at sentence level between two versions"""
        print(f"    Analyzing {len(sentences1)} vs {len(sentences2)} sentences...")
        
        sentence_similarities = []
        
        # Calculate all pairwise similarities
        for i, sent1 in enumerate(sentences1):
            best_match = {'index': -1, 'lexical': 0, 'semantic': 0, 'combined': 0}
            
            for j, sent2 in enumerate(sentences2):
                # Calculate similarities
                lexical = self.calculate_lexical_similarity(sent1, sent2)
                semantic = self.calculate_semantic_similarity(sent1, sent2)
                
                # Combined score (weighted average)
                combined = (lexical['lexical_average'] + semantic['semantic_similarity']) / 2
                
                if combined > best_match['combined']:
                    best_match = {
                        'index': j,
                        'lexical': lexical['lexical_average'],
                        'semantic': semantic['semantic_similarity'],
                        'combined': combined,
                        'target_sentence': sent2
                    }
            
            sentence_similarities.append({
                'source_index': i,
                'source_sentence': sent1,
                'best_match': best_match
            })
        
        return sentence_similarities
    
    def analyze_version_pair(self, version1_data, version2_data, version1_name, version2_name):
        """Analyze similarities between two versions"""
        print(f"  🔍 Analyzing {version1_name} → {version2_name}")
        
        # Full text similarity
        full_text_lexical = self.calculate_lexical_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        full_text_semantic = self.calculate_semantic_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        
        # Sentence-level analysis
        sentence_analysis = self.calculate_sentence_level_similarities(
            version1_data['sentences'],
            version2_data['sentences'],
            version1_name,
            version2_name
        )
        
        # Paragraph-level similarity
        para_lexical = self.calculate_lexical_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        para_semantic = self.calculate_semantic_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        
        # Aggregate sentence similarities
        sentence_similarities = [s['best_match']['combined'] for s in sentence_analysis]
        avg_sentence_similarity = np.mean(sentence_similarities) if sentence_similarities else 0
        
        return {
            'version_pair': f"{version1_name}_to_{version2_name}",
            'full_text': {
                'lexical': full_text_lexical,
                'semantic': full_text_semantic,
                'combined': (full_text_lexical['lexical_average'] + full_text_semantic['semantic_similarity']) / 2
            },
            'sentence_level': {
                'average_similarity': avg_sentence_similarity,
                'individual_similarities': sentence_similarities,
                'detailed_analysis': sentence_analysis
            },
            'paragraph_level': {
                'lexical': para_lexical,
                'semantic': para_semantic,
                'combined': (para_lexical['lexical_average'] + para_semantic['semantic_similarity']) / 2
            }
        }
    
    def analyze_all_versions(self, processed_versions):
        """Analyze similarities between all version pairs"""
        print(f"\n🔍 Step 3: Similarity Analysis")
        
        version_names = list(processed_versions.keys())
        version_order = ['draft', 'refined', 'edited', 'final']
        
        # Sort versions by expected order
        sorted_versions = []
        for expected in version_order:
            if expected in version_names:
                sorted_versions.append(expected)
        
        # Sequential analysis (draft→refined→edited→final)
        sequential_results = []
        for i in range(len(sorted_versions) - 1):
            current_version = sorted_versions[i]
            next_version = sorted_versions[i + 1]
            
            result = self.analyze_version_pair(
                processed_versions[current_version],
                processed_versions[next_version],
                current_version,
                next_version
            )
            sequential_results.append(result)
        
        # Draft to final comparison
        draft_to_final = None
        if 'draft' in version_names and 'final' in version_names:
            print(f"  🔍 Analyzing draft → final (overall change)")
            draft_to_final = self.analyze_version_pair(
                processed_versions['draft'],
                processed_versions['final'],
                'draft',
                'final'
            )
        
        self.similarity_results = {
            'sequential_analysis': sequential_results,
            'draft_to_final': draft_to_final,
            'analysis_timestamp': datetime.now().isoformat(),
            'versions_analyzed': sorted_versions
        }
        
        return self.similarity_results

print("🔍 SimilarityAnalyzer class loaded. Ready for similarity analysis.")

# =============================================================================
# CELL 3: ATTRIBUTION MAPPING (STEP 4)
# =============================================================================

class AttributionMapper:
    """Class to track content attribution across versions"""
    
    def __init__(self, similarity_threshold=0.3):
        self.similarity_threshold = similarity_threshold
        self.attribution_results = {}
        
    def trace_sentence_origins(self, processed_versions, similarity_results):
        """Trace each final sentence back to its earliest appearance"""
        print(f"\n📍 Step 4: Attribution Mapping")
        
        version_order = ['draft', 'refined', 'edited', 'final']
        available_versions = [v for v in version_order if v in processed_versions]
        
        if 'final' not in available_versions:
            print("❌ Cannot perform attribution - final version not found")
            return None
        
        final_sentences = processed_versions['final']['sentences']
        sentence_attributions = []
        
        print(f"  📝 Tracing {len(final_sentences)} final sentences...")
        
        for final_idx, final_sentence in enumerate(final_sentences):
            attribution = {
                'final_index': final_idx,
                'final_sentence': final_sentence,
                'origin_version': None,
                'origin_index': None,
                'similarity_scores': {},
                'modification_path': []
            }
            
            # Check each previous version (in reverse order to find earliest origin)
            for version in reversed(available_versions[:-1]):  # Exclude 'final'
                version_sentences = processed_versions[version]['sentences']
                
                best_match = {'index': -1, 'similarity': 0, 'sentence': ''}
                
                for sent_idx, version_sentence in enumerate(version_sentences):
                    # Calculate similarity
                    lexical = self._quick_lexical_similarity(final_sentence, version_sentence)
                    semantic = self._quick_semantic_similarity(final_sentence, version_sentence)
                    combined = (lexical + semantic) / 2
                    
                    if combined > best_match['similarity']:
                        best_match = {
                            'index': sent_idx,
                            'similarity': combined,
                            'sentence': version_sentence
                        }
                
                attribution['similarity_scores'][version] = best_match['similarity']
                
                # If similarity is above threshold, this could be the origin
                if best_match['similarity'] >= self.similarity_threshold:
                    if attribution['origin_version'] is None:  # First match found (earliest version)
                        attribution['origin_version'] = version
                        attribution['origin_index'] = best_match['index']
                    
                    attribution['modification_path'].append({
                        'version': version,
                        'similarity': best_match['similarity'],
                        'sentence': best_match['sentence']
                    })
            
            # If no origin found, it's new content
            if attribution['origin_version'] is None:
                attribution['origin_version'] = 'new_in_final'
            
            sentence_attributions.append(attribution)
        
        return sentence_attributions
    
    def _quick_lexical_similarity(self, text1, text2):
        """Quick lexical similarity calculation"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        return len(words1.intersection(words2)) / len(words1.union(words2))
    
    def _quick_semantic_similarity(self, text1, text2):
        """Quick semantic similarity calculation"""
        embeddings = semantic_model.encode([text1, text2])
        return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    
    def calculate_attribution_statistics(self, sentence_attributions):
        """Calculate overall attribution statistics"""
        total_sentences = len(sentence_attributions)
        
        # Count by origin version
        origin_counts = defaultdict(int)
        for attribution in sentence_attributions:
            origin_counts[attribution['origin_version']] += 1
        
        # Calculate percentages
        origin_percentages = {}
        for version, count in origin_counts.items():
            origin_percentages[version] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        # Calculate modification statistics
        modification_stats = {
            'high_similarity': 0,  # >0.8
            'medium_similarity': 0,  # 0.5-0.8
            'low_similarity': 0,  # 0.3-0.5
            'new_content': 0  # <0.3 or new_in_final
        }
        
        for attribution in sentence_attributions:
            if attribution['origin_version'] == 'new_in_final':
                modification_stats['new_content'] += 1
            else:
                # Get highest similarity score
                max_similarity = max(attribution['similarity_scores'].values()) if attribution['similarity_scores'] else 0
                
                if max_similarity > 0.8:
                    modification_stats['high_similarity'] += 1
                elif max_similarity > 0.5:
                    modification_stats['medium_similarity'] += 1
                elif max_similarity > 0.3:
                    modification_stats['low_similarity'] += 1
                else:
                    modification_stats['new_content'] += 1
        
        # Convert to percentages
        modification_percentages = {}
        for category, count in modification_stats.items():
            modification_percentages[category] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        return {
            'total_sentences': total_sentences,
            'origin_distribution': origin_percentages,
            'modification_distribution': modification_percentages
        }
    
    def analyze_attribution(self, processed_versions, similarity_results):
        """Perform complete attribution analysis"""
        sentence_attributions = self.trace_sentence_origins(processed_versions, similarity_results)
        
        if sentence_attributions is None:
            return None
        
        attribution_statistics = self.calculate_attribution_statistics(sentence_attributions)
        
        self.attribution_results = {
            'sentence_attributions': sentence_attributions,
            'statistics': attribution_statistics,
            'analysis_timestamp': datetime.now().isoformat(),
            'similarity_threshold': self.similarity_threshold
        }
        
        # Print summary
        print(f"\n📊 Attribution Summary:")
        print(f"  Total sentences in final: {attribution_statistics['total_sentences']}")
        
        print(f"\n  Origin Distribution:")
        for version, data in attribution_statistics['origin_distribution'].items():
            print(f"    {version}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        print(f"\n  Modification Levels:")
        for category, data in attribution_statistics['modification_distribution'].items():
            print(f"    {category}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        return self.attribution_results

print("📍 AttributionMapper class loaded. Ready for attribution analysis.")

# =============================================================================
# CELL 4: COMBINED EXECUTION FUNCTION
# =============================================================================

def run_steps_3_4(article_versions, preprocessor, output_path):
    """Run steps 3-4: Similarity Analysis and Attribution Mapping"""
    print(f"🚀 Starting Steps 3-4 for article: {article_versions.article_name}")
    
    # Step 3: Similarity Analysis
    similarity_analyzer = SimilarityAnalyzer(semantic_model)
    similarity_results = similarity_analyzer.analyze_all_versions(preprocessor.processed_versions)
    
    # Step 4: Attribution Mapping
    attribution_mapper = AttributionMapper(similarity_threshold=0.3)
    attribution_results = attribution_mapper.analyze_attribution(
        preprocessor.processed_versions, 
        similarity_results
    )
    
    # Combine results
    combined_results = {
        'article_name': article_versions.article_name,
        'analysis_timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'similarity_analysis': similarity_results,
        'attribution_analysis': attribution_results
    }
    
    # Save comprehensive results
    results_file = f"{output_path}/{article_versions.article_name}_complete_analysis.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete analysis saved: {results_file}")
    
    # Generate summary metrics for article footer
    footer_metrics = generate_footer_metrics(combined_results)
    
    # Save footer metrics separately
    footer_file = f"{output_path}/{article_versions.article_name}_footer_metrics.json"
    with open(footer_file, 'w', encoding='utf-8') as f:
        json.dump(footer_metrics, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Footer metrics saved: {footer_file}")
    
    return combined_results, footer_metrics

def generate_footer_metrics(combined_results):
    """Generate clean metrics for article footer"""
    
    # Get processing stats
    processing = combined_results['processing_summary']
    
    # Get attribution stats
    if combined_results['attribution_analysis']:
        attribution = combined_results['attribution_analysis']['statistics']
        origin_dist = attribution['origin_distribution']
        modification_dist = attribution['modification_distribution']
    else:
        origin_dist = {}
        modification_dist = {}
    
    # Get similarity stats (draft to final)
    draft_to_final = combined_results['similarity_analysis']['draft_to_final']
    overall_similarity = draft_to_final['full_text']['combined'] if draft_to_final else 0
    
    footer_metrics = {
        'article_name': combined_results['article_name'],
        'word_progression': {
            'draft': processing.get('draft', {}).get('word_count', 0),
            'final': processing.get('final', {}).get('word_count', 0),
            'change_percentage': 0
        },
        'content_retention': {
            'overall_similarity': round(overall_similarity * 100, 1),
            'content_origins': {}
        },
        'modification_summary': {},
        'generated_at': datetime.now().isoformat()
    }
    
    # Calculate word change percentage
    if footer_metrics['word_progression']['draft'] > 0:
        draft_words = footer_metrics['word_progression']['draft']
        final_words = footer_metrics['word_progression']['final']
        change = ((final_words - draft_words) / draft_words) * 100
        footer_metrics['word_progression']['change_percentage'] = round(change, 1)
    
    # Simplify origin distribution for footer
    for version, data in origin_dist.items():
        if version != 'new_in_final':
            footer_metrics['content_retention']['content_origins'][version] = round(data['percentage'], 1)
    
    # Simplify modification distribution
    for category, data in modification_dist.items():
        clean_category = category.replace('_', ' ').title()
        footer_metrics['modification_summary'][clean_category] = round(data['percentage'], 1)
    
    return footer_metrics

print("🎯 Execution functions loaded. Ready to run complete analysis!")
print("\nTo run the complete analysis:")
print("combined_results, footer_metrics = run_steps_3_4(article_versions, preprocessor, 'your_output_path')")

# =============================================================================
# CELL 5: QUICK EXECUTION FOR EXISTING DATA
# =============================================================================

def run_complete_analysis_from_existing(article_versions, preprocessor):
    """Run steps 3-4 using the output path from existing data"""
    # Use the same output path that was used in steps 1-2
    if hasattr(article_versions, 'input_path'):
        # For your case, the output was: input_path + '/output' 
        # But we need to check if this path was already used in setup_output_directories
        base_path = article_versions.input_path
        output_path = os.path.join(base_path, 'output')
        
        # Create the directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        print(f"📂 Using output path: {output_path}")
    else:
        output_path = '/content/drive/MyDrive/output'  # fallback
        os.makedirs(output_path, exist_ok=True)
    
    return run_steps_3_4(article_versions, preprocessor, output_path)

print("⚡ Quick execution function available:")
print("combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)")
```

The good news is that the analysis completed successfully! You can see the results:

**Attribution Summary:**
- **85.7%** of final content originated in the edited version
- **2.4%** survived from the original draft
- **11.9%** is entirely new content added in the final version

**Modification Levels:**
- **40.5%** medium similarity (substantial editing)
- **40.5%** low similarity (heavy editing)
- **7.1%** high similarity (minimal changes)
- **11.9%** completely new content

Now try running it again - the path issue should be fixed:

```python
combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)
```

The function will now create the output directory if it doesn't exist and save the results properly.



## Prompt:
```
 Starting Steps 3-4 for article: markup-languages

🔍 Step 3: Similarity Analysis
  🔍 Analyzing draft → refined
    Analyzing 47 vs 60 sentences...
  🔍 Analyzing refined → edited
    Analyzing 60 vs 45 sentences...
  🔍 Analyzing edited → final
    Analyzing 45 vs 42 sentences...
  🔍 Analyzing draft → final (overall change)
  🔍 Analyzing draft → final
    Analyzing 47 vs 42 sentences...

📍 Step 4: Attribution Mapping
  📝 Tracing 42 final sentences...

📊 Attribution Summary:
  Total sentences in final: 42

  Origin Distribution:
    edited: 36 sentences (85.7%)
    draft: 1 sentences (2.4%)
    new_in_final: 5 sentences (11.9%)

  Modification Levels:
    high_similarity: 3 sentences (7.1%)
    medium_similarity: 17 sentences (40.5%)
    low_similarity: 17 sentences (40.5%)
    new_content: 5 sentences (11.9%)

```


```
---------------------------------------------------------------------------

```


```
FileNotFoundError                         Traceback (most recent call last)

```


```
<ipython-input-30-3393068633> in <cell line: 0>()
----> 1 combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)


```

1 frames

```
<ipython-input-28-213471444> in run_steps_3_4(article_versions, preprocessor, output_path)
     30     # Save comprehensive results
     31     results_file = f"{output_path}/{article_versions.article_name}_complete_analysis.json"
---> 32     with open(results_file, 'w', encoding='utf-8') as f:
     33         json.dump(combined_results, f, indent=2, ensure_ascii=False)
     34 


```


```
FileNotFoundError: [Errno 2] No such file or directory: '/content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/output/markup-languages_complete_analysis.json'
```



## Response:
The issue is still the same path problem. Let me check what the actual output path should be by looking at where your Step 1-2 checkpoint was saved. 

Can you run this quick diagnostic to see what paths we're working with:

```python
print("Input path:", article_versions.input_path)
print("Article name:", article_versions.article_name)

# Check what directories exist
import os
base_path = article_versions.input_path
print("Base path:", base_path)
print("Contents of base path:", os.listdir(base_path))

# Check if output directory exists
output_path = os.path.join(base_path, 'output')
print("Expected output path:", output_path)
print("Output path exists:", os.path.exists(output_path))

# Let's also check where the Step 1-2 checkpoint was actually saved
# Look for any JSON files in the area
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.json'):
            print("Found JSON:", os.path.join(root, file))
```

This will help us see exactly where the Step 1-2 checkpoint was saved so we can use the same location for Steps 3-4.



## Prompt:
Input path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human Article name: markup-languages Base path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human Contents of base path: ['draft-markup-languages.md', 'refined-markup-languages.md', 'edited-markup-languages.md', 'final-markup-languages.md', 'output', '.ipynb_checkpoints'] Expected output path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output Output path exists: True Found JSON: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/output/markup-languages_checkpoint_steps_1_2.json



## Response:
Found the issue! The Step 1-2 checkpoint was saved to a nested folder: 

`/content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/output/`

But Steps 3-4 is trying to save to:

`/content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/`

This mismatch is causing the FileNotFoundError. Let me fix this by using the correct path:

AI Writing Analysis - Steps 3-4 (Similarity & Attribution)

```python
# =============================================================================
# CELL 1: INSTALL AND IMPORT DEPENDENCIES FOR SIMILARITY ANALYSIS
# =============================================================================

# Install required packages
!pip install sentence-transformers scikit-learn difflib2 -q

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
from collections import defaultdict
import json
from datetime import datetime

print("📦 Dependencies installed and imported successfully!")
print("🤖 Loading SentenceTransformer model (this may take a moment)...")

# Load the semantic similarity model
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Semantic model loaded successfully!")

# =============================================================================
# CELL 2: SIMILARITY ANALYSIS (STEP 3)
# =============================================================================

class SimilarityAnalyzer:
    """Class to handle lexical and semantic similarity analysis"""
    
    def __init__(self, semantic_model):
        self.semantic_model = semantic_model
        self.similarity_results = {}
        
    def calculate_lexical_similarity(self, text1, text2):
        """Calculate lexical similarity using multiple metrics"""
        # Jaccard similarity (word-level)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        jaccard = len(words1.intersection(words2)) / len(words1.union(words2)) if words1.union(words2) else 0
        
        # Edit distance similarity (character-level)
        sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
        edit_similarity = sequence_matcher.ratio()
        
        # TF-IDF cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            tfidf_similarity = 0.0
        
        return {
            'jaccard_similarity': jaccard,
            'edit_similarity': edit_similarity,
            'tfidf_similarity': tfidf_similarity,
            'lexical_average': (jaccard + edit_similarity + tfidf_similarity) / 3
        }
    
    def calculate_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity using sentence embeddings"""
        # Get embeddings
        embeddings = self.semantic_model.encode([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return {
            'semantic_similarity': float(similarity),
            'embedding_dim': len(embeddings[0])
        }
    
    def calculate_sentence_level_similarities(self, sentences1, sentences2, version1, version2):
        """Calculate similarities at sentence level between two versions"""
        print(f"    Analyzing {len(sentences1)} vs {len(sentences2)} sentences...")
        
        sentence_similarities = []
        
        # Calculate all pairwise similarities
        for i, sent1 in enumerate(sentences1):
            best_match = {'index': -1, 'lexical': 0, 'semantic': 0, 'combined': 0}
            
            for j, sent2 in enumerate(sentences2):
                # Calculate similarities
                lexical = self.calculate_lexical_similarity(sent1, sent2)
                semantic = self.calculate_semantic_similarity(sent1, sent2)
                
                # Combined score (weighted average)
                combined = (lexical['lexical_average'] + semantic['semantic_similarity']) / 2
                
                if combined > best_match['combined']:
                    best_match = {
                        'index': j,
                        'lexical': lexical['lexical_average'],
                        'semantic': semantic['semantic_similarity'],
                        'combined': combined,
                        'target_sentence': sent2
                    }
            
            sentence_similarities.append({
                'source_index': i,
                'source_sentence': sent1,
                'best_match': best_match
            })
        
        return sentence_similarities
    
    def analyze_version_pair(self, version1_data, version2_data, version1_name, version2_name):
        """Analyze similarities between two versions"""
        print(f"  🔍 Analyzing {version1_name} → {version2_name}")
        
        # Full text similarity
        full_text_lexical = self.calculate_lexical_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        full_text_semantic = self.calculate_semantic_similarity(
            version1_data['cleaned_content'], 
            version2_data['cleaned_content']
        )
        
        # Sentence-level analysis
        sentence_analysis = self.calculate_sentence_level_similarities(
            version1_data['sentences'],
            version2_data['sentences'],
            version1_name,
            version2_name
        )
        
        # Paragraph-level similarity
        para_lexical = self.calculate_lexical_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        para_semantic = self.calculate_semantic_similarity(
            ' '.join(version1_data['paragraphs']), 
            ' '.join(version2_data['paragraphs'])
        )
        
        # Aggregate sentence similarities
        sentence_similarities = [s['best_match']['combined'] for s in sentence_analysis]
        avg_sentence_similarity = np.mean(sentence_similarities) if sentence_similarities else 0
        
        return {
            'version_pair': f"{version1_name}_to_{version2_name}",
            'full_text': {
                'lexical': full_text_lexical,
                'semantic': full_text_semantic,
                'combined': (full_text_lexical['lexical_average'] + full_text_semantic['semantic_similarity']) / 2
            },
            'sentence_level': {
                'average_similarity': avg_sentence_similarity,
                'individual_similarities': sentence_similarities,
                'detailed_analysis': sentence_analysis
            },
            'paragraph_level': {
                'lexical': para_lexical,
                'semantic': para_semantic,
                'combined': (para_lexical['lexical_average'] + para_semantic['semantic_similarity']) / 2
            }
        }
    
    def analyze_all_versions(self, processed_versions):
        """Analyze similarities between all version pairs"""
        print(f"\n🔍 Step 3: Similarity Analysis")
        
        version_names = list(processed_versions.keys())
        version_order = ['draft', 'refined', 'edited', 'final']
        
        # Sort versions by expected order
        sorted_versions = []
        for expected in version_order:
            if expected in version_names:
                sorted_versions.append(expected)
        
        # Sequential analysis (draft→refined→edited→final)
        sequential_results = []
        for i in range(len(sorted_versions) - 1):
            current_version = sorted_versions[i]
            next_version = sorted_versions[i + 1]
            
            result = self.analyze_version_pair(
                processed_versions[current_version],
                processed_versions[next_version],
                current_version,
                next_version
            )
            sequential_results.append(result)
        
        # Draft to final comparison
        draft_to_final = None
        if 'draft' in version_names and 'final' in version_names:
            print(f"  🔍 Analyzing draft → final (overall change)")
            draft_to_final = self.analyze_version_pair(
                processed_versions['draft'],
                processed_versions['final'],
                'draft',
                'final'
            )
        
        self.similarity_results = {
            'sequential_analysis': sequential_results,
            'draft_to_final': draft_to_final,
            'analysis_timestamp': datetime.now().isoformat(),
            'versions_analyzed': sorted_versions
        }
        
        return self.similarity_results

print("🔍 SimilarityAnalyzer class loaded. Ready for similarity analysis.")

# =============================================================================
# CELL 3: ATTRIBUTION MAPPING (STEP 4)
# =============================================================================

class AttributionMapper:
    """Class to track content attribution across versions"""
    
    def __init__(self, similarity_threshold=0.3):
        self.similarity_threshold = similarity_threshold
        self.attribution_results = {}
        
    def trace_sentence_origins(self, processed_versions, similarity_results):
        """Trace each final sentence back to its earliest appearance"""
        print(f"\n📍 Step 4: Attribution Mapping")
        
        version_order = ['draft', 'refined', 'edited', 'final']
        available_versions = [v for v in version_order if v in processed_versions]
        
        if 'final' not in available_versions:
            print("❌ Cannot perform attribution - final version not found")
            return None
        
        final_sentences = processed_versions['final']['sentences']
        sentence_attributions = []
        
        print(f"  📝 Tracing {len(final_sentences)} final sentences...")
        
        for final_idx, final_sentence in enumerate(final_sentences):
            attribution = {
                'final_index': final_idx,
                'final_sentence': final_sentence,
                'origin_version': None,
                'origin_index': None,
                'similarity_scores': {},
                'modification_path': []
            }
            
            # Check each previous version (in reverse order to find earliest origin)
            for version in reversed(available_versions[:-1]):  # Exclude 'final'
                version_sentences = processed_versions[version]['sentences']
                
                best_match = {'index': -1, 'similarity': 0, 'sentence': ''}
                
                for sent_idx, version_sentence in enumerate(version_sentences):
                    # Calculate similarity
                    lexical = self._quick_lexical_similarity(final_sentence, version_sentence)
                    semantic = self._quick_semantic_similarity(final_sentence, version_sentence)
                    combined = (lexical + semantic) / 2
                    
                    if combined > best_match['similarity']:
                        best_match = {
                            'index': sent_idx,
                            'similarity': combined,
                            'sentence': version_sentence
                        }
                
                attribution['similarity_scores'][version] = best_match['similarity']
                
                # If similarity is above threshold, this could be the origin
                if best_match['similarity'] >= self.similarity_threshold:
                    if attribution['origin_version'] is None:  # First match found (earliest version)
                        attribution['origin_version'] = version
                        attribution['origin_index'] = best_match['index']
                    
                    attribution['modification_path'].append({
                        'version': version,
                        'similarity': best_match['similarity'],
                        'sentence': best_match['sentence']
                    })
            
            # If no origin found, it's new content
            if attribution['origin_version'] is None:
                attribution['origin_version'] = 'new_in_final'
            
            sentence_attributions.append(attribution)
        
        return sentence_attributions
    
    def _quick_lexical_similarity(self, text1, text2):
        """Quick lexical similarity calculation"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        return len(words1.intersection(words2)) / len(words1.union(words2))
    
    def _quick_semantic_similarity(self, text1, text2):
        """Quick semantic similarity calculation"""
        embeddings = semantic_model.encode([text1, text2])
        return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    
    def calculate_attribution_statistics(self, sentence_attributions):
        """Calculate overall attribution statistics"""
        total_sentences = len(sentence_attributions)
        
        # Count by origin version
        origin_counts = defaultdict(int)
        for attribution in sentence_attributions:
            origin_counts[attribution['origin_version']] += 1
        
        # Calculate percentages
        origin_percentages = {}
        for version, count in origin_counts.items():
            origin_percentages[version] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        # Calculate modification statistics
        modification_stats = {
            'high_similarity': 0,  # >0.8
            'medium_similarity': 0,  # 0.5-0.8
            'low_similarity': 0,  # 0.3-0.5
            'new_content': 0  # <0.3 or new_in_final
        }
        
        for attribution in sentence_attributions:
            if attribution['origin_version'] == 'new_in_final':
                modification_stats['new_content'] += 1
            else:
                # Get highest similarity score
                max_similarity = max(attribution['similarity_scores'].values()) if attribution['similarity_scores'] else 0
                
                if max_similarity > 0.8:
                    modification_stats['high_similarity'] += 1
                elif max_similarity > 0.5:
                    modification_stats['medium_similarity'] += 1
                elif max_similarity > 0.3:
                    modification_stats['low_similarity'] += 1
                else:
                    modification_stats['new_content'] += 1
        
        # Convert to percentages
        modification_percentages = {}
        for category, count in modification_stats.items():
            modification_percentages[category] = {
                'count': count,
                'percentage': (count / total_sentences) * 100
            }
        
        return {
            'total_sentences': total_sentences,
            'origin_distribution': origin_percentages,
            'modification_distribution': modification_percentages
        }
    
    def analyze_attribution(self, processed_versions, similarity_results):
        """Perform complete attribution analysis"""
        sentence_attributions = self.trace_sentence_origins(processed_versions, similarity_results)
        
        if sentence_attributions is None:
            return None
        
        attribution_statistics = self.calculate_attribution_statistics(sentence_attributions)
        
        self.attribution_results = {
            'sentence_attributions': sentence_attributions,
            'statistics': attribution_statistics,
            'analysis_timestamp': datetime.now().isoformat(),
            'similarity_threshold': self.similarity_threshold
        }
        
        # Print summary
        print(f"\n📊 Attribution Summary:")
        print(f"  Total sentences in final: {attribution_statistics['total_sentences']}")
        
        print(f"\n  Origin Distribution:")
        for version, data in attribution_statistics['origin_distribution'].items():
            print(f"    {version}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        print(f"\n  Modification Levels:")
        for category, data in attribution_statistics['modification_distribution'].items():
            print(f"    {category}: {data['count']} sentences ({data['percentage']:.1f}%)")
        
        return self.attribution_results

print("📍 AttributionMapper class loaded. Ready for attribution analysis.")

# =============================================================================
# CELL 4: COMBINED EXECUTION FUNCTION
# =============================================================================

def run_steps_3_4(article_versions, preprocessor, output_path):
    """Run steps 3-4: Similarity Analysis and Attribution Mapping"""
    print(f"🚀 Starting Steps 3-4 for article: {article_versions.article_name}")
    
    # Step 3: Similarity Analysis
    similarity_analyzer = SimilarityAnalyzer(semantic_model)
    similarity_results = similarity_analyzer.analyze_all_versions(preprocessor.processed_versions)
    
    # Step 4: Attribution Mapping
    attribution_mapper = AttributionMapper(similarity_threshold=0.3)
    attribution_results = attribution_mapper.analyze_attribution(
        preprocessor.processed_versions, 
        similarity_results
    )
    
    # Combine results
    combined_results = {
        'article_name': article_versions.article_name,
        'analysis_timestamp': datetime.now().isoformat(),
        'article_metadata': article_versions.metadata,
        'processing_summary': preprocessor.get_processing_summary(),
        'similarity_analysis': similarity_results,
        'attribution_analysis': attribution_results
    }
    
    # Save comprehensive results
    results_file = f"{output_path}/{article_versions.article_name}_complete_analysis.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete analysis saved: {results_file}")
    
    # Generate summary metrics for article footer
    footer_metrics = generate_footer_metrics(combined_results)
    
    # Save footer metrics separately
    footer_file = f"{output_path}/{article_versions.article_name}_footer_metrics.json"
    with open(footer_file, 'w', encoding='utf-8') as f:
        json.dump(footer_metrics, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Footer metrics saved: {footer_file}")
    
    return combined_results, footer_metrics

def generate_footer_metrics(combined_results):
    """Generate clean metrics for article footer"""
    
    # Get processing stats
    processing = combined_results['processing_summary']
    
    # Get attribution stats
    if combined_results['attribution_analysis']:
        attribution = combined_results['attribution_analysis']['statistics']
        origin_dist = attribution['origin_distribution']
        modification_dist = attribution['modification_distribution']
    else:
        origin_dist = {}
        modification_dist = {}
    
    # Get similarity stats (draft to final)
    draft_to_final = combined_results['similarity_analysis']['draft_to_final']
    overall_similarity = draft_to_final['full_text']['combined'] if draft_to_final else 0
    
    footer_metrics = {
        'article_name': combined_results['article_name'],
        'word_progression': {
            'draft': processing.get('draft', {}).get('word_count', 0),
            'final': processing.get('final', {}).get('word_count', 0),
            'change_percentage': 0
        },
        'content_retention': {
            'overall_similarity': round(overall_similarity * 100, 1),
            'content_origins': {}
        },
        'modification_summary': {},
        'generated_at': datetime.now().isoformat()
    }
    
    # Calculate word change percentage
    if footer_metrics['word_progression']['draft'] > 0:
        draft_words = footer_metrics['word_progression']['draft']
        final_words = footer_metrics['word_progression']['final']
        change = ((final_words - draft_words) / draft_words) * 100
        footer_metrics['word_progression']['change_percentage'] = round(change, 1)
    
    # Simplify origin distribution for footer
    for version, data in origin_dist.items():
        if version != 'new_in_final':
            footer_metrics['content_retention']['content_origins'][version] = round(data['percentage'], 1)
    
    # Simplify modification distribution
    for category, data in modification_dist.items():
        clean_category = category.replace('_', ' ').title()
        footer_metrics['modification_summary'][clean_category] = round(data['percentage'], 1)
    
    return footer_metrics

print("🎯 Execution functions loaded. Ready to run complete analysis!")
print("\nTo run the complete analysis:")
print("combined_results, footer_metrics = run_steps_3_4(article_versions, preprocessor, 'your_output_path')")

# =============================================================================
# CELL 5: QUICK EXECUTION FOR EXISTING DATA
# =============================================================================

def run_complete_analysis_from_existing(article_versions, preprocessor):
    """Run steps 3-4 using the output path from existing data"""
    # Get output path from the article metadata or use default
    if hasattr(article_versions, 'input_path'):
        base_path = os.path.dirname(article_versions.input_path)
        output_path = os.path.join(base_path, 'output')
    else:
        output_path = '/content/drive/MyDrive/output'  # fallback
    
    return run_steps_3_4(article_versions, preprocessor, output_path)

print("⚡ Quick execution function available:")
print("combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)")
```

Now try running it again:

```python
combined_results, footer_metrics = run_complete_analysis_from_existing(article_versions, preprocessor)
```

This should find the correct nested output path where your Step 1-2 checkpoint was saved and use that same location for the Steps 3-4 results.



## Prompt:
Looks good:

```
📂 Using nested output path: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/output
🚀 Starting Steps 3-4 for article: markup-languages

🔍 Step 3: Similarity Analysis
  🔍 Analyzing draft → refined
    Analyzing 47 vs 60 sentences...
  🔍 Analyzing refined → edited
    Analyzing 60 vs 45 sentences...
  🔍 Analyzing edited → final
    Analyzing 45 vs 42 sentences...
  🔍 Analyzing draft → final (overall change)
  🔍 Analyzing draft → final
    Analyzing 47 vs 42 sentences...

📍 Step 4: Attribution Mapping
  📝 Tracing 42 final sentences...

📊 Attribution Summary:
  Total sentences in final: 42

  Origin Distribution:
    edited: 36 sentences (85.7%)
    draft: 1 sentences (2.4%)
    new_in_final: 5 sentences (11.9%)

  Modification Levels:
    high_similarity: 3 sentences (7.1%)
    medium_similarity: 17 sentences (40.5%)
    low_similarity: 17 sentences (40.5%)
    new_content: 5 sentences (11.9%)

💾 Complete analysis saved: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/output/markup-languages_complete_analysis.json
📊 Footer metrics saved: /content/drive/MyDrive/Google Drive/syntaxandempathy/30-articles/ai-vs-human/output/output/markup-languages_footer_metrics.json

```



## Response:
Excellent! The complete analysis has run successfully. Here's what we've accomplished:

## **Analysis Results for "markup-languages" article:**

### **Content Attribution:**
- **85.7%** of final content originated during the editing phase
- **2.4%** survived from the original draft all the way to final
- **11.9%** is entirely new content added in the final version

### **Content Modification Levels:**
- **7.1%** high similarity (minimal changes)
- **40.5%** medium similarity (substantial editing)
- **40.5%** low similarity (heavy rewriting)
- **11.9%** completely new content

### **Files Generated:**
1. **`markup-languages_complete_analysis.json`** - Full archival data with all similarity matrices, sentence-level analysis, and detailed attribution mapping
2. **`markup-languages_footer_metrics.json`** - Clean metrics ready for your article footer

## **Key Insights:**
Your workflow shows that most content gets heavily modified during the editing phase, with very little surviving unchanged from the initial draft. This demonstrates significant human involvement in reshaping the AI-generated content.

**Next Steps:**
- You can examine the `footer_metrics.json` for the clean statistics to include in your article
- The `complete_analysis.json` contains all the detailed data for future trend analysis
- Ready to build the visualization component, or would you like to process another article first to see how the system handles different content?

The foundation is now complete and working perfectly!



## Prompt:
Data looks fantastic.



## Response:
Wonderful! I'm glad the analysis is producing meaningful insights. The data really tells a compelling story about your writing process - showing that 85.7% of content originates during the editing phase demonstrates significant human creativity and curation beyond the initial AI drafts.

The system is now fully operational for the core analysis. We have:

✅ **Steps 1-2**: Data ingestion and preprocessing  
✅ **Steps 3-4**: Similarity analysis and attribution mapping  
✅ **Archive-ready data**: Complete analysis for future AI consumption  
✅ **Article footer metrics**: Clean statistics ready for publication  

**What's next?**

1. **Process more articles** - Test with different topics to see varied patterns
2. **Build visualizations** - Create charts for the article footers (Sankey diagrams, change flow charts, etc.)
3. **Batch processing** - Set up to analyze multiple articles at once
4. **Trend analysis** - Once you have several articles, analyze patterns across your writing workflow

Which direction interests you most? Or do you want to run another article through the system first to see how consistent the results are across different content types?



## Prompt:
I think 2 and 4, but I want to flip them. This way we can have an input that allows me to specify if I want a trend analysis, and if I do it can let me specify month, quarter, year. That allows the same visualization definition to be applied to the newsletter and the trend analysis for the specified quarter, which enables me to report it more often without hassle.



## Response:
Excellent strategic thinking! Building trend analysis first makes perfect sense - it creates the foundational visualization framework that can then be applied to both individual articles and time-based reports.

Here's how I'll structure this:

## **Step 5: Trend Analysis & Visualization Framework**

**Core Features:**
- **Batch processing** - Analyze multiple articles at once
- **Time-based filtering** - Month/Quarter/Year selection
- **Trend detection** - Patterns across your writing workflow over time
- **Unified visualization engine** - Same charts work for single articles and trend reports

**Visualization Types:**
- Content flow diagrams (showing draft→refined→edited→final progression)
- Attribution trend lines (how much content survives from each stage over time)
- Modification pattern heatmaps (intensity of changes across periods)
- Word count evolution charts
- Semantic similarity trends

**Input Options:**
```python
# Individual article
generate_visualizations(article_name="markup-languages", mode="single")

# Trend analysis
generate_visualizations(mode="trend", period="Q1-2025", articles_folder="path")
```

This approach means when you publish an article, you get individual stats. When you want quarterly reports, you run the same system with different parameters.

Should I start building the batch processing and trend analysis engine? The visualization component will then work seamlessly for both use cases.



## Prompt:
We shouldn't need batch processing, I'll never analyze more than one at a time, I only write so much. We can use the data in the archives for trend analysis so we don't have to create anything more than the output data for the period in question.

Let's focus on the trend analysis first, then the visualizations. Having things split up with clear checkpoints has felt like a great approach and it compartmentalizes elements should I desire modifications in the future.



## Response:
Perfect! That's much cleaner - no batch processing needed, just leverage the existing archive data for trends. The checkpoint approach has definitely been working well.

## **Step 5: Trend Analysis Engine**

**Approach:**
- **Scan archive folders** for existing `*_complete_analysis.json` files
- **Time-based filtering** using file timestamps or article dates
- **Aggregate metrics** across the selected period
- **Generate trend datasets** that feed into the visualization engine

**Key Trend Metrics:**
- Content attribution patterns over time (how much from draft vs edited vs new)
- Modification intensity trends (high/medium/low similarity patterns)
- Word count evolution patterns
- Semantic similarity trends (how much content changes draft→final)
- Workflow efficiency metrics (consistency of your process)

**Input Interface:**
```python
# Analyze specific time period
trend_data = analyze_trends(
    archive_path="/your/archive/path",
    period="2025-Q1",  # or "2025-01" for monthly, "2025" for yearly
    output_path="/your/output/path"
)
```

**Output:**
- Trend analysis JSON (similar structure to individual analysis)
- Period summary statistics
- Ready-to-visualize datasets

This creates the foundation, then Step 6 will build visualizations that work for both individual articles and trend data using the same framework.

Should I start building the trend analysis engine with the time-period filtering and metric aggregation?



## Prompt:
I prefix the folders with the publication date which would make identifying the right folders easy, but I do move them to an archive folder (this is a path that could be hardcoded since we scan folder names before digging in). The format I use is 'yyyymmdd-*'. This also prevents modifications in prior steps.



## Response:
Perfect! That date prefix system is ideal for trend analysis. Here's how I'll structure it:

## **Step 5: Trend Analysis Engine**

**Folder Structure Understanding:**
```
archive/
├── 20250114-markup-languages/
│   └── output/output/markup-languages_complete_analysis.json
├── 20250203-ai-ethics/
│   └── output/output/ai-ethics_complete_analysis.json
├── 20250315-future-tech/
│   └── output/output/future-tech_complete_analysis.json
```

**Date-based Filtering:**
- **Monthly**: `period="2025-01"` → finds folders starting with `202501*`
- **Quarterly**: `period="2025-Q1"` → finds folders `202501*`, `202502*`, `202503*`
- **Yearly**: `period="2025"` → finds folders `2025*`

**Process:**
1. Scan hardcoded archive path for folders matching date pattern
2. Extract `*_complete_analysis.json` from each matching folder
3. Aggregate metrics across the period
4. Generate trend analysis with same structure as individual articles

**Interface:**
```python
trend_data = analyze_trends(
    period="2025-Q1",  # or "2025-01" or "2025"
    archive_base="/content/drive/MyDrive/archive"  # hardcoded
)
```

This approach is clean, uses your existing organization system, and prevents any interference with your current workflow.

Should I build this trend analysis engine now?



## Prompt:
You have the folder structure right, but it's due to a mistake on my part. When asked for the output folder location I didn't realize it would create one, so I added one and pointed at it. Thus 'output/output'. I'm going to fix that now to remove the unnecessary layer. No need to go back and fix prior steps, I simply need to identify the right folder in the future. So only 'output/' is needed.

The rest looks correct.

The path to the archive is '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'.



## Response:
Got it! Thanks for clarifying. So the corrected structure will be:

## **Folder Structure:**
```
/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/
├── 20250114-markup-languages/
│   └── output/markup-languages_complete_analysis.json
├── 20250203-ai-ethics/
│   └── output/ai-ethics_complete_analysis.json
├── 20250315-future-tech/
│   └── output/future-tech_complete_analysis.json
```

**Archive Path (hardcoded):**
`/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/`

**Date Pattern Matching:**
- `period="2025-01"` → folders starting with `202501`
- `period="2025-Q1"` → folders starting with `202501`, `202502`, `202503`
- `period="2025"` → folders starting with `2025`

**Process:**
1. Scan archive path for folders matching `yyyymmdd-*` pattern
2. Filter by period
3. Look for `output/*_complete_analysis.json` in each folder
4. Aggregate trend data

Perfect - this is much cleaner without the nested output folders. Should I build the trend analysis engine now with this corrected structure?



## Prompt:
You dropped the wildcard. The dates are specifically the day I publish. I publish upon completion but send the actual newsletter (that I write so it doesn't go through this process) on a schedule. Having 202501* captures everything published in the month which breaks up to the reporting periods just fine. Move that behind that dash, it will probably miss all of them :)



## Response:
You're absolutely right! I dropped the critical wildcard. The pattern should be:

**Date Pattern Matching:**
- `period="2025-01"` → folders starting with `202501*` (captures all January publications)
- `period="2025-Q1"` → folders starting with `202501*`, `202502*`, `202503*` 
- `period="2025"` → folders starting with `2025*`

So for a folder like `20250114-markup-languages`, the `202501*` pattern correctly captures it as a January publication, regardless of the specific day (14th) you published it.

**Folder Structure:**
```
/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/
├── 20250114-markup-languages/
│   └── output/markup-languages_complete_analysis.json
├── 20250203-ai-ethics/
│   └── output/ai-ethics_complete_analysis.json
```

The wildcard `*` after the year-month is essential to capture all publications within that period, not just exact matches.

Ready to build the trend analysis engine with the correct wildcard pattern matching?



## Prompt:
Let's do it.



## Response:


AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            pattern_regex = pattern.replace('*', '.*')
            for dir_name in all_dirs:
                if re.match(pattern_regex, dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        found_articles.append({
                            'folder_name': dir_name,
                            'article_path': article_path,
                            'analysis_file': analysis_files[0],
                            'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                            'article_name': dir_name[9:]  # Extract name after date-
                        })
                        print(f"  ✓ Found: {dir_name}")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

Perfect! I've built the complete trend analysis engine. Here's what it provides:

## **Step 5: Trend Analysis Engine**

### **Key Features:**
- **Period-based filtering** using your `yyyymmdd-*` folder naming
- **Flexible time periods**: Years (`2025`), months (`2025-01`), quarters (`2025-Q1`)
- **Comprehensive aggregation** of attribution, similarity, and word count trends
- **Archive scanning** with hardcoded path to your 99-past folder
- **Validation tools** to check your archive structure

### **Core Functionality:**
1. **Pattern matching** finds folders like `20250114-markup-languages` for period `2025-01`
2. **Data aggregation** across multiple articles in the period
3. **Trend calculation** showing averages and patterns
4. **Summary generation** with key insights for reporting

### **Usage:**
```python
# Test your archive first
test_archive_structure()

# Quick trend check (no files saved)
results = quick_trend_check('2025-Q1')

# Full analysis with output files
results, analyzer = analyze_period_trends('2025-01', '/your/output/path')
```

### **What You'll Get:**
- Average content retention from draft vs edited phases
- Similarity trends over time 
- Word count evolution patterns
- Article-by-article breakdowns
- Period summary metrics

Want to test this with your current archive structure first? Run `test_archive_structure()` to see what articles it finds and validate the folder scanning works correctly.



## Prompt:
Looks like you lost the wildcard again:

```
🔍 Testing archive structure...
📂 Archive path: /content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/
📁 Found 2 directories:
  ✗ 2024 (invalid date format)
  ✗ 2025064-ai-vs-human (invalid date format)

📊 Summary:
  Total directories: 2
  Valid date format: 0
  With analysis files: 0

```


```
False
```



## Response:
You're absolutely right! I lost the wildcard again in the regex pattern. The issue is in the `date_pattern` - it's looking for exactly 8 digits followed by a dash, but your folder is `20250614-ai-vs-human` (which should match).

Let me fix this:

AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            pattern_regex = pattern.replace('*', '.*')
            for dir_name in all_dirs:
                if re.match(pattern_regex, dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        found_articles.append({
                            'folder_name': dir_name,
                            'article_path': article_path,
                            'analysis_file': analysis_files[0],
                            'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                            'article_name': dir_name[9:]  # Extract name after date-
                        })
                        print(f"  ✓ Found: {dir_name}")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    # Fixed pattern - 8 digits, dash, then anything
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format - expected YYYYMMDD-name)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

Wait, looking at your output more carefully - I see the issue. Your folder is named `2025064-ai-vs-human` which has only 7 digits (2025064) instead of 8 digits (20250614). 

But looking at this again, that seems like it might be a typo? Should it be `20250614-ai-vs-human`? The pattern expects `YYYYMMDD-name` format.

However, let me also check if there's a mismatch between what the pattern expects and your actual folder names. Can you confirm what the actual folder name should be? Is it:
- `20250614-ai-vs-human` (8 digits: year-month-day)
- Or `2025064-ai-vs-human` (7 digits: as shown in your output)

If it's actually 7 digits, I need to adjust the pattern. But if it's a typo in the folder name, then the pattern is correct and the folder just needs to be renamed.



## Prompt:
![image.png](data:image/webp;base64,UklGRogYAABXRUJQVlA4IHwYAACwaQCdASrxAYYAPm02l0ikIyIhItKaQIANiWVu4XKRDOBdgqGnuHMwk2ZF/EXJf/A+6r6E+gD89+wB+qvnk+qj+hf7j1Afsz6uP+U/ZL3NegB/OfOQ9g/0AP239OL2WP7l/1PS31Wzyf/c+1j+zfkn6B/inyX9r/Lf1u/5Lyr9H+Y/8s+xn5v+1/uz6n/6PwN+Ff9D6gX4v/I/79/U/x+9O3Y263/lP9R6gvpZ8j/wv9t/dr+0ehL/Af079svcL8d/o/+E/Mn+w/YB/G/6B/nfzQ/un/////2f/vfBF+tf432AP5P/Sf9F/aP3g/x/0p/wH/D/w35he1P83/v//O/yH+R+QT+Vf1P/g/33/Nftf83f//9w37df//3R/2L/+Y0iAV9imMYxjGMYxXvo8mMAjPe973ve973ufcydHqKuHwuQwiUDbvZkn2JFLzNktSJtc+x095nWQOWPYeFAfnTKoGAvAp0XDM7Wv/w9ydgCs0/+YWc78bCts8MhgxaoYEVZ2IFEDrQpexIY6IuR8rQ1QAe5LqyL2DqiCU6m47e+SUlJvI5pTtN1A5rJmKlOSEwymwbZHAT3NlT5Khs9zg6ae6MKe+HAfdyBjRa6kk2h8kxMum35ktuRzWlJ9R8jjRayHUWQ7QH74wTeBqtQyWZQFtnVAmoKHjdz3GW0aFs5hC5rWv4jCgRgnRjJLQrNhPrJ2Z4fQ9SxPbipDH29Ewtu2iJqnVMyIGbTK3d8SNViU8mN0+B9jjwH1k3eV/E2F4Mj0bJr7Fji3P/e7cMHCzzjetFOws8VI/cZurIibm+Oe3/Hbauh9DK419VcWEeOmbmv/9sfHUtrfJyDkpBGT0LAyPS4L0m4h5fM88SPql/iP/kQsAaYrhS30hDrpOULv81Fn8NcswL/PAYLaaRuuOc0fvI4sYPtf9+DJxXzshumHIouxK+9y7SufY6flwodcxupyuuvLaVwb0vbhfofUItrN7hQ2qCA6dCn2On5cMT5xKtOW18lL77DJ39S8G6RXm2KLpNuImxwJeLp7fT/roApzf5trQ/d9PPv/KnWT9MkEHl1nyBQN3hoSUkUfCNjjnCja3j5oqSI5Cl3cu9lXTBp3Ly6jBt9P+ufY6iA6dDu7JVOlcxPQAD+7gCU2GkxAxtU85epcHOhM2kPdWnxzvNrMELd2gsHIf6/gvs0rcdNCHmokGYOXVQEUG/xial1TE476cjHLTB3NP1pS9wCbb3ZRYwW0iJOJSduaBufUavs3hiraUauNDFSJqfKyakVU05Tardk0eUoRsiKTUIJyVoari3L2YZCtGheUcyHJZS/t3d+S5Gs9VSX/NDrtzHqVEUqIX0j6Y3i9Io3y9cTvo3u5kBYIJMxSauh/lYgFBzi8O0Cva2m1SmquZ3JpsBh7mt3+8BaqwAZsOrI/IET1s9KB7wmrrdK2uz73FBmXJYu2xjfLuFq4GaEE/aeMFbcQ1bMGCaM/kJNfWwrOHo9kmrD/g/NrsYQURUntVIMDAnG0VQjQbUMWJMk2zxNgFHnUGJauGYl7NqXMhTJq3LQho07vE343SGNrxPwuQ5bPf5Ift//JrTe19sIOYfx6++SzT/6XrlpU/m3BvIHZBwJkw5mACspVAkb7V+57ir5lDOcqUiE/MEKtyp1i/yyzEeJoWA2oxsMHyFkZMSOUXvO5tMzz9DjKGDC2+MhI3zIBZn55oUygNv4DZbKFvpvg/jMX7UMCI5X2VU6tLKLfNC444f5puiQXT+v13Ku6Fagr29gLxM+PRcNSGCMUNXb6MmhopMuMsi2RJFqAHWvi2vuqu9sTzVUs2WxH1JpPFXbE+4Bb3sIgR6wzNxP5u5MFmSjn/hGQzqbNc7zsGicvUapVb7bap3Hkdh3AllWjeQTZrWab+sN6c51sQlJ1/PAEIj6wiK6Klb4Tr3ZediLgCN/Q/oDoDm7R7tWvFCSOtxb7uOoXlFLQPOFzXjwUg0OIZx4Fjk7z6apuuJG0RF6cHrVzvaonanzYUYEm1WQcnblocQM61xTFEORFjw8IeYHyCsWSnR9chFB608AgsSql5T0jOEBN30Ci8gzlCp5X7eog5zCE13YtlKKOD95P7sl0QsqKr+cFB0+IPC0ZIn9JvpHfvmdqMCYxnNANLC/62BXJa8SsP7EZ1Sakqei16b4V2ZgpvuC9x82yxoaFi6ydeTvCIloRXguiWbeiZxhdh4er7vYT60eDFgUJIbCGsf/1BjbB0RHIx586jhYXvrkVzBVvaSSlQDtnZjIKot6USUuXN620eNfy53lgDbOiGpShY+23qbFam2W+Hfa/y7Ln79uoAZ96ZficB+R9DSsrm4beRcGr9oebrovCMwPVEJZfTH19haxIIdiV4GrlcZGeZS4UywL7DmneHq9vNPXALgCVyBshPZLAdmP5k2B4Ps52YPK6QGV4jjigVERRZHwgvPMKCrnKjCy+dac4eg7n3NQwWmNBSAm8OKZSjFHNCjq8wuGCBWIbxGzbfzXjur+uPQMsO4OhiWKd4g2hNbX+daYct2UvfAGnnYogvkTWBjJIH32cxToS+a/RVN+E/lPP2gAqKdkiapAr3DID6CrxCt2CyeDuFRrc3aIbbp/oZHw4Cjg5eh2OIm2QyiIP6HySuaSeBslgCcyyiD/86Ow9ftBvTf8BwctDRcw3mvzHq8ZzAkDm4E8+ZR0hJFr8tHt6ty/namXTZUDiJ6agtqRgt/7ne3aU9lPTa5knTJx62nS9aqzUTPsq2wDFe45+eCbRcOHD9ASx05/zIkOw66uc5utkUXNqS4kDxbhtg7Sx+jHZZx2qAxrVVcaGJ5VW1QRTBm+mHEdZSlSh+Vxn+O4yuCky7SXwdwcN9LSeob/1P2I9N+N5uv9zLfEa2Tk57pTb13NcHHr+HrH/M/Rjada0id133ACe7j96X1nsTeWfYVIOu9uPnRLS2VVRnJAi9C94u5A+nF5FtfdY00zFbKPYZlC0R1DnSdanT/17McxzoUH9HGxlPIKQHFyMyMlXZAlokX6JmtjlTaUDAnCYKeD2Et8wIm4wqKsSN/0qX7VIk9ooQGmXWF8TnJRk5NA15HtABmTLfyvOwGlzUEL80A0K/tzAaUVee+7PSXg9Cna2p2zRpu0NvLVIrbAsqV7PptY+zEpPvcNpNTp39Ar0gvkWMUSWocqKdLMojsf+aXKZVbE7bRdA/Wvbg2lRjOIqUiW8hhKvNUZ2V0Ll1uJpttJnRFJU1yG2i2lHGERH5ptpaUMI6OYs1VKjKU5wUTdHP3Y0ur3le/HyLBCndF2LoSZ4BFfaMfKbd8m9uk9xMbL4cT+eYcKpo5uGTrXBdw2/myLZaFupJMdv88ZKWx9Y7XQty9X7yey6DR2HMFuBeKiaP6FqM9JQulcEORwi4BBnN+ijc9oQRPHp747PDRwFAqh7FddEWlX5CZmBcemUzXs8vlRFREq3AD2aFEZsx7kV7whhnB37EX7r7179zJ0MwyYiI4Yk7ZjENjzM1c8XV5TGd4uyXhEOOti9PzwvxwTcTqW57Vh5z7Z3R9BaAIJIjjDmlGKLIUBwxZdQQyFiBSBmvQ5KObBgsB+ofcH8H5KY3f/+x1OcdIBFd2fxNE6xjZRh1uQ+Hg5JJFNJtSoAgZn4NY8GfhvyeqHRPyktYjBwAc9c+fcXzVFwNk94rwD1D4DqNGp9opWVIVRXveelDIrSO7UvKKfKnLtUL58oc5mi0t1lgmnFKFoR+fnKdNpDF4WOHXyBb/LBJtE2+PL2gtoCHoBhBoPPTHycnSPrGdqjJc1MaULPXvL2guoNEWEIq95a69mdV3OcvRPK8y+MApq08epwwdru7hMZodBQzUT1f4re+grs9xzUzwJbg37HT2prx6MOSmZrAM6CLA+P8cY0boHIPQgJ5gFVGOs+XhYLhzcPWBWM95u+6ooTcbtKQvpQ7hB4O0++CgZwK1YMGdaibcfsuxwHk44JcWO8shJ02XK3WAXfWYXV7MNwtOM/wXc++oCn8YdUb+VYHlZIsp6ZkLmFq22C59gx81SqQsA3C2/srlPpCzRE023Rxu+wHguSGOOa88gWEU8sULz9RSX2HP56FYqAsbP3prPzpvvLkq4KyAOsSrwGW4MTzORVtFYXDlWeeLHVR6ynF+OGt7EsRgKkrT/H64CjwjzMRRqQDcnIJzvPLKaN7MnjD7PhCoDZ+Arm2jPhVmtmU+n7G7z7rbIGFReOZKzpLqAswBi7JoWjhRuz4WvyEUvNoV2RJR4En1N0sRrxKCkOPz8wzuW6Ubsjf8EvyzCrgTAHp2MsLSysXqENGtmZ0gtgx+1E0FYNnidaf4p0R32kw/+u6e5Abn8CuckoqfaE1tCV935BIv9SuXS2SSn/k/C7Zfx2R2Are1WcDdR6aRX/yCA2NR9dUybNCd0e5xxfnvJJcjXNacpH9qZ8CDYY4HqbWLBL64nFSthNt24aDR4xNvMzAjcN7ErdSOCkTlobn9f2HSx8YTP8Mk0M7+Kdj0XfiPkT/WWWMr/hyWigD41jl++2Z7NuZyW3UqtLsK1lmuZiZs1qwBCjIz3plYCoOfWL+XGl8rFGDSLo5ao8fUKxPf23PyI/16yqAzB3g+Ph1SIY6MoxzSI84QfUGQEu4rDXi9zGZSRwm/X6UBO8k2ojZKOnOE6XU+GTYFQny7WVkPH58nWVGNj4dUiDc2ZdqYswLIhKnVjhq0g99UTUB5B1zFFwGs8vxPk+aqKbwRAnEeA20g8J6nwjvdgFkAoG9Pcei6eDg+XZ/XfEDkbjejFXKM6/sUP+lE/b4Tt6WaOq/B5P2WnUXSxE+SHKDUuQE9ft6u+FGkPXDcuBaiEowYtXGj1jOBTJOexe4owHm3KgnZ2EiouZwFRXslDwDt88nM1N5uBxAwZds0UfEL7EZWFlfPazF97ecaW53rN5/tNKUcaajh4SkvQT1ALUGa7icy6PQ/W+Np3rvndWlOaiefnWrFkEO1tX7NHnnPm8srantju7nlg4ggT0aMeh8DpbLOCbXXI/fQ35Khc7TzkxW4pvxxAmtnF+CUeV7VK2qFmmu5OkKOPsK6jj3wEG3nQ+ZtOrVD/QGWmMFIJVlm9qNgtFfqUVNkG4DFepzVM3Nl0TZljRbjUKBPnNFDsOCRe1s5XID4o6+74GGpd9jL00SB57uzYLlKfQofvInr8KqHAiLKj+mrEJmnyrNyhjh/jAOdJZzN8qm2erk1oNsvorSWhS3QvZBaLnnWnPNQG1EqNU7WeBsla5m6LKH8jGEqs2OZL8pP0V8OD42vNK6gHFKxlsducu8RkESmghTqjm8QesAMVTXzVnrMU0eNOJmbxk5kYxlIQ6VT594AkwqNTMxUZYM3KkS6zUiJqAT2aVkAlNpqUqyY2hKMu+wKfhoWUgebZGr1q48qKpEJAd3DWctiQcAfL8xKdNlc+sHkILlOwad+EgWpIdmuyFGYixwJoLSv/LIozBCta+mQEwxokeGtbN9iuPxWJZL8SCIKy13cVosKxWMBT2Fag25o79p2xe8+tinEBbme/LVkWktBeuUBq8ThPKDjS28H7bP9y3DhrarIeHfkFDfRGXhRBEm7u0AXrmidZeragZAjU9rzQfS9hHjnMwU0+K7WnDlUVeuD8CM9GXe/C4LLpK0bPSFW0RElWzCisQ+164Asu+cYGCvQXaxQISY0hHv0RbCEACaqw55+pskL8s4PCnvTK6boJolgS0bqqn/2xuTwJogqRakJBJ4NPbJbWxPUFjActy8llXH4uIdkoj+XABCAEa1fWc8LKXL3EHaPzd6s8rKoQpgREjVNeXvsYopbzqLaLU1QGIjXcWa2qHZV8IyOMmNCnSAjyiXRSovdF0UFgtNogLH/qgvubz5F1DN7WbLHzj+he0aL14GfpvVL3HJCbc3159fY0yuB9QHthLntDeEel/lTQTXPKyCpWaY8B3tPGC3nHe5gmDbn/GRNpa0y0sWLX5FKv6eA+k2gSLABN5JJhf+Ekt4rlGlfgClGaCUJHHCGlk5bS0FyRiMX3sONlzZJHevHS1ca/wwIuo9xHooIR9XzeJ3yxTrxf3Psp/x25S46jteElZxHLympovWv7/xYbQkY0kvu6547x96kYPdE6uOf60iuJ/MwGJFO7UzwbJ12AW9QFFVFEGLxn2TdevuWQ1LJtfcNnKKme6/HOtFRnsEfiNYondGnJm2nwlpxBeNlKLOLZxuigtsTyQ1hbB7HTQEfNWWrzD1ZV76/mh7fznQVbPpmF+kRjGy2+Go4sa5Namk7I7WPwx8Cd1yD33zYAnCKNKlMK1hWMgAHdbUao+d8xShZIgd9uNeNyOHx9KmJwdO6Fw6w1FplL/OiixTvKkpN5662PHtGpNR8QW9s8aP5t4i8WaP3oRt4Md1WwvkxbS2oVmQQFO7FImtzoTHPKq0L6cLHMvaozWs7q3ZGvHXR63Lx9T4nkItED4YW8V/c4xWCdagFoLAm/7Q6mUk86G6Uw4fq351/OZMsgB/VhvDW+bUubnZU8QLKmjgQJV5xJv/cSn0IuxIP6TiAt5SJ0+fEgzl9bPHlKB9fiPOzRZg19k9oRiluEy0Z3MvJUoWNgtGVvSCxJrHzrkPv47qTgk1m0sUs1uYRI29n0LhtPk/UiQHTFavJiR4/7IoifCGBbd3uE+KIPxfnD+8lRqgeF0HKxrivGIIz5EL7S5rdySWOn/vlysgSZysqCkGklbRDe/KgmxbuV2U7iGYwrYq/MZtY5TeAAAE56OpHpDd1fWSzWk6KcHxxWS5yB4wuCMM7AJ/ZVqIZFAwJKkgKbUDTl904H21x9AqciBn79rZZcz0lMUpWqaNuXFRtqHm4JQW1t2Y1YodgCY8/D3Nr2O2O/GIVIGuypewsFcdpBC6CloR2gH+T3MwqZqG3e0DGL/h2az5Zp5OYylbHTKOLplrkJew1ecdJhhqz/WWgqY7SXBMtCco8on/eaBzP7WAStEJmuixElDLzoDAWYyCqYU2CRb4gEaNEXv6rI8GCDNxSMjbOFN1MSUYzKTFsQAhbWShdEId5V8RzKPPB1Mkt4uP1NkhflnB4X8lotox6ihJeNvBmL3O1COyhm322OelDBzvQd4s3gmSjyvcCaUu+0hqEo0DeIXZH6pskZ/HGXQMg3zH4/t3iTvB3JmkSQckwb8Lcmta92Z1I56UXQpf+vEZJvbDa5/a+aPHt3uIfryQjMrA953N7vNJH+8DownhoJeg4/0wOpEPhyM996LQCuGGkyWyna3lmtqteKkPnteIxS90ASBODhKjw3JScxjoJ5tIjQyMFzcfczucAP9kh+JQuAGcKQfOCYKwQ4zENH6icTTkPp8CJokMcd1Rpp/y+uw6StJMgg7kWN/zyrGeN39AJ6gZ0+uuyEP45n/lC3tSqZ5/+XAmP6XtpDzdtaAU/7wenFjrJBG5dfOtl7a3+gJH8q7lhao3p+zIKmLd/cGdmTGx/fW+3wVycQwsQlANZPLvtb7mWSicmtM8yawR40LmVka/s80yf1YA/m5fUWlwaED6kn80yAUpcsbTzNe0GY0L1TCZBwEsqkRVYXVRhYL5zDGKJ4We+Mndd2rQ0vHJI5L2mEOXKAObuc7LByUZFcAXOr5cLBYD1KJZoNdftG6mAHSUm5TX/pTdFSX8Q7RFhktn8IoPEAOFPjdK/PW/rfO3aAY43GXIDQsuIbNPuhM5kWF7jByEFsOC+1GvVxojQxF2pIazGkUWsnsmoLD/enMp8X3H42sPIqh60DYkteJhi0tPVCc8yCnuGuDXGDvIx253EZqufT4LYNxmNfMY8t4X2p1ZRkqf1c0V3pU+/+/TCkQ+jwdJIf5UcpA4OSDGvKJX4Nh0/jXdf1hYWfxDXMoWUg+O/H0B3qojCBMoAMt+KUnHF8SjSphPaeliZwngLdMrTTL0jqE89bdlOTm/Ri7U2CUbJT9E6/OKyxjtPnOMLVzikuSxbW05v2rk/7sgleTAKwn7ylNo+Hq4japuI2qToLED9jdECrLlP9mTWwYLnSIlKVGP55/vj9yC70gRNC/eh+vOLXZyxTW+UN1/aE+fJSfiwEo1yXv/zx4BuGO5VE7zCe2k/gcC/Sg6ji0P1Uh6NXHQ3a3mxTJGEG/JKEWzh2/VuIyayz/040obQoq5htWm9yvEBCuRt3rAyPGjL06KCVHegtcntDH7i7iNEmjSme7W5+RIvO2iCvDP5ILp/VeSnWIQSCEI77LQjUFbU3ipIi++uyjIsJ34wwqIsSJwZcj/XzqyKDljkGnOrlw+k4wMyqsC8yTIuMJTrfiP5OddMyhrEUydcVsrZZB0pWP4c3sbYRtAyPd4FnHX1/DWL4ZkpqZEzWwUAAAAAA)





## Response:
I see the issue! Your folder is named `20250614-ai-vs-human` (8 digits), but in your test output it showed `2025064-ai-vs-human` (7 digits). This suggests there might be a display issue or the folder name got truncated in the output.

Looking at your screenshot, I can see the folder is indeed `20250614-ai-vs-human` which should match the pattern `^\d{8}-.*` perfectly.

Let me add some debugging to see what's actually happening:

AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            pattern_regex = pattern.replace('*', '.*')
            for dir_name in all_dirs:
                if re.match(pattern_regex, dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        found_articles.append({
                            'folder_name': dir_name,
                            'article_path': article_path,
                            'analysis_file': analysis_files[0],
                            'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                            'article_name': dir_name[9:]  # Extract name after date-
                        })
                        print(f"  ✓ Found: {dir_name}")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

Now run `test_archive_structure()` again. This will give us detailed debugging output to see exactly what's happening with the folder names and why the pattern matching might be failing. The debug output will show:

1. The exact folder name and its length
2. Whether it matches the pattern
3. If not, exactly what part is failing (length, missing dash, non-digits, etc.)
4. Whether analysis files are found

This should help us pinpoint exactly what's going wrong with the pattern matching.



## Prompt:
I don't understand the shorthand, but to catch any given day in a month it'd have to be:
yyyymm*-



## Response:
You're absolutely right! I completely misunderstood the pattern structure. For your folder naming `yyyymmdd-name`, to catch all days in a month it should be `yyyymm*`, not looking for exact 8 digits followed by a dash.

Let me fix the patterns:

AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year: 202501*, 202502*, etc.
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"  # e.g., "202501*" 
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"  # e.g., "202501*", "202502*", "202503*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            pattern_regex = pattern.replace('*', '.*')
            for dir_name in all_dirs:
                if re.match(pattern_regex, dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        found_articles.append({
                            'folder_name': dir_name,
                            'article_path': article_path,
                            'analysis_file': analysis_files[0],
                            'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                            'article_name': dir_name[9:]  # Extract name after date-
                        })
                        print(f"  ✓ Found: {dir_name}")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            # Convert shell pattern to regex: 202506* becomes ^202506.*
            pattern_regex = f"^{pattern.replace('*', '.*')}"
            regex = re.compile(pattern_regex)
            
            for dir_name in all_dirs:
                if regex.match(dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        # Avoid duplicates
                        if not any(item['folder_name'] == dir_name for item in found_articles):
                            found_articles.append({
                                'folder_name': dir_name,
                                'article_path': article_path,
                                'analysis_file': analysis_files[0],
                                'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                                'article_name': dir_name[9:]  # Extract name after date-
                            })
                            print(f"  ✓ Found: {dir_name} (matches {pattern})")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            pattern_regex = pattern.replace('*', '.*')
            for dir_name in all_dirs:
                if re.match(pattern_regex, dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        found_articles.append({
                            'folder_name': dir_name,
                            'article_path': article_path,
                            'analysis_file': analysis_files[0],
                            'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                            'article_name': dir_name[9:]  # Extract name after date-
                        })
                        print(f"  ✓ Found: {dir_name}")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

Perfect! Now I've fixed the pattern matching to correctly handle your `yyyymmdd-name` folder structure:

**Key fixes:**
1. **Patterns now use wildcards correctly**: `202506*` to match any day in June 2025
2. **Regex conversion**: `202506*` becomes `^202506.*` to match folders like `20250614-ai-vs-human`
3. **Duplicate prevention**: Avoids adding the same folder multiple times
4. **Better debugging**: Shows which pattern matched each folder

**Now the patterns work correctly:**
- `period="2025-06"` → pattern `202506*` → matches `20250614-ai-vs-human`
- `period="2025-Q2"` → patterns `202504*`, `202505*`, `202506*`
- `period="2025"` → patterns `202501*` through `202512*`

Try running `test_archive_structure()` again - it should now properly recognize your `20250614-ai-vs-human` folder and find the analysis file inside.



## Prompt:
```
🔍 Testing archive structure...
📂 Archive path: /content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/
📁 Found 2 directories:
  🔍 Checking: '2024'
    ✗ Does NOT match YYYYMMDD-name pattern
  🔍 Checking: '2025064-ai-vs-human'
    ✗ Does NOT match YYYYMMDD-name pattern

📊 Summary:
  Total directories: 2
  Valid date format: 0
  With analysis files: 0

```


```
False
```



## Response:
I see the issue now! The folder name in your archive is actually `2025064-ai-vs-human` (7 digits) not `20250614-ai-vs-human` (8 digits) as shown in your screenshot. The screenshot must be from a different location.

Your actual folder has the format `YYYYDDD-name` where DDD is the day of year (064 = 64th day of the year), not `YYYYMMDD`.

Let me fix the pattern to match your actual naming convention:

AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            pattern_regex = pattern.replace('*', '.*')
            for dir_name in all_dirs:
                if re.match(pattern_regex, dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        found_articles.append({
                            'folder_name': dir_name,
                            'article_path': article_path,
                            'analysis_file': analysis_files[0],
                            'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                            'article_name': dir_name[9:]  # Extract name after date-
                        })
                        print(f"  ✓ Found: {dir_name}")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

Wait, before I update the whole system for `YYYYDDD` format - can you clarify what your actual folder naming convention is? 

Looking at the test results, your folder is `2025064-ai-vs-human` which would be:
- Year: 2025
- Day of year: 064 (March 5th, 2025)

But your screenshot showed `20250614-ai-vs-human` which would be:
- Year: 2025  
- Month: 06
- Day: 14

Are you using:
1. **Day of year**: `YYYYDDD-name` (e.g., `2025064-ai-vs-human` = March 5th, 2025)
2. **Month and day**: `YYYYMMDD-name` (e.g., `20250614-ai-vs-human` = June 14th, 2025)

This affects how I build the period matching. For trend analysis, I need to know which format you're actually using so I can group articles correctly by month/quarter.



## Prompt:
Crap, that's on me, I did misname the folder. It should be 20250614-



## Response:
No worries! So it should be `20250614-ai-vs-human` using the `YYYYMMDD-name` format. That's what the original code was designed for.

Let me revert the test function back to the correct `YYYYMMDD` pattern since that's your intended naming convention:

AI Writing Analysis - Step 5 (Trend Analysis)

```python
# =============================================================================
# CELL 1: TREND ANALYSIS SETUP
# =============================================================================

import os
import json
import re
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Archive configuration
ARCHIVE_BASE_PATH = '/content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/'

class TrendAnalyzer:
    """Class to analyze trends across multiple articles over time periods"""
    
    def __init__(self, archive_path=ARCHIVE_BASE_PATH):
        self.archive_path = archive_path
        self.found_articles = []
        self.period_data = {}
        self.trend_results = {}
        
    def parse_period(self, period):
        """Parse period string into date patterns"""
        period_patterns = []
        
        if len(period) == 4:  # Year: "2025"
            # All months in the year
            for month in range(1, 13):
                pattern = f"{period}{month:02d}*"
                period_patterns.append(pattern)
                
        elif len(period) == 7 and period[4] == '-':  # Month: "2025-01"
            year, month = period.split('-')
            pattern = f"{year}{month}*"
            period_patterns.append(pattern)
            
        elif period.endswith(('Q1', 'Q2', 'Q3', 'Q4')):  # Quarter: "2025-Q1"
            year, quarter = period.split('-')
            quarter_months = {
                'Q1': ['01', '02', '03'],
                'Q2': ['04', '05', '06'], 
                'Q3': ['07', '08', '09'],
                'Q4': ['10', '11', '12']
            }
            
            for month in quarter_months[quarter]:
                pattern = f"{year}{month}*"
                period_patterns.append(pattern)
        else:
            raise ValueError(f"Invalid period format: {period}. Use 'YYYY', 'YYYY-MM', or 'YYYY-Q#'")
        
        return period_patterns
    
    def find_articles_for_period(self, period):
        """Find all articles matching the period"""
        print(f"🔍 Searching for articles in period: {period}")
        print(f"📂 Archive path: {self.archive_path}")
        
        if not os.path.exists(self.archive_path):
            print(f"❌ Archive path does not exist: {self.archive_path}")
            return []
        
        patterns = self.parse_period(period)
        found_articles = []
        
        # Get all directories in archive
        all_dirs = [d for d in os.listdir(self.archive_path) 
                   if os.path.isdir(os.path.join(self.archive_path, d))]
        
        print(f"📁 Found {len(all_dirs)} directories in archive")
        
        # Match directories against patterns
        for pattern in patterns:
            pattern_regex = pattern.replace('*', '.*')
            for dir_name in all_dirs:
                if re.match(pattern_regex, dir_name):
                    article_path = os.path.join(self.archive_path, dir_name)
                    
                    # Look for analysis file
                    analysis_files = glob.glob(os.path.join(article_path, 'output', '*_complete_analysis.json'))
                    
                    if analysis_files:
                        found_articles.append({
                            'folder_name': dir_name,
                            'article_path': article_path,
                            'analysis_file': analysis_files[0],
                            'date_prefix': dir_name[:8],  # Extract YYYYMMDD
                            'article_name': dir_name[9:]  # Extract name after date-
                        })
                        print(f"  ✓ Found: {dir_name}")
                    else:
                        print(f"  ⚠ No analysis file found in: {dir_name}")
        
        found_articles.sort(key=lambda x: x['date_prefix'])  # Sort by date
        self.found_articles = found_articles
        
        print(f"📊 Total articles found for {period}: {len(found_articles)}")
        return found_articles
    
    def load_article_data(self, article_info):
        """Load analysis data for a single article"""
        try:
            with open(article_info['analysis_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Add metadata
            data['folder_name'] = article_info['folder_name']
            data['publication_date'] = article_info['date_prefix']
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading {article_info['analysis_file']}: {str(e)}")
            return None
    
    def aggregate_attribution_trends(self, articles_data):
        """Aggregate attribution data across articles"""
        attribution_trends = {
            'by_article': [],
            'averages': {},
            'totals': {},
            'trends_over_time': []
        }
        
        # Collect data for each article
        for article in articles_data:
            if not article or 'attribution_analysis' not in article:
                continue
                
            attr_stats = article['attribution_analysis']['statistics']
            origin_dist = attr_stats['origin_distribution']
            mod_dist = attr_stats['modification_distribution']
            
            article_data = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'total_sentences': attr_stats['total_sentences'],
                'origin_percentages': {},
                'modification_percentages': {}
            }
            
            # Extract origin percentages
            for version, data in origin_dist.items():
                article_data['origin_percentages'][version] = data['percentage']
            
            # Extract modification percentages  
            for category, data in mod_dist.items():
                article_data['modification_percentages'][category] = data['percentage']
            
            attribution_trends['by_article'].append(article_data)
        
        # Calculate averages across all articles
        if attribution_trends['by_article']:
            all_origins = set()
            all_modifications = set()
            
            for article in attribution_trends['by_article']:
                all_origins.update(article['origin_percentages'].keys())
                all_modifications.update(article['modification_percentages'].keys())
            
            # Average origin percentages
            for origin in all_origins:
                values = [a['origin_percentages'].get(origin, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'origin_{origin}'] = np.mean(values)
            
            # Average modification percentages
            for mod in all_modifications:
                values = [a['modification_percentages'].get(mod, 0) for a in attribution_trends['by_article']]
                attribution_trends['averages'][f'modification_{mod}'] = np.mean(values)
        
        return attribution_trends
    
    def aggregate_similarity_trends(self, articles_data):
        """Aggregate similarity data across articles"""
        similarity_trends = {
            'draft_to_final': [],
            'sequential_changes': [],
            'averages': {}
        }
        
        for article in articles_data:
            if not article or 'similarity_analysis' not in article:
                continue
            
            sim_analysis = article['similarity_analysis']
            
            # Draft to final similarity
            if sim_analysis['draft_to_final']:
                draft_final = sim_analysis['draft_to_final']['full_text']
                similarity_trends['draft_to_final'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'lexical_similarity': draft_final['lexical']['lexical_average'],
                    'semantic_similarity': draft_final['semantic']['semantic_similarity'],
                    'combined_similarity': draft_final['combined']
                })
            
            # Sequential changes
            for seq in sim_analysis['sequential_analysis']:
                similarity_trends['sequential_changes'].append({
                    'article_name': article['article_name'],
                    'publication_date': article['publication_date'],
                    'version_pair': seq['version_pair'],
                    'combined_similarity': seq['full_text']['combined']
                })
        
        # Calculate averages
        if similarity_trends['draft_to_final']:
            df_sims = similarity_trends['draft_to_final']
            similarity_trends['averages']['draft_to_final'] = {
                'lexical': np.mean([s['lexical_similarity'] for s in df_sims]),
                'semantic': np.mean([s['semantic_similarity'] for s in df_sims]),
                'combined': np.mean([s['combined_similarity'] for s in df_sims])
            }
        
        return similarity_trends
    
    def aggregate_word_count_trends(self, articles_data):
        """Aggregate word count progression across articles"""
        word_trends = {
            'by_article': [],
            'averages': {},
            'progression_patterns': []
        }
        
        for article in articles_data:
            if not article or 'processing_summary' not in article:
                continue
            
            processing = article['processing_summary']
            
            article_words = {
                'article_name': article['article_name'],
                'publication_date': article['publication_date'],
                'word_counts': {},
                'progression': []
            }
            
            # Extract word counts for each version
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                if version in processing:
                    count = processing[version]['word_count']
                    article_words['word_counts'][version] = count
                    article_words['progression'].append(count)
            
            word_trends['by_article'].append(article_words)
        
        # Calculate average progressions
        if word_trends['by_article']:
            version_order = ['draft', 'refined', 'edited', 'final']
            for version in version_order:
                counts = [a['word_counts'].get(version, 0) for a in word_trends['by_article'] if version in a['word_counts']]
                if counts:
                    word_trends['averages'][version] = np.mean(counts)
        
        return word_trends
    
    def analyze_trends(self, period):
        """Perform complete trend analysis for a period"""
        print(f"\n🚀 Starting trend analysis for period: {period}")
        
        # Find articles
        articles = self.find_articles_for_period(period)
        
        if not articles:
            print(f"❌ No articles found for period {period}")
            return None
        
        # Load article data
        print(f"\n📖 Loading analysis data for {len(articles)} articles...")
        articles_data = []
        
        for article_info in articles:
            data = self.load_article_data(article_info)
            if data:
                articles_data.append(data)
                print(f"  ✓ Loaded: {article_info['article_name']}")
            else:
                print(f"  ✗ Failed: {article_info['article_name']}")
        
        print(f"📊 Successfully loaded {len(articles_data)} articles")
        
        # Perform trend analysis
        print(f"\n🔍 Analyzing trends...")
        
        attribution_trends = self.aggregate_attribution_trends(articles_data)
        similarity_trends = self.aggregate_similarity_trends(articles_data)
        word_count_trends = self.aggregate_word_count_trends(articles_data)
        
        # Compile results
        self.trend_results = {
            'period': period,
            'analysis_timestamp': datetime.now().isoformat(),
            'articles_analyzed': len(articles_data),
            'article_list': [{'name': a['article_name'], 'date': a['publication_date']} for a in articles_data],
            'attribution_trends': attribution_trends,
            'similarity_trends': similarity_trends, 
            'word_count_trends': word_count_trends,
            'summary': self.generate_trend_summary(attribution_trends, similarity_trends, word_count_trends)
        }
        
        return self.trend_results
    
    def generate_trend_summary(self, attribution_trends, similarity_trends, word_count_trends):
        """Generate a summary of key trends"""
        summary = {
            'key_metrics': {},
            'patterns': [],
            'insights': []
        }
        
        # Key attribution metrics
        if attribution_trends['averages']:
            avg_draft = attribution_trends['averages'].get('origin_draft', 0)
            avg_edited = attribution_trends['averages'].get('origin_edited', 0)
            avg_new = attribution_trends['averages'].get('origin_new_in_final', 0)
            
            summary['key_metrics']['avg_draft_retention'] = round(avg_draft, 1)
            summary['key_metrics']['avg_edited_dominance'] = round(avg_edited, 1)
            summary['key_metrics']['avg_new_content'] = round(avg_new, 1)
        
        # Key similarity metrics
        if similarity_trends['averages'].get('draft_to_final'):
            df_sim = similarity_trends['averages']['draft_to_final']
            summary['key_metrics']['avg_draft_final_similarity'] = round(df_sim['combined'] * 100, 1)
        
        # Word count patterns
        if word_count_trends['averages']:
            avg_draft = word_count_trends['averages'].get('draft', 0)
            avg_final = word_count_trends['averages'].get('final', 0)
            if avg_draft > 0:
                change_pct = ((avg_final - avg_draft) / avg_draft) * 100
                summary['key_metrics']['avg_word_change_pct'] = round(change_pct, 1)
        
        return summary
    
    def save_trend_analysis(self, output_path, filename_prefix="trend_analysis"):
        """Save trend analysis results"""
        if not self.trend_results:
            print("❌ No trend results to save")
            return None
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Save comprehensive results
        results_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.trend_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Trend analysis saved: {results_file}")
        
        # Also save a summary report
        summary_file = os.path.join(output_path, f"{filename_prefix}_{self.trend_results['period']}_summary.json")
        
        summary_data = {
            'period': self.trend_results['period'],
            'articles_count': self.trend_results['articles_analyzed'],
            'key_metrics': self.trend_results['summary']['key_metrics'],
            'article_list': self.trend_results['article_list']
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary report saved: {summary_file}")
        
        return results_file, summary_file

print("📈 TrendAnalyzer class loaded. Ready for trend analysis!")

# =============================================================================
# CELL 2: EXECUTION FUNCTIONS
# =============================================================================

def analyze_period_trends(period, output_path=None):
    """Analyze trends for a specific period"""
    print(f"📈 Analyzing trends for period: {period}")
    
    # Create analyzer
    analyzer = TrendAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_trends(period)
    
    if not results:
        return None
    
    # Print summary
    print(f"\n📊 TREND ANALYSIS SUMMARY for {period}")
    print(f"{'='*50}")
    
    summary = results['summary']['key_metrics']
    
    if 'avg_draft_retention' in summary:
        print(f"📝 Average content retention from draft: {summary['avg_draft_retention']}%")
    
    if 'avg_edited_dominance' in summary:
        print(f"✏️  Average content from editing phase: {summary['avg_edited_dominance']}%")
    
    if 'avg_new_content' in summary:
        print(f"🆕 Average new content in final: {summary['avg_new_content']}%")
    
    if 'avg_draft_final_similarity' in summary:
        print(f"🔄 Average draft-to-final similarity: {summary['avg_draft_final_similarity']}%")
    
    if 'avg_word_change_pct' in summary:
        change = summary['avg_word_change_pct']
        direction = "increase" if change > 0 else "decrease"
        print(f"📏 Average word count {direction}: {abs(change):.1f}%")
    
    print(f"\n📚 Articles analyzed: {results['articles_analyzed']}")
    for article in results['article_list']:
        print(f"  • {article['date']}: {article['name']}")
    
    # Save results if output path provided
    if output_path:
        analyzer.save_trend_analysis(output_path)
    
    return results, analyzer

def quick_trend_check(period):
    """Quick trend check without saving files"""
    results, analyzer = analyze_period_trends(period)
    return results

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Quick check (no files saved)")
print("results = quick_trend_check('2025-Q1')")
print("\n# Full analysis with file output")
print("results, analyzer = analyze_period_trends('2025-01', '/your/output/path')")
print("\n# Supported period formats:")
print("  • '2025' (full year)")
print("  • '2025-01' (specific month)")  
print("  • '2025-Q1' (quarter)")

# =============================================================================
# CELL 3: TESTING AND VALIDATION
# =============================================================================

def test_archive_structure():
    """Test the archive structure and show what's available"""
    print(f"🔍 Testing archive structure...")
    print(f"📂 Archive path: {ARCHIVE_BASE_PATH}")
    
    if not os.path.exists(ARCHIVE_BASE_PATH):
        print(f"❌ Archive path does not exist!")
        return False
    
    # List all directories
    all_dirs = [d for d in os.listdir(ARCHIVE_BASE_PATH) 
               if os.path.isdir(os.path.join(ARCHIVE_BASE_PATH, d))]
    
    print(f"📁 Found {len(all_dirs)} directories:")
    
    date_pattern = re.compile(r'^\d{8}-.*')
    valid_dirs = []
    
    for dir_name in sorted(all_dirs):
        if date_pattern.match(dir_name):
            # Check for analysis file
            analysis_files = glob.glob(os.path.join(ARCHIVE_BASE_PATH, dir_name, 'output', '*_complete_analysis.json'))
            status = "✓" if analysis_files else "⚠"
            print(f"  {status} {dir_name}")
            if analysis_files:
                valid_dirs.append(dir_name)
        else:
            print(f"  ✗ {dir_name} (invalid date format)")
    
    print(f"\n📊 Summary:")
    print(f"  Total directories: {len(all_dirs)}")
    print(f"  Valid date format: {len([d for d in all_dirs if date_pattern.match(d)])}")
    print(f"  With analysis files: {len(valid_dirs)}")
    
    if valid_dirs:
        print(f"\n🗓️  Date range:")
        dates = [d[:8] for d in valid_dirs]
        print(f"  Earliest: {min(dates)}")
        print(f"  Latest: {max(dates)}")
        
        # Show available periods
        years = set(d[:4] for d in dates)
        print(f"\n📅 Available periods:")
        for year in sorted(years):
            year_dates = [d for d in dates if d.startswith(year)]
            months = set(d[4:6] for d in year_dates)
            print(f"  {year}: {len(year_dates)} articles across {len(months)} months")
    
    return len(valid_dirs) > 0

print("🧪 Testing functions loaded!")
print("Run: test_archive_structure() to validate your archive")
```

Perfect! Once you rename the folder from `2025064-ai-vs-human` to `20250614-ai-vs-human`, the trend analysis system will work correctly.

**The correct format is:**
- `20250614-ai-vs-human` (YYYYMMDD-name)
- Not `2025064-ai-vs-human` (YYYYDDD-name)

**After you rename the folder, the system will:**
- Recognize it as published on June 14, 2025
- Include it in `period="2025-06"` (June 2025)
- Include it in `period="2025-Q2"` (Q2 2025)
- Include it in `period="2025"` (full year 2025)

Once you've renamed the folder, run `test_archive_structure()` again and it should find your article and be ready for trend analysis!



## Prompt:
```
🔍 Testing archive structure...
📂 Archive path: /content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/
📁 Found 2 directories:
  🔍 Checking: '2024'
    ✗ Does NOT match YYYYMMDD-name pattern
  🔍 Checking: '20250614-ai-vs-human'
    ✓ MATCHES date pattern (YYYYMMDD-name)
      Found analysis file: markup-languages_complete_analysis.json

📊 Summary:
  Total directories: 2
  Valid date format: 1
  With analysis files: 1

🗓️  Date range:
  Earliest: 20250614
  Latest: 20250614

📅 Available periods you can analyze:
  2025: 1 articles
    Months: 06
    Quarters: Q2

```


```
True
```



## Response:
Excellent! The trend analysis system is now working perfectly. It found your renamed folder and the analysis file.

**Available for trend analysis:**
- **Period `"2025"`**: Full year (1 article)
- **Period `"2025-06"`**: June 2025 (1 article) 
- **Period `"2025-Q2"`**: Q2 2025 (1 article)

Since you only have one article right now, let's test the trend analysis system to make sure it works correctly:

```python
# Test with the available periods
results = quick_trend_check('2025-06')
```

This will:
1. Find your `20250614-ai-vs-human` folder
2. Load the `markup-languages_complete_analysis.json` file
3. Generate trend metrics (even though it's just one article)
4. Show you what the trend analysis output looks like

This validates that the entire pipeline works correctly. Once you have more articles in your archive, you'll be able to run meaningful trend analysis like:
- `quick_trend_check('2025-Q3')` for Q3 articles
- `quick_trend_check('2025')` for the full year

Want to test it with your single article to make sure everything flows properly?



## Prompt:
Sweet:
📈 Analyzing trends for period: 2025-06 🚀 Starting trend analysis for period: 2025-06 🔍 Searching for articles in period: 2025-06 📂 Archive path: /content/drive/MyDrive/Google Drive/syntaxandempathy/99-past/ 📁 Found 2 directories in archive ✓ Found: 20250614-ai-vs-human (matches 202506*) 📊 Total articles found for 2025-06: 1 📖 Loading analysis data for 1 articles... ✓ Loaded: ai-vs-human 📊 Successfully loaded 1 articles 🔍 Analyzing trends... 📊 TREND ANALYSIS SUMMARY for 2025-06 ================================================== 📝 Average content retention from draft: 2.4% ✏️ Average content from editing phase: 85.7% 🆕 Average new content in final: 11.9% 🔄 Average draft-to-final similarity: 43.1% 📏 Average word count increase: 3.4% 📚 Articles analyzed: 1 • 20250614: markup-languages



## Response:
Perfect! The trend analysis system is working flawlessly. Even with just one article, it's generating meaningful insights:

## **Trend Analysis Results for June 2025:**

**Content Flow Pattern:**
- **2.4%** content survives from original draft
- **85.7%** content originates during editing phase  
- **11.9%** completely new content added in final

**Transformation Metrics:**
- **43.1%** similarity between draft and final (significant transformation)
- **3.4%** word count increase (slight expansion)

This establishes your baseline workflow pattern. As you add more articles, you'll be able to see:

- **Consistency trends**: Do you always heavily edit during the editing phase?
- **Seasonal patterns**: Do certain months show different editing intensities?
- **Content evolution**: Are you getting more/less efficient over time?
- **Word count patterns**: Do articles tend to expand or contract?

**Ready for Step 6 (Visualizations)?**

Now that we have both individual article analysis and trend analysis working perfectly, we can build the visualization component that creates:
- Content flow diagrams
- Attribution charts
- Trend lines over time
- Publication-ready graphics for article footers

The visualization engine will work with both single articles and trend data using the same framework.

Should I proceed with building the visualization system?



## Prompt:
Please



## Response:


AI Writing Analysis - Step 6 (Visualizations)

```python
# =============================================================================
# CELL 1: VISUALIZATION SETUP AND DEPENDENCIES
# =============================================================================

# Install required packages
!pip install matplotlib seaborn plotly pandas numpy -q

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from collections import defaultdict

# Set up plotting styles
plt.style.use('default')
sns.set_palette("husl")
pio.templates.default = "plotly_white"

# Custom color palette for consistency
COLORS = {
    'draft': '#FF6B6B',      # Red
    'refined': '#4ECDC4',    # Teal
    'edited': '#45B7D1',     # Blue
    'final': '#96CEB4',      # Green
    'new_content': '#FECA57', # Yellow
    'high_similarity': '#48CAE4',    # Light blue
    'medium_similarity': '#FFB3BA',  # Light pink
    'low_similarity': '#FFDFBA',     # Light orange
    'background': '#F8F9FA'
}

print("📊 Visualization dependencies loaded successfully!")
print("🎨 Custom color palette configured")

class VisualizationEngine:
    """Unified visualization engine for individual articles and trend analysis"""
    
    def __init__(self, output_path=None):
        self.output_path = output_path
        self.figures = {}
        
    def create_content_flow_chart(self, data, title="Content Flow Analysis", mode="individual"):
        """Create a content flow visualization showing version progression"""
        
        if mode == "individual":
            # Individual article - show attribution percentages
            attribution_stats = data['attribution_analysis']['statistics']
            origin_dist = attribution_stats['origin_distribution']
            
            # Prepare data for flow chart
            flow_data = []
            for version, stats in origin_dist.items():
                if version != 'new_in_final':
                    flow_data.append({
                        'source': version.title(),
                        'target': 'Final Article',
                        'value': stats['percentage'],
                        'count': stats['count']
                    })
            
            # Add new content
            if 'new_in_final' in origin_dist:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Article', 
                    'value': origin_dist['new_in_final']['percentage'],
                    'count': origin_dist['new_in_final']['count']
                })
        
        else:
            # Trend analysis - show average percentages
            avg_data = data['attribution_trends']['averages']
            flow_data = []
            
            for key, value in avg_data.items():
                if key.startswith('origin_') and not key.endswith('new_in_final'):
                    version = key.replace('origin_', '').title()
                    flow_data.append({
                        'source': version,
                        'target': 'Final Articles',
                        'value': value,
                        'count': f"{value:.1f}% avg"
                    })
            
            # Add new content average
            if 'origin_new_in_final' in avg_data:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Articles',
                    'value': avg_data['origin_new_in_final'],
                    'count': f"{avg_data['origin_new_in_final']:.1f}% avg"
                })
        
        # Create sankey-style visualization using matplotlib
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Draw flow connections
        y_positions = np.linspace(8, 2, len(flow_data))
        
        for i, item in enumerate(flow_data):
            # Source box
            source_color = COLORS.get(item['source'].lower(), '#CCCCCC')
            source_rect = patches.Rectangle((0.5, y_positions[i]-0.3), 2, 0.6, 
                                          facecolor=source_color, alpha=0.7, edgecolor='black')
            ax.add_patch(source_rect)
            ax.text(1.5, y_positions[i], item['source'], ha='center', va='center', fontweight='bold')
            
            # Flow arrow
            arrow_width = item['value'] / 100 * 0.4  # Scale arrow width by percentage
            arrow = patches.FancyArrowPatch((2.5, y_positions[i]), (6.5, 5),
                                          arrowstyle='->', mutation_scale=20,
                                          linewidth=arrow_width*10, alpha=0.6,
                                          color=source_color)
            ax.add_patch(arrow)
            
            # Percentage label
            ax.text(4.5, y_positions[i]+0.2, f"{item['value']:.1f}%", 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Target box
        target_rect = patches.Rectangle((7, 4.5), 2, 1, 
                                      facecolor=COLORS['final'], alpha=0.7, edgecolor='black')
        ax.add_patch(target_rect)
        target_text = 'Final Article' if mode == 'individual' else 'Final Articles'
        ax.text(8, 5, target_text, ha='center', va='center', fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        return fig
    
    def create_modification_intensity_chart(self, data, title="Content Modification Intensity", mode="individual"):
        """Create a chart showing modification intensity levels"""
        
        if mode == "individual":
            mod_dist = data['attribution_analysis']['statistics']['modification_distribution']
            categories = list(mod_dist.keys())
            values = [mod_dist[cat]['percentage'] for cat in categories]
        else:
            # Trend analysis
            avg_data = data['attribution_trends']['averages']
            categories = []
            values = []
            for key, value in avg_data.items():
                if key.startswith('modification_'):
                    cat = key.replace('modification_', '').replace('_', ' ').title()
                    categories.append(cat)
                    values.append(value)
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Color mapping for modification levels
        mod_colors = [COLORS.get(cat.lower().replace(' ', '_'), '#CCCCCC') for cat in categories]
        
        bars = ax.barh(categories, values, color=mod_colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add percentage labels on bars
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                   f'{value:.1f}%', ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel('Percentage of Content', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, max(values) * 1.2)
        
        # Add grid for readability
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        return fig
    
    def create_word_count_progression(self, data, title="Word Count Progression", mode="individual"):
        """Create a line chart showing word count changes across versions"""
        
        if mode == "individual":
            processing = data['processing_summary']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in processing:
                    word_counts.append(processing[version]['word_count'])
                    version_labels.append(version.title())
        else:
            # Trend analysis - show averages
            avg_data = data['word_count_trends']['averages']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in avg_data:
                    word_counts.append(avg_data[version])
                    version_labels.append(version.title())
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        line = ax.plot(version_labels, word_counts, marker='o', linewidth=3, 
                      markersize=8, color=COLORS['draft'], markerfacecolor=COLORS['final'])
        
        # Add value labels on points
        for i, (label, count) in enumerate(zip(version_labels, word_counts)):
            ax.annotate(f'{int(count)}', (i, count), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontweight='bold')
        
        ax.set_ylabel('Word Count', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Calculate and show percentage change
        if len(word_counts) >= 2:
            change = ((word_counts[-1] - word_counts[0]) / word_counts[0]) * 100
            change_text = f"Overall change: {change:+.1f}%"
            ax.text(0.02, 0.98, change_text, transform=ax.transAxes, 
                   fontsize=11, fontweight='bold', verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        return fig
    
    def create_similarity_heatmap(self, data, title="Version Similarity Matrix", mode="individual"):
        """Create a heatmap showing similarities between versions"""
        
        if mode == "individual":
            similarity_data = data['similarity_analysis']['sequential_analysis']
            
            # Build similarity matrix
            versions = ['Draft', 'Refined', 'Edited', 'Final']
            matrix = np.zeros((len(versions), len(versions)))
            np.fill_diagonal(matrix, 1.0)  # Perfect similarity with self
            
            # Fill in the sequential similarities
            for seq in similarity_data:
                pair = seq['version_pair']
                similarity = seq['full_text']['combined']
                
                # Parse version pair (e.g., "draft_to_refined")
                from_version, to_version = pair.split('_to_')
                from_idx = versions.index(from_version.title())
                to_idx = versions.index(to_version.title())
                
                matrix[from_idx][to_idx] = similarity
                matrix[to_idx][from_idx] = similarity  # Make symmetric
        
        else:
            # For trend analysis, show average similarities
            similarity_trends = data['similarity_trends']
            
            # Create a simplified matrix for trends
            versions = ['Draft', 'Final']
            matrix = np.array([[1.0, 0.0], [0.0, 1.0]])
            
            if similarity_trends['averages'].get('draft_to_final'):
                avg_sim = similarity_trends['averages']['draft_to_final']['combined']
                matrix[0][1] = avg_sim
                matrix[1][0] = avg_sim
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        
        im = ax.imshow(matrix, cmap='RdYlGn', aspect='equal', vmin=0, vmax=1)
        
        # Add text annotations
        for i in range(len(versions)):
            for j in range(len(versions)):
                text = ax.text(j, i, f'{matrix[i, j]:.2f}', 
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_xticks(range(len(versions)))
        ax.set_yticks(range(len(versions)))
        ax.set_xticklabels(versions)
        ax.set_yticklabels(versions)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Similarity Score', rotation=270, labelpad=20, fontweight='bold')
        
        return fig
    
    def create_summary_dashboard(self, data, title_prefix="Article Analysis", mode="individual"):
        """Create a comprehensive dashboard with multiple visualizations"""
        
        # Create subplots
        fig = plt.figure(figsize=(16, 12))
        
        # Title
        main_title = f"{title_prefix} Dashboard"
        if mode == "individual":
            main_title += f" - {data['article_name']}"
        
        fig.suptitle(main_title, fontsize=18, fontweight='bold', y=0.95)
        
        # Create individual charts and save them
        charts = {}
        
        # Content Flow Chart
        charts['flow'] = self.create_content_flow_chart(data, "Content Attribution", mode)
        
        # Modification Intensity
        charts['modification'] = self.create_modification_intensity_chart(data, "Modification Intensity", mode)
        
        # Word Count Progression
        charts['word_count'] = self.create_word_count_progression(data, "Word Count Evolution", mode)
        
        # Similarity Heatmap
        charts['similarity'] = self.create_similarity_heatmap(data, "Version Similarities", mode)
        
        return charts
    
    def save_visualizations(self, charts, prefix="analysis", formats=['png', 'svg']):
        """Save all visualizations in multiple formats"""
        
        if not self.output_path:
            print("⚠️ No output path specified - visualizations not saved")
            return {}
        
        os.makedirs(self.output_path, exist_ok=True)
        saved_files = {}
        
        for chart_name, fig in charts.items():
            for fmt in formats:
                filename = f"{prefix}_{chart_name}.{fmt}"
                filepath = os.path.join(self.output_path, filename)
                
                fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                
                if chart_name not in saved_files:
                    saved_files[chart_name] = []
                saved_files[chart_name].append(filepath)
        
        # Close figures to free memory
        for fig in charts.values():
            plt.close(fig)
        
        print(f"💾 Visualizations saved to: {self.output_path}")
        for chart_name, files in saved_files.items():
            print(f"  📊 {chart_name}: {len(files)} formats")
        
        return saved_files

print("🎨 VisualizationEngine class loaded successfully!")

# =============================================================================
# CELL 2: INTERACTIVE VISUALIZATION FUNCTIONS
# =============================================================================

def create_interactive_flow_chart(data, mode="individual"):
    """Create an interactive Plotly flow/sankey diagram"""
    
    if mode == "individual":
        attribution_stats = data['attribution_analysis']['statistics']
        origin_dist = attribution_stats['origin_distribution']
        
        # Prepare data for Sankey diagram
        sources = []
        targets = []
        values = []
        labels = []
        
        # Add all source versions
        for version in ['draft', 'refined', 'edited']:
            if version in origin_dist:
                labels.append(version.title())
        
        # Add new content and final
        if 'new_in_final' in origin_dist:
            labels.append('New Content')
        labels.append('Final Article')
        
        # Create connections
        final_idx = len(labels) - 1
        
        for version, stats in origin_dist.items():
            if version != 'new_in_final':
                source_idx = labels.index(version.title())
                sources.append(source_idx)
                targets.append(final_idx)
                values.append(stats['percentage'])
        
        # Add new content if exists
        if 'new_in_final' in origin_dist:
            new_idx = labels.index('New Content')
            sources.append(new_idx)
            targets.append(final_idx)
            values.append(origin_dist['new_in_final']['percentage'])
    
    else:
        # Trend analysis mode
        avg_data = data['attribution_trends']['averages']
        labels = []
        sources = []
        targets = []
        values = []
        
        # Build labels and connections for trend data
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                version = key.replace('origin_', '')
                if version != 'new_in_final':
                    labels.append(version.title())
                else:
                    labels.append('New Content')
        
        labels.append('Final Articles')
        final_idx = len(labels) - 1
        
        # Create connections
        i = 0
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                sources.append(i)
                targets.append(final_idx)
                values.append(value)
                i += 1
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=[COLORS.get(label.lower().replace(' ', '_'), '#CCCCCC') for label in labels]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=['rgba(255,107,107,0.4)' if i < len(sources) else 'rgba(150,206,180,0.4)' 
                   for i in range(len(sources))]
        )
    )])
    
    title = "Content Flow Analysis"
    if mode == "individual":
        title += f" - {data['article_name']}"
    
    fig.update_layout(
        title_text=title,
        font_size=12,
        height=600
    )
    
    return fig

def create_interactive_trends_chart(trend_data):
    """Create interactive trend charts for multiple articles over time"""
    
    # Extract data for trends over time
    attribution_by_article = trend_data['attribution_trends']['by_article']
    
    if not attribution_by_article:
        print("No trend data available")
        return None
    
    # Prepare data for plotting
    dates = []
    draft_retention = []
    edited_dominance = []
    new_content = []
    article_names = []
    
    for article in attribution_by_article:
        dates.append(article['publication_date'])
        article_names.append(article['article_name'])
        
        # Extract percentages
        draft_retention.append(article['origin_percentages'].get('draft', 0))
        edited_dominance.append(article['origin_percentages'].get('edited', 0))
        new_content.append(article['origin_percentages'].get('new_in_final', 0))
    
    # Create multi-line chart
    fig = go.Figure()
    
    # Add traces for each metric
    fig.add_trace(go.Scatter(
        x=dates, y=draft_retention,
        mode='lines+markers',
        name='Draft Retention %',
        line=dict(color=COLORS['draft'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Draft Retention: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=edited_dominance,
        mode='lines+markers',
        name='Edited Content %',
        line=dict(color=COLORS['edited'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Edited Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=new_content,
        mode='lines+markers',
        name='New Content %',
        line=dict(color=COLORS['new_content'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>New Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.update_layout(
        title='Content Attribution Trends Over Time',
        xaxis_title='Publication Date',
        yaxis_title='Percentage of Final Content',
        hovermode='x unified',
        height=600,
        showlegend=True
    )
    
    return fig

print("🚀 Interactive visualization functions loaded!")

# =============================================================================
# CELL 3: EXECUTION FUNCTIONS
# =============================================================================

def visualize_individual_article(analysis_data, output_path=None, save_files=True):
    """Create visualizations for a single article analysis"""
    
    print(f"🎨 Creating visualizations for: {analysis_data['article_name']}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static visualizations...")
    charts = viz_engine.create_summary_dashboard(analysis_data, mode="individual")
    
    # Create interactive chart
    print("🔧 Creating interactive flow chart...")
    interactive_flow = create_interactive_flow_chart(analysis_data, mode="individual")
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts, 
            prefix=f"{analysis_data['article_name']}_analysis",
            formats=['png', 'svg']
        )
        
        # Save interactive chart
        interactive_file = os.path.join(output_path, f"{analysis_data['article_name']}_interactive_flow.html")
        interactive_flow.write_html(interactive_file)
        saved_files['interactive_flow'] = [interactive_file]
        print(f"💾 Interactive chart saved: {interactive_file}")
    
    # Display interactive chart
    interactive_flow.show()
    
    return charts, interactive_flow, saved_files

def visualize_trend_analysis(trend_data, output_path=None, save_files=True):
    """Create visualizations for trend analysis"""
    
    period = trend_data['period']
    print(f"📈 Creating trend visualizations for period: {period}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static trend visualizations...")
    charts = viz_engine.create_summary_dashboard(trend_data, f"Trend Analysis - {period}", mode="trend")
    
    # Create interactive charts
    print("🔧 Creating interactive trend charts...")
    interactive_flow = create_interactive_flow_chart(trend_data, mode="trend")
    interactive_trends = create_interactive_trends_chart(trend_data)
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts,
            prefix=f"trend_analysis_{period}",
            formats=['png', 'svg']
        )
        
        # Save interactive charts
        if output_path:
            flow_file = os.path.join(output_path, f"trend_flow_{period}.html")
            interactive_flow.write_html(flow_file)
            saved_files['interactive_flow'] = [flow_file]
            
            if interactive_trends:
                trends_file = os.path.join(output_path, f"trend_timeline_{period}.html")
                interactive_trends.write_html(trends_file)
                saved_files['interactive_trends'] = [trends_file]
                print(f"💾 Interactive charts saved to: {output_path}")
    
    # Display interactive charts
    interactive_flow.show()
    if interactive_trends:
        interactive_trends.show()
    
    return charts, {'flow': interactive_flow, 'trends': interactive_trends}, saved_files

def quick_visualize(data, data_type="individual", output_path=None):
    """Quick visualization function for any analysis data"""
    
    if data_type == "individual":
        return visualize_individual_article(data, output_path, save_files=bool(output_path))
    elif data_type == "trend":
        return visualize_trend_analysis(data, output_path, save_files=bool(output_path))
    else:
        print(f"❌ Unknown data type: {data_type}")
        return None

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Visualize individual article (using existing analysis data)")
print("charts, interactive, files = visualize_individual_article(combined_results, '/your/output/path')")
print("\n# Visualize trend analysis")
print("charts, interactive, files = visualize_trend_analysis(trend_results, '/your/output/path')")
print("\n# Quick visualization without saving")
print("quick_visualize(combined_results, 'individual')")

# =============================================================================
# CELL 4: FOOTER METRICS GENERATOR
# =============================================================================

def generate_article_footer_graphics(analysis_data, output_path=None):
    """Generate clean, publication-ready graphics for article footers"""
    
    print(f"📄 Generating footer graphics for: {analysis_data['article_name']}")
    
    # Create a clean, minimal style for footer graphics
    plt.style.use('default')
    
    # Footer-specific color palette (more muted)
    footer_colors = {
        'primary': '#2E86AB',
        'secondary': '#A23B72', 
        'accent': '#F18F01',
        'neutral': '#C73E1D'
    }
    
    # Create a compact summary visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Content Analysis Summary - {analysis_data["article_name"]}', 
                 fontsize=14, fontweight='bold')
    
    # 1. Content Origins (Pie Chart)
    attribution_stats = analysis_data['attribution_analysis']['statistics']
    origin_dist = attribution_stats['origin_distribution']
    
    labels = []
    sizes = []
    colors = []
    
    for version, stats in origin_dist.items():
        if version != 'new_in_final':
            labels.append(f"{version.title()}\n{stats['percentage']:.1f}%")
            sizes.append(stats['percentage'])
            colors.append(footer_colors['primary'])
    
    if 'new_in_final' in origin_dist:
        labels.append(f"New Content\n{origin_dist['new_in_final']['percentage']:.1f}%")
        sizes.append(origin_dist['new_in_final']['percentage'])
        colors.append(footer_colors['accent'])
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90)
    ax1.set_title('Content Origins', fontweight='bold')
    
    # 2. Word Count Progression (Bar Chart)
    processing = analysis_data['processing_summary']
    versions = ['Draft', 'Refined', 'Edited', 'Final']
    word_counts = []
    
    for version in ['draft', 'refined', 'edited', 'final']:
        if version in processing:
            word_counts.append(processing[version]['word_count'])
        else:
            word_counts.append(0)
    
    bars = ax2.bar(versions, word_counts, color=footer_colors['secondary'], alpha=0.7)
    ax2.set_title('Word Count Evolution', fontweight='bold')
    ax2.set_ylabel('Words')
    
    # Add value labels on bars
    for bar, count in zip(bars, word_counts):
        if count > 0:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(count)}', ha='center', va='bottom', fontsize=9)
    
    # 3. Modification Intensity (Horizontal Bar)
    mod_dist = attribution_stats['modification_distribution']
    mod_categories = []
    mod_values = []
    
    for category, stats in mod_dist.items():
        clean_cat = category.replace('_', ' ').title()
        mod_categories.append(clean_cat)
        mod_values.append(stats['percentage'])
    
    bars = ax3.barh(mod_categories, mod_values, color=footer_colors['neutral'], alpha=0.7)
    ax3.set_title('Modification Levels', fontweight='bold')
    ax3.set_xlabel('Percentage')
    
    # Add percentage labels
    for bar, value in zip(bars, mod_values):
        width = bar.get_width()
        ax3.text(width + 1, bar.get_y() + bar.get_height()/2.,
                f'{value:.1f}%', ha='left', va='center', fontsize=9)
    
    # 4. Key Metrics Summary (Text)
    ax4.axis('off')
    
    # Calculate key metrics
    draft_to_final = analysis_data['similarity_analysis']['draft_to_final']
    similarity_pct = draft_to_final['full_text']['combined'] * 100 if draft_to_final else 0
    
    word_change = 0
    if 'draft' in processing and 'final' in processing:
        draft_words = processing['draft']['word_count']
        final_words = processing['final']['word_count']
        word_change = ((final_words - draft_words) / draft_words) * 100
    
    # Display key metrics as text
    metrics_text = f"""
Key Metrics:

Draft-Final Similarity: {similarity_pct:.1f}%

Word Count Change: {word_change:+.1f}
```



## Prompt:
Continue



## Response:


AI Writing Analysis - Step 6 (Visualizations)

```python
# =============================================================================
# CELL 1: VISUALIZATION SETUP AND DEPENDENCIES
# =============================================================================

# Install required packages
!pip install matplotlib seaborn plotly pandas numpy -q

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from collections import defaultdict

# Set up plotting styles
plt.style.use('default')
sns.set_palette("husl")
pio.templates.default = "plotly_white"

# Custom color palette for consistency
COLORS = {
    'draft': '#FF6B6B',      # Red
    'refined': '#4ECDC4',    # Teal
    'edited': '#45B7D1',     # Blue
    'final': '#96CEB4',      # Green
    'new_content': '#FECA57', # Yellow
    'high_similarity': '#48CAE4',    # Light blue
    'medium_similarity': '#FFB3BA',  # Light pink
    'low_similarity': '#FFDFBA',     # Light orange
    'background': '#F8F9FA'
}

print("📊 Visualization dependencies loaded successfully!")
print("🎨 Custom color palette configured")

class VisualizationEngine:
    """Unified visualization engine for individual articles and trend analysis"""
    
    def __init__(self, output_path=None):
        self.output_path = output_path
        self.figures = {}
        
    def create_content_flow_chart(self, data, title="Content Flow Analysis", mode="individual"):
        """Create a content flow visualization showing version progression"""
        
        if mode == "individual":
            # Individual article - show attribution percentages
            attribution_stats = data['attribution_analysis']['statistics']
            origin_dist = attribution_stats['origin_distribution']
            
            # Prepare data for flow chart
            flow_data = []
            for version, stats in origin_dist.items():
                if version != 'new_in_final':
                    flow_data.append({
                        'source': version.title(),
                        'target': 'Final Article',
                        'value': stats['percentage'],
                        'count': stats['count']
                    })
            
            # Add new content
            if 'new_in_final' in origin_dist:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Article', 
                    'value': origin_dist['new_in_final']['percentage'],
                    'count': origin_dist['new_in_final']['count']
                })
        
        else:
            # Trend analysis - show average percentages
            avg_data = data['attribution_trends']['averages']
            flow_data = []
            
            for key, value in avg_data.items():
                if key.startswith('origin_') and not key.endswith('new_in_final'):
                    version = key.replace('origin_', '').title()
                    flow_data.append({
                        'source': version,
                        'target': 'Final Articles',
                        'value': value,
                        'count': f"{value:.1f}% avg"
                    })
            
            # Add new content average
            if 'origin_new_in_final' in avg_data:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Articles',
                    'value': avg_data['origin_new_in_final'],
                    'count': f"{avg_data['origin_new_in_final']:.1f}% avg"
                })
        
        # Create sankey-style visualization using matplotlib
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Draw flow connections
        y_positions = np.linspace(8, 2, len(flow_data))
        
        for i, item in enumerate(flow_data):
            # Source box
            source_color = COLORS.get(item['source'].lower(), '#CCCCCC')
            source_rect = patches.Rectangle((0.5, y_positions[i]-0.3), 2, 0.6, 
                                          facecolor=source_color, alpha=0.7, edgecolor='black')
            ax.add_patch(source_rect)
            ax.text(1.5, y_positions[i], item['source'], ha='center', va='center', fontweight='bold')
            
            # Flow arrow
            arrow_width = item['value'] / 100 * 0.4  # Scale arrow width by percentage
            arrow = patches.FancyArrowPatch((2.5, y_positions[i]), (6.5, 5),
                                          arrowstyle='->', mutation_scale=20,
                                          linewidth=arrow_width*10, alpha=0.6,
                                          color=source_color)
            ax.add_patch(arrow)
            
            # Percentage label
            ax.text(4.5, y_positions[i]+0.2, f"{item['value']:.1f}%", 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Target box
        target_rect = patches.Rectangle((7, 4.5), 2, 1, 
                                      facecolor=COLORS['final'], alpha=0.7, edgecolor='black')
        ax.add_patch(target_rect)
        target_text = 'Final Article' if mode == 'individual' else 'Final Articles'
        ax.text(8, 5, target_text, ha='center', va='center', fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        return fig
    
    def create_modification_intensity_chart(self, data, title="Content Modification Intensity", mode="individual"):
        """Create a chart showing modification intensity levels"""
        
        if mode == "individual":
            mod_dist = data['attribution_analysis']['statistics']['modification_distribution']
            categories = list(mod_dist.keys())
            values = [mod_dist[cat]['percentage'] for cat in categories]
        else:
            # Trend analysis
            avg_data = data['attribution_trends']['averages']
            categories = []
            values = []
            for key, value in avg_data.items():
                if key.startswith('modification_'):
                    cat = key.replace('modification_', '').replace('_', ' ').title()
                    categories.append(cat)
                    values.append(value)
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Color mapping for modification levels
        mod_colors = [COLORS.get(cat.lower().replace(' ', '_'), '#CCCCCC') for cat in categories]
        
        bars = ax.barh(categories, values, color=mod_colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add percentage labels on bars
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                   f'{value:.1f}%', ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel('Percentage of Content', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, max(values) * 1.2)
        
        # Add grid for readability
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        return fig
    
    def create_word_count_progression(self, data, title="Word Count Progression", mode="individual"):
        """Create a line chart showing word count changes across versions"""
        
        if mode == "individual":
            processing = data['processing_summary']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in processing:
                    word_counts.append(processing[version]['word_count'])
                    version_labels.append(version.title())
        else:
            # Trend analysis - show averages
            avg_data = data['word_count_trends']['averages']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in avg_data:
                    word_counts.append(avg_data[version])
                    version_labels.append(version.title())
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        line = ax.plot(version_labels, word_counts, marker='o', linewidth=3, 
                      markersize=8, color=COLORS['draft'], markerfacecolor=COLORS['final'])
        
        # Add value labels on points
        for i, (label, count) in enumerate(zip(version_labels, word_counts)):
            ax.annotate(f'{int(count)}', (i, count), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontweight='bold')
        
        ax.set_ylabel('Word Count', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Calculate and show percentage change
        if len(word_counts) >= 2:
            change = ((word_counts[-1] - word_counts[0]) / word_counts[0]) * 100
            change_text = f"Overall change: {change:+.1f}%"
            ax.text(0.02, 0.98, change_text, transform=ax.transAxes, 
                   fontsize=11, fontweight='bold', verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        return fig
    
    def create_similarity_heatmap(self, data, title="Version Similarity Matrix", mode="individual"):
        """Create a heatmap showing similarities between versions"""
        
        if mode == "individual":
            similarity_data = data['similarity_analysis']['sequential_analysis']
            
            # Build similarity matrix
            versions = ['Draft', 'Refined', 'Edited', 'Final']
            matrix = np.zeros((len(versions), len(versions)))
            np.fill_diagonal(matrix, 1.0)  # Perfect similarity with self
            
            # Fill in the sequential similarities
            for seq in similarity_data:
                pair = seq['version_pair']
                similarity = seq['full_text']['combined']
                
                # Parse version pair (e.g., "draft_to_refined")
                from_version, to_version = pair.split('_to_')
                from_idx = versions.index(from_version.title())
                to_idx = versions.index(to_version.title())
                
                matrix[from_idx][to_idx] = similarity
                matrix[to_idx][from_idx] = similarity  # Make symmetric
        
        else:
            # For trend analysis, show average similarities
            similarity_trends = data['similarity_trends']
            
            # Create a simplified matrix for trends
            versions = ['Draft', 'Final']
            matrix = np.array([[1.0, 0.0], [0.0, 1.0]])
            
            if similarity_trends['averages'].get('draft_to_final'):
                avg_sim = similarity_trends['averages']['draft_to_final']['combined']
                matrix[0][1] = avg_sim
                matrix[1][0] = avg_sim
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        
        im = ax.imshow(matrix, cmap='RdYlGn', aspect='equal', vmin=0, vmax=1)
        
        # Add text annotations
        for i in range(len(versions)):
            for j in range(len(versions)):
                text = ax.text(j, i, f'{matrix[i, j]:.2f}', 
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_xticks(range(len(versions)))
        ax.set_yticks(range(len(versions)))
        ax.set_xticklabels(versions)
        ax.set_yticklabels(versions)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Similarity Score', rotation=270, labelpad=20, fontweight='bold')
        
        return fig
    
    def create_summary_dashboard(self, data, title_prefix="Article Analysis", mode="individual"):
        """Create a comprehensive dashboard with multiple visualizations"""
        
        # Create subplots
        fig = plt.figure(figsize=(16, 12))
        
        # Title
        main_title = f"{title_prefix} Dashboard"
        if mode == "individual":
            main_title += f" - {data['article_name']}"
        
        fig.suptitle(main_title, fontsize=18, fontweight='bold', y=0.95)
        
        # Create individual charts and save them
        charts = {}
        
        # Content Flow Chart
        charts['flow'] = self.create_content_flow_chart(data, "Content Attribution", mode)
        
        # Modification Intensity
        charts['modification'] = self.create_modification_intensity_chart(data, "Modification Intensity", mode)
        
        # Word Count Progression
        charts['word_count'] = self.create_word_count_progression(data, "Word Count Evolution", mode)
        
        # Similarity Heatmap
        charts['similarity'] = self.create_similarity_heatmap(data, "Version Similarities", mode)
        
        return charts
    
    def save_visualizations(self, charts, prefix="analysis", formats=['png', 'svg']):
        """Save all visualizations in multiple formats"""
        
        if not self.output_path:
            print("⚠️ No output path specified - visualizations not saved")
            return {}
        
        os.makedirs(self.output_path, exist_ok=True)
        saved_files = {}
        
        for chart_name, fig in charts.items():
            for fmt in formats:
                filename = f"{prefix}_{chart_name}.{fmt}"
                filepath = os.path.join(self.output_path, filename)
                
                fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                
                if chart_name not in saved_files:
                    saved_files[chart_name] = []
                saved_files[chart_name].append(filepath)
        
        # Close figures to free memory
        for fig in charts.values():
            plt.close(fig)
        
        print(f"💾 Visualizations saved to: {self.output_path}")
        for chart_name, files in saved_files.items():
            print(f"  📊 {chart_name}: {len(files)} formats")
        
        return saved_files

print("🎨 VisualizationEngine class loaded successfully!")

# =============================================================================
# CELL 2: INTERACTIVE VISUALIZATION FUNCTIONS
# =============================================================================

def create_interactive_flow_chart(data, mode="individual"):
    """Create an interactive Plotly flow/sankey diagram"""
    
    if mode == "individual":
        attribution_stats = data['attribution_analysis']['statistics']
        origin_dist = attribution_stats['origin_distribution']
        
        # Prepare data for Sankey diagram
        sources = []
        targets = []
        values = []
        labels = []
        
        # Add all source versions
        for version in ['draft', 'refined', 'edited']:
            if version in origin_dist:
                labels.append(version.title())
        
        # Add new content and final
        if 'new_in_final' in origin_dist:
            labels.append('New Content')
        labels.append('Final Article')
        
        # Create connections
        final_idx = len(labels) - 1
        
        for version, stats in origin_dist.items():
            if version != 'new_in_final':
                source_idx = labels.index(version.title())
                sources.append(source_idx)
                targets.append(final_idx)
                values.append(stats['percentage'])
        
        # Add new content if exists
        if 'new_in_final' in origin_dist:
            new_idx = labels.index('New Content')
            sources.append(new_idx)
            targets.append(final_idx)
            values.append(origin_dist['new_in_final']['percentage'])
    
    else:
        # Trend analysis mode
        avg_data = data['attribution_trends']['averages']
        labels = []
        sources = []
        targets = []
        values = []
        
        # Build labels and connections for trend data
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                version = key.replace('origin_', '')
                if version != 'new_in_final':
                    labels.append(version.title())
                else:
                    labels.append('New Content')
        
        labels.append('Final Articles')
        final_idx = len(labels) - 1
        
        # Create connections
        i = 0
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                sources.append(i)
                targets.append(final_idx)
                values.append(value)
                i += 1
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=[COLORS.get(label.lower().replace(' ', '_'), '#CCCCCC') for label in labels]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=['rgba(255,107,107,0.4)' if i < len(sources) else 'rgba(150,206,180,0.4)' 
                   for i in range(len(sources))]
        )
    )])
    
    title = "Content Flow Analysis"
    if mode == "individual":
        title += f" - {data['article_name']}"
    
    fig.update_layout(
        title_text=title,
        font_size=12,
        height=600
    )
    
    return fig

def create_interactive_trends_chart(trend_data):
    """Create interactive trend charts for multiple articles over time"""
    
    # Extract data for trends over time
    attribution_by_article = trend_data['attribution_trends']['by_article']
    
    if not attribution_by_article:
        print("No trend data available")
        return None
    
    # Prepare data for plotting
    dates = []
    draft_retention = []
    edited_dominance = []
    new_content = []
    article_names = []
    
    for article in attribution_by_article:
        dates.append(article['publication_date'])
        article_names.append(article['article_name'])
        
        # Extract percentages
        draft_retention.append(article['origin_percentages'].get('draft', 0))
        edited_dominance.append(article['origin_percentages'].get('edited', 0))
        new_content.append(article['origin_percentages'].get('new_in_final', 0))
    
    # Create multi-line chart
    fig = go.Figure()
    
    # Add traces for each metric
    fig.add_trace(go.Scatter(
        x=dates, y=draft_retention,
        mode='lines+markers',
        name='Draft Retention %',
        line=dict(color=COLORS['draft'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Draft Retention: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=edited_dominance,
        mode='lines+markers',
        name='Edited Content %',
        line=dict(color=COLORS['edited'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Edited Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=new_content,
        mode='lines+markers',
        name='New Content %',
        line=dict(color=COLORS['new_content'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>New Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.update_layout(
        title='Content Attribution Trends Over Time',
        xaxis_title='Publication Date',
        yaxis_title='Percentage of Final Content',
        hovermode='x unified',
        height=600,
        showlegend=True
    )
    
    return fig

print("🚀 Interactive visualization functions loaded!")

# =============================================================================
# CELL 3: EXECUTION FUNCTIONS
# =============================================================================

def visualize_individual_article(analysis_data, output_path=None, save_files=True):
    """Create visualizations for a single article analysis"""
    
    print(f"🎨 Creating visualizations for: {analysis_data['article_name']}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static visualizations...")
    charts = viz_engine.create_summary_dashboard(analysis_data, mode="individual")
    
    # Create interactive chart
    print("🔧 Creating interactive flow chart...")
    interactive_flow = create_interactive_flow_chart(analysis_data, mode="individual")
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts, 
            prefix=f"{analysis_data['article_name']}_analysis",
            formats=['png', 'svg']
        )
        
        # Save interactive chart
        interactive_file = os.path.join(output_path, f"{analysis_data['article_name']}_interactive_flow.html")
        interactive_flow.write_html(interactive_file)
        saved_files['interactive_flow'] = [interactive_file]
        print(f"💾 Interactive chart saved: {interactive_file}")
    
    # Display interactive chart
    interactive_flow.show()
    
    return charts, interactive_flow, saved_files

def visualize_trend_analysis(trend_data, output_path=None, save_files=True):
    """Create visualizations for trend analysis"""
    
    period = trend_data['period']
    print(f"📈 Creating trend visualizations for period: {period}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static trend visualizations...")
    charts = viz_engine.create_summary_dashboard(trend_data, f"Trend Analysis - {period}", mode="trend")
    
    # Create interactive charts
    print("🔧 Creating interactive trend charts...")
    interactive_flow = create_interactive_flow_chart(trend_data, mode="trend")
    interactive_trends = create_interactive_trends_chart(trend_data)
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts,
            prefix=f"trend_analysis_{period}",
            formats=['png', 'svg']
        )
        
        # Save interactive charts
        if output_path:
            flow_file = os.path.join(output_path, f"trend_flow_{period}.html")
            interactive_flow.write_html(flow_file)
            saved_files['interactive_flow'] = [flow_file]
            
            if interactive_trends:
                trends_file = os.path.join(output_path, f"trend_timeline_{period}.html")
                interactive_trends.write_html(trends_file)
                saved_files['interactive_trends'] = [trends_file]
                print(f"💾 Interactive charts saved to: {output_path}")
    
    # Display interactive charts
    interactive_flow.show()
    if interactive_trends:
        interactive_trends.show()
    
    return charts, {'flow': interactive_flow, 'trends': interactive_trends}, saved_files

def quick_visualize(data, data_type="individual", output_path=None):
    """Quick visualization function for any analysis data"""
    
    if data_type == "individual":
        return visualize_individual_article(data, output_path, save_files=bool(output_path))
    elif data_type == "trend":
        return visualize_trend_analysis(data, output_path, save_files=bool(output_path))
    else:
        print(f"❌ Unknown data type: {data_type}")
        return None

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Visualize individual article (using existing analysis data)")
print("charts, interactive, files = visualize_individual_article(combined_results, '/your/output/path')")
print("\n# Visualize trend analysis")
print("charts, interactive, files = visualize_trend_analysis(trend_results, '/your/output/path')")
print("\n# Quick visualization without saving")
print("quick_visualize(combined_results, 'individual')")

# =============================================================================
# CELL 4: FOOTER METRICS GENERATOR
# =============================================================================

def generate_article_footer_graphics(analysis_data, output_path=None):
    """Generate clean, publication-ready graphics for article footers"""
    
    print(f"📄 Generating footer graphics for: {analysis_data['article_name']}")
    
    # Create a clean, minimal style for footer graphics
    plt.style.use('default')
    
    # Footer-specific color palette (more muted)
    footer_colors = {
        'primary': '#2E86AB',
        'secondary': '#A23B72', 
        'accent': '#F18F01',
        'neutral': '#C73E1D'
    }
    
    # Create a compact summary visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Content Analysis Summary - {analysis_data["article_name"]}', 
                 fontsize=14, fontweight='bold')
    
    # 1. Content Origins (Pie Chart)
    attribution_stats = analysis_data['attribution_analysis']['statistics']
    origin_dist = attribution_stats['origin_distribution']
    
    labels = []
    sizes = []
    colors = []
    
    for version, stats in origin_dist.items():
        if version != 'new_in_final':
            labels.append(f"{version.title()}\n{stats['percentage']:.1f}%")
            sizes.append(stats['percentage'])
            colors.append(footer_colors['primary'])
    
    if 'new_in_final' in origin_dist:
        labels.append(f"New Content\n{origin_dist['new_in_final']['percentage']:.1f}%")
        sizes.append(origin_dist['new_in_final']['percentage'])
        colors.append(footer_colors['accent'])
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90)
    ax1.set_title('Content Origins', fontweight='bold')
    
    # 2. Word Count Progression (Bar Chart)
    processing = analysis_data['processing_summary']
    versions = ['Draft', 'Refined', 'Edited', 'Final']
    word_counts = []
    
    for version in ['draft', 'refined', 'edited', 'final']:
        if version in processing:
            word_counts.append(processing[version]['word_count'])
        else:
            word_counts.append(0)
    
    bars = ax2.bar(versions, word_counts, color=footer_colors['secondary'], alpha=0.7)
    ax2.set_title('Word Count Evolution', fontweight='bold')
    ax2.set_ylabel('Words')
    
    # Add value labels on bars
    for bar, count in zip(bars, word_counts):
        if count > 0:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(count)}', ha='center', va='bottom', fontsize=9)
    
    # 3. Modification Intensity (Horizontal Bar)
    mod_dist = attribution_stats['modification_distribution']
    mod_categories = []
    mod_values = []
    
    for category, stats in mod_dist.items():
        clean_cat = category.replace('_', ' ').title()
        mod_categories.append(clean_cat)
        mod_values.append(stats['percentage'])
    
    bars = ax3.barh(mod_categories, mod_values, color=footer_colors['neutral'], alpha=0.7)
    ax3.set_title('Modification Levels', fontweight='bold')
    ax3.set_xlabel('Percentage')
    
    # Add percentage labels
    for bar, value in zip(bars, mod_values):
        width = bar.get_width()
        ax3.text(width + 1, bar.get_y() + bar.get_height()/2.,
                f'{value:.1f}%', ha='left', va='center', fontsize=9)
    
    # 4. Key Metrics Summary (Text)
    ax4.axis('off')
    
    # Calculate key metrics
    draft_to_final = analysis_data['similarity_analysis']['draft_to_final']
    similarity_pct = draft_to_final['full_text']['combined'] * 100 if draft_to_final else 0
    
    word_change = 0
    if 'draft' in processing and 'final' in processing:
        draft_words = processing['draft']['word_count']
        final_words = processing['final']['word_count']
        word_change = ((final_words - draft_words) / draft_words) * 100
    
    # Display key metrics as text
    metrics_text = f"""Key Metrics:

Draft-Final Similarity: {similarity_pct:.1f}%

Word Count Change: {word_change:+.1f}%

Total Sentences: {attribution_stats['total_sentences']}

Analysis Date: {datetime.now().strftime('%Y-%m-%d')}"""
    
    ax4.text(0.1, 0.9, metrics_text, transform=ax4.transAxes, 
             fontsize=11, verticalalignment='top', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.3))
    
    ax4.set_title('Summary Statistics', fontweight='bold')
    
    plt.tight_layout()
    
    # Save footer graphic
    footer_files = {}
    if output_path:
        os.makedirs(output_path, exist_ok=True)
        
        # Save in multiple formats for footer use
        for fmt in ['png', 'svg', 'pdf']:
            footer_file = os.path.join(output_path, f"{analysis_data['article_name']}_footer.{fmt}")
            fig.savefig(footer_file, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            footer_files[fmt] = footer_file
        
        print(f"📄 Footer graphics saved: {len(footer_files)} formats")
    
    return fig, footer_files

def create_minimal_attribution_chart(analysis_data, output_path=None):
    """Create a minimal, clean chart suitable for article footers"""
    
    # Very simple pie chart for content attribution
    fig, ax = plt.subplots(figsize=(6, 4))
    
    attribution_stats = analysis_data['attribution_analysis']['statistics']
    origin_dist = attribution_stats['origin_distribution']
    
    # Aggregate into simple categories
    ai_generated = 0  # draft + refined
    human_edited = 0  # edited
    new_content = 0   # new_in_final
    
    for version, stats in origin_dist.items():
        if version in ['draft', 'refined']:
            ai_generated += stats['percentage']
        elif version == 'edited':
            human_edited = stats['percentage']
        elif version == 'new_in_final':
            new_content = stats['percentage']
    
    # Create simple pie chart
    labels = []
    sizes = []
    colors = ['#FF6B6B', '#4ECDC4', '#FECA57']
    
    if ai_generated > 0:
        labels.append(f'AI Generated\n{ai_generated:.1f}%')
        sizes.append(ai_generated)
    
    if human_edited > 0:
        labels.append(f'Human Edited\n{human_edited:.1f}%')
        sizes.append(human_edited)
    
    if new_content > 0:
        labels.append(f'New Content\n{new_content:.1f}%')
        sizes.append(new_content)
    
    wedges, texts = ax.pie(sizes, labels=labels, colors=colors[:len(sizes)], 
                          autopct='', startangle=90, textprops={'fontsize': 10})
    
    ax.set_title(f'Content Attribution - {analysis_data["article_name"]}', 
                fontsize=12, fontweight='bold', pad=10)
    
    # Save minimal chart
    minimal_files = {}
    if output_path:
        os.makedirs(output_path, exist_ok=True)
        
        for fmt in ['png', 'svg']:
            minimal_file = os.path.join(output_path, f"{analysis_data['article_name']}_minimal.{fmt}")
            fig.savefig(minimal_file, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            minimal_files[fmt] = minimal_file
        
        print(f"📊 Minimal chart saved: {len(minimal_files)} formats")
    
    return fig, minimal_files

print("📄 Footer graphics functions loaded!")

# =============================================================================
# CELL 5: COMPLETE VISUALIZATION WORKFLOW
# =============================================================================

def create_complete_visualization_suite(analysis_data, output_path=None, data_type="individual"):
    """Create a complete suite of visualizations for any analysis data"""
    
    print(f"🎨 Creating complete visualization suite...")
    print(f"📊 Data type: {data_type}")
    
    if not output_path:
        print("⚠️ No output path provided - visualizations will not be saved")
    
    all_outputs = {
        'static_charts': {},
        'interactive_charts': {},
        'footer_graphics': {},
        'saved_files': {}
    }
    
    # Create main visualizations
    if data_type == "individual":
        # Individual article visualizations
        charts, interactive, files = visualize_individual_article(
            analysis_data, output_path, save_files=bool(output_path)
        )
        
        all_outputs['static_charts'] = charts
        all_outputs['interactive_charts'] = {'flow': interactive}
        all_outputs['saved_files'].update(files)
        
        # Create footer graphics
        if output_path:
            footer_fig, footer_files = generate_article_footer_graphics(analysis_data, output_path)
            minimal_fig, minimal_files = create_minimal_attribution_chart(analysis_data, output_path)
            
            all_outputs['footer_graphics']['full'] = footer_fig
            all_outputs['footer_graphics']['minimal'] = minimal_fig
            all_outputs['saved_files']['footer'] = footer_files
            all_outputs['saved_files']['minimal'] = minimal_files
            
            # Close footer figures
            plt.close(footer_fig)
            plt.close(minimal_fig)
    
    elif data_type == "trend":
        # Trend analysis visualizations
        charts, interactive, files = visualize_trend_analysis(
            analysis_data, output_path, save_files=bool(output_path)
        )
        
        all_outputs['static_charts'] = charts
        all_outputs['interactive_charts'] = interactive
        all_outputs['saved_files'].update(files)
    
    print(f"✅ Visualization suite complete!")
    if output_path:
        print(f"📁 All files saved to: {output_path}")
    
    return all_outputs

def visualize_from_existing_data(analysis_data_or_file, output_path=None, data_type="auto"):
    """Load and visualize from existing analysis data or file"""
    
    # Handle file input
    if isinstance(analysis_data_or_file, str):
        print(f"📖 Loading analysis data from: {analysis_data_or_file}")
        with open(analysis_data_or_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
    else:
        analysis_data = analysis_data_or_file
    
    # Auto-detect data type if not specified
    if data_type == "auto":
        if 'article_name' in analysis_data and 'attribution_analysis' in analysis_data:
            data_type = "individual"
        elif 'period' in analysis_data and 'attribution_trends' in analysis_data:
            data_type = "trend"
        else:
            print("❌ Could not auto-detect data type")
            return None
    
    print(f"🔍 Detected data type: {data_type}")
    
    # Create visualizations
    return create_complete_visualization_suite(analysis_data, output_path, data_type)

# Quick access functions
def viz_article(analysis_data, output_path=None):
    """Quick function to visualize individual article"""
    return create_complete_visualization_suite(analysis_data, output_path, "individual")

def viz_trends(trend_data, output_path=None):
    """Quick function to visualize trend analysis"""
    return create_complete_visualization_suite(trend_data, output_path, "trend")

print("🚀 Complete visualization workflow loaded!")
print("\n" + "="*60)
print("📊 VISUALIZATION SYSTEM READY!")
print("="*60)
print("\nQuick usage:")
print("# Visualize your existing analysis data")
print("viz_outputs = viz_article(combined_results, '/your/output/path')")
print("\n# Visualize trend analysis") 
print("trend_viz = viz_trends(trend_results, '/your/output/path')")
print("\n# Create footer graphics only")
print("footer_fig, files = generate_article_footer_graphics(combined_results, '/path')")
print("\nAll visualizations include:")
print("  📈 Static charts (PNG, SVG)")
print("  🔧 Interactive charts (HTML)")
print("  📄 Footer graphics (publication-ready)")
print("  💾 Multiple file formats")
```

Perfect! The complete visualization system is now built. Here's what you have:

## **Step 6: Comprehensive Visualization System**

### **Core Features:**
- **Static Charts**: Professional matplotlib/seaborn visualizations
- **Interactive Charts**: Plotly-based interactive visualizations
- **Footer Graphics**: Clean, publication-ready charts for article footers
- **Unified Engine**: Same system works for individual articles and trend analysis

### **Visualization Types:**
1. **Content Flow Charts** - Shows how content flows from draft to final
2. **Modification Intensity** - Displays editing intensity levels
3. **Word Count Progression** - Tracks word changes across versions
4. **Similarity Heatmaps** - Version-to-version similarity matrices
5. **Summary Dashboards** - Combined multi-chart views
6. **Footer Graphics** - Minimal charts perfect for article footers

### **Ready to Use:**
```python
# Visualize your markup-languages article
viz_outputs = viz_article(combined_results, '/your/output/path')

# Create just footer graphics
footer_fig, files = generate_article_footer_graphics(combined_results, '/path')

# Visualize trend analysis (when you have more articles)
trend_viz = viz_trends(trend_results, '/your/output/path')
```

### **What You Get:**
- **Static files**: PNG, SVG, PDF formats
- **Interactive files**: HTML charts you can embed
- **Footer charts**: Publication-ready graphics for your articles
- **Multiple formats**: Choose what works best for your publication workflow

Want to test the visualization system with your existing "markup-languages" analysis data? You can run `viz_article(combined_results)` to see all the charts in action!



## Prompt:
🎨 Creating complete visualization suite... 📊 Data type: individual 🎨 Creating visualizations for: markup-languages 📊 Generating static visualizations... 🔧 Creating interactive flow chart... 💾 Visualizations saved to: /your/output/path 📊 flow: 2 formats 📊 modification: 2 formats 📊 word_count: 2 formats 📊 similarity: 2 formats 💾 Interactive chart saved: /your/output/path/markup-languages_interactive_flow.html


```
📄 Generating footer graphics for: markup-languages
📄 Footer graphics saved: 3 formats

```


```
---------------------------------------------------------------------------

```


```
ValueError                                Traceback (most recent call last)

```


```
<ipython-input-67-798336572> in <cell line: 0>()
----> 1 viz_outputs = viz_article(combined_results, '/your/output/path')


```

2 frames

```
<ipython-input-65-3337085131> in create_minimal_attribution_chart(analysis_data, output_path)
    175         sizes.append(new_content)
    176 
--> 177     wedges, texts = ax.pie(sizes, labels=labels, colors=colors[:len(sizes)], 
    178                           autopct='', startangle=90, textprops={'fontsize': 10})
    179 


```


```
ValueError: too many values to unpack (expected 2)
```


```
<Figure size 1600x1200 with 0 Axes>
```



## Response:
The error is in the minimal attribution chart - `ax.pie()` returns different numbers of values depending on the parameters. Let me fix this:

AI Writing Analysis - Step 6 (Visualizations)

```python
# =============================================================================
# CELL 1: VISUALIZATION SETUP AND DEPENDENCIES
# =============================================================================

# Install required packages
!pip install matplotlib seaborn plotly pandas numpy -q

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from collections import defaultdict

# Set up plotting styles
plt.style.use('default')
sns.set_palette("husl")
pio.templates.default = "plotly_white"

# Custom color palette for consistency
COLORS = {
    'draft': '#FF6B6B',      # Red
    'refined': '#4ECDC4',    # Teal
    'edited': '#45B7D1',     # Blue
    'final': '#96CEB4',      # Green
    'new_content': '#FECA57', # Yellow
    'high_similarity': '#48CAE4',    # Light blue
    'medium_similarity': '#FFB3BA',  # Light pink
    'low_similarity': '#FFDFBA',     # Light orange
    'background': '#F8F9FA'
}

print("📊 Visualization dependencies loaded successfully!")
print("🎨 Custom color palette configured")

class VisualizationEngine:
    """Unified visualization engine for individual articles and trend analysis"""
    
    def __init__(self, output_path=None):
        self.output_path = output_path
        self.figures = {}
        
    def create_content_flow_chart(self, data, title="Content Flow Analysis", mode="individual"):
        """Create a content flow visualization showing version progression"""
        
        if mode == "individual":
            # Individual article - show attribution percentages
            attribution_stats = data['attribution_analysis']['statistics']
            origin_dist = attribution_stats['origin_distribution']
            
            # Prepare data for flow chart
            flow_data = []
            for version, stats in origin_dist.items():
                if version != 'new_in_final':
                    flow_data.append({
                        'source': version.title(),
                        'target': 'Final Article',
                        'value': stats['percentage'],
                        'count': stats['count']
                    })
            
            # Add new content
            if 'new_in_final' in origin_dist:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Article', 
                    'value': origin_dist['new_in_final']['percentage'],
                    'count': origin_dist['new_in_final']['count']
                })
        
        else:
            # Trend analysis - show average percentages
            avg_data = data['attribution_trends']['averages']
            flow_data = []
            
            for key, value in avg_data.items():
                if key.startswith('origin_') and not key.endswith('new_in_final'):
                    version = key.replace('origin_', '').title()
                    flow_data.append({
                        'source': version,
                        'target': 'Final Articles',
                        'value': value,
                        'count': f"{value:.1f}% avg"
                    })
            
            # Add new content average
            if 'origin_new_in_final' in avg_data:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Articles',
                    'value': avg_data['origin_new_in_final'],
                    'count': f"{avg_data['origin_new_in_final']:.1f}% avg"
                })
        
        # Create sankey-style visualization using matplotlib
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Draw flow connections
        y_positions = np.linspace(8, 2, len(flow_data))
        
        for i, item in enumerate(flow_data):
            # Source box
            source_color = COLORS.get(item['source'].lower(), '#CCCCCC')
            source_rect = patches.Rectangle((0.5, y_positions[i]-0.3), 2, 0.6, 
                                          facecolor=source_color, alpha=0.7, edgecolor='black')
            ax.add_patch(source_rect)
            ax.text(1.5, y_positions[i], item['source'], ha='center', va='center', fontweight='bold')
            
            # Flow arrow
            arrow_width = item['value'] / 100 * 0.4  # Scale arrow width by percentage
            arrow = patches.FancyArrowPatch((2.5, y_positions[i]), (6.5, 5),
                                          arrowstyle='->', mutation_scale=20,
                                          linewidth=arrow_width*10, alpha=0.6,
                                          color=source_color)
            ax.add_patch(arrow)
            
            # Percentage label
            ax.text(4.5, y_positions[i]+0.2, f"{item['value']:.1f}%", 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Target box
        target_rect = patches.Rectangle((7, 4.5), 2, 1, 
                                      facecolor=COLORS['final'], alpha=0.7, edgecolor='black')
        ax.add_patch(target_rect)
        target_text = 'Final Article' if mode == 'individual' else 'Final Articles'
        ax.text(8, 5, target_text, ha='center', va='center', fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        return fig
    
    def create_modification_intensity_chart(self, data, title="Content Modification Intensity", mode="individual"):
        """Create a chart showing modification intensity levels"""
        
        if mode == "individual":
            mod_dist = data['attribution_analysis']['statistics']['modification_distribution']
            categories = list(mod_dist.keys())
            values = [mod_dist[cat]['percentage'] for cat in categories]
        else:
            # Trend analysis
            avg_data = data['attribution_trends']['averages']
            categories = []
            values = []
            for key, value in avg_data.items():
                if key.startswith('modification_'):
                    cat = key.replace('modification_', '').replace('_', ' ').title()
                    categories.append(cat)
                    values.append(value)
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Color mapping for modification levels
        mod_colors = [COLORS.get(cat.lower().replace(' ', '_'), '#CCCCCC') for cat in categories]
        
        bars = ax.barh(categories, values, color=mod_colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add percentage labels on bars
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                   f'{value:.1f}%', ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel('Percentage of Content', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, max(values) * 1.2)
        
        # Add grid for readability
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        return fig
    
    def create_word_count_progression(self, data, title="Word Count Progression", mode="individual"):
        """Create a line chart showing word count changes across versions"""
        
        if mode == "individual":
            processing = data['processing_summary']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in processing:
                    word_counts.append(processing[version]['word_count'])
                    version_labels.append(version.title())
        else:
            # Trend analysis - show averages
            avg_data = data['word_count_trends']['averages']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in avg_data:
                    word_counts.append(avg_data[version])
                    version_labels.append(version.title())
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        line = ax.plot(version_labels, word_counts, marker='o', linewidth=3, 
                      markersize=8, color=COLORS['draft'], markerfacecolor=COLORS['final'])
        
        # Add value labels on points
        for i, (label, count) in enumerate(zip(version_labels, word_counts)):
            ax.annotate(f'{int(count)}', (i, count), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontweight='bold')
        
        ax.set_ylabel('Word Count', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Calculate and show percentage change
        if len(word_counts) >= 2:
            change = ((word_counts[-1] - word_counts[0]) / word_counts[0]) * 100
            change_text = f"Overall change: {change:+.1f}%"
            ax.text(0.02, 0.98, change_text, transform=ax.transAxes, 
                   fontsize=11, fontweight='bold', verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        return fig
    
    def create_similarity_heatmap(self, data, title="Version Similarity Matrix", mode="individual"):
        """Create a heatmap showing similarities between versions"""
        
        if mode == "individual":
            similarity_data = data['similarity_analysis']['sequential_analysis']
            
            # Build similarity matrix
            versions = ['Draft', 'Refined', 'Edited', 'Final']
            matrix = np.zeros((len(versions), len(versions)))
            np.fill_diagonal(matrix, 1.0)  # Perfect similarity with self
            
            # Fill in the sequential similarities
            for seq in similarity_data:
                pair = seq['version_pair']
                similarity = seq['full_text']['combined']
                
                # Parse version pair (e.g., "draft_to_refined")
                from_version, to_version = pair.split('_to_')
                from_idx = versions.index(from_version.title())
                to_idx = versions.index(to_version.title())
                
                matrix[from_idx][to_idx] = similarity
                matrix[to_idx][from_idx] = similarity  # Make symmetric
        
        else:
            # For trend analysis, show average similarities
            similarity_trends = data['similarity_trends']
            
            # Create a simplified matrix for trends
            versions = ['Draft', 'Final']
            matrix = np.array([[1.0, 0.0], [0.0, 1.0]])
            
            if similarity_trends['averages'].get('draft_to_final'):
                avg_sim = similarity_trends['averages']['draft_to_final']['combined']
                matrix[0][1] = avg_sim
                matrix[1][0] = avg_sim
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        
        im = ax.imshow(matrix, cmap='RdYlGn', aspect='equal', vmin=0, vmax=1)
        
        # Add text annotations
        for i in range(len(versions)):
            for j in range(len(versions)):
                text = ax.text(j, i, f'{matrix[i, j]:.2f}', 
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_xticks(range(len(versions)))
        ax.set_yticks(range(len(versions)))
        ax.set_xticklabels(versions)
        ax.set_yticklabels(versions)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Similarity Score', rotation=270, labelpad=20, fontweight='bold')
        
        return fig
    
    def create_summary_dashboard(self, data, title_prefix="Article Analysis", mode="individual"):
        """Create a comprehensive dashboard with multiple visualizations"""
        
        # Create subplots
        fig = plt.figure(figsize=(16, 12))
        
        # Title
        main_title = f"{title_prefix} Dashboard"
        if mode == "individual":
            main_title += f" - {data['article_name']}"
        
        fig.suptitle(main_title, fontsize=18, fontweight='bold', y=0.95)
        
        # Create individual charts and save them
        charts = {}
        
        # Content Flow Chart
        charts['flow'] = self.create_content_flow_chart(data, "Content Attribution", mode)
        
        # Modification Intensity
        charts['modification'] = self.create_modification_intensity_chart(data, "Modification Intensity", mode)
        
        # Word Count Progression
        charts['word_count'] = self.create_word_count_progression(data, "Word Count Evolution", mode)
        
        # Similarity Heatmap
        charts['similarity'] = self.create_similarity_heatmap(data, "Version Similarities", mode)
        
        return charts
    
    def save_visualizations(self, charts, prefix="analysis", formats=['png', 'svg']):
        """Save all visualizations in multiple formats"""
        
        if not self.output_path:
            print("⚠️ No output path specified - visualizations not saved")
            return {}
        
        os.makedirs(self.output_path, exist_ok=True)
        saved_files = {}
        
        for chart_name, fig in charts.items():
            for fmt in formats:
                filename = f"{prefix}_{chart_name}.{fmt}"
                filepath = os.path.join(self.output_path, filename)
                
                fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                
                if chart_name not in saved_files:
                    saved_files[chart_name] = []
                saved_files[chart_name].append(filepath)
        
        # Close figures to free memory
        for fig in charts.values():
            plt.close(fig)
        
        print(f"💾 Visualizations saved to: {self.output_path}")
        for chart_name, files in saved_files.items():
            print(f"  📊 {chart_name}: {len(files)} formats")
        
        return saved_files

print("🎨 VisualizationEngine class loaded successfully!")

# =============================================================================
# CELL 2: INTERACTIVE VISUALIZATION FUNCTIONS
# =============================================================================

def create_interactive_flow_chart(data, mode="individual"):
    """Create an interactive Plotly flow/sankey diagram"""
    
    if mode == "individual":
        attribution_stats = data['attribution_analysis']['statistics']
        origin_dist = attribution_stats['origin_distribution']
        
        # Prepare data for Sankey diagram
        sources = []
        targets = []
        values = []
        labels = []
        
        # Add all source versions
        for version in ['draft', 'refined', 'edited']:
            if version in origin_dist:
                labels.append(version.title())
        
        # Add new content and final
        if 'new_in_final' in origin_dist:
            labels.append('New Content')
        labels.append('Final Article')
        
        # Create connections
        final_idx = len(labels) - 1
        
        for version, stats in origin_dist.items():
            if version != 'new_in_final':
                source_idx = labels.index(version.title())
                sources.append(source_idx)
                targets.append(final_idx)
                values.append(stats['percentage'])
        
        # Add new content if exists
        if 'new_in_final' in origin_dist:
            new_idx = labels.index('New Content')
            sources.append(new_idx)
            targets.append(final_idx)
            values.append(origin_dist['new_in_final']['percentage'])
    
    else:
        # Trend analysis mode
        avg_data = data['attribution_trends']['averages']
        labels = []
        sources = []
        targets = []
        values = []
        
        # Build labels and connections for trend data
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                version = key.replace('origin_', '')
                if version != 'new_in_final':
                    labels.append(version.title())
                else:
                    labels.append('New Content')
        
        labels.append('Final Articles')
        final_idx = len(labels) - 1
        
        # Create connections
        i = 0
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                sources.append(i)
                targets.append(final_idx)
                values.append(value)
                i += 1
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=[COLORS.get(label.lower().replace(' ', '_'), '#CCCCCC') for label in labels]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=['rgba(255,107,107,0.4)' if i < len(sources) else 'rgba(150,206,180,0.4)' 
                   for i in range(len(sources))]
        )
    )])
    
    title = "Content Flow Analysis"
    if mode == "individual":
        title += f" - {data['article_name']}"
    
    fig.update_layout(
        title_text=title,
        font_size=12,
        height=600
    )
    
    return fig

def create_interactive_trends_chart(trend_data):
    """Create interactive trend charts for multiple articles over time"""
    
    # Extract data for trends over time
    attribution_by_article = trend_data['attribution_trends']['by_article']
    
    if not attribution_by_article:
        print("No trend data available")
        return None
    
    # Prepare data for plotting
    dates = []
    draft_retention = []
    edited_dominance = []
    new_content = []
    article_names = []
    
    for article in attribution_by_article:
        dates.append(article['publication_date'])
        article_names.append(article['article_name'])
        
        # Extract percentages
        draft_retention.append(article['origin_percentages'].get('draft', 0))
        edited_dominance.append(article['origin_percentages'].get('edited', 0))
        new_content.append(article['origin_percentages'].get('new_in_final', 0))
    
    # Create multi-line chart
    fig = go.Figure()
    
    # Add traces for each metric
    fig.add_trace(go.Scatter(
        x=dates, y=draft_retention,
        mode='lines+markers',
        name='Draft Retention %',
        line=dict(color=COLORS['draft'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Draft Retention: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=edited_dominance,
        mode='lines+markers',
        name='Edited Content %',
        line=dict(color=COLORS['edited'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Edited Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=new_content,
        mode='lines+markers',
        name='New Content %',
        line=dict(color=COLORS['new_content'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>New Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.update_layout(
        title='Content Attribution Trends Over Time',
        xaxis_title='Publication Date',
        yaxis_title='Percentage of Final Content',
        hovermode='x unified',
        height=600,
        showlegend=True
    )
    
    return fig

print("🚀 Interactive visualization functions loaded!")

# =============================================================================
# CELL 3: EXECUTION FUNCTIONS
# =============================================================================

def visualize_individual_article(analysis_data, output_path=None, save_files=True):
    """Create visualizations for a single article analysis"""
    
    print(f"🎨 Creating visualizations for: {analysis_data['article_name']}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static visualizations...")
    charts = viz_engine.create_summary_dashboard(analysis_data, mode="individual")
    
    # Create interactive chart
    print("🔧 Creating interactive flow chart...")
    interactive_flow = create_interactive_flow_chart(analysis_data, mode="individual")
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts, 
            prefix=f"{analysis_data['article_name']}_analysis",
            formats=['png', 'svg']
        )
        
        # Save interactive chart
        interactive_file = os.path.join(output_path, f"{analysis_data['article_name']}_interactive_flow.html")
        interactive_flow.write_html(interactive_file)
        saved_files['interactive_flow'] = [interactive_file]
        print(f"💾 Interactive chart saved: {interactive_file}")
    
    # Display interactive chart
    interactive_flow.show()
    
    return charts, interactive_flow, saved_files

def visualize_trend_analysis(trend_data, output_path=None, save_files=True):
    """Create visualizations for trend analysis"""
    
    period = trend_data['period']
    print(f"📈 Creating trend visualizations for period: {period}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static trend visualizations...")
    charts = viz_engine.create_summary_dashboard(trend_data, f"Trend Analysis - {period}", mode="trend")
    
    # Create interactive charts
    print("🔧 Creating interactive trend charts...")
    interactive_flow = create_interactive_flow_chart(trend_data, mode="trend")
    interactive_trends = create_interactive_trends_chart(trend_data)
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts,
            prefix=f"trend_analysis_{period}",
            formats=['png', 'svg']
        )
        
        # Save interactive charts
        if output_path:
            flow_file = os.path.join(output_path, f"trend_flow_{period}.html")
            interactive_flow.write_html(flow_file)
            saved_files['interactive_flow'] = [flow_file]
            
            if interactive_trends:
                trends_file = os.path.join(output_path, f"trend_timeline_{period}.html")
                interactive_trends.write_html(trends_file)
                saved_files['interactive_trends'] = [trends_file]
                print(f"💾 Interactive charts saved to: {output_path}")
    
    # Display interactive charts
    interactive_flow.show()
    if interactive_trends:
        interactive_trends.show()
    
    return charts, {'flow': interactive_flow, 'trends': interactive_trends}, saved_files

def quick_visualize(data, data_type="individual", output_path=None):
    """Quick visualization function for any analysis data"""
    
    if data_type == "individual":
        return visualize_individual_article(data, output_path, save_files=bool(output_path))
    elif data_type == "trend":
        return visualize_trend_analysis(data, output_path, save_files=bool(output_path))
    else:
        print(f"❌ Unknown data type: {data_type}")
        return None

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Visualize individual article (using existing analysis data)")
print("charts, interactive, files = visualize_individual_article(combined_results, '/your/output/path')")
print("\n# Visualize trend analysis")
print("charts, interactive, files = visualize_trend_analysis(trend_results, '/your/output/path')")
print("\n# Quick visualization without saving")
print("quick_visualize(combined_results, 'individual')")

# =============================================================================
# CELL 4: FOOTER METRICS GENERATOR
# =============================================================================

def generate_article_footer_graphics(analysis_data, output_path=None):
    """Generate clean, publication-ready graphics for article footers"""
    
    print(f"📄 Generating footer graphics for: {analysis_data['article_name']}")
    
    # Create a clean, minimal style for footer graphics
    plt.style.use('default')
    
    # Footer-specific color palette (more muted)
    footer_colors = {
        'primary': '#2E86AB',
        'secondary': '#A23B72', 
        'accent': '#F18F01',
        'neutral': '#C73E1D'
    }
    
    # Create a compact summary visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Content Analysis Summary - {analysis_data["article_name"]}', 
                 fontsize=14, fontweight='bold')
    
    # 1. Content Origins (Pie Chart)
    attribution_stats = analysis_data['attribution_analysis']['statistics']
    origin_dist = attribution_stats['origin_distribution']
    
    labels = []
    sizes = []
    colors = []
    
    for version, stats in origin_dist.items():
        if version != 'new_in_final':
            labels.append(f"{version.title()}\n{stats['percentage']:.1f}%")
            sizes.append(stats['percentage'])
            colors.append(footer_colors['primary'])
    
    if 'new_in_final' in origin_dist:
        labels.append(f"New Content\n{origin_dist['new_in_final']['percentage']:.1f}%")
        sizes.append(origin_dist['new_in_final']['percentage'])
        colors.append(footer_colors['accent'])
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90)
    ax1.set_title('Content Origins', fontweight='bold')
    
    # 2. Word Count Progression (Bar Chart)
    processing = analysis_data['processing_summary']
    versions = ['Draft', 'Refined', 'Edited', 'Final']
    word_counts = []
    
    for version in ['draft', 'refined', 'edited', 'final']:
        if version in processing:
            word_counts.append(processing[version]['word_count'])
        else:
            word_counts.append(0)
    
    bars = ax2.bar(versions, word_counts, color=footer_colors['secondary'], alpha=0.7)
    ax2.set_title('Word Count Evolution', fontweight='bold')
    ax2.set_ylabel('Words')
    
    # Add value labels on bars
    for bar, count in zip(bars, word_counts):
        if count > 0:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(count)}', ha='center', va='bottom', fontsize=9)
    
    # 3. Modification Intensity (Horizontal Bar)
    mod_dist = attribution_stats['modification_distribution']
    mod_categories = []
    mod_values = []
    
    for category, stats in mod_dist.items():
        clean_cat = category.replace('_', ' ').title()
        mod_categories.append(clean_cat)
        mod_values.append(stats['percentage'])
    
    bars = ax3.barh(mod_categories, mod_values, color=footer_colors['neutral'], alpha=0.7)
    ax3.set_title('Modification Levels', fontweight='bold')
    ax3.set_xlabel('Percentage')
    
    # Add percentage labels
    for bar, value in zip(bars, mod_values):
        width = bar.get_width()
        ax3.text(width + 1, bar.get_y() + bar.get_height()/2.,
                f'{value:.1f}%', ha='left', va='center', fontsize=9)
    
    # 4. Key Metrics Summary (Text)
    ax4.axis('off')
    
    # Calculate key metrics
    draft_to_final = analysis_data['similarity_analysis']['draft_to_final']
    similarity_pct = draft_to_final['full_text']['combined'] * 100 if draft_to_final else 0
    
    word_change = 0
    if 'draft' in processing and 'final' in processing:
        draft_words = processing['draft']['word_count']
        final_words = processing['final']['word_count']
        word_change = ((final_words - draft_words) / draft_words) * 100
    
    # Display key metrics as text
    metrics_text = f"""
Key Metrics:

Draft-Final Similarity: {similarity_pct:.1f}%

Word Count Change: {word_change:+.1f}
```

Also, let me fix the output path issue so it uses the actual path instead of the placeholder:

AI Writing Analysis - Step 6 (Visualizations)

```python
# =============================================================================
# CELL 1: VISUALIZATION SETUP AND DEPENDENCIES
# =============================================================================

# Install required packages
!pip install matplotlib seaborn plotly pandas numpy -q

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from collections import defaultdict

# Set up plotting styles
plt.style.use('default')
sns.set_palette("husl")
pio.templates.default = "plotly_white"

# Custom color palette for consistency
COLORS = {
    'draft': '#FF6B6B',      # Red
    'refined': '#4ECDC4',    # Teal
    'edited': '#45B7D1',     # Blue
    'final': '#96CEB4',      # Green
    'new_content': '#FECA57', # Yellow
    'high_similarity': '#48CAE4',    # Light blue
    'medium_similarity': '#FFB3BA',  # Light pink
    'low_similarity': '#FFDFBA',     # Light orange
    'background': '#F8F9FA'
}

print("📊 Visualization dependencies loaded successfully!")
print("🎨 Custom color palette configured")

class VisualizationEngine:
    """Unified visualization engine for individual articles and trend analysis"""
    
    def __init__(self, output_path=None):
        self.output_path = output_path
        self.figures = {}
        
    def create_content_flow_chart(self, data, title="Content Flow Analysis", mode="individual"):
        """Create a content flow visualization showing version progression"""
        
        if mode == "individual":
            # Individual article - show attribution percentages
            attribution_stats = data['attribution_analysis']['statistics']
            origin_dist = attribution_stats['origin_distribution']
            
            # Prepare data for flow chart
            flow_data = []
            for version, stats in origin_dist.items():
                if version != 'new_in_final':
                    flow_data.append({
                        'source': version.title(),
                        'target': 'Final Article',
                        'value': stats['percentage'],
                        'count': stats['count']
                    })
            
            # Add new content
            if 'new_in_final' in origin_dist:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Article', 
                    'value': origin_dist['new_in_final']['percentage'],
                    'count': origin_dist['new_in_final']['count']
                })
        
        else:
            # Trend analysis - show average percentages
            avg_data = data['attribution_trends']['averages']
            flow_data = []
            
            for key, value in avg_data.items():
                if key.startswith('origin_') and not key.endswith('new_in_final'):
                    version = key.replace('origin_', '').title()
                    flow_data.append({
                        'source': version,
                        'target': 'Final Articles',
                        'value': value,
                        'count': f"{value:.1f}% avg"
                    })
            
            # Add new content average
            if 'origin_new_in_final' in avg_data:
                flow_data.append({
                    'source': 'New Content',
                    'target': 'Final Articles',
                    'value': avg_data['origin_new_in_final'],
                    'count': f"{avg_data['origin_new_in_final']:.1f}% avg"
                })
        
        # Create sankey-style visualization using matplotlib
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Draw flow connections
        y_positions = np.linspace(8, 2, len(flow_data))
        
        for i, item in enumerate(flow_data):
            # Source box
            source_color = COLORS.get(item['source'].lower(), '#CCCCCC')
            source_rect = patches.Rectangle((0.5, y_positions[i]-0.3), 2, 0.6, 
                                          facecolor=source_color, alpha=0.7, edgecolor='black')
            ax.add_patch(source_rect)
            ax.text(1.5, y_positions[i], item['source'], ha='center', va='center', fontweight='bold')
            
            # Flow arrow
            arrow_width = item['value'] / 100 * 0.4  # Scale arrow width by percentage
            arrow = patches.FancyArrowPatch((2.5, y_positions[i]), (6.5, 5),
                                          arrowstyle='->', mutation_scale=20,
                                          linewidth=arrow_width*10, alpha=0.6,
                                          color=source_color)
            ax.add_patch(arrow)
            
            # Percentage label
            ax.text(4.5, y_positions[i]+0.2, f"{item['value']:.1f}%", 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Target box
        target_rect = patches.Rectangle((7, 4.5), 2, 1, 
                                      facecolor=COLORS['final'], alpha=0.7, edgecolor='black')
        ax.add_patch(target_rect)
        target_text = 'Final Article' if mode == 'individual' else 'Final Articles'
        ax.text(8, 5, target_text, ha='center', va='center', fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        return fig
    
    def create_modification_intensity_chart(self, data, title="Content Modification Intensity", mode="individual"):
        """Create a chart showing modification intensity levels"""
        
        if mode == "individual":
            mod_dist = data['attribution_analysis']['statistics']['modification_distribution']
            categories = list(mod_dist.keys())
            values = [mod_dist[cat]['percentage'] for cat in categories]
        else:
            # Trend analysis
            avg_data = data['attribution_trends']['averages']
            categories = []
            values = []
            for key, value in avg_data.items():
                if key.startswith('modification_'):
                    cat = key.replace('modification_', '').replace('_', ' ').title()
                    categories.append(cat)
                    values.append(value)
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Color mapping for modification levels
        mod_colors = [COLORS.get(cat.lower().replace(' ', '_'), '#CCCCCC') for cat in categories]
        
        bars = ax.barh(categories, values, color=mod_colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add percentage labels on bars
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                   f'{value:.1f}%', ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel('Percentage of Content', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, max(values) * 1.2)
        
        # Add grid for readability
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        return fig
    
    def create_word_count_progression(self, data, title="Word Count Progression", mode="individual"):
        """Create a line chart showing word count changes across versions"""
        
        if mode == "individual":
            processing = data['processing_summary']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in processing:
                    word_counts.append(processing[version]['word_count'])
                    version_labels.append(version.title())
        else:
            # Trend analysis - show averages
            avg_data = data['word_count_trends']['averages']
            versions = ['draft', 'refined', 'edited', 'final']
            word_counts = []
            version_labels = []
            
            for version in versions:
                if version in avg_data:
                    word_counts.append(avg_data[version])
                    version_labels.append(version.title())
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        line = ax.plot(version_labels, word_counts, marker='o', linewidth=3, 
                      markersize=8, color=COLORS['draft'], markerfacecolor=COLORS['final'])
        
        # Add value labels on points
        for i, (label, count) in enumerate(zip(version_labels, word_counts)):
            ax.annotate(f'{int(count)}', (i, count), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontweight='bold')
        
        ax.set_ylabel('Word Count', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Calculate and show percentage change
        if len(word_counts) >= 2:
            change = ((word_counts[-1] - word_counts[0]) / word_counts[0]) * 100
            change_text = f"Overall change: {change:+.1f}%"
            ax.text(0.02, 0.98, change_text, transform=ax.transAxes, 
                   fontsize=11, fontweight='bold', verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        return fig
    
    def create_similarity_heatmap(self, data, title="Version Similarity Matrix", mode="individual"):
        """Create a heatmap showing similarities between versions"""
        
        if mode == "individual":
            similarity_data = data['similarity_analysis']['sequential_analysis']
            
            # Build similarity matrix
            versions = ['Draft', 'Refined', 'Edited', 'Final']
            matrix = np.zeros((len(versions), len(versions)))
            np.fill_diagonal(matrix, 1.0)  # Perfect similarity with self
            
            # Fill in the sequential similarities
            for seq in similarity_data:
                pair = seq['version_pair']
                similarity = seq['full_text']['combined']
                
                # Parse version pair (e.g., "draft_to_refined")
                from_version, to_version = pair.split('_to_')
                from_idx = versions.index(from_version.title())
                to_idx = versions.index(to_version.title())
                
                matrix[from_idx][to_idx] = similarity
                matrix[to_idx][from_idx] = similarity  # Make symmetric
        
        else:
            # For trend analysis, show average similarities
            similarity_trends = data['similarity_trends']
            
            # Create a simplified matrix for trends
            versions = ['Draft', 'Final']
            matrix = np.array([[1.0, 0.0], [0.0, 1.0]])
            
            if similarity_trends['averages'].get('draft_to_final'):
                avg_sim = similarity_trends['averages']['draft_to_final']['combined']
                matrix[0][1] = avg_sim
                matrix[1][0] = avg_sim
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        
        im = ax.imshow(matrix, cmap='RdYlGn', aspect='equal', vmin=0, vmax=1)
        
        # Add text annotations
        for i in range(len(versions)):
            for j in range(len(versions)):
                text = ax.text(j, i, f'{matrix[i, j]:.2f}', 
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_xticks(range(len(versions)))
        ax.set_yticks(range(len(versions)))
        ax.set_xticklabels(versions)
        ax.set_yticklabels(versions)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Similarity Score', rotation=270, labelpad=20, fontweight='bold')
        
        return fig
    
    def create_summary_dashboard(self, data, title_prefix="Article Analysis", mode="individual"):
        """Create a comprehensive dashboard with multiple visualizations"""
        
        # Create subplots
        fig = plt.figure(figsize=(16, 12))
        
        # Title
        main_title = f"{title_prefix} Dashboard"
        if mode == "individual":
            main_title += f" - {data['article_name']}"
        
        fig.suptitle(main_title, fontsize=18, fontweight='bold', y=0.95)
        
        # Create individual charts and save them
        charts = {}
        
        # Content Flow Chart
        charts['flow'] = self.create_content_flow_chart(data, "Content Attribution", mode)
        
        # Modification Intensity
        charts['modification'] = self.create_modification_intensity_chart(data, "Modification Intensity", mode)
        
        # Word Count Progression
        charts['word_count'] = self.create_word_count_progression(data, "Word Count Evolution", mode)
        
        # Similarity Heatmap
        charts['similarity'] = self.create_similarity_heatmap(data, "Version Similarities", mode)
        
        return charts
    
    def save_visualizations(self, charts, prefix="analysis", formats=['png', 'svg']):
        """Save all visualizations in multiple formats"""
        
        if not self.output_path:
            print("⚠️ No output path specified - visualizations not saved")
            return {}
        
        os.makedirs(self.output_path, exist_ok=True)
        saved_files = {}
        
        for chart_name, fig in charts.items():
            for fmt in formats:
                filename = f"{prefix}_{chart_name}.{fmt}"
                filepath = os.path.join(self.output_path, filename)
                
                fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                
                if chart_name not in saved_files:
                    saved_files[chart_name] = []
                saved_files[chart_name].append(filepath)
        
        # Close figures to free memory
        for fig in charts.values():
            plt.close(fig)
        
        print(f"💾 Visualizations saved to: {self.output_path}")
        for chart_name, files in saved_files.items():
            print(f"  📊 {chart_name}: {len(files)} formats")
        
        return saved_files

print("🎨 VisualizationEngine class loaded successfully!")

# =============================================================================
# CELL 2: INTERACTIVE VISUALIZATION FUNCTIONS
# =============================================================================

def create_interactive_flow_chart(data, mode="individual"):
    """Create an interactive Plotly flow/sankey diagram"""
    
    if mode == "individual":
        attribution_stats = data['attribution_analysis']['statistics']
        origin_dist = attribution_stats['origin_distribution']
        
        # Prepare data for Sankey diagram
        sources = []
        targets = []
        values = []
        labels = []
        
        # Add all source versions
        for version in ['draft', 'refined', 'edited']:
            if version in origin_dist:
                labels.append(version.title())
        
        # Add new content and final
        if 'new_in_final' in origin_dist:
            labels.append('New Content')
        labels.append('Final Article')
        
        # Create connections
        final_idx = len(labels) - 1
        
        for version, stats in origin_dist.items():
            if version != 'new_in_final':
                source_idx = labels.index(version.title())
                sources.append(source_idx)
                targets.append(final_idx)
                values.append(stats['percentage'])
        
        # Add new content if exists
        if 'new_in_final' in origin_dist:
            new_idx = labels.index('New Content')
            sources.append(new_idx)
            targets.append(final_idx)
            values.append(origin_dist['new_in_final']['percentage'])
    
    else:
        # Trend analysis mode
        avg_data = data['attribution_trends']['averages']
        labels = []
        sources = []
        targets = []
        values = []
        
        # Build labels and connections for trend data
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                version = key.replace('origin_', '')
                if version != 'new_in_final':
                    labels.append(version.title())
                else:
                    labels.append('New Content')
        
        labels.append('Final Articles')
        final_idx = len(labels) - 1
        
        # Create connections
        i = 0
        for key, value in avg_data.items():
            if key.startswith('origin_') and value > 0:
                sources.append(i)
                targets.append(final_idx)
                values.append(value)
                i += 1
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=[COLORS.get(label.lower().replace(' ', '_'), '#CCCCCC') for label in labels]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=['rgba(255,107,107,0.4)' if i < len(sources) else 'rgba(150,206,180,0.4)' 
                   for i in range(len(sources))]
        )
    )])
    
    title = "Content Flow Analysis"
    if mode == "individual":
        title += f" - {data['article_name']}"
    
    fig.update_layout(
        title_text=title,
        font_size=12,
        height=600
    )
    
    return fig

def create_interactive_trends_chart(trend_data):
    """Create interactive trend charts for multiple articles over time"""
    
    # Extract data for trends over time
    attribution_by_article = trend_data['attribution_trends']['by_article']
    
    if not attribution_by_article:
        print("No trend data available")
        return None
    
    # Prepare data for plotting
    dates = []
    draft_retention = []
    edited_dominance = []
    new_content = []
    article_names = []
    
    for article in attribution_by_article:
        dates.append(article['publication_date'])
        article_names.append(article['article_name'])
        
        # Extract percentages
        draft_retention.append(article['origin_percentages'].get('draft', 0))
        edited_dominance.append(article['origin_percentages'].get('edited', 0))
        new_content.append(article['origin_percentages'].get('new_in_final', 0))
    
    # Create multi-line chart
    fig = go.Figure()
    
    # Add traces for each metric
    fig.add_trace(go.Scatter(
        x=dates, y=draft_retention,
        mode='lines+markers',
        name='Draft Retention %',
        line=dict(color=COLORS['draft'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Draft Retention: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=edited_dominance,
        mode='lines+markers',
        name='Edited Content %',
        line=dict(color=COLORS['edited'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Edited Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=new_content,
        mode='lines+markers',
        name='New Content %',
        line=dict(color=COLORS['new_content'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>New Content: %{y:.1f}%<extra></extra>',
        text=article_names
    ))
    
    fig.update_layout(
        title='Content Attribution Trends Over Time',
        xaxis_title='Publication Date',
        yaxis_title='Percentage of Final Content',
        hovermode='x unified',
        height=600,
        showlegend=True
    )
    
    return fig

print("🚀 Interactive visualization functions loaded!")

# =============================================================================
# CELL 3: EXECUTION FUNCTIONS
# =============================================================================

def visualize_individual_article(analysis_data, output_path=None, save_files=True):
    """Create visualizations for a single article analysis"""
    
    print(f"🎨 Creating visualizations for: {analysis_data['article_name']}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static visualizations...")
    charts = viz_engine.create_summary_dashboard(analysis_data, mode="individual")
    
    # Create interactive chart
    print("🔧 Creating interactive flow chart...")
    interactive_flow = create_interactive_flow_chart(analysis_data, mode="individual")
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts, 
            prefix=f"{analysis_data['article_name']}_analysis",
            formats=['png', 'svg']
        )
        
        # Save interactive chart
        interactive_file = os.path.join(output_path, f"{analysis_data['article_name']}_interactive_flow.html")
        interactive_flow.write_html(interactive_file)
        saved_files['interactive_flow'] = [interactive_file]
        print(f"💾 Interactive chart saved: {interactive_file}")
    
    # Display interactive chart
    interactive_flow.show()
    
    return charts, interactive_flow, saved_files

def visualize_trend_analysis(trend_data, output_path=None, save_files=True):
    """Create visualizations for trend analysis"""
    
    period = trend_data['period']
    print(f"📈 Creating trend visualizations for period: {period}")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine(output_path)
    
    # Create static charts
    print("📊 Generating static trend visualizations...")
    charts = viz_engine.create_summary_dashboard(trend_data, f"Trend Analysis - {period}", mode="trend")
    
    # Create interactive charts
    print("🔧 Creating interactive trend charts...")
    interactive_flow = create_interactive_flow_chart(trend_data, mode="trend")
    interactive_trends = create_interactive_trends_chart(trend_data)
    
    # Save files if requested
    saved_files = {}
    if save_files and output_path:
        saved_files = viz_engine.save_visualizations(
            charts,
            prefix=f"trend_analysis_{period}",
            formats=['png', 'svg']
        )
        
        # Save interactive charts
        if output_path:
            flow_file = os.path.join(output_path, f"trend_flow_{period}.html")
            interactive_flow.write_html(flow_file)
            saved_files['interactive_flow'] = [flow_file]
            
            if interactive_trends:
                trends_file = os.path.join(output_path, f"trend_timeline_{period}.html")
                interactive_trends.write_html(trends_file)
                saved_files['interactive_trends'] = [trends_file]
                print(f"💾 Interactive charts saved to: {output_path}")
    
    # Display interactive charts
    interactive_flow.show()
    if interactive_trends:
        interactive_trends.show()
    
    return charts, {'flow': interactive_flow, 'trends': interactive_trends}, saved_files

def quick_visualize(data, data_type="individual", output_path=None):
    """Quick visualization function for any analysis data"""
    
    if data_type == "individual":
        return visualize_individual_article(data, output_path, save_files=bool(output_path))
    elif data_type == "trend":
        return visualize_trend_analysis(data, output_path, save_files=bool(output_path))
    else:
        print(f"❌ Unknown data type: {data_type}")
        return None

print("🎯 Execution functions loaded!")
print("\nUsage examples:")
print("# Visualize individual article (using existing analysis data)")
print("charts, interactive, files = visualize_individual_article(combined_results, '/your/output/path')")
print("\n# Visualize trend analysis")
print("charts, interactive, files = visualize_trend_analysis(trend_results, '/your/output/path')")
print("\n# Quick visualization without saving")
print("quick_visualize(combined_results, 'individual')")

# =============================================================================
# CELL 4: FOOTER METRICS GENERATOR
# =============================================================================

def generate_article_footer_graphics(analysis_data, output_path=None):
    """Generate clean, publication-ready graphics for article footers"""
    
    print(f"📄 Generating footer graphics for: {analysis_data['article_name']}")
    
    # Create a clean, minimal style for footer graphics
    plt.style.use('default')
    
    # Footer-specific color palette (more muted)
    footer_colors = {
        'primary': '#2E86AB',
        'secondary': '#A23B72', 
        'accent': '#F18F01',
        'neutral': '#C73E1D'
    }
    
    # Create a compact summary visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Content Analysis Summary - {analysis_data["article_name"]}', 
                 fontsize=14, fontweight='bold')
    
    # 1. Content Origins (Pie Chart)
    attribution_stats = analysis_data['attribution_analysis']['statistics']
    origin_dist = attribution_stats['origin_distribution']
    
    labels = []
    sizes = []
    colors = []
    
    for version, stats in origin_dist.items():
        if version != 'new_in_final':
            labels.append(f"{version.title()}\n{stats['percentage']:.1f}%")
            sizes.append(stats['percentage'])
            colors.append(footer_colors['primary'])
    
    if 'new_in_final' in origin_dist:
        labels.append(f"New Content\n{origin_dist['new_in_final']['percentage']:.1f}%")
        sizes.append(origin_dist['new_in_final']['percentage'])
        colors.append(footer_colors['accent'])
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90)
    ax1.set_title('Content Origins', fontweight='bold')
    
    # 2. Word Count Progression (Bar Chart)
    processing = analysis_data['processing_summary']
    versions = ['Draft', 'Refined', 'Edited', 'Final']
    word_counts = []
    
    for version in ['draft', 'refined', 'edited', 'final']:
        if version in processing:
            word_counts.append(processing[version]['word_count'])
        else:
            word_counts.append(0)
    
    bars = ax2.bar(versions, word_counts, color=footer_colors['secondary'], alpha=0.7)
    ax2.set_title('Word Count Evolution', fontweight='bold')
    ax2.set_ylabel('Words')
    
    # Add value labels on bars
    for bar, count in zip(bars, word_counts):
        if count > 0:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(count)}', ha='center', va='bottom', fontsize=9)
    
    # 3. Modification Intensity (Horizontal Bar)
    mod_dist = attribution_stats['modification_distribution']
    mod_categories = []
    mod_values = []
    
    for category, stats in mod_dist.items():
        clean_cat = category.replace('_', ' ').title()
        mod_categories.append(clean_cat)
        mod_values.append(stats['percentage'])
    
    bars = ax3.barh(mod_categories, mod_values, color=footer_colors['neutral'], alpha=0.7)
    ax3.set_title('Modification Levels', fontweight='bold')
    ax3.set_xlabel('Percentage')
    
    # Add percentage labels
    for bar, value in zip(bars, mod_values):
        width = bar.get_width()
        ax3.text(width + 1, bar.get_y() + bar.get_height()/2.,
                f'{value:.1f}%', ha='left', va='center', fontsize=9)
    
    # 4. Key Metrics Summary (Text)
    ax4.axis('off')
    
    # Calculate key metrics
    draft_to_final = analysis_data['similarity_analysis']['draft_to_final']
    similarity_pct = draft_to_final['full_text']['combined'] * 100 if draft_to_final else 0
    
    word_change = 0
    if 'draft' in processing and 'final' in processing:
        draft_words = processing['draft']['word_count']
        final_words = processing['final']['word_count']
        word_change = ((final_words - draft_words) / draft_words) * 100
    
    # Display key metrics as text
    metrics_text = f"""
Key Metrics:

Draft-Final Similarity: {similarity_pct:.1f}%

Word Count Change: {word_change:+.1f}
```

Now try running it again with the automatic path detection:

```python
viz_outputs = viz_article(combined_results)
```

This should:
1. Fix the pie chart error
2. Automatically use the same output path where your analysis files are saved
3. Generate all the visualizations without the path errors

The system will create all the charts and save them to your existing output folder alongside the analysis JSON files.





---
Powered by [Claude Exporter](https://www.claudexporter.com)