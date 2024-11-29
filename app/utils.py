
def get_award_intervals():
    winners = Movie.query.filter_by(winner=True).all()
    producer_awards = {}

    # Organizar os prêmios por produtor e ano
    for movie in winners:
        producers = [p.strip() for p in movie.producers.split(",")]
        for producer in producers:
            if producer not in producer_awards:
                producer_awards[producer] = []
            producer_awards[producer].append(movie.year)

    intervals = []

    # Calcular intervalos para cada produtor
    for producer, years in producer_awards.items():
        years.sort()
        for i in range(len(years) - 1):
            interval = years[i + 1] - years[i]
            intervals.append({
                "producer": producer,
                "interval": interval,
                "previousWin": years[i],
                "followingWin": years[i + 1]
            })

    # Ordenar todos os intervalos por intervalo de prêmios
    intervals.sort(key=lambda x: x['interval'])

    if not intervals:
        return {"min": [], "max": []}  # Caso não haja intervalos

    # Encontrar o menor intervalo
    min_interval = intervals[0]['interval']
    max_interval = intervals[-1]['interval']

    # Filtrar os produtores com o menor e o maior intervalo
    min_intervals = [i for i in intervals if i['interval'] == min_interval]
    max_intervals = [i for i in intervals if i['interval'] == max_interval]

    # Montar a resposta no formato solicitado
    response = {
        "min": [
            {
                "producer": item['producer'],
                "interval": item['interval'],
                "previousWin": item['previousWin'],
                "followingWin": item['followingWin']
            } for item in min_intervals
        ],
        "max": [
            {
                "producer": item['producer'],
                "interval": item['interval'],
                "previousWin": item['previousWin'],
                "followingWin": item['followingWin']
            } for item in max_intervals
        ]
    }

    return response


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


