import json
import psycopg2
from kafka import KafkaConsumer

DB_CONFIG = {
    "dbname": "ifood_db",
    "user": "ifood_user",
    "password": "ifood_password",
    "host": "127.0.0.1",
    "port": 5432
}

KAFKA_TOPIC = "ifood-search-events"
KAFKA_SERVER = "localhost:9092"

def safe_json_deserializer(x):
    try:
        return json.loads(x.decode('utf-8'))
    except Exception as e:
        print("⚠️ Mensagem com JSON malformado/inválido ignorada.")
        return None

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Conectado ao PostgreSQL com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar no banco de dados: {e}")
        return

    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='latest',
            group_id='ifood-consumer-v4',
            value_deserializer=safe_json_deserializer
        )
        print(f"Aguardando eventos do tópico {KAFKA_TOPIC}...")
    except Exception as e:
        print(f"Erro ao conectar ao Kafka: {e}")
        conn.close()
        return

    insert_query = """
        INSERT INTO SEARCH_EVENTS (USER_ID, SEARCH_QUERY, LATITUDE, LONGITUDE, H3_INDEX)
        VALUES (%s, %s, %s, %s, %s);
    """

    for message in consumer:
        event = message.value
        if event is None:
            continue

        print(f"Evento recebido: {event}")

        try:
            cursor.execute(insert_query, (
                event.get("userId"),
                event.get("searchQuery"),
                event.get("latitude"),
                event.get("longitude"),
                event.get("h3Index")
            ))
            conn.commit()
            print("Evento gravado no banco de dados com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir evento no banco: {e}")
            conn.rollback()

if __name__ == "__main__":
    main()