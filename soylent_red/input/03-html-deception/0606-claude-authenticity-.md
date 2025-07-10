# Authenticity 

**Created:** 6/6/2025 6:47  
**Updated:** 6/6/2025 7:43  
**Exported:** 6/14/2025 13:46  

## Prompt:
I use AI to write articles in 5 stages:
1. Research, even if I’m familiar with the topic
2. I give the research materials along with my notes and prompt it to draft the article. 
3. I then refine the article by prompting the AI, these tend to be sweeping changes
4. I then put the article in a word processor with AI integrations and edit with the occasional assistance from AI
5 The final edit is all me so I know I’ve seen every word. 

I want to be transparent about how I’m using AI by measuring and reporting the correct information and metrics at each stage of my writing process, so that’s 4 checkpoints. What can you provide in the way of code that a non-developer can use to achieve this?



## Response:
I'll help you create a tracking system for your AI-assisted writing process. Since you're a non-developer, I'll provide a simple, user-friendly solution using HTML and JavaScript that runs entirely in your browser.

AI Writing Process Tracker

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Writing Process Tracker</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        
        .stage {
            background: #ecf0f1;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        
        .stage h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        
        .input-group {
            margin: 10px 0;
        }
        
        label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
            color: #555;
        }
        
        input, textarea {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 14px;
        }
        
        textarea {
            min-height: 80px;
            resize: vertical;
        }
        
        button {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
        }
        
        button:hover {
            background: #2980b9;
        }
        
        .save-button {
            background: #27ae60;
        }
        
        .save-button:hover {
            background: #229954;
        }
        
        .clear-button {
            background: #e74c3c;
        }
        
        .clear-button:hover {
            background: #c0392b;
        }
        
        .report {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: monospace;
            border: 1px solid #dee2e6;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .metric-card {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 5px;
        }
        
        #savedProjects {
            margin-top: 20px;
        }
        
        .project-item {
            background: #f8f9fa;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .project-item:hover {
            background: #e9ecef;
        }
        
        .delete-project {
            background: #dc3545;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Writing Process Tracker</h1>
        
        <div class="input-group">
            <label for="projectName">Project Name:</label>
            <input type="text" id="projectName" placeholder="Enter article title or project name">
        </div>
        
        <div class="stage">
            <h3>Stage 1: Research</h3>
            <div class="input-group">
                <label for="researchPrompts">Number of AI prompts used:</label>
                <input type="number" id="researchPrompts" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="researchTime">Time spent (minutes):</label>
                <input type="number" id="researchTime" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="researchNotes">Notes:</label>
                <textarea id="researchNotes" placeholder="Key sources, AI tools used, etc."></textarea>
            </div>
        </div>
        
        <div class="stage">
            <h3>Stage 2: Initial Draft</h3>
            <div class="input-group">
                <label for="draftPrompts">Number of AI prompts used:</label>
                <input type="number" id="draftPrompts" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="draftWords">Word count generated:</label>
                <input type="number" id="draftWords" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="draftTime">Time spent (minutes):</label>
                <input type="number" id="draftTime" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="draftNotes">Notes:</label>
                <textarea id="draftNotes" placeholder="AI model used, approach, etc."></textarea>
            </div>
        </div>
        
        <div class="stage">
            <h3>Stage 3: AI-Assisted Refinement</h3>
            <div class="input-group">
                <label for="refinePrompts">Number of AI prompts used:</label>
                <input type="number" id="refinePrompts" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="refineChanges">Estimated % of content changed:</label>
                <input type="number" id="refineChanges" min="0" max="100" value="0">
            </div>
            <div class="input-group">
                <label for="refineTime">Time spent (minutes):</label>
                <input type="number" id="refineTime" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="refineNotes">Notes:</label>
                <textarea id="refineNotes" placeholder="Types of changes made, focus areas, etc."></textarea>
            </div>
        </div>
        
        <div class="stage">
            <h3>Stage 4: Word Processor Editing</h3>
            <div class="input-group">
                <label for="editPrompts">Number of AI assists:</label>
                <input type="number" id="editPrompts" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="editTime">Time spent (minutes):</label>
                <input type="number" id="editTime" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="editNotes">Notes:</label>
                <textarea id="editNotes" placeholder="AI tools used, types of assistance, etc."></textarea>
            </div>
        </div>
        
        <div class="stage">
            <h3>Stage 5: Final Human Edit</h3>
            <div class="input-group">
                <label for="finalWords">Final word count:</label>
                <input type="number" id="finalWords" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="finalTime">Time spent (minutes):</label>
                <input type="number" id="finalTime" min="0" value="0">
            </div>
            <div class="input-group">
                <label for="finalNotes">Notes:</label>
                <textarea id="finalNotes" placeholder="Final observations, quality assessment, etc."></textarea>
            </div>
        </div>
        
        <div style="margin-top: 30px;">
            <button onclick="generateReport()">Generate Report</button>
            <button class="save-button" onclick="saveProject()">Save Project</button>
            <button class="clear-button" onclick="clearForm()">Clear Form</button>
        </div>
        
        <div id="savedProjects"></div>
        
        <div id="reportSection"></div>
    </div>
    
    <script>
        // Load saved projects on page load
        window.onload = function() {
            displaySavedProjects();
        };
        
        function calculateMetrics() {
            const totalPrompts = 
                parseInt(document.getElementById('researchPrompts').value) +
                parseInt(document.getElementById('draftPrompts').value) +
                parseInt(document.getElementById('refinePrompts').value) +
                parseInt(document.getElementById('editPrompts').value);
            
            const totalTime = 
                parseInt(document.getElementById('researchTime').value) +
                parseInt(document.getElementById('draftTime').value) +
                parseInt(document.getElementById('refineTime').value) +
                parseInt(document.getElementById('editTime').value) +
                parseInt(document.getElementById('finalTime').value);
            
            const aiTime = totalTime - parseInt(document.getElementById('finalTime').value);
            const aiPercentage = totalTime > 0 ? ((aiTime / totalTime) * 100).toFixed(1) : 0;
            
            return {
                totalPrompts,
                totalTime,
                aiTime,
                aiPercentage,
                finalWords: parseInt(document.getElementById('finalWords').value),
                draftWords: parseInt(document.getElementById('draftWords').value)
            };
        }
        
        function generateReport() {
            const projectName = document.getElementById('projectName').value || 'Untitled Project';
            const metrics = calculateMetrics();
            const timestamp = new Date().toLocaleString();
            
            const report = `AI WRITING PROCESS REPORT
========================
Project: ${projectName}
Generated: ${timestamp}

OVERVIEW METRICS
---------------
Total AI Prompts: ${metrics.totalPrompts}
Total Time: ${metrics.totalTime} minutes (${(metrics.totalTime / 60).toFixed(1)} hours)
AI-Assisted Time: ${metrics.aiTime} minutes (${metrics.aiPercentage}% of total)
Human-Only Time: ${document.getElementById('finalTime').value} minutes
Final Word Count: ${metrics.finalWords}

STAGE-BY-STAGE BREAKDOWN
-----------------------

STAGE 1 - Research
• AI Prompts: ${document.getElementById('researchPrompts').value}
• Time: ${document.getElementById('researchTime').value} minutes
• Notes: ${document.getElementById('researchNotes').value || 'None'}

STAGE 2 - Initial Draft
• AI Prompts: ${document.getElementById('draftPrompts').value}
• Words Generated: ${document.getElementById('draftWords').value}
• Time: ${document.getElementById('draftTime').value} minutes
• Notes: ${document.getElementById('draftNotes').value || 'None'}

STAGE 3 - AI-Assisted Refinement
• AI Prompts: ${document.getElementById('refinePrompts').value}
• Content Changed: ${document.getElementById('refineChanges').value}%
• Time: ${document.getElementById('refineTime').value} minutes
• Notes: ${document.getElementById('refineNotes').value || 'None'}

STAGE 4 - Word Processor Editing
• AI Assists: ${document.getElementById('editPrompts').value}
• Time: ${document.getElementById('editTime').value} minutes
• Notes: ${document.getElementById('editNotes').value || 'None'}

STAGE 5 - Final Human Edit
• Final Word Count: ${document.getElementById('finalWords').value}
• Time: ${document.getElementById('finalTime').value} minutes
• Notes: ${document.getElementById('finalNotes').value || 'None'}

TRANSPARENCY STATEMENT
--------------------
This article was created using AI assistance across ${metrics.totalPrompts} prompts, 
representing ${metrics.aiPercentage}% of the total ${metrics.totalTime}-minute writing process. 
The final edit was completed entirely by human review.`;
            
            // Display report with metrics visualization
            document.getElementById('reportSection').innerHTML = `
                <h2>Generated Report</h2>
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-value">${metrics.totalPrompts}</div>
                        <div class="metric-label">Total AI Prompts</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${metrics.aiPercentage}%</div>
                        <div class="metric-label">AI-Assisted Time</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${(metrics.totalTime / 60).toFixed(1)}h</div>
                        <div class="metric-label">Total Time</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${metrics.finalWords}</div>
                        <div class="metric-label">Final Words</div>
                    </div>
                </div>
                <div class="report">${report}</div>
                <button onclick="copyReport()">Copy Report to Clipboard</button>
                <button onclick="downloadReport('${projectName}')">Download Report</button>
            `;
        }
        
        function copyReport() {
            const reportText = document.querySelector('.report').textContent;
            navigator.clipboard.writeText(reportText).then(() => {
                alert('Report copied to clipboard!');
            });
        }
        
        function downloadReport(projectName) {
            const reportText = document.querySelector('.report').textContent;
            const blob = new Blob([reportText], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${projectName.replace(/[^a-z0-9]/gi, '_')}_AI_Report.txt`;
            a.click();
            window.URL.revokeObjectURL(url);
        }
        
        function saveProject() {
            const projectName = document.getElementById('projectName').value || 'Untitled Project';
            const projectData = {
                name: projectName,
                timestamp: new Date().toISOString(),
                data: {
                    researchPrompts: document.getElementById('researchPrompts').value,
                    researchTime: document.getElementById('researchTime').value,
                    researchNotes: document.getElementById('researchNotes').value,
                    draftPrompts: document.getElementById('draftPrompts').value,
                    draftWords: document.getElementById('draftWords').value,
                    draftTime: document.getElementById('draftTime').value,
                    draftNotes: document.getElementById('draftNotes').value,
                    refinePrompts: document.getElementById('refinePrompts').value,
                    refineChanges: document.getElementById('refineChanges').value,
                    refineTime: document.getElementById('refineTime').value,
                    refineNotes: document.getElementById('refineNotes').value,
                    editPrompts: document.getElementById('editPrompts').value,
                    editTime: document.getElementById('editTime').value,
                    editNotes: document.getElementById('editNotes').value,
                    finalWords: document.getElementById('finalWords').value,
                    finalTime: document.getElementById('finalTime').value,
                    finalNotes: document.getElementById('finalNotes').value
                }
            };
            
            // Get existing projects
            let projects = JSON.parse(localStorage.getItem('aiWritingProjects') || '[]');
            projects.push(projectData);
            localStorage.setItem('aiWritingProjects', JSON.stringify(projects));
            
            alert('Project saved successfully!');
            displaySavedProjects();
        }
        
        function displaySavedProjects() {
            const projects = JSON.parse(localStorage.getItem('aiWritingProjects') || '[]');
            const container = document.getElementById('savedProjects');
            
            if (projects.length === 0) {
                container.innerHTML = '';
                return;
            }
            
            container.innerHTML = '<h2>Saved Projects</h2>';
            projects.forEach((project, index) => {
                const projectDiv = document.createElement('div');
                projectDiv.className = 'project-item';
                projectDiv.innerHTML = `
                    <span onclick="loadProject(${index})">${project.name} - ${new Date(project.timestamp).toLocaleDateString()}</span>
                    <button class="delete-project" onclick="deleteProject(${index})">Delete</button>
                `;
                container.appendChild(projectDiv);
            });
        }
        
        function loadProject(index) {
            const projects = JSON.parse(localStorage.getItem('aiWritingProjects') || '[]');
            const project = projects[index];
            
            document.getElementById('projectName').value = project.name;
            
            // Load all the data
            Object.keys(project.data).forEach(key => {
                document.getElementById(key).value = project.data[key];
            });
            
            alert('Project loaded!');
        }
        
        function deleteProject(index) {
            if (!confirm('Are you sure you want to delete this project?')) return;
            
            let projects = JSON.parse(localStorage.getItem('aiWritingProjects') || '[]');
            projects.splice(index, 1);
            localStorage.setItem('aiWritingProjects', JSON.stringify(projects));
            displaySavedProjects();
        }
        
        function clearForm() {
            if (!confirm('Are you sure you want to clear all fields?')) return;
            
            document.querySelectorAll('input, textarea').forEach(element => {
                if (element.type === 'number') {
                    element.value = '0';
                } else {
                    element.value = '';
                }
            });
            document.getElementById('reportSection').innerHTML = '';
        }
    </script>
</body>
</html>
```

I've created a comprehensive AI Writing Process Tracker that you can use without any coding knowledge. Here's what it provides:

## Key Features:

1. **Stage-by-Stage Tracking**: Records metrics for all 5 stages of your writing process
   - Research: AI prompts used and time spent
   - Initial Draft: AI prompts, word count generated, and time
   - Refinement: AI prompts, percentage of content changed, and time
   - Word Processor Editing: Number of AI assists and time
   - Final Human Edit: Final word count and time

2. **Automatic Calculations**:
   - Total AI prompts across all stages
   - Total time and AI-assisted time percentage
   - Hours spent on the project
   - Visual metrics dashboard

3. **Report Generation**:
   - Creates a detailed, formatted report you can copy or download
   - Includes a transparency statement summarizing AI usage
   - Professional format suitable for disclosure

4. **Project Management**:
   - Save multiple projects
   - Load previous projects to review or update
   - All data stored locally in your browser

## How to Use:

1. **Save the file**: Copy the code to a text editor and save it as `ai-tracker.html`
2. **Open in browser**: Double-click the file to open it in your web browser
3. **Track your process**: Fill in the metrics as you complete each stage
4. **Generate reports**: Click "Generate Report" to create your transparency disclosure

The report includes a ready-to-use transparency statement like:
> "This article was created using AI assistance across 25 prompts, representing 75% of the total 4-hour writing process. The final edit was completed entirely by human review."

This tool stores everything locally on your computer, so your data remains private. You can bookmark the file for easy access and use it for all your writing projects.



## Prompt:
I could manage that with paper, no wonder you went with a web page. I want to give the 4 articles to something (I assumed python) that would measure things like counts, changes, shifts in semantics. Actual transparency



## Response:
You're absolutely right - you want actual computational analysis of the text changes between stages, not just manual tracking. Let me create a Python script that analyzes the evolution of your articles through the AI-assisted writing process.

AI Writing Process Analyzer

```python
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
```

Now THIS is real transparency! I've created a Python script that analyzes the actual text transformations between your writing stages. Here's what it measures:

## Key Metrics Analyzed:

1. **Content Similarity** - How much text is retained vs. changed between stages
2. **Word Count Changes** - Precise tracking of expansion/reduction
3. **Vocabulary Analysis** - New words added, words removed, vocabulary diversity
4. **Structural Changes** - Paragraph count, sentence length variations
5. **Semantic Shifts** - Which themes emerge or diminish through the process
6. **Change Operations** - Specific insertions, deletions, and replacements

## How to Use:

1. **Save the script** as `ai_writing_analyzer.py`
2. **Run it** from command line: `python ai_writing_analyzer.py`
3. **Input your texts** either by:
   - Providing file paths to your 4 versions
   - Pasting the text directly into the terminal

## What You Get:

The script produces:
- **Stage-by-stage analysis** showing what changed between each version
- **Overall transformation metrics** from initial draft to final
- **Estimated AI contribution percentage** based on similarity analysis
- **Auto-generated transparency statement** with real metrics
- **JSON file** with all detailed data for record-keeping

## Example Output:
```
Content retention: 67.3%
Word count change: +18.5%
Vocabulary expansion: 1,247 → 1,432 unique words
Estimated AI contribution: ~32.7% of content transformed
```

This gives you actual, measurable transparency - not just "I used AI" but "here's exactly how much the AI-generated content was transformed through human editing."

The semantic analysis even shows which themes were emphasized or de-emphasized through your editing process, giving readers insight into how human judgment shaped the AI output.

Would you like me to add any specific metrics, like readability scores (Flesch-Kincaid), sentiment analysis, or style consistency measures?





---
Powered by [Claude Exporter](https://www.claudexporter.com)