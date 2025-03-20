# Multi-Language Automated Test Generator

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