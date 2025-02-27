// Pygame to JavaScript translation

// Initialize Pygame
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
document.body.appendChild(canvas);

const clock = { tick: (fps) => setTimeout(() => {}, 1000 / fps) };

// Create a Pygame window
canvas.width = 1240;
canvas.height = 930;
document.title = 'TCHS Interactive Map';

// Load map
const mapImage = new Image();
mapImage.src = 'graphics/map_copy.png';

// Load images of school
// Red
const rm601Image = new Image();
rm601Image.src = 'graphics/601.png';
const staffLoungeImage = new Image();
staffLoungeImage.src = 'graphics/staff_lounge.png';

// Create current screen variable
let currentScreen = mapImage;

// Create a font object
// Red
const fontRegular33 = '33px Arial';
const fontRegular25 = '25px Arial';
// Purple
const fontPurple30 = '30px Arial';
const fontPurple20 = '20px Arial';
// Green
const fontGreen20 = '20px Arial';
const fontGreen15 = '15px Arial';
// Yellow
const fontYellow30 = '30px Arial';
const fontYellow20 = '20px Arial';
// Blue
const fontBlue25 = '25px Arial';
const fontBlue16 = '16px Arial';
// Orange
const fontOrange13 = '13px Arial';
const fontOrange30 = '30px Arial';
const fontOrange20 = '20px Arial';
const fontOrange18 = '18px Arial';
const fontOrange27 = '27px Arial';
const fontNurse28 = '28px Arial';
const fontRgr28 = '28px Arial';

// Create a surface for the button
// Red
const rm601ButtonSurface = { width: 50, height: 25 };
const staffLoungeButtonSurface = { width: 115, height: 51 };

// Back
const backButtonSurface = { width: 100, height: 50 };

// Render text on the button
// Red
const rm601Text = '601';
const rm601TextRect = { x: rm601ButtonSurface.width / 2, y: rm601ButtonSurface.height / 2 };

const staffLoungeText = 'Staff Lounge';
const staffLoungeTextRect = { x: staffLoungeButtonSurface.width / 2, y: staffLoungeButtonSurface.height / 2 };

//Back
const backButtonText = 'Back';
const backButtonRect = { x: backButtonSurface.width / 2, y: backButtonSurface.height / 2 };

// Create button boundaries
// Red
const rm601ButtonRect = { x: 775, y: 400, width: 50, height: 25 };
const staffLoungeButtonRect = { x: 743, y: 268, width: 115, height: 51 };

//Back
const backButtonRectBoundary = { x: 30, y: 20, width: 100, height: 50 };

// Create button hover effect function
function buttonHoverEffect(buttonRect, buttonSurface) {
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    if (mouseX >= buttonRect.x && mouseX <= buttonRect.x + buttonRect.width &&
        mouseY >= buttonRect.y && mouseY <= buttonRect.y + buttonRect.height) {
        context.fillStyle = 'rgba(127, 255, 212, 1)';
        context.fillRect(buttonRect.x, buttonRect.y, buttonRect.width, buttonRect.height);
    } else {
        context.fillStyle = 'white';
        context.fillRect(buttonRect.x, buttonRect.y, buttonRect.width, buttonRect.height);
    }
}

// Start the main loop
function mainLoop() {
    // Set the frame rate
    clock.tick(60);

    // Fill the display with color
    context.fillStyle = 'rgba(155, 255, 155, 1)';
    context.fillRect(0, 0, canvas.width, canvas.height);

    // Get events from the event queue
    window.addEventListener('click', function (event) {
        // Check for the mouse button down event
        if (event.button === 0) {
            // Red
            if (mouseX >= rm601ButtonRect.x && mouseX <= rm601ButtonRect.x + rm601ButtonRect.width &&
                mouseY >= rm601ButtonRect.y && mouseY <= rm601ButtonRect.y + rm601ButtonRect.height) {
                currentScreen = rm601Image;
            } else if (mouseX >= staffLoungeButtonRect.x && mouseX <= staffLoungeButtonRect.x + staffLoungeButtonRect.width &&
                mouseY >= staffLoungeButtonRect.y && mouseY <= staffLoungeButtonRect.y + staffLoungeButtonRect.height) {
                currentScreen = staffLoungeImage;
            } else if (mouseX >= backButtonRectBoundary.x && mouseX <= backButtonRectBoundary.x + backButtonRectBoundary.width &&
                mouseY >= backButtonRectBoundary.y && mouseY <= backButtonRectBoundary.y + backButtonRectBoundary.height) {
                currentScreen = mapImage;
            }
        }
    });

    // Check if the mouse is over the button. This will create the button hover effect
    // Red
    buttonHoverEffect(rm601ButtonRect, rm601ButtonSurface);
    buttonHoverEffect(staffLoungeButtonRect, staffLoungeButtonSurface);

    // Back
    buttonHoverEffect(backButtonRectBoundary, backButtonSurface);
    // Back

    // Draw the map and button on the screen
    if (currentScreen === mapImage) {
        context.drawImage(currentScreen, 0, 0);  // controls test_surface location
        // Red
        context.fillText(rm601Text, rm601ButtonRect.x + rm601TextRect.x, rm601ButtonRect.y + rm601TextRect.y);
        context.fillText(staffLoungeText, staffLoungeButtonRect.x + staffLoungeTextRect.x, staffLoungeButtonRect.y + staffLoungeTextRect.y);
    } else {
        context.drawImage(currentScreen, 0, 0);
        // Back
        context.fillText(backButtonText, backButtonRectBoundary.x + backButtonRect.x, backButtonRectBoundary.y + backButtonRect.y);
        // Back
    }

    // Update the game state
    requestAnimationFrame(mainLoop);
}

mainLoop();
