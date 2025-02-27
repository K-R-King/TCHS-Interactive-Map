// Get canvas context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Load images
const map = new Image();
map.src = 'graphics/map_copy.png';
const rm_601_image = new Image();
rm_601_image.src = 'graphics/601.png';
const staff_lounge_image = new Image();
staff_lounge_image.src = 'graphics/staff_lounge.png';

// Button objects
const rm_601_button = { x: 775, y: 400, width: 50, height: 25 };
const staff_lounge_button = { x: 743, y: 268, width: 115, height: 51 };
const back_button = { x: 30, y: 20, width: 100, height: 50 };

// Font definitions
const font = '33px Arial';
const font1 = '25px Arial';
const font2 = '30px Arial';
const font3 = '20px Arial';

// Variables to track the current screen
let currentScreen = map;

// Event listeners
canvas.addEventListener('click', handleMouseClick);

// Handle mouse clicks to switch between images and go back
function handleMouseClick(event) {
    const mouseX = event.offsetX;
    const mouseY = event.offsetY;

    console.log('Mouse Clicked at:', mouseX, mouseY); // Debugging line to see the mouse click coordinates

    // Button click logic
    if (isButtonClicked(mouseX, mouseY, rm_601_button)) {
        currentScreen = rm_601_image;
        console.log("Switched to RM 601");
    } else if (isButtonClicked(mouseX, mouseY, staff_lounge_button)) {
        currentScreen = staff_lounge_image;
        console.log("Switched to Staff Lounge");
    } else if (isButtonClicked(mouseX, mouseY, back_button)) {
        currentScreen = map;
        console.log("Back button clicked - Switched to Map");
    }
}

// Check if mouse click is inside a button's area
function isButtonClicked(x, y, button) {
    return x >= button.x && x <= button.x + button.width && y >= button.y && y <= button.y + button.height;
}

// Draw the buttons
function drawButton(button, text, font, color) {
    ctx.fillStyle = color;
    ctx.fillRect(button.x, button.y, button.width, button.height);
    ctx.fillStyle = 'black';
    ctx.font = font;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, button.x + button.width / 2, button.y + button.height / 2);
}

// Main game loop
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the current screen
    ctx.drawImage(currentScreen, 0, 0);

    // Draw buttons
    drawButton(rm_601_button, '601', font, '#ffffff');
    drawButton(staff_lounge_button, 'Staff Lounge', font1, '#ffffff');
    drawButton(back_button, 'Back', font2, '#ffffff');

    requestAnimationFrame(gameLoop);
}

// Start the game loop when images are loaded
map.onload = function () {
    gameLoop();
};
rm_601_image.onload = function () {};
staff_lounge_image.onload = function () {};
