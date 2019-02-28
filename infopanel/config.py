"""Configuration file stuff."""

import inspect

import yaml
import voluptuous as vol

from infopanel import sprites, scenes

SPRITE_NAMES = [name for name,
                value in inspect.getmembers(sprites, inspect.isclass)]

MQTT = vol.Schema({'broker': str,
                   vol.Optional('port', default=1883): int,
                   'client_id': str,
                   vol.Optional('keepalive', default=60): int,
                   vol.Optional('username'): str,
                   vol.Optional('password'): str,
                   vol.Optional('certificate'): str,
                   vol.Optional('protocol', default='3.1'): vol.Coerce(str),
                   'topic': str})

SPRITE = vol.Schema({'type': vol.Any(*SPRITE_NAMES)},
                    extra=vol.ALLOW_EXTRA)
SPRITES = vol.Schema({str: SPRITE})

SCENE_NAMES = [name for name,
               value in inspect.getmembers(scenes, inspect.isclass)]
# sprite list in scenes is a list because you may want multiple of one
# sprite in a scene.
SCENES = vol.Schema({str: {vol.Optional('type', default='Scene'): vol.Any(*SCENE_NAMES),
                           vol.Optional('path'): str,
                           vol.Optional('sprites'): list}}, extra=vol.ALLOW_EXTRA)

MODES = vol.Schema({str: list})

RGBMATRIX = vol.Schema({vol.Optional('led-rows', default=32): int,
                        vol.Optional('led-cols', default=32): int,
                        vol.Optional('led-chain', default=1): int,
                        vol.Optional('led-parallel', default=1): int,
                        vol.Optional('led-pwm-bits', default=11): int,
                        vol.Optional('led-brightness', default=100): int,
                        vol.Optional('led-gpio-mapping', default='regular'): str, 
                        vol.Optional('led-scan-mode', default=0): int,
                        vol.Optional('led-pwm-lsb-nanoseconds', default=130): int,
                        vol.Optional('led-show-refresh', default=False): bool,
                        vol.Optional('led-slowdown-gpio', default=1): int,
                        vol.Optional('led-no-hardware-pulse', default=False): bool,
                        vol.Optional('led-pixel-mapper', default='') : str,
                        vol.Optional('led-multiplexing', default=10) : int
                        })

GLOBAL = vol.Schema({'font_dir': str,
                     'default_mode': str,
                     vol.Optional('log_level', default="ERROR"): vol.Any('DEBUG','INFO','WARNING','ERROR','CRITICAL'),
                     'random': bool})

SCHEMA = vol.Schema({'mqtt': MQTT,
                     'sprites': SPRITES,
                     'scenes': SCENES,
                     'modes': MODES,
                     vol.Optional('RGBMatrix'): RGBMATRIX,
                     vol.Optional('DummyMatrix'): None,
                     'global': GLOBAL})


def load_config_yaml(path):
    """Load and validate config file as an alternative to command line options."""
    with open(path, encoding='utf8') as configfile:
        config = yaml.load(configfile)
    config = SCHEMA(config)

    return config
