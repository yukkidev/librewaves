// consts

const loginModalCloseButton = document.getElementById('closeButton');
const loginModal = document.getElementById('loginModal');
const registerForm = document.getElementById('registration-form');

// events

loginModalCloseButton.addEventListener('click', function() {
	// clear the form

	document.getElementById('username').value = '';
	document.getElementById('password').value = '';

	loginModal.close();
});

loginModal.addEventListener('submit', function(event) {
	event.preventDefault();

	// attempt to login user here

	// if auth failed, send alert and return 

	// else, store token

	// redirect user to dashboard
	window.location.href = "index.html";

});

registerForm.addEventListener('submit', function(event) {
	event.preventDefault(); // Prevent the default form submission behavior

	// attempt to register user here  

	// store token

	// Redirect to the dashboard
	window.location.href = "index.html";
});

// functions

function switchToLoginForm() {
	loginModal.showModal();
}