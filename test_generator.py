import os
import re
import subprocess
from openai import OpenAI

# Configure OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
languages = os.environ.get('LANGUAGES', 'swift,kotlin').split(',')
model = os.environ.get('MODEL', 'gpt-4-turbo')

def get_changed_files():
    # Get list of changed files in the last commit
    result = subprocess.run(
        ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'], 
        capture_output=True, 
        text=True
    )
    return result.stdout.strip().split('\n')

def generate_unit_tests(file_path):
    # Read the source file
    with open(file_path, 'r') as f:
        source_code = f.read()

    # Determine language and generate appropriate test prompt
    if file_path.endswith('.swift') or file_path.endswith('.swiftui'):
        prompt = f"""
        Generate comprehensive unit tests for this Swift/SwiftUI code. 
        Use XCTest framework. Cover different scenarios, edge cases, 
        and potential error conditions.
        
        IMPORTANT: Return ONLY the Swift code for the tests, with no explanations or markdown formatting.
        Start your response with 'import XCTest' and include only valid Swift code.
        
        Source code:
        ```swift
        {source_code}
        ```
        """
    
    elif file_path.endswith('.kt') or file_path.endswith('.kts'):
        prompt = f"""
        Generate comprehensive unit tests for this Kotlin code. 
        Use JUnit 5 for testing. Cover different scenarios, edge cases, 
        and potential error conditions. Use Kotlin's testing idioms.
        
        IMPORTANT: Return ONLY the Kotlin code for the tests, with no explanations or markdown formatting.
        Start your response with appropriate import statements and include only valid Kotlin code.
        
        Source code:
        ```kotlin
        {source_code}
        ```
        """
    
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    # Call OpenAI API to generate tests - UPDATED for OpenAI v1.0+
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a code generator that outputs only valid code with no explanations or markdown. Your output should be ready to use in an IDE without any modifications."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the generated test code - UPDATED for OpenAI v1.0+
    test_code = response.choices[0].message.content
    
    # Clean up the response if it contains markdown code blocks
    if "```" in test_code:
        # Extract code between code blocks
        code_match = re.search(r'```(?:swift|kotlin)?\s*(.*?)\s*```', test_code, re.DOTALL)
        if code_match:
            test_code = code_match.group(1).strip()
    
    return test_code

def create_test_file(source_file, test_code):
    # Determine test file path based on language
    if source_file.endswith('.swift') or source_file.endswith('.swiftui'):
        test_file_path = source_file.replace('.swift', 'Tests.swift').replace('.swiftui', 'Tests.swift')
    elif source_file.endswith('.kt') or source_file.endswith('.kts'):
        test_file_path = source_file.replace('.kt', 'Test.kt').replace('.kts', 'Test.kt')
    else:
        raise ValueError(f"Unsupported file type: {source_file}")
    
    # Write test code to file
    with open(test_file_path, 'w') as f:
        f.write(test_code)

    return test_file_path

def commit_tests(test_files):
    if not test_files:
        print("No test files to commit")
        return
        
    # Print git status for debugging
    print("Git status before committing:")
    subprocess.run(['git', 'status'])
    
    # Configure git
    subprocess.run(['git', 'config', 'user.name', 'GitHub Test Generator Bot'])
    subprocess.run(['git', 'config', 'user.email', '<>'])
    
    # Stage the new test files
    for test_file in test_files:
        subprocess.run(['git', 'add', test_file])
        print(f"Staged file: {test_file}")
    
    # Check if we're in a PR
    event_name = os.environ.get('GITHUB_EVENT_NAME')
    print(f"GitHub event: {event_name}")
    
    # Check if there are changes to commit
    result = subprocess.run(['git', 'diff', '--staged', '--quiet'], capture_output=True)
    if result.returncode == 0:
        print("No changes to commit")
        return
    
    if event_name == 'pull_request':
        # For pull requests, create a commit but don't push
        subprocess.run(['git', 'commit', '-m', 'Add auto-generated unit tests'])
        print("Created commit with generated tests. Changes will appear in the PR.")
    else:
        # For direct pushes to branches, commit and push
        subprocess.run(['git', 'commit', '-m', 'Add auto-generated unit tests'])
        
        # Print current branch for debugging
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        current_branch = result.stdout.strip()
        print(f"Pushing to branch: {current_branch}")
        
        # Push changes
        push_result = subprocess.run(['git', 'push'], capture_output=True, text=True)
        if push_result.returncode != 0:
            print(f"Push failed: {push_result.stderr}")
        else:
            print("Committed and pushed generated tests successfully.")

def main():
    # Get supported languages from environment
    supported_extensions = []
    if 'swift' in languages:
        supported_extensions.extend(['.swift', '.swiftui'])
    if 'kotlin' in languages:
        supported_extensions.extend(['.kt', '.kts'])
    
    # Get changed files for supported languages
    changed_files = [
        f for f in get_changed_files() 
        if any(f.endswith(ext) for ext in supported_extensions)
        and not re.search(r'(Test|Tests)\.(swift|kt)$', f)  # Exclude existing test files
    ]

    # Generate and commit tests for each changed file
    test_files = []
    for file in changed_files:
        try:
            test_code = generate_unit_tests(file)
            test_file = create_test_file(file, test_code)
            test_files.append(test_file)
            print(f"Generated test file for {file}")
        except Exception as e:
            print(f"Error generating tests for {file}: {e}")

    # Commit generated tests
    commit_tests(test_files)

if __name__ == '__main__':
    main() 