function loadReplies(commentId) {
    var replyContainer = document.getElementById("replies-" + commentId);

    if (replyContainer.innerHTML.trim() === "") {
        fetch(`/dashboard/${commentId}/replies/`)
            .then(response => response.text())
            .then(html => {
                replyContainer.innerHTML = html;
                replyContainer.style.display = "block";
            });
    } else {
        replyContainer.style.display = replyContainer.style.display === "none" ? "block" : "none";
    }
}
