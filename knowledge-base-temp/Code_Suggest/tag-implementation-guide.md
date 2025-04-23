# Neurodiversity-Affirming Clinical Knowledge Base: Tag Implementation Guide

## Overview

This guide outlines the tagging structure and implementation for our clinical transcript analysis repository. The goal is to create a consistent, searchable knowledge base that evolves as our understanding of neurodiversity-affirming approaches develops.

## File Naming Convention

All transcript analysis files should follow this naming convention:
```
MM-DD-YYYY_brief-concept-description.md
```

Examples:
- `04-23-2025_interest-based-nervous-systems-parent-coaching.md`
- `04-15-2025_combined-neurotype-spoon-theory.md`

## YAML Front Matter Structure

Each transcript analysis should begin with YAML front matter containing metadata about the session:

```yaml
---
title: "Interest-Based Nervous Systems and Bottom-Up Processing: Parent Coaching for Autistic Adolescent Dysregulation"
date: 2025-04-23
client_type: 
  - adolescent
  - parent-coaching
presenting_issue:
  - dysregulation
  - homework-struggles
  - transitions
neurotype:
  - autism
  - adhd
concepts:
  - interest-based-nervous-system
  - bottom-up-processing
  - monotropism
  - autistic-inertia
  - dialectical-understanding
metaphors:
  - tropism-model
  - ice-pick-on-slope
  - 80-20-model
  - dialectical-pairs
strategies:
  - three-part-communication
  - sensory-regulation
  - collaborative-problem-solving
  - parental-modeling
related_analyses:
  - "04-15-2025_combined-neurotype-spoon-theory.md"
version: 1
---
```

## Tag Hierarchies

Tags follow a hierarchical structure to allow for more granular categorization and searching:

### Conceptual Framework Tags
- `neurological:interest-based-nervous-system`
- `neurological:monotropism`
- `regulatory:bottom-up-processing`
- `regulatory:co-regulation`
- `regulatory:dysregulation-cascade`
- `systems:family-dynamics`
- `systems:educational-impact`
- `developmental:adolescent`
- `developmental:school-age`
- `communication:three-part-sequence`

### Client-Centered Application Tags
- `client:adhd`
- `client:autism`
- `client:combined-neurotype`
- `client:school-challenges`
- `intervention:parent-coaching`
- `intervention:family-systems`
- `intervention:transition-management`
- `intervention:sensory-regulation`

### Metaphor and Tool Tags
- `metaphor:tropism-model`
- `metaphor:ice-pick-slope`
- `metaphor:dialectical-pairs`
- `metaphor:bottom-up-top-down`
- `metaphor:energy-battery`

## Inline Hashtag Usage

When discussing specific concepts within the document, use inline hashtags to mark their appearance:

```markdown
## Novel Concepts

The therapist introduced the concept of "attention tunneling" #monotropism #attention-dynamics when explaining 
why transitions are particularly difficult for Clayton. This perspective helps reframe seemingly oppositional 
behavior as a neurological difference in how attention is allocated and shifted.
```

These inline tags help identify where specific concepts appear within the document, making them easier to search and reference.

## Cross-Reference System

At the end of each analysis, include a "Related Analyses" section that links to other transcript analyses sharing key concepts:

```markdown
## Related Analyses

- [Combined Neurotype Experience and Spoon Theory](04-15-2025_combined-neurotype-spoon-theory.md) - Also discusses energy management and sensory regulation
- [Collaborative Problem-Solving for School Transitions](03-30-2025_collaborative-problem-solving-school.md) - Contains additional strategies for supporting transitions
```

## Tag Glossary

Maintain a central `tag-glossary.md` file that defines each tag and its proper usage:

```markdown
# Tag Glossary

## Neurological Frameworks
- **interest-based-nervous-system**: Describes neurological patterns where attention and motivation are primarily guided by interest rather than external demands.
- **monotropism**: Attention style characterized by intense focus on a single interest or task at a time.

## Regulatory Models
- **bottom-up-processing**: Neural processing that prioritizes sensory and physiological information over cognitive control.
- **co-regulation**: Process where one person helps another regulate their emotional state.

...
```

This glossary serves as both documentation and a reference for consistent tag application.

## Evolution Tracking

To track the evolution of concepts over time:

1. Include a `version` field in the YAML front matter
2. When significant updates are made to a concept, increment the version number
3. Document major conceptual shifts in a `concept-evolution.md` file

Example:

```markdown
# Concept Evolution Log

## interest-based-nervous-system
- v1 (04-23-2025): Initial conceptualization focusing on attention allocation
- v2 (06-12-2025): Expanded to include motivational aspects and connection to dopamine signaling

## monotropism
- v1 (04-23-2025): Described as "attention tunneling" with emphasis on challenges
- v2 (07-08-2025): Refined to emphasize strengths and include "flow state" connections
```

## Search and Navigation

While we're not creating folders for different topics, we can enhance searchability through:

1. GitHub's built-in search functionality
2. GitHub Topics at the repository level
3. Links between related documents
4. Tag-based index files

Create an `index.md` file that organizes analyses by tag category:

```markdown
# Clinical Transcript Analysis Index

## By Neurotype
- [Autism](#autism)
- [ADHD](#adhd)
- [Combined Neurotype](#combined-neurotype)

## By Conceptual Framework
- [Interest-Based Nervous System](#interest-based-nervous-system)
- [Monotropism](#monotropism)
- [Bottom-Up Processing](#bottom-up-processing)

...

### Autism
- [Interest-Based Nervous Systems and Bottom-Up Processing](04-23-2025_interest-based-nervous-systems-parent-coaching.md)
- [Sensory Regulation Techniques for School Environments](05-10-2025_sensory-regulation-school.md)

### Interest-Based Nervous System
- [Interest-Based Nervous Systems and Bottom-Up Processing](04-23-2025_interest-based-nervous-systems-parent-coaching.md)
- [Combined Neurotype Experience and Spoon Theory](04-15-2025_combined-neurotype-spoon-theory.md)
```

## Implementation Steps

1. Convert existing transcript analyses to include YAML front matter
2. Create the tag glossary
3. Implement inline hashtags in existing documents
4. Set up the cross-reference system
5. Create the concept evolution log
6. Develop index files for navigation
7. Set up GitHub Actions for tag validation
