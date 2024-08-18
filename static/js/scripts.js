function loadReplies(commentId) {
    var replyContainer = document.getElementById('replies-' + commentId);

    // Check if replies are already loaded
    if (replyContainer.innerHTML.trim() === '') {
        fetch(`/comments/${commentId}/replies/`)
            .then(response => response.text())
            .then(html => {
                replyContainer.innerHTML = html;
                replyContainer.style.display = "block";
            });
    } else {
        replyContainer.style.display = replyContainer.style.display === "none" ? "block" : "none";
    }
}
