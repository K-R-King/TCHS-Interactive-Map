// Create Canvas and Context
const canvas = document.createElement("canvas");
canvas.width = 1240;
canvas.height = 930;
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");

// Load map image
const mapImage = new Image();
mapImage.src = "graphics/map_copy.png";

// Load room images
const images = {
    "rm_601": "graphics/601.png",
    "staff_lounge": "graphics/staff_lounge.png"
};

const loadedImages = {};
let currentScreen = mapImage;

for (let key in images) {
    loadedImages[key] = new Image();
    loadedImages[key].src = images[key];
}

// Interactive button areas
const buttons = [
    { x: 775, y: 400, width: 50, height: 25, room: "rm_601", label: "601" },
    { x: 743, y: 268, width: 115, height: 51, room: "staff_lounge", label: "Staff Lounge" },
    { x: 30, y: 20, width: 100, height: 50, room: "back", label: "Back" }
];

// Draw initial map
document.addEventListener("DOMContentLoaded", () => {
    mapImage.onload = () => {
        ctx.drawImage(mapImage, 0, 0, canvas.width, canvas.height);
        drawButtons();
    };
});

// Draw buttons with hover effect
function drawButtons() {
    buttons.forEach(button => {
        ctx.fillStyle = isHovering(button) ? "#7FFFD4" : "#FFFFFF";
        ctx.fillRect(button.x, button.y, button.width, button.height);
        ctx.strokeStyle = "black";
        ctx.strokeRect(button.x, button.y, button.width, button.height);
        
        ctx.fillStyle = "black";
        ctx.font = "20px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(button.label, button.x + button.width / 2, button.y + button.height / 2);
    });
}

// Handle click events
canvas.addEventListener("click", (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    buttons.forEach(button => {
        if (x >= button.x && x <= button.x + button.width && y >= button.y && y <= button.y + button.height) {
            if (button.room === "back") {
                currentScreen = mapImage;
            } else {
                currentScreen = loadedImages[button.room];
            }
            redraw();
        }
    });
});

// Check if mouse is hovering over a button
function isHovering(button) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    return x >= button.x && x <= button.x + button.width && y >= button.y && y <= button.y + button.height;
}

// Handle mouse movement for hover effect
canvas.addEventListener("mousemove", () => redraw());

// Redraw screen with current map and buttons
function redraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(currentScreen, 0, 0, canvas.width, canvas.height);
    if (currentScreen === mapImage) {
        drawButtons();
    } else {
        drawButtons(); // Draw back button only
    }
}
