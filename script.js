const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');

// Create canvas (similar to pygame display)
const canvas = createCanvas(1240, 930);
const ctx = canvas.getContext('2d');

// Load images
let map, rm_601_image, staff_lounge_image;
loadImage('graphics/map_copy.png').then((image) => {
    map = image;
    checkAllImagesLoaded();
});
loadImage('graphics/601.png').then((image) => {
    rm_601_image = image;
    checkAllImagesLoaded();
});
loadImage('graphics/staff_lounge.png').then((image) => {
    staff_lounge_image = image;
    checkAllImagesLoaded();
});

let current_screen = null;
let rm_601_button_rect = { x: 775, y: 400, width: 50, height: 25 };
let staff_lounge_button_rect = { x: 743, y: 268, width: 115, height: 51 };
let back_button_rect = { x: 30, y: 20, width: 100, height: 50 };

// Check if all images are loaded
let imagesLoaded = 0;
function checkAllImagesLoaded() {
    imagesLoaded++;
    if (imagesLoaded === 3) {
        current_screen = map;
        startMainLoop();
    }
}

// Button hover effect
function buttonHoverEffect(buttonRect, mouseX, mouseY) {
    if (mouseX > buttonRect.x && mouseX < buttonRect.x + buttonRect.width &&
        mouseY > buttonRect.y && mouseY < buttonRect.y + buttonRect.height) {
        ctx.fillStyle = '#7FFF7A'; // Hover color
    } else {
        ctx.fillStyle = 'white'; // Default color
    }
    ctx.fillRect(buttonRect.x, buttonRect.y, buttonRect.width, buttonRect.height);
}

// Draw the buttons and screen
function draw() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw current screen (either map or a different image)
    if (current_screen) {
        ctx.drawImage(current_screen, 0, 0, canvas.width, canvas.height);
    }

    // Draw buttons with hover effect
    buttonHoverEffect(rm_601_button_rect, 0, 0); // Replace with actual mouse position for real use
    buttonHoverEffect(staff_lounge_button_rect, 0, 0); // Replace with actual mouse position
    buttonHoverEffect(back_button_rect, 0, 0); // Replace with actual mouse position

    // Draw button text
    ctx.font = '33px Arial';
    ctx.fillStyle = 'black';
    ctx.fillText('601', rm_601_button_rect.x + 10, rm_601_button_rect.y + 17);
    ctx.font = '25px Arial';
    ctx.fillText('Staff Lounge', staff_lounge_button_rect.x + 10, staff_lounge_button_rect.y + 30);
    ctx.fillText('Back', back_button_rect.x + 10, back_button_rect.y + 30);
}

// Event listener for mouse click (simulated here with mock data)
function handleMouseClick(x, y) {
    // Check for button clicks
    if (x > rm_601_button_rect.x && x < rm_601_button_rect.x + rm_601_button_rect.width &&
        y > rm_601_button_rect.y && y < rm_601_button_rect.y + rm_601_button_rect.height) {
        current_screen = rm_601_image;
    } else if (x > staff_lounge_button_rect.x && x < staff_lounge_button_rect.x + staff_lounge_button_rect.width &&
               y > staff_lounge_button_rect.y && y < staff_lounge_button_rect.y + staff_lounge_button_rect.height) {
        current_screen = staff_lounge_image;
    } else if (x > back_button_rect.x && x < back_button_rect.x + back_button_rect.width &&
               y > back_button_rect.y && y < back_button_rect.y + back_button_rect.height) {
        current_screen = map;
    }
    draw(); // Redraw the canvas after a click
}

// Main loop (mocked here as a simple timer for continuous redrawing)
function startMainLoop() {
    setInterval(() => {
        draw();
    }, 1000 / 60); // ~60 FPS
}

// Simulate a mouse click (example: clicking on '601' button at (780, 410))
handleMouseClick(780, 410); // Change these coordinates based on real user interaction

