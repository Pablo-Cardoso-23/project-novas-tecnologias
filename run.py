from app import create_app
# from app.routes import main_bp
from dotenv import load_dotenv

load_dotenv("secrets.env")
app = create_app()

if __name__ == '__main__':

    app.run(debug=True)
