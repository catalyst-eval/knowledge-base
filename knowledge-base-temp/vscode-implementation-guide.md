# VS Code Implementation Guide: Neurodiversity-Affirming Clinical Knowledge Base

This guide provides instructions for setting up and using VS Code to manage the clinical transcript analysis knowledge base. These configurations will enhance your ability to maintain consistent tagging, navigate between related analyses, and validate your markdown files.

## Initial Setup

### 1. Install VS Code Extensions

Install the following extensions to enhance your workflow:

- **YAML** (Red Hat) - For YAML front matter validation and schema support
- **Markdown All in One** (Yu Zhang) - For markdown editing, TOC, and preview
- **GitHub Pull Requests and Issues** (GitHub) - For GitHub integration
- **Path Intellisense** (Christian Kohler) - For file path autocompletion
- **Front Matter** (eliostruyf) - For managing front matter in markdown files
- **Markdown Preview Enhanced** (Yiyi Wang) - Advanced markdown preview
- **Foam** (Foam) - For personal knowledge management
- **GitLens** (GitKraken) - Enhanced Git capabilities

### 2. Configure Workspace Settings

Create a `.vscode` folder in your repository root and add a `settings.json` file:

```json
{
  "editor.formatOnSave": true,
  "markdown.preview.breaks": true,
  "yaml.schemas": {
    "./schemas/transcript-analysis-schema.json": ["*.md"]
  },
  "foam.edit.linkReferenceDefinitions": "withExtensions",
  "foam.openDailyNote.directory": ".",
  "foam.openDailyNote.filenameFormat": "MM-DD-YYYY_daily-notes",
  "foam.openDailyNote.fileExtension": "md",
  "search.exclude": {
    "**/node_modules": true,
    "**/bower_components": true,
    "**/*.code-search": true
  }
}
```

### 3. Set Up YAML Schema Validation

Create a `schemas` folder in your repository and add a `transcript-analysis-schema.json` file:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Transcript Analysis",
  "description": "Schema for transcript analysis front matter",
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "The title of the analysis"
    },
    "date": {
      "type": ["string", "object"],
      "description": "The date of the analysis"
    },
    "client_type": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["adolescent", "adult", "parent-coaching", "individual-therapy", "family-therapy"]
      }
    },
    "presenting_issue": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "neurotype": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["autism", "adhd", "combined-neurotype"]
      }
    },
    "concepts": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "metaphors": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "strategies": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "related_analyses": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "version": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": ["title", "date", "concepts", "version"]
}
```

## Workflow for Creating New Analyses

### 1. Use the Custom Template

Create a template file in a `.templates` folder at the repository root. Name it `transcript-analysis-template.md`:

```markdown
---
title: ""
date: ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}
client_type: 
  - 
presenting_issue:
  - 
neurotype:
  - 
concepts:
  - 
metaphors:
  - 
strategies:
  - 
related_analyses:
  - 
version: 1
---

# ${TM_FILENAME_BASE}

## Summary of Key Insights

[Summary content here]

## Novel Concepts Identified

### [Concept Name]

[Concept description] #tag1 #tag2

### [Concept Name]

[Concept description] #tag1 #tag2

## Metaphors and Explanatory Tools Used

### [Metaphor Name]

[Metaphor description] #tag1 #tag2

## Client-Centered Applications

### [Application Area]

[Application description] #tag1 #tag2

## Practical Strategies Demonstrated

### [Strategy Name]

[Strategy description] #tag1 #tag2

## Research Validation and Connections to Existing Literature

### [Research Area]

[Research connections] #tag1 #tag2

## Recommendations for Framework Additions or Modifications

[Recommendations] #tag1 #tag2

## Related Analyses

- [Related Analysis](related-file.md) - Brief description

---

