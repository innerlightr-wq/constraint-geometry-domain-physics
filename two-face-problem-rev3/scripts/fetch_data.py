"""Download the SXS catalog metadata used in Section 9 (release v3.0.0) and verify it.

    python3 fetch_data.py

Writes data_simulations.json next to this script.
"""
import hashlib, os, urllib.request

URL = "https://raw.githubusercontent.com/sxs-collaboration/sxscatalogdata/v3.0.0/simulations.json"
MD5 = "c9a80be926346769178c9178f5d7590d"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_simulations.json")

if not os.path.exists(OUT):
    print("downloading", URL)
    urllib.request.urlretrieve(URL, OUT)
digest = hashlib.md5(open(OUT, "rb").read()).hexdigest()
if digest != MD5:
    raise SystemExit(f"checksum mismatch: got {digest}, expected {MD5}")
print("ok:", OUT, digest)
