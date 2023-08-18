import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

class Player:
    """Class to represent a player's paddle."""
    def __init__(self):
        self.y = 0

class Ball:
    """Class to represent the game ball."""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 1

players = [Player(), Player()]
ball = Ball()

def update_game_state():
    """Update the game state based on ball movement and collisions."""
    ball.x += ball.dx
    ball.y += ball.dy

    # Check and handle collisions with walls and paddles
    if ball.x >= 100 or ball.x <= 0:
        ball.dx = -ball.dx

    for player in players:
        if player.y <= ball.y <= player.y + 10 and ball.dx == -1:
            ball.dy = 1
        elif player.y <= ball.y <= player.y + 10 and ball.dx == 1:
            ball.dy = -1

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: int):
    """WebSocket endpoint to handle player input and ball updates."""
    await websocket.accept()

    try:
        while True:
            # Receive player's paddle position from the WebSocket
            data = await websocket.receive_text()
            players[player_id].y = int(data)
            
            # Update the game state and send ball position back to client
            update_game_state()
            await websocket.send_text(f"{ball.x},{ball.y}")
    except WebSocketDisconnect:
        # Reset player's position on disconnect
        players[player_id].y = 0

@app.get("/", response_class=HTMLResponse)
async def get():
"""GET endpoint to serve the Pong game HTML page."""
    return """
    <html>
        <head>
            <title>Pong</title>
        </head>
        <body>
            <h1>Pong</h1>
            <div>
                <div style="position: absolute; top: 0; left: 0; width: 100px; height: 10px; background-color: red;"></div>
                <div style="position: absolute; top: 0; right: 0; width: 100px; height: 10px; background-color: blue;"></div>
                <div id="ball" style="position: absolute; top: 0; left: 0; width: 10px; height: 10px; background-color: black;"></div>
            </div>
            <script>
                const socket = new WebSocket(`ws://${location.host}/ws/${prompt("Player ID (0 or 1):")}`);
                const ball = document.getElementById("ball");

                // Update ball position based on received WebSocket data
                socket.onmessage = function(event) {
                    const [ballX, ballY] = event.data.split(",");
                    ball.style.transform = `translate(${ballX}px, ${ballY}px)`;
                };

                // Send paddle position when arrow keys are pressed
                window.addEventListener("keydown", (event) => {
                    const y = Number(ball.style.transform.split("(")[1].split("px")[0]) + (event.key === "ArrowUp" ? -10 : 10);
                    socket.send(y.toString());
                });
            </script>
        </body>
    </html>
    """
