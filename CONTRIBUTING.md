# Contributing to the Neurodiversity-Affirming Clinical Knowledge Base

Thank you for contributing to our neurodiversity-affirming clinical knowledge base. This guide will help ensure consistency across all transcript analyses.

## Adding New Transcript Analyses

### 1. Begin with a Template

Use the template in `/templates/transcript-analysis.md` as a starting point for new analyses. This ensures all required sections and front matter are included.

### 2. Follow File Naming Conventions

Name transcript analysis files using this format:
```
MM-DD-YYYY_brief-concept-description.md
```

For example:
- `04-23-2025_interest-based-nervous-systems-parent-coaching.md`
- `04-15-2025_combined-neurotype-spoon-theory.md`

### 3. Include Required YAML Front Matter

Each analysis must include this YAML front matter at the top of the file:

```yaml
---
title: "Descriptive Title of Analysis"
date: YYYY-MM-DD
client_type: 
  - [client type tags]
presenting_issue:
  - [issue tags]
neurotype:
  - [neurotype tags]
concepts:
  - [concept tags]
metaphors:
  - [metaphor tags]
strategies:
  - [strategy tags]
related_analyses:
  - [related analysis filenames]
version: 1
---
```

### 4. Use Proper Tags

All tags must be defined in the `tag-glossary.md` file. If you need a new tag:

1. Check if a similar tag already exists
2. If not, add the new tag to the glossary with a clear definition
3. Consider how it relates to existing tags

### 5. Use Inline Hashtags

When discussing specific concepts within your analysis, mark them with inline hashtags:

```markdown
The therapist introduced the concept of #monotropism when explaining why transitions are difficult.
```

This makes concepts easier to search and reference.

### 6. Include Quote Attribution

When including transcript quotes, always attribute them to the speaker:

```markdown
Speaker A: "This is a direct quote from the transcript."

Speaker B: "This is a response."
```

### 7. Connect to Research

Whenever possible, connect clinical observations to published research:

```markdown
This approach aligns with research by Smith et al. (2022) on sensory processing in autism.
```

## Version Control for Concepts

When updating a concept:

1. Increment the version number in the front matter
2. Document the conceptual evolution in `concept-evolution-log.md`

Example evolution entry:

```markdown
### monotropism
- **v1 (04-23-2025)**: Initial conceptualization focusing on attention tunneling
- **v2 (07-15-2025)**: Expanded to include benefits of focused attention and flow states
```

## Using the GitHub Workflow

### Automated Validation

When you push changes or create a pull request, automated checks will:

1. Validate that all tags exist in the glossary
2. Suggest additional tags based on content analysis
3. Check for required front matter fields
4. Update index files when merging to main

Review any validation errors or suggestions in the pull request comments.

### Manual Review Process

After submitting a new analysis or major update:

1. Compare your analysis to existing ones for consistency
2. Check that tags are applied appropriately
3. Verify that cross-references to related documents are accurate
4. Ensure research connections are well-sourced

## Questions or Suggestions

If you have questions about the contribution process or suggestions for improving the knowledge base structure, please open an issue in the repository.