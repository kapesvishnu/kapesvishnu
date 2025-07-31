const canvas = document.getElementById('cricketCanvas');
const ctx = canvas.getContext('2d');

// Game objects
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 10,
    dx: 2,
    dy: -2
};

const batsman = {
    x: canvas.width / 2 - 50,
    y: canvas.height - 150,
    width: 100,
    height: 20
};

// Draw functions
function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = '#FF0000';
    ctx.fill();
    ctx.closePath();
}

function drawBatsman() {
    ctx.beginPath();
    ctx.rect(batsman.x, batsman.y, batsman.width, batsman.height);
    ctx.fillStyle = '#0000FF';
    ctx.fill();
    ctx.closePath();
}

function drawStumps() {
    ctx.fillStyle = '#FFFF00';
    ctx.fillRect(canvas.width / 2 - 5, canvas.height - 100, 10, 50);
}

// Game logic
function update() {
    // Move the ball
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Wall collision (top/bottom)
    if (ball.y + ball.dy > canvas.height - ball.radius || ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    }

    // Wall collision (left/right)
    if (ball.x + ball.dx > canvas.width - ball.radius || ball.x + ball.dx < ball.radius) {
        ball.dx = -ball.dx;
    }

    // Bat collision
    if (
        ball.x > batsman.x &&
        ball.x < batsman.x + batsman.width &&
        ball.y + ball.radius > batsman.y &&
        ball.y < batsman.y + batsman.height
    ) {
        ball.dy = -ball.dy;
    }
}

function draw() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the pitch
    ctx.fillStyle = '#4CAF50';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    drawStumps();
    drawBall();
    drawBatsman();
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// Mouse controls
document.addEventListener('mousemove', (e) => {
    const relativeX = e.clientX - canvas.offsetLeft;
    if (relativeX > 0 && relativeX < canvas.width) {
        batsman.x = relativeX - batsman.width / 2;
    }
});

// Start the game loop
gameLoop();
