"""
Performance tests
"""
# pylint: disable=W1203

import json
import logging
from typing import Dict, Optional

from lib import iperf3
from . import register_plugin

LOGGER = logging.getLogger("SIPpy.Performance")


def _read_codecs_from_file(filename: str = './codecs.json') -> Dict:
    """ Read codec information from file """
    codecs: Dict = {}
    try:
        codecs = json.load(open(filename))
    except FileNotFoundError:
        LOGGER.critical(f"Can not find codec configuration file {filename}")
    except json.JSONDecodeError:
        LOGGER.critical(f"Could not decode data from {filename}")

    return codecs


def _iperf(target: str, codec: Optional[str] = None) -> Dict:
    """ Run the iperf3 client """
    codecs = _read_codecs_from_file()
    if codecs and codec:
        args = codecs.get(codec)
    else:
        args = None

    client = iperf3.Client()
    if args:
        for key, val in args.items():
            setattr(client, key, val)

    client.server_hostname = target
    result = client.run()

    if result.error:  # if we got error
        result = {'error': result.error}
    elif client.protocol == "udp":
        result = {'jitter_ms': result.jitter_ms,
                  'lost_packets': result.lost_packets,
                  'lost_percent': result.lost_percent,
                  'mbps': result.Mbps}
    else:  # tcp - default
        result = {'retransmits': result.retransmits,
                  'sent_mbps': result.sent_Mbps,
                  'rcvd_mbps': result.received_Mbps}
    return result


@register_plugin
def g711(target: str) -> Dict:
    """ Emulate the g711 codec """
    return _iperf(target, 'g711')


@register_plugin
def g729(target: str) -> Dict:
    """ Emulate the g729 codec """
    return _iperf(target, 'g729')


@register_plugin
def perftest_tcp(target: str) -> Dict:
    """ Run a maximum performance test """
    return _iperf(target, 'perftest_tcp')


@register_plugin
def perftest_udp(target: str) -> Dict:
    """ Run a maximum performance test """
    return _iperf(target, 'perftest_udp')
