const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
const signupForm = document.querySelector("form.signup");
const signupMessage = document.getElementById("signup-message");
const signinForm = document.querySelector("form.login");
function clearSignupMessage() {
    if (signupMessage) {
        signupMessage.textContent = "";
        signupMessage.removeAttribute("style");
    }
}

signupBtn.onclick = (()=>{
 loginForm.style.marginLeft = "-50%";
 loginText.style.marginLeft = "-50%";
 clearSignupMessage();
});
loginBtn.onclick = (()=>{
 loginForm.style.marginLeft = "0%";
 loginText.style.marginLeft = "0%";
 clearSignupMessage();
});
signupLink.onclick = (()=>{
 signupBtn.click();
 return false;
});




signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(signupForm);
    const data = {
        name: formData.get("username"),
        email: formData.get("email"),
        password: formData.get("password"),
    };

    const res = await fetch("/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    signupMessage.style.padding = "10px";
    signupMessage.style.marginBottom = "10px";
    signupMessage.style.color = "white";

    if (result.success) {
        signupMessage.style.background = "green";
        signupMessage.textContent = result.msg;
        signupForm.reset();
    } else {
        signupMessage.style.background = "red";
        signupMessage.textContent = result.msg || "Error";
        signupForm.reset();
    }
});


signinForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(signinForm);
    const data = {
        name: formData.get("username"),
        password: formData.get("password"),
    };

    const res = await fetch("/api/auth/signin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    signupMessage.style.padding = "10px";
    signupMessage.style.marginBottom = "10px";
    signupMessage.style.color = "white";

    if (result.success) {
        window.location.href = "/api/profile";
        signupForm.reset();
    } else {
        signupMessage.style.background = "red";
        signupMessage.textContent = result.msg || "Error";
    }
});
