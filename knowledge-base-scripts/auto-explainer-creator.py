#!/usr/bin/env python3
"""
Automatic Explainer Creator Script

This script takes the weekly explainer update report and automatically
creates new explainer articles or updates existing ones based on the suggestions.

Usage:
    python auto-explainer-creator.py [--report=explainer-update-report.md] [--priority=5]

Arguments:
    --report       Path to the explainer update report (default: explainer-update-report.md)
    --priority     Number of new explainers to create (default: 5)
"""

import os
import re
import sys
import yaml
import argparse
import datetime
from pathlib import Path
from collections import defaultdict

# Configuration
REPO_ROOT = Path(__file__).resolve().parents[2]  # Concept_Dev directory
TRANSCRIPT_DIR = REPO_ROOT / "transcript-analyses"
EXPLAINER_DIR = REPO_ROOT / "explainers"
TEMPLATE_PATH = EXPLAINER_DIR / "explainer-template.md"
LOG_FILE = REPO_ROOT / "explainer-updates-log.md"
INDEX_FILE = REPO_ROOT / "explainers_index.md"

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Create explainer articles from update report")
    parser.add_argument("--report", default="explainer-update-report.md", help="Path to explainer update report")
    parser.add_argument("--priority", type=int, default=5, help="Number of new explainers to create")
    parser.add_argument("--update-all", action="store_true", help="Update all existing explainers")
    return parser.parse_args()

def read_template():
    """Read the explainer template file."""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def parse_update_report(report_path):
    """Parse the update report to extract suggested new explainers and updates."""
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract new explainer suggestions
    new_section_match = re.search(r'## Suggested New Explainers\n\n(.*?)(?=\n\n## Suggested Explainer Updates|\Z)', content, re.DOTALL)
    new_explainers = {}
    
    if new_section_match:
        new_section = new_section_match.group(1)
        concept_blocks = re.findall(r'### ([\w-]+)\n\nFound in (\d+) transcript\(s\):\n\n(.*?)(?=\n\n### |\n\nNo new|\Z)', new_section, re.DOTALL)
        
        for concept, count, sources_text in concept_blocks:
            sources = re.findall(r'- (.*?) \(`(.*?)`\)', sources_text)
            new_explainers[concept] = {
                'count': int(count),
                'sources': [{'title': title, 'file': file} for title, file in sources]
            }
    
    # Extract update suggestions
    update_section_match = re.search(r'## Suggested Explainer Updates\n\n(.*?)(?=\n\n## |\Z)', content, re.DOTALL)
    update_explainers = {}
    
    if update_section_match:
        update_section = update_section_match.group(1)
        if "No explainer updates suggested" not in update_section:
            concept_blocks = re.findall(r'### ([\w-]+) \(current version: (\d+)\)\n\nLast updated: (.*?)\n\nNew information found in (\d+) transcript\(s\):\n\n(.*?)(?=\n\n### |\Z)', update_section, re.DOTALL)
            
            for concept, version, last_updated, count, sources_text in concept_blocks:
                sources = re.findall(r'- (.*?) \(`(.*?)`\)', sources_text)
                update_explainers[concept] = {
                    'current_version': int(version),
                    'last_updated': last_updated,
                    'count': int(count),
                    'sources': [{'title': title, 'file': file} for title, file in sources]
                }
    
    return new_explainers, update_explainers

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from a markdown file."""
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

def extract_transcript_content(file_path):
    """Extract content from a transcript analysis file excluding frontmatter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    return content

def get_related_tags(concept, transcript_files):
    """Identify related tags based on transcript content."""
    related_tags = set()
    
    for file_path in transcript_files:
        frontmatter = extract_frontmatter(file_path)
        
        # Get concepts from frontmatter
        if 'concepts' in frontmatter and isinstance(frontmatter['concepts'], list):
            concepts = [c for c in frontmatter['concepts'] if c is not None]
            if concept in concepts:
                related_tags.update([c for c in concepts if c != concept])
        
        # Get neurotype tags
        if 'neurotype' in frontmatter and isinstance(frontmatter['neurotype'], list):
            neurotypes = [n for n in frontmatter['neurotype'] if n is not None]
            related_tags.update(neurotypes)
        
        # Get strategies
        if 'strategies' in frontmatter and isinstance(frontmatter['strategies'], list):
            strategies = [s for s in frontmatter['strategies'] if s is not None]
            related_tags.update(strategies)
    
    # Limit to 5 most relevant related tags
    return list(related_tags)[:5]

