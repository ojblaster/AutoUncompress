import sys
import struct
import json

def read(incomingBytes):
    print("Reading message", file=sys.stderr, flush=True)
    try:
        textLength = struct.unpack('=I', incomingBytes)[0]
        rawString = sys.stdin.buffer.read(textLength).decode('utf-8')
        return json.loads(rawString)
    except Exception:
            sys.exit(1)

def write(outgoingMessage):
    try:
        response_bytes = outgoingMessage.encode('utf-8')
        sys.stdout.buffer.write(struct.pack('=I', len(response_bytes)))
        sys.stdout.buffer.write(response_bytes)
        sys.stdout.buffer.flush()
    except Exception:
        sys.exit(1)