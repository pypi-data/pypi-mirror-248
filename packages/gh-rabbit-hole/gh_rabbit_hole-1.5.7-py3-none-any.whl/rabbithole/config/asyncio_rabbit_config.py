import json
from rabbithole.config import ConfigFileManager

DEFAULT_CONFIG = {
    "amqp_url": "amqp://guest:guest@localhost:5672/",
    "sending_queue": "my_sending_queue",
    "listening_queue": "my_listening_queue",
    "sending_exchange": "my_exchange",
    "reconnect_delay": 5,
    "max_reconnect_attempts": 3,
}

REQUIRED_KEYS = [
    {"key": "amqp_url", "type": str},
    {"key": "sending_queue", "type": str},
    {"key": "listening_queue", "type": str},
    {"key": "sending_exchange", "type": str},
    {"key": "reconnect_delay", "type": int},
    {"key": "max_reconnect_attempts", "type": int},
]


class RabbitConfig:
    def __init__(
        self,
        config_file_manager: ConfigFileManager = ConfigFileManager(
            "app_config", "config.json"
        ),
        required_keys: list = REQUIRED_KEYS,
        default_config: dict = DEFAULT_CONFIG,
    ):
        self.config_file_manager = config_file_manager
        self._default_config = default_config
        self.__required_keys = required_keys
        self.config: dict = self.load_or_initialize_config()

    def load_or_initialize_config(self):
        config = self.config_file_manager.load()
        if config is None:  # Se il file di configurazione non esiste o è vuoto
            config = self._default_config
            config_to_save = self.__check_config(config)
            self.config_file_manager.save(
                config_to_save
            )  # Crea un file di configurazione di default
            return config_to_save
        else:
            return self.__check_config(config)

    def __check_config(self, config):
        default = self._default_config

        for required in self.__required_keys:
            key, required_type = required["key"], required["type"]

            # Verifica la presenza della chiave
            if key not in config:
                if key in default:
                    config[key] = default[key]
                else:
                    raise ValueError(
                        f"La chiave di configurazione obbligatoria '{key}' manca."
                    )

            # Verifica il tipo della chiave
            if not isinstance(config[key], required_type):
                raise ValueError(
                    f"La chiave '{key}' deve essere di tipo {required_type.__name__}"
                )

        return config

    def update_config(self, new_config):
        validated_config = self.__check_config(new_config)
        if validated_config is None:
            return
        for key, value in validated_config.items():
            if key in self.config:
                self.config[key] = value

        self.config_file_manager.save(self.config)

    def get_config(self):
        return self.config

    def save_config(self, save_path):
        # Prima di salvare, converti il valore del font in una stringa
        save_config = self.config.copy()
        with open(save_path, "w") as config_file:
            json.dump(save_config, config_file, indent=4)
