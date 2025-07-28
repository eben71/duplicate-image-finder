from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Duplicate Image Finder Frontend")


@app.get("/", response_class=HTMLResponse)
async def welcome_page() -> HTMLResponse:
    return HTMLResponse(
        content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Duplicate Image Finder</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f4f4f9;
            }
            h1 {
                color: #333;
            }
            p {
                color: #666;
                font-size: 1.2em;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Duplicate Image Finder</h1>
        <p>Find and manage duplicate images with ease.</p>
        <p>Backend API is available at <a href="http://localhost:8000/docs">http://localhost:8000/docs</a>.</p>
    </body>
    </html>
    """
    )
