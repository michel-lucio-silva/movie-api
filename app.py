from app import create_app
from app.utils import load_csv_to_db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        load_csv_to_db('data/movielist.csv')  # Carregar os dados aqui
    app.run(debug=True)
