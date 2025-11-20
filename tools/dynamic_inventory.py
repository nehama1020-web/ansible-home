#!/usr/bin/env python3.
import json
import sys

HOSTS = {
    "vm1": {
        "ansible_host": "10.56.44.183",
        "ansible_user": "ubuntu",
        "ansible_ssh_private_key_file": "~/.ssh/id_rsa",
    },
    "vm2": {
        "ansible_host": "10.56.44.29",
        "ansible_user": "ubuntu",
        "ansible_ssh_private_key_file": "~/.ssh/id_rsa",
    },
    "vm3": {
        "ansible_host": "10.56.44.246",
        "ansible_user": "ubuntu",
        "ansible_ssh_private_key_file": "~/.ssh/id_rsa",
    },
}

inventory = {
    "web": {
        "hosts": ["vm1"],
    },
    "db": {
        "hosts": ["vm2"],
    },
    "galaxy_web": {
        "hosts": ["vm3"],
    },
    "_meta": {
        "hostvars": HOSTS,
    },
}

def main():
    # ansible-inventory --list
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(inventory))
    # ansible-inventory --host <hostname>
    elif len(sys.argv) == 3 and sys.argv[1] == "--host":
        host = sys.argv[2]
        print(json.dumps(inventory["_meta"]["hostvars"].get(host, {})))
    else:
        # default empty
        print(json.dumps({}))

if __name__ == "__main__":
    main()
