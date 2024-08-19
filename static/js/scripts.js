function loadReplies(commentId) {
    var replyContainer = document.getElementById("replies-" + commentId);
    var button = document.getElementById("comment-button-" + commentId);

    if (replyContainer.style.display === "none" || replyContainer.style.display === "") {
        if (replyContainer.innerHTML.trim() === "") {
            fetch(`/dashboard/${commentId}/replies/`)
                .then(response => response.text())
                .then(html => {
                    replyContainer.innerHTML = html;
                    replyContainer.style.display = "block";
                    button.textContent = "Hide replies";
                });
        } else {
            replyContainer.style.display = "block";
            button.textContent = "Hide replies";
        }
    } else {
        replyContainer.style.display = "none";
        button.textContent = `Show replies`;
    }
}
