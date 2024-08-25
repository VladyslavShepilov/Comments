function showReplyForm(replyId) {
    const formContainer = document.getElementById(`reply-form-${replyId}`);
    const formTemplate = document.getElementById("reply-form-template");

    if (!formContainer) {
        console.error(`Form container with ID 'reply-form-${replyId}' does not exist.`);
        return;
    }

    // Check if the form is already visible
    const isFormVisible = formContainer.style.display === "block";

    // If the form is not visible and no form exists in the container, clone and append the form template
    if (!isFormVisible && !formContainer.querySelector("form")) {
        // Clear any existing content
        formContainer.innerHTML = "";

        // Clone the form template and set its properties
        const clonedForm = formTemplate.cloneNode(true);
        clonedForm.id = `reply-form-${replyId}`;
        clonedForm.style.display = "block"; // Make sure the form is visible

        // Update the form action URL
        const formElement = clonedForm.querySelector("form");
        formElement.action = `/dashboard/`;

        // Set the parent ID in the form
        const parentField = formElement.querySelector("input[name='parent']");
        if (parentField) {
            parentField.value = replyId;
        }

        // Append the cloned form to the container
        formContainer.appendChild(clonedForm);
    }

    // Toggle the display of the form container
    formContainer.style.display = isFormVisible ? "none" : "block";
}

// Ensure the form scrolls into view if a hash is present in the URL
document.addEventListener("DOMContentLoaded", function() {
    const fragment = window.location.hash;
    if (fragment) {
        const targetElement = document.querySelector(fragment);
        if (targetElement) {
            targetElement.style.display = "block"; // Ensure the target element is visible
            targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }
});
