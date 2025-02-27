<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TCHS Interactive Map</title>
    <style>
        body {
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #99FF99; /* Light Green */
        }
        canvas {
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <canvas id="interactiveMap" width="1240" height="930"></canvas>
    <script>
        const canvas = document.getElementById('interactiveMap');
        const ctx = canvas.getContext('2d');

        // Load images
        const mapImage = new Image();
        mapImage.src = 'graphics/map_copy.png';

        const rm601Image = new Image();
        rm601Image.src = 'graphics/601.png';

        const staffLoungeImage = new Image();
        staffLoungeImage.src = 'graphics/staff_lounge.png';

        // Button locations and sizes
        const rm601Button = { x: 775, y: 400, width: 50, height: 25 };
        const staffLoungeButton = { x: 743, y: 268, width: 115, height: 51 };
        const backButton = { x: 30, y: 20, width: 100, height: 50 };

        // Current screen (map by default)
        let currentScreen = 'map';

        // Text Rendering (for buttons)
        const font = '33px Arial';
        const font1 = '25px Arial';

        function drawButtonHoverEffect(rect, buttonText, fontStyle) {
            const mouseX = event.offsetX;
            const mouseY = event.offsetY;

            if (mouseX > rect.x && mouseX < rect.x + rect.width && mouseY > rect.y && mouseY < rect.y + rect.height) {
                ctx.fillStyle = 'lightgreen';
                ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
            } else {
                ctx.fillStyle = 'white';
                ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
            }

            ctx.strokeStyle = 'white';
            ctx.lineWidth = 2;
            ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);

            ctx.font = fontStyle;
            ctx.fillStyle = 'black';
            ctx.fillText(buttonText, rect.x + rect.width / 2 - ctx.measureText(buttonText).width / 2, rect.y + rect.height / 2 + 10);
        }

        // Button click handler
        canvas.addEventListener('click', (event) => {
            const mouseX = event.offsetX;
            const mouseY = event.offsetY;

            // Check if a button was clicked
            if (mouseX > rm601Button.x && mouseX < rm601Button.x + rm601Button.width &&
                mouseY > rm601Button.y && mouseY < rm601Button.y + rm601Button.height) {
                currentScreen = 'rm601';
            }

            if (mouseX > staffLoungeButton.x && mouseX < staffLoungeButton.x + staffLoungeButton.width &&
                mouseY > staffLoungeButton.y && mouseY < staffLoungeButton.y + staffLoungeButton.height) {
                currentScreen = 'staffLounge';
            }

            if (mouseX > backButton.x && mouseX < backButton.x + backButton.width &&
                mouseY > backButton.y && mouseY < backButton.y + backButton.height) {
                currentScreen = 'map';
            }
        });

        // Main render function
        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

            if (currentScreen === 'map') {
                ctx.drawImage(mapImage, 0, 0);

                // Draw buttons
                drawButtonHoverEffect(rm601Button, '601', font);
                drawButtonHoverEffect(staffLoungeButton, 'Staff Lounge', font1);
            } else if (currentScreen === 'rm601') {
                ctx.drawImage(rm601Image, 0, 0);
                drawButtonHoverEffect(backButton, 'Back', font);
            } else if (currentScreen === 'staffLounge') {
                ctx.drawImage(staffLoungeImage, 0, 0);
                drawButtonHoverEffect(backButton, 'Back', font);
            }

            requestAnimationFrame(render); // Keep rendering
        }

        // Start the render loop once images are loaded
        mapImage.onload = () => {
            render();
        };
    </script>
</body>
</html>
