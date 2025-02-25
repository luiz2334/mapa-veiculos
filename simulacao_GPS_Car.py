from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

# Configuração do Banco de Dados
DB_CONFIG = {
    "dbname": "Grupo-ponte-dez24",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

app = Flask(__name__)
CORS(app)

def get_vehicle_locations(data_simulada=None, hora_simulada=None):
    """
    Busca a localização dos veículos filtrando por data e hora com margem de erro.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if data_simulada and hora_simulada:
            # Convertendo a hora para um objeto de hora
            hora_simulada = datetime.strptime(hora_simulada, "%H:%M").time()

            # Criando intervalo de 1 minuto antes e depois
            hora_inicio = (datetime.combine(datetime.today(), hora_simulada) - timedelta(minutes=1)).time()
            hora_fim = (datetime.combine(datetime.today(), hora_simulada) + timedelta(minutes=1)).time()

            query = """
            SELECT lineid, carnbr, latitude, longitude, rtcdatetime 
            FROM "location-header"
            WHERE DATE(rtcdatetime) = %s 
            AND rtcdatetime::time BETWEEN %s AND %s
            ORDER BY rtcdatetime ASC;
            """
            cur.execute(query, (data_simulada, hora_inicio, hora_fim))
        else:
            query = """
            SELECT lineid, carnbr, latitude, longitude, rtcdatetime 
            FROM "location-header"
            ORDER BY rtcdatetime DESC
            LIMIT 50;
            """
            cur.execute(query)

        results = cur.fetchall()
        cur.close()
        conn.close()

        return results

    except Exception as e:
        print("Erro ao acessar o banco de dados:", e)
        return []

@app.route('/api/vehicles', methods=['GET'])
def vehicles():
    """
    Retorna a localização dos veículos, filtrando por data e hora.
    """
    data_simulada = request.args.get("data")  
    hora_simulada = request.args.get("hora")  
    resultado = get_vehicle_locations(data_simulada, hora_simulada)

    if not resultado:
        return jsonify({"message": "Nenhum dado encontrado"}), 404

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
