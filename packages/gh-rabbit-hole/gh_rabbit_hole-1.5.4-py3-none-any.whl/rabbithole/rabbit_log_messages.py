# log_messages.py


class RabbitLogMessages:
    GENERIC_ERROR = "Error: {}"

    # Costanti per i messaggi di log
    CONNECTION_OPENED = "Connection opened"
    CONNECTION_OPENED_DEBUG = "Connection opened: {}"
    CONNECTION_NOT_ESTABLISHED = "Connection not established"
    CONNECTION_CLOSED = "Connection closed: {}"
    CONNECTION_CLOSED_DEBUG = "Connection closed: {}"
    CONNECTION_NOT_OPEN_ERROR = "Connection not open"
    CONNECTION_OPEN_ERROR = "Connection open error: {}"
    CONNECTION_OPEN_ERROR_DEBUG = "Connection {} open error: {}"
    CONNECTION_FAILED = "Failed to connect to RabbitMQ: {}"
    ATTEMPT_RECONNECT = "Attempt to reconnect {}/{} in {} seconds..."
    RECONNECT_FAILED = "Reached the maximum number of reconnection attempts ({})."
    CONNECTION_CLOSING_ERROR = "Error in closing connection: {}"
    CONNECTION_NOT_OPENED = "Connection not opened"

    CHANNEL_OPENED = "Channel opened"
    CHANNEL_OPENED_DEBUG = "Channel opened: {}"
    CHANNEL_OPEN_FAILED = "Failed to open channel: {}"
    CHANNEL_OPEN_ERROR = "Error in opening channel: {}"
    CHANNEL_OPEN_ERROR_DEBUG = "Channel {} open error: {}"
    CHANNEL_CLOSED = "RabbitMQ channel closed."
    CHANNEL_CLOSING_ERROR = "Error in closing channel: {}"
    CHANNEL_NOT_OPENED = "Channel not opened"

    QUEUE_DECLARED = "[x] {} declared"
    QUEUE_DECLARED_DEBUG = "[x] {} declared: {}"

    MESSAGE_RECEIVED = "Received message: {} on channel: {}"
    MESSAGE_RECEIVED_DEBUG = (
        "Received message: {} on channel: {}, method: {}, properties: {}"
    )
    MESSAGE_SENT = "Message sent to {}: {}"
    MESSAGE_SENDING_ERROR = "Error while sending message: {}"
    MESSAGE_SENDING_ERROR_DEBUG = (
        "Error while sending message: {} on channel: {}, error: {}"
    )
    MESSAGE_SEND_FAILED = "Failed to send message: {}"
    MESSAGE_PROCESSING_ERROR = "Error while processing message: {}"
    MESSAGE_PROCESSING_ERROR_DEBUG = "Error while processing message: {} on channel: {}, method: {}, properties: {}, error: {}"
