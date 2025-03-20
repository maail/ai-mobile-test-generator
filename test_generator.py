import os
import re
import subprocess
import openai

# Configure OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']
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
        
        Source code:
        ```swift
        {source_code}
        ```

        Generate the test file content.
        """
    
    elif file_path.endswith('.kt') or file_path.endswith('.kts'):
        prompt = f"""
        Generate comprehensive unit tests for this Kotlin code. 
        Use JUnit 5 for testing. Cover different scenarios, edge cases, 
        and potential error conditions. Use Kotlin's testing idioms.
        
        Source code:
        ```kotlin
        {source_code}
        ```

        Generate the test file content.
        """
    
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    # Call OpenAI API to generate tests
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates unit tests for different programming languages."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the generated test code
    test_code = response.choices[0].message.content

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
    # Stage the new test files
    for test_file in test_files:
        subprocess.run(['git', 'add', test_file])

    # Commit if there are changes
    if test_files:
        subprocess.run([
            'git', 'config', 'user.name', 'GitHub Test Generator Bot'
        ])
        subprocess.run([
            'git', 'config', 'user.email', '<>'
        ])
        subprocess.run([
            'git', 'commit', '-m', 'Add auto-generated unit tests'
        ])
        subprocess.run(['git', 'push'])

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