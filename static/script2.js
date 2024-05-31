document.addEventListener('DOMContentLoaded', function () {
    fetchAndDisplayPosts("newest"); // Default sorting order
});

function changeSortOrder(order) {
    fetchAndDisplayPosts(order);
}

function fetchAndDisplayPosts(order) {
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sort_order: order })
    })
    .then(response => response.json())
    .then(data => {
        updatePosts(data.posts);
    })
    .catch(error => {
        console.error('Error fetching and displaying posts:', error);
    });
}

function updatePosts(posts) {
    const postsContainer = document.getElementById('posts');
    postsContainer.innerHTML = '';

    posts.forEach(post => {
        const postElement = createPostElement(post);
        postsContainer.appendChild(postElement);
    });
}

function createPostElement(post) {
    const postElement = document.createElement('div');
    postElement.id = post.id;
    postElement.classList.add('post');

    const titleElement = createElement('h2', post.title);
    const contentElement = createElement('p', post.content);
    const actionsElement = createActionsElement(post);
    const commentsSection = createCommentsSection(post);

    postElement.appendChild(titleElement);
    postElement.appendChild(contentElement);
    postElement.appendChild(actionsElement);
    postElement.appendChild(commentsSection);

    return postElement;
}

function createElement(tag, text) {
    const element = document.createElement(tag);
    element.innerText = text;
    return element;
}

function createActionsElement(post) {
    const actionsElement = document.createElement('div');
    actionsElement.classList.add('post-actions');

    const likeButton = createReactionButton(post.id, 'like', post.likes);
    const dislikeButton = createReactionButton(post.id, 'dislike', post.dislikes);

    actionsElement.appendChild(likeButton);
    actionsElement.appendChild(dislikeButton);

    return actionsElement;
}

function createCommentsSection(post) {
    const commentsSection = document.createElement('div');
    commentsSection.classList.add('comments-section');

    const commentContent = document.createElement('textarea');
    commentContent.classList.add('comment-content');
    commentContent.placeholder = 'Write your comment';

    const commentButton = document.createElement('button');
    commentButton.innerText = 'Comment';
    commentButton.addEventListener('click', () => addComment(post.id, commentContent));

    const commentsList = createCommentsList(post.replies);

    commentsSection.appendChild(commentContent);
    commentsSection.appendChild(commentButton);
    commentsSection.appendChild(commentsList);

    return commentsSection;
}

function createCommentsList(replies) {
    const commentsList = document.createElement('div');
    commentsList.classList.add('comments-list');

    if (replies) {
        replies.forEach(reply => {
            const commentElement = createCommentElement(reply);
            commentsList.appendChild(commentElement);
        });
    }

    return commentsList;
}

function createCommentElement(comment) {
    const commentElement = document.createElement('div');
    commentElement.classList.add('comment');

    const commentContent = createElement('p', comment.content);
    commentElement.appendChild(commentContent);

    return commentElement;
}

function createReactionButton(postId, reactionType, count) {
    const button = document.createElement('button');
    button.innerText = `${capitalizeFirstLetter(reactionType)} (${count})`;
    button.addEventListener('click', () => reactToPost(postId, reactionType));
    return button;
}

function reactToPost(postId, reactionType) {
    fetch('/like_dislike', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ post_id: postId, reaction_type: reactionType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const updatedPost = data.post;
            updateReactionButton(postId, 'like', updatedPost.likes);
            updateReactionButton(postId, 'dislike', updatedPost.dislikes);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error reacting to post:', error);
    });
}

function updateReactionButton(postId, reactionType, count) {
    const postElement = document.getElementById(postId);
    const button = postElement.querySelector(`.post-actions button:contains("${capitalizeFirstLetter(reactionType)}")`);

    if (button) {
        button.innerText = `${capitalizeFirstLetter(reactionType)} (${count})`;
    }
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
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const commentsList = document.querySelector(`#${postId} .comments-list`);
                const commentElement = createCommentElement({ content: commentContent });
                commentsList.appendChild(commentElement);

                // Clear the textarea
                commentContentElement.value = '';
            } else {
                alert('Failed to add comment');
            }
        })
        .catch(error => {
            console.error('Error adding comment:', error);
        });
    }
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function createPost() {
    // Get post title and content from input fields
    const title = document.getElementById('post-title').value;
    const content = document.getElementById('post-content').value;

    // Create a JSON object with the post data
    const postData = {
        title: title,
        content: content
    };

    // Send a POST request to the server
    fetch('/post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data (JSON) here
        console.log(data);
    })
    .catch(error => {
        console.error('Error creating post:', error);
    });
}
