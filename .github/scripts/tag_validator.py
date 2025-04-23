#!/usr/bin/env python3
"""
Tag Validator and Suggester for Clinical Transcript Analyses

This script:
1. Validates that all tags used in markdown files are defined in the tag glossary
2. Suggests additional tags based on content analysis
3. Updates cross-references between related documents
4. Verifies required YAML front matter is present

Usage:
  python tag_validator.py

Output:
  - Prints validation results to stdout
  - Writes tag suggestions to tag_suggestions.json for GitHub Action use
  - Updates cross-references in markdown files when appropriate
"""

import os
import re
import json
import yaml
import glob
from collections import defaultdict

# Configuration
TAG_GLOSSARY_FILE = 'tag-glossary.md'
REQUIRED_FRONT_MATTER = ['title', 'date', 'concepts', 'version']
MIN_CONFIDENCE_THRESHOLD = 0.6

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

def extract_tags_from_glossary():
    """Extract all valid tags from the tag glossary file."""
    if not os.path.exists(TAG_GLOSSARY_FILE):
        print(f"Warning: Tag glossary file '{TAG_GLOSSARY_FILE}' not found.")
        return set()
    
    valid_tags = set()
    tag_pattern = re.compile(r'\*\*([a-z0-9-]+)\*\*:')
    hierarchical_tag_pattern = re.compile(r'\*\*([a-z0-9-]+:[a-z0-9-]+)\*\*:')
    
    with open(TAG_GLOSSARY_FILE, 'r') as f:
        content = f.read()
        
        # Extract simple tags
        for match in tag_pattern.finditer(content):
            valid_tags.add(match.group(1))
            
        # Extract hierarchical tags
        for match in hierarchical_tag_pattern.finditer(content):
            valid_tags.add(match.group(1))
    
    return valid_tags

def extract_tags_from_file(file_path):
    """Extract all tags from a markdown file including front matter and inline hashtags."""
    used_tags = set()
    
    try:
        # Parse front matter
        front_matter, content = extract_yaml_front_matter(file_path)
        if not front_matter:
            return used_tags
            
        # Extract tags from front matter
        for tag_category in ['concepts', 'metaphors', 'strategies', 'neurotype', 'client_type', 'presenting_issue']:
            if tag_category in front_matter:
                tags = front_matter[tag_category]
                if isinstance(tags, list):
                    for tag in tags:
                        if isinstance(tag, (str, int, float, bool)):  # Ensure value is hashable
                            used_tags.add(tag)
                elif isinstance(tags, (str, int, float, bool)):
                    used_tags.add(tags)
        
        # Extract inline hashtags
        hashtag_pattern = re.compile(r'#([a-z0-9-]+)')
        for match in hashtag_pattern.finditer(content):
            used_tags.add(match.group(1))
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return used_tags

def validate_required_front_matter(file_path):
    """Check if a file has all required front matter fields."""
    missing_fields = []
    
    try:
        front_matter, _ = extract_yaml_front_matter(file_path)
        if not front_matter:
            return REQUIRED_FRONT_MATTER
            
        for field in REQUIRED_FRONT_MATTER:
            if field not in front_matter:
                missing_fields.append(field)
                
    except Exception as e:
        print(f"Error validating front matter in {file_path}: {e}")
        missing_fields = REQUIRED_FRONT_MATTER  # Assume all are missing
        
    return missing_fields

