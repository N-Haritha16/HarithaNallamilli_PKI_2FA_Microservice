#!/usr/bin/env python3

import subprocess
import json
import sys

def run(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.decode(), err.decode(), p.returncode

# 1) signature test
out, err, code = run(["python3", "scripts/sign_message.py"])
print("SIGNATURE OUTPUT:")
print(out)

# 2) encryption test
out, err, code = run(["python3", "scripts/encrypt_message.py"])
print("ENCRYPT OUTPUT:")
print(out)

# 3) proof test
out, err, code = run(["python3", "scripts/generate_proof.py"])
print("PROOF OUTPUT:")
print(out)
