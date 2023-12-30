import confuse


def get_config():
    config = confuse.Configuration("trident", __name__)
    config.set_file("trident/configs/default.yaml")
    return config


config = get_config()
