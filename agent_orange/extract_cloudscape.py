#!/usr/bin/env python3
"""
Direct Cloudscape extraction script - gets the actual HTML/CSS files you need
No AI agents, no TypeScript nonsense, just the raw materials.
"""

import requests
import os
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup

class CloudscapeExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = "https://cloudscape.design"
        self.output_dir = Path("refined_materials/cloudscape_complete")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_demo_page(self, demo_url, name):
        """Extract a demo page with all its CSS and assets"""
        print(f"📄 Extracting: {name}")
        
        try:
            response = self.session.get(demo_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Download CSS files
            css_links = soup.find_all('link', rel='stylesheet')
            css_dir = self.output_dir / "css"
            css_dir.mkdir(exist_ok=True)
            
            for link in css_links:
                if link.get('href'):
                    css_url = urljoin(demo_url, link['href'])
                    css_filename = Path(urlparse(css_url).path).name
                    if css_filename:
                        self.download_file(css_url, css_dir / css_filename)
                        # Update the link to point to local file
                        link['href'] = f"css/{css_filename}"
            
            # Download JS files (might contain styling info)
            js_links = soup.find_all('script', src=True)
            js_dir = self.output_dir / "js"
            js_dir.mkdir(exist_ok=True)
            
            for script in js_links:
                if script.get('src'):
                    js_url = urljoin(demo_url, script['src'])
                    js_filename = Path(urlparse(js_url).path).name
                    if js_filename and not js_filename.startswith('http'):
                        self.download_file(js_url, js_dir / js_filename)
                        script['src'] = f"js/{js_filename}"
            
            # Save the complete HTML file
            html_file = self.output_dir / f"{name}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
            print(f"✅ Saved: {html_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed {name}: {e}")
            return False
    
    def download_file(self, url, local_path):
        """Download a file if it doesn't exist"""
        if local_path.exists():
            return
            
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
                
        except Exception as e:
            print(f"⚠️  Failed to download {url}: {e}")
    
    def extract_component_docs(self):
        """Extract component documentation pages"""
        print("🔍 Finding component pages...")
        
        # Get the main components page
        components_url = f"{self.base_url}/components"
        try:
            response = self.session.get(components_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all component links
            component_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/components/' in href and href != '/components':
                    full_url = urljoin(self.base_url, href)
                    component_name = href.split('/')[-1]
                    component_links.append((full_url, component_name))
            
            print(f"📋 Found {len(component_links)} component pages")
            
            for url, name in component_links[:20]:  # Limit to first 20 for now
                self.extract_demo_page(url, f"component_{name}")
                time.sleep(0.5)  # Be nice to their servers
                
        except Exception as e:
            print(f"❌ Failed to get component list: {e}")
    
    def extract_css_from_github(self):
        """Extract CSS files directly from GitHub"""
        print("📦 Extracting CSS from GitHub repositories...")
        
        repos = [
            'cloudscape-design/components',
            'cloudscape-design/global-styles'
        ]
        
        for repo in repos:
            print(f"🔍 Processing {repo}...")
            self.download_github_css(repo)
    
    def download_github_css(self, repo_path):
        """Download CSS/SCSS files from a GitHub repo"""
        api_url = f"https://api.github.com/repos/{repo_path}/contents"
        
        try:
            # Get repository contents
            response = self.session.get(api_url)
            response.raise_for_status()
            contents = response.json()
            
            repo_dir = self.output_dir / "github_css" / repo_path.replace('/', '_')
            repo_dir.mkdir(parents=True, exist_ok=True)
            
            self._download_directory_contents(contents, repo_dir, repo_path)
            
        except Exception as e:
            print(f"❌ Failed to download from {repo_path}: {e}")
    
    def _download_directory_contents(self, contents, local_dir, repo_path, max_depth=3):
        """Recursively download directory contents"""
        if max_depth <= 0:
            return
            
        for item in contents:
            if item['type'] == 'file':
                # Only download CSS, SCSS, and related files
                if any(item['name'].endswith(ext) for ext in ['.css', '.scss', '.sass', '.less']):
                    file_path = local_dir / item['name']
                    self.download_file(item['download_url'], file_path)
                    
            elif item['type'] == 'dir':
                # Recursively process directories
                subdir = local_dir / item['name']
                subdir.mkdir(exist_ok=True)
                
                try:
                    sub_response = self.session.get(item['url'])
                    sub_response.raise_for_status()
                    sub_contents = sub_response.json()
                    self._download_directory_contents(sub_contents, subdir, repo_path, max_depth - 1)
                except Exception as e:
                    print(f"⚠️  Failed to process directory {item['name']}: {e}")

def main():
    print("🔶 Starting Cloudscape Direct Extraction")
    print("📁 Output directory: refined_materials/cloudscape_complete/")
    print()
    
    extractor = CloudscapeExtractor()
    
    # Extract component documentation with CSS
    extractor.extract_component_docs()
    
    # Extract CSS from GitHub repos
    extractor.extract_css_from_github()
    
    print()
    print("✅ Extraction complete!")
    print("📁 Check refined_materials/cloudscape_complete/ for:")
    print("   • Component HTML files with embedded CSS references")
    print("   • css/ directory with stylesheets")
    print("   • js/ directory with JavaScript files")
    print("   • github_css/ directory with source CSS/SCSS files")
    print()
    print("🎯 You now have clean HTML files with their CSS intact!")

if __name__ == "__main__":
    main()