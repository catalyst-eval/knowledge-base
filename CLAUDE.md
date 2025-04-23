# Workflow Guide for Claude

This document outlines the workflow process for analyzing transcripts and managing framework modifications.

## Complete Workflow Illustration

```
1. User provides transcript for analysis
   │
   ▼
2. Claude analyzes transcript
   │
   ▼
3. Claude creates transcript analysis file
   │   - Uses proper YAML front matter
   │   - Includes only existing tags from glossary
   │   - Follows template structure
   │
   ▼
4. Claude creates separate framework modifications file
   │   - Compares transcript concepts against existing tags
   │   - Identifies potential new tags and categories
   │   - Provides definitions and justifications
   │
   ▼
5. Claude presents framework modifications to user
   │   - "Based on my analysis, I recommend these additions to the framework:"
   │   - Lists each recommendation with explanation
   │
   ▼
6. Claude asks for user approval
   │   - "Would you like me to implement any of these changes to the tag glossary?"
   │   - Lists each recommendation as a separate option
   │
   ▼
7. User provides feedback
   │   - Approves specific recommendations
   │   - Suggests modifications
   │   - Denies certain recommendations
   │
   ▼
8. Claude implements approved changes
    - Updates tag-glossary.md with new tags and definitions
    - Updates concept-evolution-log.md if needed
    - Confirms changes made to the user
```

## Transcript Analysis Workflow

### 1. Analyze the Transcript
- Read and analyze the transcript content
- Create a properly formatted markdown file with YAML front matter
- Include appropriate tags from the tag glossary
- Follow the template structure

### 2. Create Framework Modifications File
- Create a separate framework-mods file with recommendations
- Use the naming format: `YYYY-MM-DD_brief-description_framework-mods.md`
- Include YAML front matter with metadata
- Reference existing tags and indexes when making recommendations

### 3. Compare Against Existing Structure
- Before recommending new tags, check if similar tags already exist
- Compare recommendations against existing conceptual framework
- Review the tag glossary for existing definitions
- Ensure recommendations align with the overall framework

### 4. Prompt User for Approval
- Present the framework modifications to the user
- Ask specifically which changes they would like to implement
- Provide options for approving/denying individual recommendations
- Allow for user suggestions and modifications

### 5. Implement Approved Changes
- Update tag-glossary.md with approved new tags and definitions
- Update concept-evolution-log.md if needed
- Ensure cross-references are maintained

## Framework Modification Guidelines

When creating framework modifications:

1. **Focus on Incremental Evolution**
   - Build on existing concepts rather than creating entirely new frameworks
   - Connect new ideas to established patterns and models

2. **Maintain Hierarchical Structure**
   - Place new tags within appropriate categories
   - Consider whether a tag should be hierarchical (e.g., category:tag)

3. **Include Clear Definitions**
   - Provide concise, clear definitions for new tags
   - Explain the conceptual basis and practical applications
   - Reference research or clinical observations that support the concept

4. **Consider Cross-Categorical Impact**
   - Evaluate how a new tag might relate to multiple categories
   - Identify connections between conceptual frameworks

## Example Implementation Process

### 1. Framework Modification File

```md
---
title: "Framework Modifications - Executive Function in ADHD Entrepreneurship"
date: 2025-04-23
related_analysis: "transcript-analyses/executive-function-adhd-entrepreneurship.md"
---

# Framework Modification Recommendations

## New Tag Suggestions

### adhd-entrepreneurship
**Definition**: A specialized approach addressing the unique intersection of ADHD traits and entrepreneurial contexts, focusing on leveraging hyperfocus, creativity, and risk tolerance while accommodating executive function challenges.
**Category**: client-centered-applications
**Related tags**: executive-function, adhd, energy-management

## Category Expansion Suggestions

### Expand "Energy Management" Category
To include "Strategic Energy Allocation" - This moves beyond basic energy conservation to include the intentional direction of limited executive resources toward high-value activities.

## Conceptual Framework Additions

### Add "Value-Based Decision Making" to Practical Strategies
Given the importance of aligning decisions with personal values to reduce cognitive strain and rejection sensitivity, this category would include:
- Methods for identifying core values vs. societal expectations
- Decision-making frameworks that prioritize value alignment
- Techniques for communicating value-based boundaries
- Approaches for minimizing people-pleasing behaviors that deplete resources
```

### 2. User Approval Request

```
Based on my analysis of the transcript, I recommend these additions to the framework:

1. New tag: "adhd-entrepreneurship" - A specialized approach addressing the unique intersection of ADHD traits and entrepreneurial contexts.

2. Category expansion: Add "Strategic Energy Allocation" to the "Energy Management" category - This includes intentional direction of limited executive resources toward high-value activities.

3. New strategy category: "Value-Based Decision Making" - Methods for aligning decisions with personal values to reduce cognitive strain and rejection sensitivity.

Would you like me to implement any of these changes to the tag glossary? You can select specific options or suggest modifications.
```

### 3. Implementation of Approved Changes

If the user approves the first recommendation:

```python
# Update tag-glossary.md

# Find the client-centered-applications section
# Add new tag definition in alphabetical order:

"""
**adhd-entrepreneurship**: A specialized approach addressing the unique intersection of ADHD traits and entrepreneurial contexts, focusing on leveraging hyperfocus, creativity, and risk tolerance while accommodating executive function challenges. Related tags: executive-function, adhd, energy-management
"""

# Confirm to user:
"I've added the 'adhd-entrepreneurship' tag to the glossary under the client-centered-applications section. Would you like me to proceed with any other changes?"
```