#!/usr/bin/env python3
import json
import subprocess
import sys


# Get all multipass instances as JSON
def get_multipass_instances():
    result = subprocess.run(
        ["multipass", "list", "--format", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)
    return data.get("list", [])


def build_inventory():
    instances = get_multipass_instances()

    inventory = {
        "web": {"hosts": []},
        "db": {"hosts": []},
        "galaxy_web": {"hosts": []},
        "_meta": {"hostvars": {}},
    }

    for inst in instances:
        name = inst["name"]
        ips = inst.get("ipv4", [])
        if not ips:
            continue

        ip = ips[0]

        # Map instance name → Ansible group
        if name == "hs1":
            group = "web"
        elif name == "hs2":
            group = "db"
        elif name == "hs3":
            group = "galaxy_web"
        else:
            # Ignore other multipass VMs
            continue

        inventory[group]["hosts"].append(name)

        inventory["_meta"]["hostvars"][name] = {
            "ansible_host": ip,
            "ansible_user": "ubuntu",
            # adjust this path if your key is somewhere else on the runner
            "ansible_ssh_private_key_file": "/home/neha/.ssh/ansible_vm",
        }

    return inventory


if __name__ == "__main__":
    # Ansible calls with --list / --host
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(build_inventory(), indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == "--host":
        # not needed because we use _meta.hostvars
        print(json.dumps({}))
    else:
        print(json.dumps(build_inventory(), indent=2))
