# AI Mobile Test Generator

Automatically generates unit tests for Swift and Kotlin code using AI.

## Usage

```yaml
name: Generate Tests

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test-generation:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Generate Tests
      uses: maail/ai-mobile-test-generator@v1.0.3
      with:
        openai-api-key: ${{ secrets.OPENAI_API_KEY }}
        languages: 'swift,kotlin'
        model: 'gpt-4-turbo'

    - name: Push Changes
      run: |
        if [[ -n "$(git status --porcelain)" ]]; then
          git config user.name "GitHub Test Generator Bot"
          git config user.email "<>"
          git add .
          git commit -m "Add auto-generated unit tests"
          git push
        fi
```

## Inputs

- `openai-api-key`: Your OpenAI API key (required)
- `languages`: Comma-separated list of languages to generate tests for (default: 'swift,kotlin')
- `model`: OpenAI model to use (default: 'gpt-4-turbo')

## How It Works

This action:
1. Detects Swift and Kotlin files changed in the last commit
2. Generates comprehensive unit tests using AI
3. Commits and pushes the generated tests

## Requirements

- An OpenAI API key with access to the specified model
- Repository permissions to push changes

## Supported Languages
- Swift / SwiftUI
- Kotlin / Jetpack Compose

## Overview
This GitHub Action automatically generates unit tests for Swift and Kotlin files using OpenAI's GPT models when code is pushed to the repository.

## Prerequisites
- A GitHub repository with Swift or Kotlin source files
- An OpenAI API key
- Access to GPT-4 or GPT-3.5 Turbo models

## Key Features
- Detects changed Swift and Kotlin files
- Generates language-specific unit tests
- Automatically commits generated test files
- Supports multiple testing frameworks:
  - XCTest for Swift
  - JUnit 5 for Kotlin

## Setup Instructions

1. **Create OpenAI API Key**
   - Go to [OpenAI's website](https://platform.openai.com/)
   - Generate an API key

2. **Add GitHub Secret**
   - In your repository settings, go to Secrets and Variables > Actions
   - Create a new repository secret named `OPENAI_API_KEY`
   - Add your OpenAI API key

3. **Add Workflow File**
   - Create `.github/workflows/test-generator.yml`
   - Copy the contents from the provided workflow file

## Workflow Behavior
- Triggers on pushes to the main branch
- Identifies changed Swift and Kotlin files
- Generates corresponding unit tests using GPT
- Commits and pushes test files with naming convention:
  - Swift: `OriginalFileName` → `OriginalFileNameTests.swift`
  - Kotlin: `OriginalFileName.kt` → `OriginalFileNameTest.kt`

## Customization
- Modify `generate_unit_tests()` function to adjust test generation
- Change OpenAI model or prompting strategy
- Add more sophisticated language detection

## Limitations
- Requires OpenAI API key
- Test generation may not be 100% accurate
- Consumes OpenAI API credits

## Best Practices
- Always review generated tests
- Use as a supplementary tool
- Manually verify and refine generated tests

## Troubleshooting
- Check GitHub Actions logs
- Verify OpenAI API key and credits
- Ensure dependencies are correctly installed

## Example Workflow
1. Commit a new Swift or Kotlin file
2. Action triggers automatically
3. GPT generates appropriate unit tests
4. Tests are committed to the repository

## Security Considerations
- Never commit your OpenAI API key directly
- Always use GitHub Secrets
- Limit repository access to trusted collaborators

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
[Insert your license here]

## Disclaimer
This tool is an AI-assisted test generation tool and should not replace comprehensive manual testing.