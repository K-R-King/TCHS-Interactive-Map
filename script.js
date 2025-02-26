// JavaScript interactive map conversion

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
    "staff_lounge": "graphics/staff_lounge.png",
    "rm_216": "graphics/214.png",
    "rm_215": "graphics/214.png"

    // Add remaining rooms here
};

const loadedImages = {};
for (let key in images) {
    loadedImages[key] = new Image();
    loadedImages[key].src = images[key];
}

// Draw initial map
mapImage.onload = () => {
    ctx.drawImage(mapImage, 0, 0, canvas.width, canvas.height);
};

// Interactive button areas
const buttons = [
    { x: 775, y: 400, width: 50, height: 25, room: "rm_601" },
    { x: 743, y: 268, width: 115, height: 51, room: "staff_lounge" },
    { x: 847, y: 655, width: 50, height: 25, room: "rm_216" },
    { x: 904, y: 655, width: 50, height: 25, room: "rm_215" }
    // Add more button coordinates here
];

// Handle click events
canvas.addEventListener("click", (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    for (let button of buttons) {
        if (
            x >= button.x &&
            x <= button.x + button.width &&
            y >= button.y &&
            y <= button.y + button.height
        ) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(loadedImages[button.room], 0, 0, canvas.width, canvas.height);
            break;
        }
    }
});
