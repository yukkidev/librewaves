const API_URL = 'http://127.0.0.1:5000';

const loginModalCloseButton = document.getElementById('closeButton');
const loginModal = document.getElementById('loginModal');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registration-form');

loginModalCloseButton.addEventListener('click', function() {
	document.getElementById('username').value = '';
	document.getElementById('password').value = '';
	loginModal.close();
});

loginForm.addEventListener('submit', function(event) {
	event.preventDefault();

	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;

	fetch(`${API_URL}/login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ username, password })
	})
		.then(response => response.json())
		.then(data => {
			if (data.error) {
				alert(data.error || data.message);
				return;
			}
			localStorage.setItem('username', username);
			window.location.href = "index.html";
		})
		.catch(error => {
			console.error('Login error:', error);
			alert('Login failed. Please try again.');
		});
});

registerForm.addEventListener('submit', function(event) {
	event.preventDefault();

	const formData = new FormData(registerForm);

	fetch(`${API_URL}/register`, {
		method: 'POST',
		body: formData
	})
		.then(response => response.json())
		.then(data => {
			if (data.error) {
				alert(data.error);
				return;
			}
			alert('Registration successful! Please login.');
			loginModal.showModal();
		})
		.catch(error => {
			console.error('Registration error:', error);
			alert('Registration failed. Please try again.');
		});
});

function switchToLoginForm() {
	loginModal.showModal();
}
