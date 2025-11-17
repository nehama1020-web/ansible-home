#!/usr/bin/env python3
import json
import sys

# Simple dynamic inventory for Ansible
# Replace these with your real hostnames or IPs
web_hosts = ["vm1", "vm2", "vm3"]

inventory = {
    "web": {
        "hosts": web_hosts,
        "vars": {
            "ansible_user": "ubuntu"   # change if your user is different
        }
    },
    "_meta": {
        "hostvars": {}
    }
}

if len(sys.argv) == 2 and sys.argv[1] == "--list":
    print(json.dumps(inventory))
elif len(sys.argv) == 3 and sys.argv[1] == "--host":
    # per-host variables (we keep it empty for now)
    print(json.dumps(inventory["_meta"]["hostvars"].get(sys.argv[2], {})))
else:
    # fallback empty
    print(json.dumps({}))
