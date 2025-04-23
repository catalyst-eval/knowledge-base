#!/usr/bin/env python3
"""
Index File Generator for Clinical Transcript Analyses

This script generates and updates index files that organize transcript analyses
by different categories (concepts, client types, metaphors, etc.)

Usage:
  python update_indexes.py

Output:
  - Creates/updates index.md with links to all analyses
  - Creates/updates category-specific index files
"""

import os
import re
import frontmatter
import glob
from collections import defaultdict

# Configuration
CATEGORIES = {
    'concepts': 'Conceptual Frameworks',
    'neurotype': 'Neurotype',
    'client_type': 'Client Type',
    'presenting_issue': 'Presenting Issues',
    'metaphors': 'Metaphors and Explanatory Tools',
    'strategies': 'Practical Strategies'
}

def extract_metadata_from_files():
    """Extract metadata from all markdown files."""
    md_files = glob.glob('*.md')
    
    # Skip existing index files
    md_files = [f for f in md_files if not f.startswith('index')]
    
    file_metadata = {}
    
    for file_path in md_files:
        try:
            with open(file_path, 'r') as f:
                post = frontmatter.load(f)
            
            # Only include files with proper front matter
            if 'title' in post.metadata and 'date' in post.metadata:
                file_metadata[file_path] = post.metadata
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return file_metadata

def generate_main_index(file_metadata):
    """Generate the main index file with links to category-specific indexes."""
    content = "# Clinical Transcript Analysis Index\n\n"
    
    # Add introduction
    content += "This index organizes transcript analyses by different categories for easy navigation.\n\n"
    
    # Add category sections
    content += "## Browse by Category\n\n"
    
    for category_key, category_name in CATEGORIES.items():
        content += f"- [{category_name}](index_{category_key}.md)\n"
    
    content += "\n## All Analyses\n\n"
    
    # Sort files by date, newest first
    sorted_files = sorted(
        [(path, meta) for path, meta in file_metadata.items() if 'date' in meta],
        key=lambda x: x[1]['date'],
        reverse=True
    )
    
    # Add all files with their titles
    for file_path, metadata in sorted_files:
        title = metadata.get('title', file_path)
        date_str = str(metadata.get('date', ''))
        content += f"- [{title}]({file_path}) - {date_str}\n"
    
    # Write to file
    with open('index.md', 'w') as f:
        f.write(content)
    
    print(f"Generated main index.md with {len(sorted_files)} analyses")

def generate_category_indexes(file_metadata):
    """Generate category-specific index files."""
    for category_key, category_name in CATEGORIES.items():
        # Skip if no files have this category
        if not any(category_key in meta for meta in file_metadata.values()):
            continue
            
        content = f"# {category_name} Index\n\n"
        content += f"This index organizes transcript analyses by {category_name.lower()}.\n\n"
        
        # Group files by category values
        category_groups = defaultdict(list)
        
        for file_path, metadata in file_metadata.items():
            if category_key in metadata:
                category_values = metadata[category_key]
                
                # Handle both string and list values
                if isinstance(category_values, str):
                    category_groups[category_values].append((file_path, metadata))
                elif isinstance(category_values, list):
                    for value in category_values:
                        category_groups[value].append((file_path, metadata))
        
        # Add table of contents
        content += "## Contents\n\n"
        
        for category_value in sorted(category_groups.keys()):
            anchor = category_value.lower().replace(' ', '-').replace('/', '-')
            content += f"- [{category_value}](#{anchor})\n"
        
        content += "\n"
        
        # Add sections for each category value
        for category_value in sorted(category_groups.keys()):
            content += f"## {category_value}\n\n"
            
            # Sort files in each category by date
            sorted_files = sorted(
                category_groups[category_value],
                key=lambda x: x[1].get('date', ''),
                reverse=True
            )
            
            for file_path, metadata in sorted_files:
                title = metadata.get('title', file_path)
                date_str = str(metadata.get('date', ''))
                content += f"- [{title}]({file_path}) - {date_str}\n"
            
            content += "\n"
        
        # Write to file
        index_file = f"index_{category_key}.md"
        with open(index_file, 'w') as f:
            f.write(content)
        
        print(f"Generated {index_file} with {len(category_groups)} {category_name.lower()}")

def main():
    # Extract metadata from all files
    file_metadata = extract_metadata_from_files()
    
    if not file_metadata:
        print("No valid markdown files with front matter found.")
        return
    
    # Generate main index
    generate_main_index(file_metadata)