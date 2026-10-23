package com.videoplatform.worker.queue;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

@Service("workerAzureQueueService")
public class AzureQueueService implements MessageQueueService {

    private static final Logger log = LoggerFactory.getLogger(AzureQueueService.class);

    private final String connectionString;
    private final String queueName;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private Object queueClient;

    public AzureQueueService(
            @Value("${queue.azure.connection-string:}") String connectionString,
            @Value("${queue.azure.queue-name:video-compression-jobs}") String queueName) {
        this.connectionString = connectionString;
        this.queueName = queueName;
    }

    private synchronized Object getQueueClient() {
        if (queueClient == null) {
            if (!StringUtils.hasText(connectionString)) {
                throw new IllegalStateException("Azure Storage Connection String is required for Azure Queue!");
            }
            try {
                Class<?> builderClass = Class.forName("com.azure.storage.queue.QueueClientBuilder");
                Object builder = builderClass.getDeclaredConstructor().newInstance();
                Method connMethod = builderClass.getMethod("connectionString", String.class);
                connMethod.invoke(builder, connectionString);
                Method queueNameMethod = builderClass.getMethod("queueName", String.class);
                queueNameMethod.invoke(builder, queueName);
                Method buildMethod = builderClass.getMethod("buildClient");
                queueClient = buildMethod.invoke(builder);
            } catch (Exception e) {
                log.error("Failed to connect to Azure Queue Storage: {}", e.getMessage(), e);
                throw new RuntimeException("Azure Queue init failed", e);
            }
        }
        return queueClient;
    }

    @Override
    public void enqueueJob(JobQueueMessage message) {
        try {
            String json = objectMapper.writeValueAsString(message);
            String base64 = Base64.getEncoder().encodeToString(json.getBytes(StandardCharsets.UTF_8));
            Object client = getQueueClient();
            Method sendMethod = client.getClass().getMethod("sendMessage", String.class);
            sendMethod.invoke(client, base64);
        } catch (Exception e) {
            throw new RuntimeException("Failed to enqueue message to Azure Queue", e);
        }
    }

    @Override
    public JobQueueMessage pollJob() {
        try {
            Object client = getQueueClient();
            Method receiveMethod = client.getClass().getMethod("receiveMessage");
            Object messageItem = receiveMethod.invoke(client);
            if (messageItem != null) {
                Method getBodyMethod = messageItem.getClass().getMethod("getBody");
                Object bodyObj = getBodyMethod.invoke(messageItem);
                String raw = bodyObj.toString();
                String json;
                try {
                    json = new String(Base64.getDecoder().decode(raw), StandardCharsets.UTF_8);
                } catch (IllegalArgumentException e) {
                    json = raw;
                }
                JobQueueMessage msg = objectMapper.readValue(json, JobQueueMessage.class);

                Method getIdMethod = messageItem.getClass().getMethod("getMessageId");
                String messageId = (String) getIdMethod.invoke(messageItem);
                Method getPopMethod = messageItem.getClass().getMethod("getPopReceipt");
                String popReceipt = (String) getPopMethod.invoke(messageItem);

                Method deleteMethod = client.getClass().getMethod("deleteMessage", String.class, String.class);
                deleteMethod.invoke(client, messageId, popReceipt);
                return msg;
            }
        } catch (Exception e) {
            log.warn("Worker error polling message from Azure Queue: {}", e.getMessage());
        }
        return null;
    }

    @Override
    public int getQueueDepth() {
        try {
            Object client = getQueueClient();
            Method getPropsMethod = client.getClass().getMethod("getProperties");
            Object props = getPropsMethod.invoke(client);
            Method getCountMethod = props.getClass().getMethod("getApproximateMessagesCount");
            return (int) getCountMethod.invoke(props);
        } catch (Exception e) {
            return 0;
        }
    }

    @Override
    public String getQueueType() {
        return "AZURE_QUEUE_STORAGE";
    }
}
