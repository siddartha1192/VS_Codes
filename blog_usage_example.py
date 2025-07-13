#!/usr/bin/env python3
"""
Example script showing how to add different types of posts to TechBlog
"""

from blog_post_updater import TechBlogUpdater, create_sample_post

def create_python_tutorial():
    """Create a Python tutorial post"""
    content_sections = [
        {
            'type': 'heading',
            'level': 2,
            'text': 'Introduction to List Comprehensions'
        },
        {
            'type': 'text',
            'text': 'List comprehensions are a powerful feature in Python that allow you to create lists in a concise and readable way.'
        },
        {
            'type': 'section_end'
        },
        {
            'type': 'heading',
            'level': 2,
            'text': 'Basic Syntax'
        },
        {
            'type': 'text',
            'text': 'The basic syntax of a list comprehension is:'
        },
        {
            'type': 'code',
            'language': 'python',
            'code': '''# Basic list comprehension
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
print(squared)  # Output: [1, 4, 9, 16, 25]

# With condition
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(even_squares)  # Output: [4, 16]'''
        },
        {
            'type': 'section_end'
        },
        {
            'type': 'heading',
            'level': 2,
            'text': 'Advanced Examples'
        },
        {
            'type': 'text',
            'text': 'Here are some more complex examples:'
        },
        {
            'type': 'code',
            'language': 'python',
            'code': '''# Nested list comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Dictionary comprehension
words = ['python', 'java', 'javascript']
word_lengths = {word: len(word) for word in words}
print(word_lengths)  # Output: {'python': 6, 'java': 4, 'javascript': 10}'''
        },
        {
            'type': 'section_end'
        },
        {
            'type': 'heading',
            'level': 2,
            'text': 'Best Practices'
        },
        {
            'type': 'list',
            'items': [
                'Keep list comprehensions simple and readable',
                'Use regular loops for complex logic',
                'Consider generator expressions for large datasets',
                'Use meaningful variable names even in comprehensions'
            ]
        },
        {
            'type': 'faq',
            'question': 'When should I use list comprehensions?',
            'answer': 'Use list comprehensions when you need to transform or filter data in a simple, readable way. They are more Pythonic than traditional for loops for simple transformations.'
        },
        {
            'type': 'section_end'
        }
    ]
    return content_sections

def create_automation_post():
    """Create an automation/DevOps post"""
    content_sections = [
        {
            'type': 'heading',
            'level': 2,
            'text': 'Setting Up CI/CD with GitHub Actions'
        },
        {
            'type': 'text',
            'text': 'GitHub Actions provides a powerful platform for automating your development workflow. This guide will show you how to set up a basic CI/CD pipeline.'
        },
        {
            'type': 'section_end'
        },
        {
            'type': 'heading',
            'level': 2,
            'text': 'Basic Workflow Configuration'
        },
        {
            'type': 'text',
            'text': 'Create a .github/workflows/ci.yml file in your repository:'
        },
        {
            'type': 'code',
            'language': 'yaml',
            'code': '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/'''
        },
        {
            'type': 'section_end'
        },
        {
            'type': 'heading',
            'level': 2,
            'text': 'Adding Deployment Stage'
        },
        {
            'type': 'code',
            'language': 'yaml',
            'code': '''  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production server"
        # Add your deployment commands here'''
        },
        {
            'type': 'text',
            'text': 'This configuration will run tests on every push and deploy only when pushing to the main branch.'
        },
        {
            'type': 'section_end'
        }
    ]
    return content_sections

def add_multiple_posts():
    """Example of adding multiple posts"""
    
    updater = TechBlogUpdater("techblog.db")
    
    try:
        updater.connect()
        
        # Add Python tutorial
        print("Adding Python tutorial...")
        updater.add_post(
            title="Mastering Python List Comprehensions",
            excerpt="Learn how to write clean, efficient Python code using list comprehensions with practical examples and best practices.",
            content_sections=create_python_tutorial(),
            category_name="Programming",
            topics=["Python", "Tutorial", "Best Practices"],
            author_email="siddartha1192@gmail.com",
            featured=True,
            featured_image="/static/images/posts/python-list-comprehensions.png",
            read_time=8,
            primary_language="python"
        )
        
        # Add automation post  
        print("\nAdding automation tutorial...")
        updater.add_post(
            title="GitHub Actions CI/CD Pipeline Setup",
            excerpt="Step-by-step guide to setting up automated testing and deployment using GitHub Actions for your projects.",
            content_sections=create_automation_post(),
            category_name="Automation",
            topics=["GitHub Actions", "CI/CD", "DevOps", "Automation"],
            author_email="siddartha1192@gmail.com",
            featured=False,
            featured_image="/static/images/posts/github-actions.png",
            read_time=12,
            primary_language="yaml"
        )
        
        # List all recent posts
        print("\n" + "="*60)
        updater.list_recent_posts(10)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        updater.disconnect()

def quick_add_post():
    """Quick way to add a simple post"""
    
    updater = TechBlogUpdater("techblog.db")
    
    try:
        updater.connect()
        
        # Simple post with minimal content
        simple_content = [
            {
                'type': 'heading',
                'level': 2,
                'text': 'Quick Post Example'
            },
            {
                'type': 'text',
                'text': 'This is a quick example of how to add a simple post to your blog database.'
            },
            {
                'type': 'code',
                'language': 'python',
                'code': 'print("Hello from TechBlog!")'
            },
            {
                'type': 'section_end'
            }
        ]
        
        updater.add_post(
            title="Quick Test Post",
            excerpt="A simple test post to verify the database update functionality.",
            content_sections=simple_content,
            category_name="Tech News",
            topics=["Testing", "Database"],
            read_time=2
        )
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        updater.disconnect()

if __name__ == "__main__":
    print("TechBlog Post Creator")
    print("="*50)
    
    choice = input("""
Choose an option:
1. Add sample posts (Python + Automation)
2. Add a quick test post
3. Just run the basic example

Enter choice (1-3): """).strip()
    
    if choice == "1":
        add_multiple_posts()
    elif choice == "2":
        quick_add_post()
    else:
        # Run the basic example from the main module
        from blog_post_updater import main
        main()