def create_explainer_content(concept, sources, template):
    """Create content for a new explainer article."""
    # Get file paths for transcript sources
    transcript_files = [TRANSCRIPT_DIR / f"{source['file']}.md" for source in sources]
    existing_files = [f for f in transcript_files if os.path.exists(f)]
    
    # Gather content from transcripts
    clinical_description = []
    client_friendly_definition = []
    neurological_basis = []
    therapeutic_approaches = []
    case_examples = []
    research_connections = []
    related_concepts = []
    
    for file_path in existing_files:
        content = extract_transcript_content(file_path)
        
        # Extract relevant sections about the concept
        concept_sections = re.findall(r'(?:^|\n)#{1,3} .*?\b' + re.escape(concept) + r'\b.*?\n(.*?)(?=\n#{1,3}|\Z)', content, re.DOTALL, re.IGNORECASE)
        
        if concept_sections:
            clinical_description.append(concept_sections[0])
        
        # Extract research connections
        research_match = re.search(r'(?:^|\n)## Research Validation.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if research_match:
            research_connections.append(research_match.group(1))
        
        # Extract case examples or therapeutic approaches
        approaches_match = re.search(r'(?:^|\n)## (?:Practical Strategies|Therapeutic Approaches).*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if approaches_match:
            therapeutic_approaches.append(approaches_match.group(1))
    
    # Get related tags
    related_tags = get_related_tags(concept, existing_files)
    
    # Create the explainer content
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Replace placeholders in template
    explainer = template.replace("[concept-tag]", concept)
    explainer = explainer.replace("[CONCEPT NAME]", concept.replace("-", " ").title())
    explainer = explainer.replace("YYYY-MM-DD", today)
    
    # Add related tags
    if related_tags:
        related_tags_text = "\n".join([f"  - {tag}" for tag in related_tags])
        explainer = explainer.replace("  - [related-tag-1]\n  - [related-tag-2]\n  - [related-tag-3]", related_tags_text)
    
    # Add clinical description
    if clinical_description:
        explainer = explainer.replace("[Comprehensive definition and explanation of the concept, integrating information from all relevant transcript analyses]", 
                                      "\n\n".join(clinical_description))
    
    # Add therapeutic approaches
    if therapeutic_approaches:
        explainer = explainer.replace("### 1. [Approach Name]\n\n**Clinical Rationale**: [Explanation of why this approach works for this concept]\n\n**Implementation Example**:\n\n*Anonymized and Enhanced for Clinical Use*:\n\n\"[Example of how a clinician might explain or implement this approach with a client]\"\n\n**Concrete Strategy**:\n- [Specific technique 1]\n- [Specific technique 2]\n- [Specific technique 3]", 
                                      "\n\n".join(therapeutic_approaches))
    
    # Add research connections
    if research_connections:
        explainer = explainer.replace("[Academic research supporting or related to this concept]", 
                                     "\n\n".join(research_connections))
    
    # Add transcript references
    transcript_refs = "\n".join([f"- [{source['title']}](../transcript-analyses/{source['file']}.md)" for source in sources])
    explainer = explainer.replace("[List of transcript analyses that discuss this concept, with links]\n\n- [Transcript Analysis Title 1](../transcript-analyses/YYYY-MM-DD_transcript-analysis-filename.md)\n- [Transcript Analysis Title 2](../transcript-analyses/YYYY-MM-DD_transcript-analysis-filename.md)", 
                                 transcript_refs)
    
    return explainer

def create_new_explainer(concept, sources, template):
    """Create a new explainer article."""
    # Format filename
    filename = f"{concept}.md"
    file_path = EXPLAINER_DIR / filename
    
    # Create content
    content = create_explainer_content(concept, sources, template)
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path

def update_explainer(concept, current_version, sources, new_content=None):
    """Update an existing explainer article."""
    # Get file path
    filename = f"{concept}.md"
    file_path = EXPLAINER_DIR / filename
    
    # Read current content
    with open(file_path, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Extract frontmatter
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', current_content, re.DOTALL)
    if frontmatter_match:
        frontmatter_yaml = frontmatter_match.group(1)
        try:
            frontmatter = yaml.safe_load(frontmatter_yaml)
        except yaml.YAMLError:
            print(f"Error parsing frontmatter in {file_path}")
            return None
        
        # Update version and last_updated
        frontmatter['version'] = current_version + 1
        frontmatter['last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # Update content (placeholder - in a real implementation, you'd analyze and merge content)
        new_frontmatter = yaml.dump(frontmatter, default_flow_style=False)
        updated_content = current_content.replace(frontmatter_yaml, new_frontmatter)
        
        # Add new transcript references if they don't exist
        for source in sources:
            ref_line = f"- [{source['title']}](../transcript-analyses/{source['file']}.md)"
            if ref_line not in updated_content:
                # Find the transcript references section
                transcript_refs_match = re.search(r'## Transcript References\s*\n(.*?)(?=\n##|\Z)', updated_content, re.DOTALL)
                if transcript_refs_match:
                    # Append the new reference
                    refs_section = transcript_refs_match.group(1)
                    new_refs_section = f"{refs_section}\n{ref_line}"
                    updated_content = updated_content.replace(refs_section, new_refs_section)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return file_path
    
    return None

def update_log_file(new_explainers, updated_explainers):
    """Update the explainer updates log."""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Read current log
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        current_log = f.read()
    
    # Create new log entry
    new_entry = f"### {today}\n\n"
    
    if new_explainers:
        new_entry += "#### New Explainers Created\n"
        for concept, info in new_explainers.items():
            source_titles = ", ".join([f'"{s["title"]}"' for s in info['sources']])
            new_entry += f"- **{concept}**: Created initial version synthesizing information from {source_titles}\n"
        new_entry += "\n"
    
    if updated_explainers:
        new_entry += "#### Explainers Updated\n"
        for concept, info in updated_explainers.items():
            source_titles = ", ".join([f'"{s["title"]}"' for s in info['sources']])
            new_entry += f"- **{concept}**: Updated with new information from {source_titles} (version {info['current_version']} → {info['current_version'] + 1})\n"
        new_entry += "\n"
    
    # Insert new entry after the format section
    format_section_end = current_log.find("## Updates")
    if format_section_end != -1:
        format_section_end = current_log.find("\n\n", format_section_end)
        updated_log = current_log[:format_section_end + 2] + new_entry + current_log[format_section_end + 2:]
        
        # Write updated log
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_log)

def main():
    """Main function."""
    args = parse_args()
    
    # Parse update report
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = REPO_ROOT / report_path
    
    print(f"Parsing update report: {report_path}")
    new_explainers, update_explainers = parse_update_report(report_path)
    
    print(f"Found {len(new_explainers)} new explainer suggestions")
    print(f"Found {len(update_explainers)} explainer update suggestions")
    
    # Sort new explainers by count (frequency of appearance in transcripts)
    sorted_new_explainers = sorted(new_explainers.items(), key=lambda x: x[1]['count'], reverse=True)
    
    # Read template
    template = read_template()
    
    # Create new explainers
    created_explainers = {}
    for concept, info in sorted_new_explainers[:args.priority]:
        print(f"Creating explainer for '{concept}' (mentioned in {info['count']} transcripts)")
        file_path = create_new_explainer(concept, info['sources'], template)
        created_explainers[concept] = info
    
    # Update existing explainers
    updated_explainers = {}
    if args.update_all:
        for concept, info in update_explainers.items():
            print(f"Updating explainer for '{concept}' (version {info['current_version']} → {info['current_version'] + 1})")
            file_path = update_explainer(concept, info['current_version'], info['sources'])
            if file_path:
                updated_explainers[concept] = info
    
    # Update log file
    if created_explainers or updated_explainers:
        print("Updating explainer updates log")
        update_log_file(created_explainers, updated_explainers)
    
    print(f"\nCreated {len(created_explainers)} new explainers")
    print(f"Updated {len(updated_explainers)} existing explainers")
    
    print("\nNext steps:")
    print("1. Review the created/updated explainers")
    print("2. Edit and improve the content as needed")
    print("3. Update the explainers_index.md file if needed")

if __name__ == "__main__":
    main()