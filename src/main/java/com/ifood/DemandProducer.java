package com.ifood;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.uber.h3core.H3Core;

import java.io.IOException;
import java.util.Properties;
import java.util.Random;

public class DemandProducer {

    private static final String TOPIC = "ifood-search-events";
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";

    private static final double BASE_LAT = -22.8732;
    private static final double BASE_LON = -42.3428;

    private static final String[] CATEGORIES = {"pizza", "sushi", "hamburguer", "açai", "marmita", "pastel"};

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);
        ObjectMapper objectMapper = new ObjectMapper();
        Random random = new Random();

        try {
            H3Core h3 = H3Core.newInstance();

            System.out.println("🚀 Iniciando envio de eventos de busca para o Kafka...");

            for (int i = 0; i < 50; i++) {
                double lat = BASE_LAT + (random.nextDouble() - 0.5) * 0.04;
                double lon = BASE_LON + (random.nextDouble() - 0.5) * 0.04;
                
                String userId = "user_" + random.nextInt(20);
                String searchQuery = CATEGORIES[random.nextInt(CATEGORIES.length)];
                String h3Index = h3.geoToH3Address(lat, lon, 8);

                searchEvent event = new searchEvent(userId, searchQuery, lat, lon, h3Index);
                String jsonPayload = objectMapper.writeValueAsString(event);

                ProducerRecord<String, String> record = new ProducerRecord<>(TOPIC, userId, jsonPayload);
                producer.send(record);

                System.out.println("Enviado: " + jsonPayload);
                Thread.sleep(150);
            }

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        } finally {
            producer.close();
            System.out.println("✅ Envio finalizado!");
        }
    }
}