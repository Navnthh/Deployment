document.addEventListener('DOMContentLoaded', function () {
    fetchPosts();
});

function updatePosts(posts) {
    const postsContainer = document.getElementById('posts');
    postsContainer.innerHTML = '';

    posts.forEach(post => {
        const postElement = createPostElement(post);
        postsContainer.appendChild(postElement);
    });
}

function fetchPosts() {
    fetch('/').then(response => response.json())
        .then(data => {
            updatePosts(data.posts);
        });
}

function createPostElement(post) {
    const postElement = document.createElement('div');
    postElement.id = post.id;
    postElement.classList.add('post');

    const titleElement = document.createElement('h2');
    titleElement.innerText = post.title;

    const contentElement = document.createElement('p');
    contentElement.innerText = post.content;

    const actionsElement = document.createElement('div');
    actionsElement.classList.add('post-actions');

    const likeButton = document.createElement('button');
    likeButton.innerText = 'Like (' + post.likes + ')';
    likeButton.addEventListener('click', () => reactToPost(post.id, 'like'));

    const dislikeButton = document.createElement('button');
    dislikeButton.innerText = 'Dislike (' + post.dislikes + ')';
    dislikeButton.addEventListener('click', () => reactToPost(post.id, 'dislike'));

    actionsElement.appendChild(likeButton);
    actionsElement.appendChild(dislikeButton);

    const commentsSection = document.createElement('div');
    commentsSection.classList.add('comments-section');

    const commentContent = document.createElement('textarea');
    commentContent.classList.add('comment-content');
    commentContent.placeholder = 'Write your comment';

    const commentButton = document.createElement('button');
    commentButton.innerText = 'Comment';
    commentButton.addEventListener('click', () => addComment(post.id, commentContent));

    commentsSection.appendChild(commentContent);
    commentsSection.appendChild(commentButton);

    const commentsList = document.createElement('div');
    commentsList.classList.add('comments-list');

    post.replies.forEach(reply => {
        const commentElement = createCommentElement(reply);
        commentsList.appendChild(commentElement);
    });

    postElement.appendChild(titleElement);
    postElement.appendChild(contentElement);
    postElement.appendChild(actionsElement);
    postElement.appendChild(commentsSection);
    postElement.appendChild(commentsList);

    return postElement;
}

function createCommentElement(comment) {
    const commentElement = document.createElement('div');
    commentElement.classList.add('comment');

    const commentContent = document.createElement('p');
    commentContent.innerText = comment.content;

    commentElement.appendChild(commentContent);
    return commentElement;
}

function createPost() {
    const postTitle = document.getElementById('post-title').value;
    const postContent = document.getElementById('post-content').value;

    if (postTitle.trim() !== '' && postContent.trim() !== '') {
        fetch('/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: postTitle, content: postContent })
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchPosts();
                document.getElementById('post-title').value = '';
                document.getElementById('post-content').value = '';
            } else {
                alert('Failed to create post');
            }
        });
    }
}

function reactToPost(postId, reactionType) {
    fetch('/like_dislike', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ post_id: postId, reaction_type: reactionType })
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            
            document.getElementById(postId).querySelector('.post-actions button:first-child').innerText = 'Like (' + data.likes + ')';
            document.getElementById(postId).querySelector('.post-actions button:last-child').innerText = 'Dislike (' + data.dislikes + ')';
        } else {
            alert(data.message);
        }
    });
}

function addComment(postId, commentContentElement) {
    const commentContent = commentContentElement.value.trim();

    if (commentContent !== '') {
        fetch('/comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ post_id: postId, content: commentContent })
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update comments list
                const postElement = document.getElementById(postId);
                if (postElement) {
                    const commentsList = postElement.querySelector('.comments-list');
                    const commentElement = createCommentElement({ content: commentContent });
                    commentsList.appendChild(commentElement);
                } else {
                    console.error('Post element not found.');
                }
            } else {
                alert('Failed to add comment');
            }
        }).catch(error => {
            console.error('Error adding comment:', error);
        });
    }
}

