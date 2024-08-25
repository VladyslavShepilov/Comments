function showReplyForm(replyId) {
    var formId = "reply-form-" + replyId;
    var formContainer = document.getElementById(formId);

    if (!formContainer || formContainer.style.display === "none") {
        var formTemplate = document.getElementById("reply-form-template");
        var clonedForm = formTemplate.cloneNode(true);
        clonedForm.style.display = "block";
        clonedForm.id = formId;

        var formElement = clonedForm.querySelector("form");
        formElement.action = `/dashboard/`;

        var parentField = formElement.querySelector("input[name='parent']");
        if (parentField) {
            parentField.value = replyId;
        }

        if (formContainer) {
            formContainer.innerHTML = "";
            formContainer.appendChild(clonedForm);
        } else {
            var newFormContainer = document.createElement("div");
            newFormContainer.id = formId;
            newFormContainer.style.display = "block";
            newFormContainer.appendChild(clonedForm);
            document.getElementById("comment-" + replyId).appendChild(newFormContainer);
        }
    }

    formContainer.style.display = (formContainer.style.display === "none" || formContainer.style.display === "") ? "block" : "none";
}

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
        button.textContent = "Show replies";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var fragment = "{{ fragment_identifier }}";
    if (fragment) {
        var element = document.getElementById(fragment);

        if (!element && fragment.includes("reply-form")) {
            var parentCommentId = fragment.replace("reply-form-", "");
            loadReplies(parentCommentId);
            element = document.getElementById(fragment);
        }

        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    }
});
