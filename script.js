// Set up the canvas and context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Load images
const mapImage = new Image();
mapImage.src = 'graphics/map_copy.png';

const rm601Image = new Image();
rm601Image.src = 'graphics/601.png';

const staffLoungeImage = new Image();
staffLoungeImage.src = 'graphics/staff_lounge.png';

// Button objects (coordinates and sizes)
const rm601Button = { x: 775, y: 400, width: 50, height: 25 };
const staffLoungeButton = { x: 743, y: 268, width: 115, height: 51 };
const backButton = { x: 30, y: 20, width: 100, height: 50 };

// Current screen state
let currentScreen = mapImage;

// Font settings
const font = '33px Arial';
const font1 = '25px Arial';
const font2 = '30px Arial';

// Event listener for mouse clicks
canvas.addEventListener('click', (event) => {
    const mouseX = event.offsetX;
    const mouseY = event.offsetY;

    // Check if a button is clicked
    if (isButtonClicked(mouseX, mouseY, rm601Button)) {
        currentScreen = rm601Image; // Switch to 601 image
    } else if (isButtonClicked(mouseX, mouseY, staffLoungeButton)) {
        currentScreen = staffLoungeImage; // Switch to Staff Lounge image
    } else if (isButtonClicked(mouseX, mouseY, backButton)) {
        currentScreen = mapImage; // Go back to map
    }
});

// Function to check if a button is clicked
function isButtonClicked(x, y, button) {
    return x >= button.x && x <= button.x + button.width && y >= button.y && y <= button.y + button.height;
}

// Draw a button on the canvas
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
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    // Draw the current screen (image)
    ctx.drawImage(currentScreen, 0, 0);

    // Draw buttons
    drawButton(rm601Button, '601', font, '#ffffff');
    drawButton(staffLoungeButton, 'Staff Lounge', font1, '#ffffff');
    drawButton(backButton, 'Back', font2, '#ffffff');

    requestAnimationFrame(gameLoop); // Continue the loop
}

// Start the game loop once images are loaded
mapImage.onload = function () {
    gameLoop(); // Start the game loop after the map is loaded
};
rm601Image.onload = function () {};
staffLoungeImage.onload = function () {};
