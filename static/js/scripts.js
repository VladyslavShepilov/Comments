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


function showReplyForm(replyId) {
    var formId = "reply-form-" + replyId;
    var formContainer = document.getElementById(formId);

    if (formContainer.innerHTML.trim() === "") {
        var formTemplate = document.getElementById("reply-form-template");
        var clonedForm = formTemplate.cloneNode(true);
        clonedForm.style.display = "block";
        clonedForm.id = "";

        var formElement = clonedForm.querySelector("form");
        formElement.action = `/dashboard/`;

        var parentField = formElement.querySelector("input[name='parent']");
        if (parentField) {
            parentField.value = replyId;
        }

        formContainer.appendChild(clonedForm);
    }

    formContainer.style.display = (formContainer.style.display === "none" || formContainer.style.display === "") ? "block" : "none";
}
