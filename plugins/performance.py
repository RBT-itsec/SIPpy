"""
Performance tests
"""

from typing import List, Dict, Callable, Tuple

from lib import iperf3
from . import register_plugin


def _iperf(func: Callable):
    def wrapper(*args: List, **kwargs: Dict):
        target, options = func(*args, **kwargs)
        client = iperf3.Client()
        for key, val in options.items():
            setattr(client, key, val)
        client.server_hostname = target
        # TODO: Server port -> config.json
        result = client.run()
        return result  # TODO: whole result, or just jitter, loss and bandwidth?
    return wrapper


@register_plugin
@_iperf
def g711(target=str) -> Tuple[str, Dict]:
    """ Profile of codec G711 """
    # read codec profile from codecs.json
    args = {'foo': 'bar'}
    return target, args

# # @register_plugin
# def iperf(target: str) -> Dict:
#     """ Run a simple IPerf3 UDP test """
#     iperf_client = iperf3.Client()
#     iperf_client.duration = 10
#     iperf_client.server_hostname = target
#     iperf_client.port = 5001
#     iperf_client.num_streams = 1
#     iperf_client.bandwidth = int(10e6)
#     iperf_client.protocol = "udp"

#     results = iperf_client.run()

#     return {'jitter': results.jitter_ms,
#             'packetloss': results.lost_packets,
#             'packetloss_percent': results.lost_percent,
#             'Mbps': results.Mbps}
