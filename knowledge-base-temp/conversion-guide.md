# Guide to Converting Existing Analyses to the New Format

This guide provides instructions for converting existing transcript analyses to use our new YAML front matter and inline hashtag system. Following these steps will ensure consistency across all analyses and enable searchability and cross-referencing.

## Step 1: Choose an Appropriate Filename

Rename the file using the convention:
```
MM-DD-YYYY_brief-concept-description.md
```

Example:
- From: `Interest-Based Nervous Systems Analysis.md`
- To: `04-23-2025_interest-based-nervous-systems-parent-coaching.md`

## Step 2: Add YAML Front Matter

Add the following YAML front matter at the beginning of the file:

```yaml
---
title: "Original Title of Analysis"
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

Example:
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

## Step 3: Add Inline Hashtags

Throughout the document, add inline hashtags after key concepts are mentioned:

1. Identify important concepts, metaphors, and strategies in your text
2. Add hashtags directly after the relevant passages
3. Use simple tag format (e.g., #monotropism) rather than hierarchical format

Example:
```markdown
The clinician introduces the concept that "autism, ADHD, these are interest-based nervous systems" (Speaker A). This framework represents an evolution beyond traditional deficit-focused models. #interest-based-nervous-system #neurological-frameworks
```

Placement tips:
- Add tags at the end of paragraphs when possible to avoid breaking up the flow of text
- Group related tags together
- Use 2-3 tags per paragraph maximum to avoid cluttering the text

## Step 4: Add Cross-References

At the end of the document, add a "Related Analyses" section:

```markdown
## Related Analyses

- [Title of Related Analysis](MM-DD-YYYY_related-analysis-filename.md) - Brief description of relevance
- [Another Related Analysis](MM-DD-YYYY_another-related-analysis.md) - Brief description of relevance
```

Example:
```markdown
## Related Analyses

- [Combined Neurotype Experience and Spoon Theory](04-15-2025_combined-neurotype-spoon-theory.md) - Explores energy management concepts and combined autism-ADHD experiences
```

## Step 5: Review Tag Usage

Before finalizing the conversion:

1. Verify all tags used are defined in the tag glossary
2. Check for consistency in tag usage throughout the document
3. Ensure major concepts from the analysis are represented in the front matter
4. Confirm appropriate use of inline hashtags for key concepts

## Example Conversion

Here's an excerpt showing the before/after of a converted section:

### Before:
```
The therapist introduced the concept of "attention tunneling" when explaining 
why transitions are particularly difficult for Clayton. This perspective helps reframe 
seemingly oppositional behavior as a neurological difference in how attention is 
allocated and shifted.
```

### After:
```
The therapist introduced the concept of "attention tunneling" #monotropism #attention-dynamics when explaining 
why transitions are particularly difficult for Clayton. This perspective helps reframe 
seemingly oppositional behavior as a neurological difference in how attention is 
allocated and shifted.
```

## Running the Tag Validator

After converting your document, run the tag validator script to check for any issues:

```bash
python .github/scripts/tag_validator.py
```

This will:
- Validate that all tags used are defined in the glossary
- Suggest additional tags based on content analysis
- Check for required front matter fields
- Update cross-references based on tag similarity

Review the output and make any necessary corrections before committing your changes.
