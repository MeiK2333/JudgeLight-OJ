from app import create_app
from config import CONFIG

app = create_app(CONFIG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
