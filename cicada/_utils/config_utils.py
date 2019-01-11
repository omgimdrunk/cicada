import os
import configparser

global config_paths


class _keyCaller(dict):
    def __init__(self):
        super().__init__()

    def __getattribute__(self, item, *args, **kwargs):
        if str(item) in self:
            return self[str(item)]
        else:
            return


def fig_finder(search_paths: list = None):
    #
    # home supercedes, then etc
    for v_path in search_paths:
        try:
            _cdir = os.listdir(v_path)
        except:
            pass
        else:
            if 'cicada.d.conf' in _cdir:
                fpath = os.path.join(v_path, 'cicada.d.conf')
                #
                # first find wins
                return fpath


def parse_config(conf: _keyCaller):
    try:
        conf_parse = configparser.ConfigParser()
        conf_parse.read(conf)
    except Exception as E:
        raise E
    else:
        #
        # TODO :: All dis
        # The obj passed back should be a inherited class of dict with functions pertaing to the conf.
        # Example: conf.get('name')
        #
        p_conf = _keyCaller()
        for sect in conf_parse.sections():
            _sect = p_conf[sect] = _keyCaller
            for opt in conf_parse.options(sect):
                _sect[opt] = conf_parse.get(sect, opt)
        return p_conf
