import yaml
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()


def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config("config.yaml")
google_config = config.get("google")

oauth.register(
    name="google",
    client_id=google_config.get("client_id"),
    client_secret=google_config.get("client_secret"),
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)
