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
# from functools import partial

from lib import iperf3
from . import register_plugin, Plugin

LOGGER = logging.getLogger("SIPpy.Performance")


class IperfCodec(Plugin):
    """ IPerf generic plugin """
    name = "iperfcodec"
    category = "codec"

    def __init__(self, config: Optional[Dict] = None):
        super().__init__()
        self.config = config or {}

    def __repr__(self):
        """ Set repr """
        return f"IPerf {self.name}"

    def _run(self, target: str):
        """ Run the plugin """
        return _iperf(target, self.config)


class IperfUDPCodec(IperfCodec):
    """ Represents an UDP based codec built in iperf """
    name = "iperfudpcodec"
    category = "codec"

    def __init__(self):
        super().__init__()
        self.jitter_ms: float = 0
        self.lost_packets: int = 0
        self.lost_percent: float = 0
        self.mbps: float = 0

    def __repr__(self):
        """ Set repr """
        return f"Iperf UDP Codec {self.name}"


class IperfTCPCodec(IperfCodec):
    """ Represents an TCP based codec built in iperf """
    name = "iperftcpcodec"
    category = "codec"

    def __init__(self):
        super().__init__()
        self.retransmits: int = 0
        self.sent_mbps: float = 0
        self.rcvd_mbps: float = 0

    def __repr__(self):
        """ Set repr """
        return f"Iperf TCP Codec {self.name}"


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


# move into class
def _iperf(target: str, codec_config: Optional[Dict] = None) -> Dict:
    """ Run the iperf3 client """
    client = iperf3.Client()
    if codec_config:
        for key, val in codec_config.items():
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


# for codec, config in _read_codecs_from_file().items():
#     _codec = IperfCodec()
#     _codec.name = codec
#     _codec.config = config
#     _codec.output = {}
#     register_plugin(_codec)

for codec, config in _read_codecs_from_file().items():
    _codec: IperfCodec  # _codec is of type or instance of IperfCodec
    if config.get("protocol") == "udp":
        _codec = IperfUDPCodec()
    else:
        _codec = IperfTCPCodec()
    _codec.name = codec
    _codec.config = config
    _codec.output = {}
    register_plugin(_codec)