© Copyright ${CURRENT_YEAR} Bridge Family Therapy, LLC. All rights reserved. This material is the property of Bridge Family Therapy, LLC and may not be reproduced in any way without permission.
```

To use this template, right-click in the explorer and select "New File" and enter the filename using the convention `MM-DD-YYYY_brief-concept-description.md`, then right-click and select "Open with Template" > "transcript-analysis-template.md".

### 2. Set Up Custom Snippets

Create custom snippets to quickly insert common patterns.

Open the Command Palette (Ctrl+Shift+P) and type "Configure User Snippets", then select "New Global Snippets file..." and name it "transcript-analysis".

```json
{
  "Insert concept section": {
    "prefix": "concept",
    "body": [
      "### ${1:Concept Name}",
      "",
      "${2:Description of the concept} #${3:tag1} #${4:tag2}",
      ""
    ],
    "description": "Insert a concept section with tags"
  },
  "Insert YAML front matter": {
    "prefix": "front",
    "body": [
      "---",
      "title: \"${1:Title}\"",
      "date: ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}",
      "client_type: ",
      "  - ${2:client_type}",
      "presenting_issue:",
      "  - ${3:issue}",
      "neurotype:",
      "  - ${4:neurotype}",
      "concepts:",
      "  - ${5:concept}",
      "metaphors:",
      "  - ${6:metaphor}",
      "strategies:",
      "  - ${7:strategy}",
      "related_analyses:",
      "  - \"${8:filename}.md\"",
      "version: 1",
      "---",
      ""
    ],
    "description": "Insert YAML front matter for transcript analysis"
  },
  "Insert related analysis link": {
    "prefix": "related",
    "body": [
      "- [${1:Title}](${2:filename}.md) - ${3:Brief description}"
    ],
    "description": "Insert a related analysis link"
  },
  "Insert tag": {
    "prefix": "tag",
    "body": "#${1:tag-name}",
    "description": "Insert a hashtag"
  }
}
```

## Tag Validation and Assistance

### 1. Set Up Tag Auto-Completion

Create a `tags.txt` file in the repository root with all valid tags:

```
interest-based-nervous-system
monotropism
combined-neurotype-experience
autistic-inertia
interoception
bottom-up-processing
co-regulation
...
```

Then install the **Custom Autocomplete** extension (Eno Yao) and add this to your settings.json:

```json
"custom-auto-complete.includePatterns": [
    "tags.txt"
],
"custom-auto-complete.triggerCharacters": [
    "#"
]
```

### 2. Add Tag Validation Script

Create a `.vscode/tasks.json` file:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate Tags",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/.github/scripts/tag_validator.py",
        "${file}"
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Update Indexes",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/.github/scripts/update_indexes.py"
      ],
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

## Navigation Features

### 1. Set Up Foam for Navigation

The Foam extension provides wiki-style linking and navigation. Configure it by creating a `.foam/templates.json` file:

```json
{
  "templates": [
    {
      "name": "New Transcript Analysis",
      "pathToTemplate": ".templates/transcript-analysis-template.md",
      "directory": "."
    }
  ]
}
```

### 2. Configure Graph View

Foam provides a graph view that shows connections between your notes. Use Ctrl+Alt+G to open it.

### 3. Link Previews and Navigation

When hovering over links to other analyses, VS Code will show a preview of the content. Ctrl+click on links to navigate between files.

## Working with Claude and the Repository

### 1. Interacting with Claude About the Repository

When providing files to Claude for analysis, use the VS Code to pull the current content from GitHub, then share the relevant files in the chat session.

Instructions for Claude:
- When referencing files from the repository, include the full filename with date prefix
- Follow the established tag conventions from the tag glossary
- When suggesting changes, be specific about which file and section to modify
- When analyzing new transcripts, follow the standardized format for analyses

### 2. Commit and Push Changes with VS Code

After making changes based on Claude's recommendations:

1. Open the Source Control tab (Ctrl+Shift+G)
2. Stage your changes
3. Enter a commit message with a clear format:
   - "Add analysis: [brief description]" for new analyses
   - "Update tags: [filename]" for tag updates
   - "Modify concept: [concept name]" for content changes
4. Push your changes to GitHub

### 3. Handling Tag Evolution

When concepts evolve:

1. Update the tag version in the YAML front matter
2. Add the updated concept to the Concept Evolution Log
3. Run the "Update Indexes" task to refresh cross-references

## VS Code Shortcuts for Efficient Workflow

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+P | Command Palette |
| Ctrl+P | Quick Open File |
| Ctrl+Space | Trigger Suggestions |
| Ctrl+L | Select Current Line |
| Ctrl+/ | Toggle Line Comment |
| Alt+Z | Toggle Word Wrap |
| Ctrl+K V | Open Preview to Side |
| Ctrl+K Ctrl+T | Select Color Theme |
| F1 | Show Help |

## Recommended Workflow

1. **Start with the Template**: Use the transcript analysis template for consistency
2. **Use Snippets**: Insert sections and tags using snippets
3. **Validate Tags**: Run the validation task to check tags against the glossary
4. **Cross-Reference**: Add links to related analyses
5. **Update Indexes**: Run the index update task to refresh navigation files
6. **Commit Changes**: Use the Source Control tab to commit and push

## Troubleshooting

### YAML Front Matter Issues

If VS Code shows errors in the YAML front matter:
- Check for proper indentation (2 spaces)
- Ensure all arrays use the correct format with hyphens
- Verify that string values with special characters are in quotes

### Tag Validation Failures

If the tag validator reports issues:
- Check the tag glossary to ensure you're using valid tags
- Add new tags to the glossary before using them
- Verify that hierarchical tags use the correct format (with colons)

### Navigation Problems

If links between files aren't working:
- Ensure filenames match exactly (case-sensitive)
- Check that file paths are relative to the repository root
- Verify that the Foam extension is properly configured

## Resources

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Foam Wiki Documentation](https://foambubble.github.io/foam/)
- [Markdown Guide](https://www.markdownguide.org/)
- [YAML Syntax](https://yaml.org/spec/1.2/spec.html)
- [Regular Expressions Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions)
