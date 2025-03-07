from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Use PORT from environment variable if available (for Render, Fly.io, etc.), default to 10000 for local dev
    port = int(os.getenv('PORT', 10000))

    # Important: Set debug=False by default to avoid accidental debug mode in production
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    app.run(host='0.0.0.0', port=port, debug=debug)
