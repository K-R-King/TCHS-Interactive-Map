// This code is a translation from Python Pygame to JavaScript using a hypothetical Pygame-like library in JavaScript.

import { createCanvas, loadImage, font, drawRect, updateDisplay } from 'pygame-like-library'; // Hypothetical library

// Initialize Pygame
const canvas = createCanvas(1240, 930);
const context = canvas.getContext('2d');
const clock = setInterval(() => {}, 1000 / 60); // 60 FPS

// Load map
let mapImage = loadImage('graphics/map_copy.png');

// Load images of school
// Red
let rm601Image = loadImage('graphics/601.png');
let staffLoungeImage = loadImage('graphics/staff_lounge.png');

// Create current screen variable
let currentScreen = mapImage;

// Create font objects
// Red
let defaultFont33 = font('Arial', 33);
let defaultFont25 = font('Arial', 25);
// Red
// Purple
let purpleFont30 = font('Arial', 30);
let purpleFont20 = font('Arial', 20);
// Purple
// Green
let greenFont20 = font('Arial', 20);
let smallGreenFont15 = font('Arial', 15);
// Green
// Yellow
let yellowFont30 = font('Arial', 30);
let yellowFont20 = font('Arial', 20);
// Yellow
// Blue
let blueFont25 = font('Arial', 25);
let senateRoomFont16 = font('Arial', 16);
// Blue
// Orange
let orangeFont13 = font('Arial', 13);
let defaultFont30 = font('Arial', 30);
let defaultFont20 = font('Arial', 20);
let defaultFont18 = font('Arial', 18);
let defaultFont27 = font('Arial', 27);
let nurseFont28 = font('Arial', 28); // ToBeUpdated by Orange - 'size' as applicable
let rgrFont28 = font('Arial', 28); // ToBeUpdated by Orange - 'size' as applicable
// Orange

// Create surfaces for buttons
// Red
let rm601ButtonSurface = createSurface(50, 25);
let staffLoungeButtonSurface = createSurface(115, 51);

// Back
let backButtonSurface = createSurface(100, 50);
// Back

// Render text on the buttons
// Red
let rm601Text = defaultFont33.render("601", true, (0, 0, 0));
let rm601TextRect = rm601Text.getRect(
  (rm601ButtonSurface.width / 2), (rm601ButtonSurface.height / 2)
);

let staffLoungeText = defaultFont25.render("Staff Lounge", true, (0, 0, 0));
let staffLoungeTextRect = staffLoungeText.getRect(
  (staffLoungeButtonSurface.width / 2), (staffLoungeButtonSurface.height / 2)
);

// Back
let backButtonText = defaultFont33.render("Back", true, (0, 0, 0));
let backButtonRect = backButtonText.getRect(
  (backButtonSurface.width / 2), (backButtonSurface.height / 2)
);
// Back

// Create button boundaries
// Red
let rm601ButtonRect = { x: 775, y: 400, width: 50, height: 25 };
let staffLoungeButtonRect = { x: 743, y: 268, width: 115, height: 51 };

// Back
let backButtonRect = { x: 30, y: 20, width: 100, height: 50 };
// Back

// Create button hover effect function
function buttonHoverEffect(buttonRect, buttonSurface) {
  if (mouseOver(buttonRect)) {
    drawRect(buttonSurface, (127, 255, 212), 1, 1, 148, 48);
  } else {
    drawRect(buttonSurface, (255, 255, 255), 0, 0, 150, 50);
    drawRect(buttonSurface, (255, 255, 255), 1, 1, 148, 48);
    drawRect(buttonSurface, (255, 255, 255), 1, 1, 148, 1);
    drawRect(buttonSurface, (255, 255, 255), 1, 48, 148, 10);
  }
}

// Start the main loop
function mainLoop() {
  // Fill the display with color
  context.fillStyle = 'rgb(155, 255, 155)';
  context.fillRect(0, 0, canvas.width, canvas.height);

  // Handle events
  handleEvents();

  // Check if the mouse is over the button
  buttonHoverEffect(rm601ButtonRect, rm601ButtonSurface);
  buttonHoverEffect(staffLoungeButtonRect, staffLoungeButtonSurface);
  buttonHoverEffect(backButtonRect, backButtonSurface);

  // Show the button text
  rm601ButtonSurface.blit(rm601Text, rm601TextRect);
  staffLoungeButtonSurface.blit(staffLoungeText, staffLoungeTextRect);
  backButtonSurface.blit(backButtonText, backButtonRect);

  // Draw the map and buttons on the screen
  if (currentScreen === mapImage) {
    context.drawImage(currentScreen, 0, 0); // controls test_surface location
    context.drawImage(rm601ButtonSurface, rm601ButtonRect.x, rm601ButtonRect.y);
    context.drawImage(staffLoungeButtonSurface, staffLoungeButtonRect.x, staffLoungeButtonRect.y);
  } else {
    context.drawImage(currentScreen, 0, 0);
    context.drawImage(backButtonSurface, backButtonRect.x, backButtonRect.y);
  }

  // Update the game state
  updateDisplay();
}

// Run the main loop
setInterval(mainLoop, 1000 / 60); // 60 FPS
