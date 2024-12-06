from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'blog_posts.json')


def ensure_json_exists():
    """
    Ensure the JSON file exists. If it doesn't, create it with an empty list.
    """
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'w') as file:
            json.dump([], file)


def load_blog_posts():
    """
    Load blog posts from the JSON file and return them as a list.
    """
    with open(JSON_PATH, 'r') as file:
        return json.load(file)


def save_blog_posts(blog_posts):
    """
    Save the given list of blog posts back to the JSON file.
    """
    with open(JSON_PATH, 'w') as file:
        json.dump(blog_posts, file, indent=4)


def fetch_post_by_id(post_id):
    """
    Fetch a single blog post by its ID.
    """
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


ensure_json_exists()


@app.route('/')
def index():
    """
    Display the list of all blog posts on the homepage.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the creation of a new blog post.
    """
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_blog_posts()

        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)

        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Delete a blog post by its ID.
    """
    blog_posts = load_blog_posts()

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_blog_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update an existing blog post's details.
    """
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        blog_posts = load_blog_posts()
        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    """
    Start the Flask application.
    """
    app.run(host="0.0.0.0", port=5001, debug=True)