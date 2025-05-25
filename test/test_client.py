import pytest
import requests_mock

from pathlib import Path

import vartaclient

@pytest.fixture
def read_sample():
    def _read(filename):
        path = Path(__file__).parent / "sample_responses" / filename
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return _read

def test_ems_data(read_sample, requests_mock):
    requests_mock.get("http://varta-host/cgi/ems_data.js", text=read_sample("ems_data_js.txt"))
    
    client = vartaclient.VartaStorageClient("varta-host")
    result = client.get_ems_data()
    
    assert('wr' in result)
    assert('emeter' in result)
    assert('ens' in result)
    assert('charger_data' in result)

def test_param_data(read_sample, requests_mock):
    requests_mock.get("http://varta-host/cgi/param", text=read_sample("param.txt"))
    
    client = vartaclient.VartaStorageClient("varta-host")
    result = client.get_params()
    
    assert("VPN_SERV" in result)
