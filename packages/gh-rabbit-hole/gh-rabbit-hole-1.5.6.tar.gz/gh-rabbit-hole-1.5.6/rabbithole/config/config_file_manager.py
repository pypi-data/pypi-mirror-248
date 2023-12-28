import json
import os


class ConfigFileManager:
    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def get_full_path(self):
        return os.path.join(self.directory, self.filename)

    def load(self):
        full_path = self.get_full_path()
        if not os.path.isfile(full_path):  # Se il file non esiste, restituisci None o un valore di default
            return None  # Oppure potresti restituire self.default_config se ha senso per il tuo caso d'uso

        with open(full_path, "r") as file:
            return json.load(file)

    def save(self, config):
        with open(self.get_full_path(), "w") as file:
            json.dump(config, file, indent=4)
