from flask import Flask
from app.models import db
from app.routes import api
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app


import pandas as pd
from app.models import db, Movie


def load_csv_to_db(csv_path):
    try:
        # Usar uma abordagem para ignorar linhas problemáticas
        data = pd.read_csv(csv_path, sep=';', engine='python', on_bad_lines='skip')
    except pd.errors.ParserError as e:
        print(f"Erro ao processar o arquivo CSV: {e}")
        return

    # Verificar se as colunas esperadas estão presentes
    required_columns = {'year', 'title', 'studios', 'producers', 'winner'}
    if not required_columns.issubset(data.columns):
        print(f"Colunas ausentes no arquivo CSV. Esperado: {required_columns}")
        return

    # Corrigir possíveis problemas de valores nulos ou tipos de dados
    data = data.dropna(subset=['year', 'title', 'studios', 'producers', 'winner'])
    data['year'] = pd.to_numeric(data['year'], errors='coerce')
    data = data.dropna(subset=['year'])
    data['year'] = data['year'].astype(int)

    # Processar e adicionar os dados ao banco
    for _, row in data.iterrows():
        movie = Movie(
            year=row['year'],
            title=row['title'],
            studios=row['studios'],
            producers=row['producers'],
            winner=row['winner'].strip().lower() == 'yes'
        )
        db.session.add(movie)

    db.session.commit()
    print("Dados carregados com sucesso!")


