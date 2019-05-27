# SIPpy
SIP Connection Tester
```
Syntax: python -m sippy
```

## Requirements
 * Linux OS with iproute2
 * Python3.7
 * iperf3 (tested with 3.6+)

## Base Checks
 * Link check
 * Gateway check
 * Ping check

## Performance Checks
 * Basic Codec Tests with iperf3 (see codecs.json, set blksize parameter for correct timing)
