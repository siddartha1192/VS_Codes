#!/usr/bin/env python3
"""
TechBlog Database Post Updater
Adds new posts to SQLite database with consistent styling and structure
"""

import sqlite3
import datetime
import re
from typing import List, Dict, Optional

class TechBlogUpdater:
    def __init__(self, db_path: str = "techblog.db"):
        """Initialize the blog updater with database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Standard CSS template based on existing posts
        self.css_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.0/themes/prism.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.0/components/prism-{language}.min.js"></script>
    <style>
        pre[class*="language-"],
        code[class*="language-"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        h1, h2, h3 {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            font-size: 22px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .code-box {{
            position: relative;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            overflow: auto;
            background-color: #ffffff;
            border: 1px solid #ddd;
        }}
        .copy-button {{
            background-color: #0074d9;
            color: #fff;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            position: absolute;
            top: 10px;
            right: 10px;
        }}
        .copy-button.copied {{
            background-color: #4CAF50;
            transition: background-color 0.5s;
        }}
        pre {{
            margin: 0;
        }}
        ul {{
            padding-left: 20px;
        }}
        .faq {{
            background-color: #fff;
            border-left: 5px solid #0074d9;
            padding: 15px 20px;
            margin: 20px 0;
        }}
        .faq p {{
            margin: 10px 0;
        }}
    </style>
</head>
<body>

{content}

<script>
    Prism.highlightAll();

    function copyToClipboard(index) {{
        const codeBlocks = document.querySelectorAll('.code-box code');
        const selectedCode = codeBlocks[index].textContent;
        const button = document.querySelectorAll('.copy-button')[index];
        
        const textarea = document.createElement('textarea');
        textarea.value = selectedCode;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        // Add the 'copied' class to change button color temporarily
        button.classList.add('copied');
        setTimeout(function() {{
            button.classList.remove('copied');
        }}, 500);
    }}
</script>
</body>
</html>"""

    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("📊 Database connection closed")

    def create_slug(self, title: str) -> str:
        """Create URL-friendly slug from title"""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = slug.strip('-')
        return slug

    def get_or_create_category(self, name: str, description: str = "", color: str = "#0074d9") -> int:
        """Get existing category or create new one"""
        slug = self.create_slug(name)
        
        # Check if category exists
        self.cursor.execute("SELECT id FROM category WHERE slug = ?", (slug,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        
        # Create new category
        self.cursor.execute("""
            INSERT INTO category (name, slug, description, color)
            VALUES (?, ?, ?, ?)
        """, (name, slug, description, color))
        
        category_id = self.cursor.lastrowid
        print(f"📂 Created new category: {name} (ID: {category_id})")
        return category_id

    def get_or_create_topic(self, name: str) -> int:
        """Get existing topic or create new one"""
        slug = self.create_slug(name)
        
        # Check if topic exists
        self.cursor.execute("SELECT id FROM topic WHERE slug = ?", (slug,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        
        # Create new topic
        self.cursor.execute("""
            INSERT INTO topic (name, slug)
            VALUES (?, ?)
        """, (name, slug))
        
        topic_id = self.cursor.lastrowid
        print(f"🏷️ Created new topic: {name} (ID: {topic_id})")
        return topic_id

    def get_author_id(self, email: str) -> Optional[int]:
        """Get author ID by email"""
        self.cursor.execute("SELECT id FROM author WHERE email = ?", (email,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def format_code_block(self, code: str, language: str = "python", index: int = 0) -> str:
        """Format code with copy button and syntax highlighting"""
        return f"""<div class="code-box">
        <button class="copy-button" onclick="copyToClipboard({index})">Copy Code</button>
        <pre><code class="language-{language}">
{code}
        </code></pre>
    </div>"""

    def format_content_with_styling(self, sections: List[Dict]) -> str:
        """Format content sections with proper HTML structure"""
        content_html = ""
        code_index = 0
        
        for section in sections:
            section_type = section.get('type', 'text')
            
            if section_type == 'heading':
                level = section.get('level', 2)
                content_html += f'<div class="section">\n    <h{level}>{section["text"]}</h{level}>\n'
                
            elif section_type == 'text':
                content_html += f'    <p>{section["text"]}</p>\n'
                
            elif section_type == 'code':
                language = section.get('language', 'python')
                code_block = self.format_code_block(section["code"], language, code_index)
                content_html += f'    {code_block}\n'
                code_index += 1
                
            elif section_type == 'list':
                items = section.get('items', [])
                content_html += '    <ul>\n'
                for item in items:
                    content_html += f'        <li>{item}</li>\n'
                content_html += '    </ul>\n'
                
            elif section_type == 'faq':
                content_html += f'''    <div class="faq">
        <h3>{section.get("question", "FAQ")}</h3>
        <p>{section.get("answer", "")}</p>
    </div>\n'''
                
            elif section_type == 'section_end':
                content_html += '</div>\n\n'
        
        return content_html

    def add_post(self, 
                 title: str,
                 excerpt: str,
                 content_sections: List[Dict],
                 category_name: str,
                 topics: List[str],
                 author_email: str = "siddartha1192@gmail.com",
                 featured: bool = False,
                 featured_image: str = "",
                 read_time: int = 5,
                 primary_language: str = "python") -> int:
        """
        Add a new post to the database with consistent styling
        
        Args:
            title: Post title
            excerpt: Short description
            content_sections: List of content sections with type and content
            category_name: Category name (will be created if doesn't exist)
            topics: List of topic names
            author_email: Author email (must exist in database)
            featured: Whether post is featured
            featured_image: Path to featured image
            read_time: Estimated read time in minutes
            primary_language: Primary programming language for syntax highlighting
        """
        
        try:
            # Get author ID
            author_id = self.get_author_id(author_email)
            if not author_id:
                raise ValueError(f"Author with email {author_email} not found")
            
            # Create slug
            slug = self.create_slug(title)
            
            # Get or create category
            category_id = self.get_or_create_category(category_name)
            
            # Format content with styling
            formatted_content = self.format_content_with_styling(content_sections)
            full_html = self.css_template.format(
                title=title,
                language=primary_language,
                content=formatted_content
            )
            
            # Insert post
            publish_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            
            self.cursor.execute("""
                INSERT INTO post (title, slug, excerpt, content, publish_date, read_time, 
                                featured, featured_image, category_id, author_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, slug, excerpt, full_html, publish_date, read_time, 
                  featured, featured_image, category_id, author_id))
            
            post_id = self.cursor.lastrowid
            
            # Add topics
            for topic_name in topics:
                topic_id = self.get_or_create_topic(topic_name)
                self.cursor.execute("""
                    INSERT INTO post_topics (post_id, topic_id)
                    VALUES (?, ?)
                """, (post_id, topic_id))
            
            # Commit changes
            self.conn.commit()
            
            print(f"✅ Successfully added post: '{title}' (ID: {post_id})")
            print(f"📂 Category: {category_name}")
            print(f"🏷️ Topics: {', '.join(topics)}")
            
            return post_id
            
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error adding post: {e}")
            raise

    def list_recent_posts(self, limit: int = 5):
        """List recent posts"""
        self.cursor.execute("""
            SELECT p.id, p.title, p.slug, c.name as category, p.publish_date
            FROM post p
            JOIN category c ON p.category_id = c.id
            ORDER BY p.publish_date DESC
            LIMIT ?
        """, (limit,))
        
        posts = self.cursor.fetchall()
        print(f"\n📝 Recent Posts ({len(posts)}):")
        print("-" * 50)
        for post in posts:
            print(f"ID: {post[0]} | {post[1]} | {post[3]} | {post[4][:10]}")

# Example usage and helper functions
def create_sample_post():
    """Example of how to create a post with proper structure"""
    
    content_sections = [
        {
            'type': 'heading',
            'level': 2,
            'text': 'Introduction'
        },
        {
            'type': 'text',
            'text': 'This is a sample blog post demonstrating how to add content to the TechBlog database with consistent styling.'
        },
        {
            'type': 'section_end'
        },
        {
            'type': 'heading',
            'level': 2,
            'text': 'Code Example'
        },
        {
            'type': 'text',
            'text': 'Here\'s a simple Python example:'
        },
        {
            'type': 'code',
            'language': 'python',
            'code': '''def hello_world():
    print("Hello, TechBlog!")
    return True

# Call the function
result = hello_world()'''
        },
        {
            'type': 'section_end'
        },
        {
            'type': 'heading',
            'level': 2,
            'text': 'Key Features'
        },
        {
            'type': 'list',
            'items': [
                'Automatic CSS styling matching existing posts',
                'Code syntax highlighting with copy buttons',
                'Responsive design for mobile devices',
                'SEO-friendly slug generation'
            ]
        },
        {
            'type': 'faq',
            'question': 'Why use this approach?',
            'answer': 'This approach ensures consistency across all blog posts while maintaining the professional styling and functionality of your existing content.'
        },
        {
            'type': 'section_end'
        }
    ]
    
    return content_sections

def main():
    """Main execution function"""
    
    # Initialize the blog updater
    updater = TechBlogUpdater("techblog.db")
    
    try:
        # Connect to database
        updater.connect()
        
        # Example: Add a new post
        sample_content = create_sample_post()
        
        post_id = updater.add_post(
            title="Sample Blog Post with Consistent Styling",
            excerpt="Learn how to add new posts to the TechBlog database while maintaining consistent CSS styling and HTML structure.",
            content_sections=sample_content,
            category_name="Programming",
            topics=["Python", "Database", "Web Development"],
            author_email="siddartha1192@gmail.com",
            featured=False,
            featured_image="/static/images/posts/sample-post.png",
            read_time=7,
            primary_language="python"
        )
        
        # List recent posts
        updater.list_recent_posts()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Always disconnect
        updater.disconnect()

if __name__ == "__main__":
    main()
