// const canvas = document.getElementById("waveCanvas");
// const ctx = canvas.getContext("2d");

// // Wave properties
// let amplitude = 70; // Base amplitude of the waves
// const variation = 0; // Amplitude variation
// const frequency = 0.015; // Controls the number of waves
// const speed = 0.02; // Controls the speed of the waves
// let time = 0;

// function resizeCanvas() {
//   // Set canvas size
//   canvas.width = window.innerWidth;
//   canvas.height = window.innerHeight;

//   // Adjust amplitude based on the new canvas height
//   amplitude = Math.min(amplitude, canvas.height / 2);
// }

// function drawWave() {
//   // Clear the canvas
//   ctx.clearRect(0, 0, canvas.width, canvas.height);

//   // Loop through each pixel on the x-axis
//   for (let x = 0; x < canvas.width; x++) {
//     // Calculate the corresponding y position
//     const y = canvas.height / 2 + Math.sin(x * frequency + time) * (amplitude + Math.random() * variation);

//     // Draw a line segment at the current x, y position
//     ctx.beginPath();
//     ctx.moveTo(x, y);
//     ctx.lineTo(x, canvas.height);
//     ctx.strokeStyle = "#45364B";
//     ctx.stroke();
//   }

//   // Update time for animation
//   time += speed;

//   // Call the drawWave function recursively
//   requestAnimationFrame(drawWave);
// }

// // Initialize the canvas and start the animation
// resizeCanvas();
// drawWave();

// // Handle window resizing
// window.addEventListener("resize", () => {
//   // Clear the canvas and restart the animation on resize
//   ctx.clearRect(0, 0, canvas.width, canvas.height);
//   resizeCanvas();
//   drawWave();
// });
