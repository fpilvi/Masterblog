from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_blog_posts():
    """
    Load the blog posts from the JSON file and return them as a list.
    This function reads the 'blog_posts.json' file and loads the blog posts into memory.
    """
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_blog_posts(blog_posts):
    """
    Save the given list of blog posts back to the JSON file.
    This function writes the blog posts into the 'blog_posts.json' file, formatting them as
    indented JSON for better readability.
    """
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)


def fetch_post_by_id(post_id):
    """
    Fetch a single blog post by its ID.
    This function looks through all blog posts in the JSON file and returns the one
    that matches the provided post_id. If no post is found, it returns None.
    return a dict or None: The post dictionary if found, otherwise None.
    """
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    """
    Display the list of all blog posts on the homepage.
    The rendered 'index.html' template with the blog posts.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the creation of a new blog post.
    Redirects to the homepage after adding a new post.
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

    This route deletes a blog post from the JSON file. After the
    post is deleted, the page is redirected to the homepage.

    """
    blog_posts = load_blog_posts()

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_blog_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update an existing blog post's details.

    This route displays a form pre-filled with the current details of a blog post (via GET request)
    and updates the blog post when the form is submitted (via POST request). After updating, the
    page is redirected to the homepage.

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
    This block will run the Flask application.
    """
    app.run(host="0.0.0.0", port=5000, debug=True)