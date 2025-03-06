from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Use PORT from environment variable if available (Render provides this), else default to 10000
    port = int(os.getenv('PORT', 10000))

    # `debug=True` can be removed for production - recommended for local development only
    app.run(host='0.0.0.0', port=port)
