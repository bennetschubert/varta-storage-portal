import requests
import chompjs
import json

from .conf_maps import WR_CONF, ENS_CONF, EMETER_CONF, CHARGER_CONF, BATT_CONF, MODULE_CONF

class VartaStorageClient:
    def __init__(self, host: str):
        self.host = host

    def get_ems_data(self):
        res = requests.get(f"http://{self.host}/cgi/ems_data.js")
        js_content = res.text
        js_objects = chompjs.parse_js_objects(js_content)
        js_confs = [WR_CONF, EMETER_CONF, ENS_CONF, CHARGER_CONF]

        wr_data = dict(zip(WR_CONF, next(js_objects)))
        emeter_data = dict(zip(EMETER_CONF, next(js_objects)))
        ens_data = dict(zip(ENS_CONF, next(js_objects)))
        charger_data = []
        for charger in next(js_objects):
            d = dict(zip(CHARGER_CONF, charger))
            d["BattData"] = dict(zip(BATT_CONF, d["BattData"]))
            module_data = []
            for modul in d["BattData"]["ModulData"]:
                module_data.append(dict(zip(MODULE_CONF, modul)))
            d["BattData"]["ModulData"] = module_data
            charger_data.append(d)

        return {
                "wr": wr_data,
                "emeter": emeter_data,
                "ens": ens_data,
                "charger_data": charger_data,
        }

    def get_params(self):
        res = requests.get(f"http://{self.host}/cgi/param")
        js_content = res.text
        result = dict()
        for line in js_content.splitlines():
            k, *v = line.split("=")
            value_str = "".join(v).strip(";").strip(" ")
            try:
                result[k.strip()] = json.loads(value_str)
            except:
                result[k.strip()] = value_str
        return result
