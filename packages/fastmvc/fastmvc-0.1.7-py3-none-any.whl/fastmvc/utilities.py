import json
from pathlib import Path
import os
import enum

CONFIG_PATH = Path(__file__).parent.resolve() / 'user_config.json'


class Platform(enum.Enum):
    GOOGLE_APP_ENGINE = 'GOOGLE_APP_ENGINE'
    DETA = 'DETA'


def platforms():
    platforms = dict()
    for i, p in enumerate(Platform):
        platforms[f"{i}"] = p
    return platforms


def get_project_platform():
    for (_, _, filenames) in os.walk(os.curdir):
        for fn in filenames:
            if 'app.yaml' in fn:
                return Platform.GOOGLE_APP_ENGINE
    return Platform.DETA


def __fetch_config() -> dict:
    with open(CONFIG_PATH, 'r') as j:
        return json.loads(j.read())


def set_project_key(project_key: str):
    conf = __fetch_config()
    conf['project_key'] = project_key
    with open(CONFIG_PATH, 'w') as j:
        j.write(json.dumps(conf, indent=4))


def set_default_smtp_from_current_project():
    conf = __fetch_config()
    env_file = Path(os.curdir) / '.env'
    smtp_settings = dict()
    with open(env_file, 'r') as e:
        for r in e.readlines():
            if 'SMTP' in r and 'SENDER' not in r:
                k, v = r.split('=')
                smtp_settings[k] = v.replace('\n', '')
    conf.update({'smtp_defaults': smtp_settings})
    with open(CONFIG_PATH, 'w') as c:
        c.write(json.dumps(conf, indent=4))


def get_smtp_defaults() -> dict:
    conf = __fetch_config()
    return conf.get('smtp_defaults', dict())


def set_default_service_account_file_from_current_project():
    conf = __fetch_config()
    try:
        ig_f = Path(os.curdir) / 'ignore'
        servacc = None
        for (_, _, filenames) in os.walk(ig_f):
            for fn in filenames:
                if '.json' in fn:
                    with open(ig_f / fn, 'r') as j:
                        servacc = json.loads(j.read())
                        if not 'universe_domain' in servacc:
                            continue
        if servacc:
            conf.update({'default_service_account': servacc})
            with open(CONFIG_PATH, 'w') as c:
                c.write(json.dumps(conf, indent=4))
            print('Default Service Account File set.')
        else:
            print('No valid service account file found.')
    except:
        print('No valid service account file found.')


def get_default_service_account_file() -> dict:
    conf = __fetch_config()
    return conf.get('default_service_account', dict())


def clear_project_key():
    set_project_key("")


def config(key: str or None = None):
    if key:
        return __fetch_config().get(key)
    return __fetch_config()


def run_server():
    server_cmd = "uvicorn main:app --reload"
    os.system(server_cmd)
