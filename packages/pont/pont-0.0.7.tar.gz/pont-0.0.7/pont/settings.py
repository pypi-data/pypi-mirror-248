import logging
from dataclasses import dataclass
from pathlib import Path

import platformdirs
from strictyaml import (
    EmptyNone,
    Enum,
    Int,
    Map,
    Optional,
    Seq,
    Str,
    YAMLValidationError,
    as_document,
)
from strictyaml import load as strictyaml_load


class SettingsError(Exception):
    pass


@dataclass
class ProxySettings:
    protocol: str
    local_host: str
    local_port: int
    remote_host: str | None = None
    remote_port: int | None = None


class Settings:
    # This is the schema for the pont.yml file validation
    PROXY_SCHEMA = Map(
        {
            "protocol": Enum(["http", "redis"]),
            Optional("remote_host", default=None): EmptyNone() | Str(),
            Optional("remote_port", default=None): EmptyNone() | Int(),
            "local_port": Int(),
            "local_host": Str(),
        }
    )
    SCHEMA = Map({"host": Str(), "port": Int(), "proxies": Seq(PROXY_SCHEMA)})

    port: int
    host: str
    proxies: list[ProxySettings]
    config_file: Path | None

    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = 1984
        self.proxies = [
            ProxySettings(protocol="http", local_host="127.0.0.1", local_port=1985)
        ]
        self.config_file = None

    def config_directory(self) -> Path:
        """
        Return the directory where the config file is located
        """
        if self.config_file is None:
            raise SettingsError("No config file loaded")
        return self.config_file.parent

    def load(self):
        pont_yaml_path = self.project_config_directory() / "pont.yml"
        if pont_yaml_path.exists():
            self.load_file(pont_yaml_path)
        else:
            pont_yaml_path = self.user_config_directory() / "pont.yml"
            if pont_yaml_path.exists():
                self.load_file(pont_yaml_path)
            else:
                logging.warning(
                    "No pont.yml file found, using default settings. You can use pont init to create a pont.yml file."
                )

    def save(self):
        """
        Save the settings to the config file
        """
        if self.config_file is None:
            raise SettingsError("No config file loaded")
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with self.config_file.open("w+") as file:
            settings = {
                "host": self.host,
                "port": self.port,
                "proxies": [],
            }
            for proxy in self.proxies:
                proxy = {
                    "protocol": proxy.protocol,
                    "remote_host": proxy.remote_host,
                    "remote_port": proxy.remote_port,
                    "local_port": proxy.local_port,
                    "local_host": proxy.local_host,
                }
                proxy = {
                    k: v for k, v in proxy.items() if v is not None
                }  # Remove None values
                settings["proxies"].append(proxy)
            file.write(as_document(settings).as_yaml())
        logging.info(f"Settings saved to {self.config_file}")

    def init(self):
        """
        Initialize a pont settings file.
        """
        if (self.user_config_directory() / "pont.yml").exists():
            raise SettingsError("pont.yml already exists")
        self.config_file = self.user_config_directory() / "pont.yml"

    def user_config_directory(self) -> Path:
        return Path(platformdirs.user_config_dir("pont"))

    def project_config_directory(self) -> Path:
        return Path.cwd() / ".pont"

    def load_file(self, pont_yaml_path: Path):
        try:
            with pont_yaml_path.open("r") as file:
                pont_yaml = strictyaml_load(file.read(), schema=self.SCHEMA)
                self.port = int(pont_yaml["port"])
                self.host = str(pont_yaml["host"])
                self.proxies = []
                for proxy in pont_yaml["proxies"]:
                    proxy_settings = ProxySettings(
                        str(proxy["protocol"]),
                        str(proxy["local_host"]),
                        int(proxy["local_port"]),
                    )
                    if "remote_host" in proxy:
                        proxy_settings.remote_host = str(proxy["remote_host"])
                    if "remote_port" in proxy:
                        proxy_settings.remote_port = int(proxy["remote_port"])
                    self.proxies.append(proxy_settings)
            self.config_file = pont_yaml_path
            logging.info(f"Settings loaded from {pont_yaml_path}")
        except (OSError, YAMLValidationError) as error:
            raise SettingsError(f"Error loading {pont_yaml_path}: {error}") from error


if __name__ == "__main__":
    # Use to test the code from the command line
    settings = Settings()
    settings.load()
    print(f"The port is {settings.port}")
    for proxy in settings.proxies:
        print(f"Proxy {proxy.protocol} listening on {proxy.local_port}")