def extract_content_for_analysis(file_path):
    """Extract the content from a markdown file for text analysis."""
    try:
        _, content = extract_yaml_front_matter(file_path)
        
        # Remove front matter and just return the markdown content
        match = re.match(r'^---\s*\n.*?\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            return match.group(1)
        return content
    except Exception as e:
        print(f"Error extracting content from {file_path}: {e}")
        return ""

def create_tag_mapping(valid_tags):
    """Create a mapping of keywords to tags for suggestion."""
    tag_keywords = {
        # Neurological concepts
        'interest-based-nervous-system': ['interest', 'attention', 'focus', 'motivation', 'engagement'],
        'monotropism': ['tunnel', 'focus', 'attention', 'singular', 'intense', 'fixation'],
        'bottom-up-processing': ['physiological', 'sensory', 'body', 'emotions', '80/20', 'bottom-up'],
        'autistic-inertia': ['inertia', 'transition', 'shift', 'movement', 'stuck', 'switching'],
        
        # Metaphors
        'tropism-model': ['tropism', 'plant', 'attention', 'focus', 'monotropic', 'polytropic', 'varotropic'],
        'ice-pick-on-slope': ['slope', 'ice', 'arrest', 'fall', 'stop', 'regulation', 'dysregulation'],
        '80-20-model': ['80/20', 'percent', 'bottom-up', 'top-down', 'processing', 'rational'],
        
        # Client types
        'adhd': ['adhd', 'attention', 'hyperactive', 'impulsive', 'executive', 'function'],
        'autism': ['autism', 'autistic', 'asd', 'neurodevelopmental', 'monotropic'],
        'combined-neurotype': ['combined', 'co-occurring', 'both', 'adhd', 'autism'],
        
        # Strategies
        'three-part-communication': ['self-admission', 'empathy', 'ambition', 'communication'],
        'sensory-regulation': ['sensory', 'regulation', 'stimuli', 'input', 'soothe', 'reset'],
        'collaborative-problem-solving': ['collaborative', 'problem-solving', 'partnership', 'solution']
    }
    
    # Add hierarchical tag alternatives
    hierarchical_mapping = {
        'interest-based-nervous-system': 'neurological:interest-based-nervous-system',
        'monotropism': 'neurological:monotropism',
        'bottom-up-processing': 'regulatory:bottom-up-processing',
        'co-regulation': 'regulatory:co-regulation',
        'autistic-inertia': 'neurological:autistic-inertia',
        'adhd': 'client:adhd',
        'autism': 'client:autism',
        'combined-neurotype': 'client:combined-neurotype',
        'three-part-communication': 'communication:three-part-sequence',
        'sensory-regulation': 'intervention:sensory-regulation',
        'collaborative-problem-solving': 'intervention:collaborative-problem-solving'
    }
    
    # Add hierarchical versions to keywords
    for tag, hierarchical_tag in hierarchical_mapping.items():
        if tag in tag_keywords and hierarchical_tag in valid_tags:
            tag_keywords[hierarchical_tag] = tag_keywords[tag]
    
    return tag_keywords

def suggest_tags(file_path, valid_tags, tag_keywords):
    """Suggest additional tags based on content analysis."""
    content = extract_content_for_analysis(file_path)
    if not content:
        return [], {}
    
    # Simple keyword counting approach instead of NLTK
    content_lower = content.lower()
    
    # Calculate tag confidence scores
    tag_confidence = {}
    
    for tag, keywords in tag_keywords.items():
        if tag not in valid_tags:
            continue
            
        # Count keyword occurrences
        keyword_count = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Count occurrences of whole words only
            keyword_count += len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', content_lower))
        
        # Normalize by content length (rough estimate)
        content_size = max(1, len(content.split()))  # Avoid division by zero
        confidence = min(keyword_count / (content_size * 0.01), 1.0)
        
        if confidence > MIN_CONFIDENCE_THRESHOLD:
            tag_confidence[tag] = confidence
    
    # Get current tags
    current_tags = extract_tags_from_file(file_path)
    
    # Filter suggestions to only include tags not already used
    suggested_tags = [tag for tag in tag_confidence.keys() if tag not in current_tags]
    
    # Return suggestions sorted by confidence
    return sorted(suggested_tags, key=lambda tag: tag_confidence[tag], reverse=True), tag_confidence

def update_cross_references(files_and_tags):
    """Update cross-references between related documents."""
    # Build a similarity matrix between documents
    file_tags = {file: tags for file, tags in files_and_tags.items()}
    files = list(file_tags.keys())
    
    # Calculate Jaccard similarity between tag sets
    similarities = {}
    for i, file1 in enumerate(files):
        similarities[file1] = {}
        tags1 = file_tags[file1]
        for file2 in files:
            if file1 != file2:
                tags2 = file_tags[file2]
                # Jaccard similarity: |A ∩ B| / |A ∪ B|
                if not tags1 or not tags2:
                    similarity = 0
                else:
                    intersection = len(tags1.intersection(tags2))
                    union = len(tags1.union(tags2))
                    similarity = intersection / union if union > 0 else 0
                similarities[file1][file2] = similarity
    
    # Update related_analyses in each file
    for file_path in files:
        try:
            # Get the top 3 most similar files
            similar_files = sorted(
                [(other_file, sim) for other_file, sim in similarities[file_path].items()],
                key=lambda x: x[1], 
                reverse=True
            )[:3]
            
            # Only include files with similarity above threshold
            related_files = [os.path.basename(f) for f, sim in similar_files if sim > 0.3]
            
            if related_files:
                front_matter, content = extract_yaml_front_matter(file_path)
                
                if front_matter:
                    # Update related_analyses in front matter
                    front_matter['related_analyses'] = related_files
                    
                    # Write back to file
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Update YAML front matter in content
                    new_content = re.sub(
                        r'^---\s*\n.*?\n---\s*\n',
                        '---\n' + yaml.dump(front_matter, default_flow_style=False) + '---\n',
                        content,
                        flags=re.DOTALL
                    )
                    
                    with open(file_path, 'w') as f:
                        f.write(new_content)
                    
        except Exception as e:
            print(f"Error updating cross-references in {file_path}: {e}")

def main():
    # Extract valid tags from glossary
    valid_tags = extract_tags_from_glossary()
    print(f"Found {len(valid_tags)} valid tags in glossary")
    
    # Process all markdown files
    md_files = glob.glob('transcript-analyses/*.md')
    
    # Skip the glossary and index files
    md_files = [f for f in md_files if not os.path.basename(f).startswith('index')]
    
    # Track results
    invalid_tags = []
    missing_front_matter = []
    files_and_tags = {}
    tag_suggestions = {}
    tag_confidence_scores = {}
    
    # Create tag keyword mapping
    tag_keywords = create_tag_mapping(valid_tags)
    
    # Process each file
    for file_path in md_files:
        # Check front matter
        missing_fields = validate_required_front_matter(file_path)
        if missing_fields:
            missing_front_matter.append({"file": file_path, "missing_fields": missing_fields})
            
        # Extract and validate tags
        used_tags = extract_tags_from_file(file_path)
        files_and_tags[file_path] = used_tags
        
        for tag in used_tags:
            if tag not in valid_tags:
                invalid_tags.append({"file": file_path, "tag": tag})
                
        # Generate tag suggestions
        suggested_tags, confidence = suggest_tags(file_path, valid_tags, tag_keywords)
        if suggested_tags:
            tag_suggestions[file_path] = suggested_tags
            tag_confidence_scores[file_path] = {tag: float(conf) for tag, conf in confidence.items()}
    
    # Update cross-references
    update_cross_references(files_and_tags)
    
    # Output results
    print(f"Processed {len(md_files)} markdown files")
    print(f"Found {len(invalid_tags)} invalid tags")
    print(f"Found {len(missing_front_matter)} files with missing front matter")
    print(f"Generated suggestions for {len(tag_suggestions)} files")
    
    # Write suggestions to file for GitHub Action
    with open('tag_suggestions.json', 'w') as f:
        json.dump({
            "invalid_tags": invalid_tags,
            "missing_front_matter": [f["file"] for f in missing_front_matter],
            "tag_suggestions": tag_suggestions,
            "tag_confidence": tag_confidence_scores
        }, f, indent=2)
    
    # Set output for GitHub Action
    has_suggestions = bool(invalid_tags or missing_front_matter or tag_suggestions)
    print(f"::set-output name=has_suggestions::{str(has_suggestions).lower()}")
    
if __name__ == "__main__":
    main()