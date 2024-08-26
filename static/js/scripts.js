function showReplyForm(replyId) {
    const formContainer = document.getElementById(`reply-form-${replyId}`);
    const formTemplate = document.getElementById("reply-form-template");

    if (!formContainer) {
        console.error(`Form container with ID 'reply-form-${replyId}' does not exist.`);
        return;
    }

    const isFormVisible = formContainer.style.display === "block";

    if (!isFormVisible && !formContainer.querySelector("form")) {
        formContainer.innerHTML = "";

        const clonedForm = formTemplate.cloneNode(true);
        clonedForm.id = `reply-form-${replyId}`;
        clonedForm.style.display = "block";
        const formElement = clonedForm.querySelector("form");
        formElement.action = `/dashboard/`;

        const parentField = formElement.querySelector("input[name='parent']");
        if (parentField) {
            parentField.value = replyId;
        }

        formContainer.appendChild(clonedForm);
    }

    formContainer.style.display = isFormVisible ? "none" : "block";
}

document.addEventListener("DOMContentLoaded", function() {
    const fragment = window.location.hash;
    if (fragment) {
        const targetElement = document.querySelector(fragment);
        if (targetElement) {
            targetElement.style.display = "block";
            targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }

    const accessToken = document.querySelector('meta[name="access_token"]')?.content;
    const refreshToken = document.querySelector('meta[name="refresh_token"]')?.content;

    if (accessToken) {
        document.cookie = `access_token=${accessToken}; path=/; secure; HttpOnly`;
    }

    if (refreshToken) {
        document.cookie = `refresh_token=${refreshToken}; path=/; secure; HttpOnly`;
    }
});

async function checkAndRefreshToken() {
    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    };

    const accessToken = getCookie('access_token');
    const refreshToken = getCookie('refresh_token');

    if (!accessToken || !refreshToken) {
        console.error("Tokens are missing, user might need to log in again.");
        window.location.href = "/user/login/";
        return;
    }

    const tokenPayload = JSON.parse(atob(accessToken.split(".")[1]));
    const currentTime = Math.floor(Date.now() / 1000);

    if (tokenPayload.exp < currentTime) {
        const response = await fetch("/api/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `access_token=${data.access}; path=/; secure; HttpOnly`;
        } else {
            console.error("Token refresh failed, redirecting to login.");
            window.location.href = "/user/login/";
        }
    }
}

async function fetchWithAuth(url, options = {}) {
    await checkAndRefreshToken();

    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        console.error("No access token found, redirecting to login.");
        window.location.href = "/user/login/";
        return;
    }

    options.headers = options.headers || {};
    options.headers["Authorization"] = `Bearer ${accessToken}`; // Add JWT token to the header
    options.headers["Content-Type"] = options.headers["Content-Type"] || "application/json";

    return fetch(url, options);
}