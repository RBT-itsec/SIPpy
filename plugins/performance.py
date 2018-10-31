"""
Performance tests

config.json:
Needed fields
 * bandwidth: Bandwidth in bits/second
 * protocol: "udp" or "tcp"
 * blksize: bandwidth / packets_per_second / 8 (needs bytes!)
 * num_streams: Number of streams to use (each stream has bandwidth)
 * duration: Test duration. Use >30s for correct jitter measurement (udp)
"""
# pylint: disable=W1203

import json
import logging
from typing import Dict, Optional
from functools import partial

from lib import iperf3
from . import PLUGINS

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


def _iperf(target: str, codec: Optional[Dict] = None) -> Dict:
    """ Run the iperf3 client """
    client = iperf3.Client()
    if codec:
        for key, val in codec.items():
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


# Create plugins for codecs in codecs.json
# Sideload them into plugins - TODO: Needs restart !!!
for _codec, _config in _read_codecs_from_file().items():
    PLUGINS[_codec] = partial(_iperf, codec=_config)
