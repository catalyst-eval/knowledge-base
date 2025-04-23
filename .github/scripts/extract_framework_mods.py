#!/usr/bin/env python3
"""
Framework Modification Extractor for Clinical Transcript Analyses

This script:
1. Extracts "Recommendations for Framework Additions or Modifications" sections from transcript analyses
2. Creates separate framework-mods files with these recommendations
3. Generates a timestamp for when the extraction occurred
4. Optionally removes these sections from the original files

Usage:
  python extract_framework_mods.py [--remove]

Options:
  --remove    Remove the recommendations sections from the original files after extraction
"""

import os
import re
import yaml
import glob
import argparse
from datetime import datetime

def extract_yaml_front_matter(file_path):
    """Extract YAML front matter from a markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if file has YAML front matter (between --- markers)
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            # Parse YAML content
            front_matter = yaml.safe_load(match.group(1))
            return front_matter, content
        except Exception as e:
            print(f"Error parsing YAML in {file_path}: {e}")
    
    return None, content

def extract_recommendations_section(content):
    """Extract the 'Recommendations for Framework Additions or Modifications' section from content."""
    section_pattern = r'## Recommendations for Framework Additions or Modifications\s*\n(.*?)(?:\n##|\Z)'
    match = re.search(section_pattern, content, re.DOTALL)
    
    if match:
        # Capture the entire section including all subsections
        recommendations = match.group(1).strip()
        return recommendations
    
    return None

def remove_recommendations_section(content):
    """Remove the 'Recommendations for Framework Additions or Modifications' section from content."""
    section_pattern = r'## Recommendations for Framework Additions or Modifications\s*\n(.*?)(?=\n##|\Z)'
    return re.sub(section_pattern, '', content, flags=re.DOTALL)

def create_framework_mod_file(original_file, title, recommendations, timestamp):
    """Create a new framework modification file with the extracted recommendations."""
    # Generate file name based on the original file and timestamp
    base_name = os.path.basename(original_file).replace('.md', '')
    mod_file_name = f"framework-mods/{timestamp}_{base_name}_framework-mods.md"
    
    content = f"""---
title: "Framework Modifications from {title}"
source_file: "{original_file}"
date: {timestamp}
---

# Framework Modification Recommendations

*Extracted from: {title}*

{recommendations}
"""
    
    with open(mod_file_name, 'w') as f:
        f.write(content)
    
    return mod_file_name

def main():
    parser = argparse.ArgumentParser(description='Extract framework modification recommendations from transcript analyses.')
    parser.add_argument('--remove', action='store_true', help='Remove recommendations from original files after extraction')
    args = parser.parse_args()
    
    # Generate timestamp for the extraction
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    # Get all transcript analysis files
    md_files = glob.glob('transcript-analyses/*.md')
    
    # Skip files that don't need processing
    md_files = [f for f in md_files if not os.path.basename(f).startswith('index')]
    
    # Track results
    processed_files = []
    extracted_files = []
    
    for file_path in md_files:
        try:
            # Extract front matter and content
            front_matter, content = extract_yaml_front_matter(file_path)
            
            if not front_matter:
                print(f"Warning: No front matter found in {file_path}, skipping")
                continue
            
            # Get title from front matter
            title = front_matter.get('title', os.path.basename(file_path))
            
            # Extract recommendations section
            recommendations = extract_recommendations_section(content)
            
            if recommendations:
                # Create new framework mod file
                mod_file = create_framework_mod_file(file_path, title, recommendations, timestamp)
                extracted_files.append((file_path, mod_file))
                
                # Remove section from original file if requested
                if args.remove:
                    new_content = remove_recommendations_section(content)
                    with open(file_path, 'w') as f:
                        f.write(new_content)
                
                processed_files.append(file_path)
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Print summary
    print(f"Processed {len(processed_files)} files")
    print(f"Extracted recommendations from {len(extracted_files)} files")
    
    if args.remove:
        print(f"Removed recommendations sections from original files")
    
    for original, mod_file in extracted_files:
        print(f"  {original} → {mod_file}")

if __name__ == "__main__":
    main()