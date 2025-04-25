#!/usr/bin/env python3
"""
Weekly Explainer Update Script

This script identifies transcript analyses from the past week and suggests which
explainer articles should be created or updated based on the concepts they contain.

Usage:
    python weekly-explainer-update.py [--days=7] [--output=report.md]

Arguments:
    --days      Number of days back to look for new/updated transcripts (default: 7)
    --output    Output file for the update report (default: explainer-update-report.md)
"""

import os
import sys
import re
import glob
import yaml
import datetime
import argparse
from collections import defaultdict
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).resolve().parents[2]  # Concept_Dev directory
TRANSCRIPT_DIR = REPO_ROOT / "transcript-analyses"
EXPLAINER_DIR = REPO_ROOT / "explainers"
LOG_FILE = REPO_ROOT / "explainer-updates-log.md"

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate weekly explainer update report")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back")
    parser.add_argument("--output", default="explainer-update-report.md", help="Output report file")
    return parser.parse_args()

def get_recent_transcripts(days_back):
    """Find transcript analyses from the past N days."""
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_back)
    recent_files = []
    
    transcript_files = glob.glob(str(TRANSCRIPT_DIR / "*.md"))
    for file_path in transcript_files:
        file_stat = os.stat(file_path)
        file_date = datetime.datetime.fromtimestamp(file_stat.st_mtime)
        
        if file_date >= cutoff_date:
            recent_files.append(file_path)
    
    return recent_files

def extract_frontmatter(file_path):
    """Extract the YAML frontmatter from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if frontmatter_match:
        frontmatter_yaml = frontmatter_match.group(1)
        try:
            return yaml.safe_load(frontmatter_yaml)
        except yaml.YAMLError:
            print(f"Error parsing frontmatter in {file_path}")
            return {}
    
    return {}

def get_concepts_from_transcript(file_path):
    """Extract concepts and tags from a transcript analysis."""
    frontmatter = extract_frontmatter(file_path)
    
    concepts = []
    
    # Get concepts from frontmatter
    if 'concepts' in frontmatter and isinstance(frontmatter['concepts'], list):
        concepts.extend([c for c in frontmatter['concepts'] if c is not None])
    
    # Get neurotype tags
    if 'neurotype' in frontmatter and isinstance(frontmatter['neurotype'], list):
        concepts.extend([n for n in frontmatter['neurotype'] if n is not None])
    
    # Get strategies
    if 'strategies' in frontmatter and isinstance(frontmatter['strategies'], list):
        concepts.extend([s for s in frontmatter['strategies'] if s is not None])
    
    # Extract inline hashtags from content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    hashtags = re.findall(r'#([\w-]+)', content)
    concepts.extend(hashtags)
    
    # Remove duplicates and None values
    filtered_concepts = [c for c in set(concepts) if c is not None]
    
    return filtered_concepts

def get_existing_explainers():
    """Get a list of existing explainer articles."""
    explainer_files = glob.glob(str(EXPLAINER_DIR / "*.md"))
    existing_explainers = {}
    
    for file_path in explainer_files:
        # Skip README and template files
        filename = os.path.basename(file_path)
        if filename in ['README.md', 'explainer-template.md']:
            continue
        
        # Extract concept name from filename or frontmatter
        concept = Path(file_path).stem
        frontmatter = extract_frontmatter(file_path)
        
        if 'concept' in frontmatter:
            concept = frontmatter['concept']
        
        version = frontmatter.get('version', 1)
        existing_explainers[concept] = {
            'path': file_path,
            'version': version,
            'last_updated': frontmatter.get('last_updated', 'Unknown')
        }
    
    return existing_explainers

def generate_update_report(recent_transcripts, existing_explainers, output_file):
    """Generate a report of suggested explainer updates."""
    # Organize concepts by transcript
    concept_sources = defaultdict(list)
    transcript_data = {}
    
    for transcript_path in recent_transcripts:
        filename = os.path.basename(transcript_path)
        transcript_name = os.path.splitext(filename)[0]
        
        concepts = get_concepts_from_transcript(transcript_path)
        frontmatter = extract_frontmatter(transcript_path)
        title = frontmatter.get('title', transcript_name)
        
        transcript_data[transcript_name] = {
            'path': transcript_path,
            'title': title,
            'concepts': concepts
        }
        
        for concept in concepts:
            concept_sources[concept].append(transcript_name)
    
    # Generate report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Weekly Explainer Update Report\n\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Recent Transcript Analyses\n\n")
        for name, data in transcript_data.items():
            f.write(f"- {data['title']} (`{name}`)\n")
        f.write("\n")
        
        f.write("## Suggested New Explainers\n\n")
        new_concepts = [c for c in concept_sources.keys() if c not in existing_explainers]
        
        if new_concepts:
            # Filter out None values and sort
            filtered_new_concepts = [c for c in new_concepts if c is not None]
            for concept in sorted(filtered_new_concepts):
                sources = concept_sources[concept]
                f.write(f"### {concept}\n\n")
                f.write(f"Found in {len(sources)} transcript(s):\n\n")
                for source in sources:
                    title = transcript_data[source]['title']
                    f.write(f"- {title} (`{source}`)\n")
                f.write("\n")
        else:
            f.write("No new explainers suggested this week.\n\n")
        
        f.write("## Suggested Explainer Updates\n\n")
        update_concepts = [c for c in concept_sources.keys() if c in existing_explainers]
        
        if update_concepts:
            # Filter out None values and sort
            filtered_update_concepts = [c for c in update_concepts if c is not None]
            for concept in sorted(filtered_update_concepts):
                sources = concept_sources[concept]
                explainer_info = existing_explainers[concept]
                
                f.write(f"### {concept} (current version: {explainer_info['version']})\n\n")
                f.write(f"Last updated: {explainer_info['last_updated']}\n\n")
                f.write(f"New information found in {len(sources)} transcript(s):\n\n")
                
                for source in sources:
                    title = transcript_data[source]['title']
                    f.write(f"- {title} (`{source}`)\n")
                f.write("\n")
        else:
            f.write("No explainer updates suggested this week.\n\n")
    
    print(f"Report generated: {output_file}")
    return output_file

def main():
    """Main function."""
    args = parse_args()
    
    print(f"Looking for transcript analyses from the past {args.days} days...")
    recent_transcripts = get_recent_transcripts(args.days)
    print(f"Found {len(recent_transcripts)} recent transcript analyses.")
    
    print("Getting existing explainer articles...")
    existing_explainers = get_existing_explainers()
    print(f"Found {len(existing_explainers)} existing explainer articles.")
    
    print("Generating update report...")
    report_file = generate_update_report(recent_transcripts, existing_explainers, args.output)
    
    print(f"\nNext steps:")
    print(f"1. Review the report: {report_file}")
    print(f"2. Create/update explainer articles as suggested")
    print(f"3. Update the log file: {LOG_FILE}")

if __name__ == "__main__":
    main()