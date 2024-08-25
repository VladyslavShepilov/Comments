function showReplyForm(replyId) {
    const formContainer = document.getElementById(`reply-form-${replyId}`);
    const formTemplate = document.getElementById("reply-form-template");

    // Toggle form visibility
    if (formContainer.style.display === "none" || !formContainer.style.display) {
        // Clear any existing form and clone the template
        formContainer.innerHTML = "";
        const clonedForm = formTemplate.cloneNode(true);
        clonedForm.style.display = "block";
        clonedForm.id = `reply-form-${replyId}`;

        // Update form action and set the parent ID
        const formElement = clonedForm.querySelector("form");
        formElement.action = "/dashboard/";

        const parentField = formElement.querySelector("input[name='parent']");
        if (parentField) {
            parentField.value = replyId;
        }

        // Append the cloned form to the container
        formContainer.appendChild(clonedForm);
    }

    // Toggle display
    formContainer.style.display = formContainer.style.display === "block" ? "none" : "block";
}

function loadReplies(commentId) {
    const replyContainer = document.getElementById(`replies-${commentId}`);
    const button = document.getElementById(`comment-button-${commentId}`);

    // Toggle reply visibility
    if (replyContainer.style.display === "none" || !replyContainer.style.display) {
        if (!replyContainer.innerHTML.trim()) {
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
        button.textContent = "Show replies";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const fragment = window.location.hash;
    if (fragment) {
        const targetElement = document.querySelector(fragment);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }
});
