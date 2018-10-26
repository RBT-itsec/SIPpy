"""
Performance tests
"""

from lib import iperf3
from . import register_plugin


@register_plugin
def iperf(target: str):
    """ Run a simple IPerf3 UDP test """
    iperf_client = iperf3.Client()
    iperf_client.duration = 10
    iperf_client.server_hostname = target
    iperf_client.port = 5001
    iperf_client.protocol = "udp"
