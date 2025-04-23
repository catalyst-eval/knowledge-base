# Workflow Guide for Claude

This document outlines the workflow process for analyzing transcripts and managing framework modifications.

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

## Example Framework Modification

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