import json
from flask import Flask, jsonify
import subprocess

def remove_empty_lists(item):
    if isinstance(item, list):
        if len(item) == 1:
            return remove_empty_lists(item[0])
        else:
            return [remove_empty_lists(n) for n in item]
    elif isinstance(item, dict):
        return {k: remove_empty_lists(v) for k, v in item.items()}
    else:
        return item
    
app = Flask(__name__)

@app.route("/")
def hello():
    return "<p>API is active!</p>"

@app.route("/api/status")
def status():
    return jsonify({"status": "active"})

@app.route("/api/cpu")
def cpu():
    sys_out = subprocess.run(["mpstat", "-P", "ALL", "-o", "JSON", "1", "1"], capture_output = True, text = True).stdout
    cpu_out = subprocess.run(["cat", "/proc/cpuinfo"], capture_output = True, text = True).stdout
    
    cpu_dict = dict()
    sub_dict = dict()
    count = 0
    for line in cpu_out.strip().split("\n"):
        line = line.strip()
        if len(line) == 0:
            cpu_dict[str(count)] = sub_dict
            sub_dict = dict()
            count += 1
            continue

        line = " ".join(line.split())
        
        items = line.split(" : ")

        if len(items) < 2:
            continue

        sub_dict[items[0]] = items[1]
    cpu_dict[str(count)] = sub_dict

    out = remove_empty_lists(json.loads(sys_out)['sysstat'])
    out.update({"cpus": cpu_dict})
    return jsonify(out)

@app.route("/api/temps")
def temps():
    out = subprocess.run(["sensors", "-A", "-j"], capture_output = True, text = True).stdout
    return jsonify(json.loads(out))

@app.route("/api/disks")
def disks():
    out = subprocess.run(["iostat", "-d", "-o", "JSON"], capture_output = True, text = True).stdout
    return jsonify(remove_empty_lists(json.loads(out)))

@app.route("/api/memory")
def memory():
    out = subprocess.run(["free"], capture_output = True, text = True).stdout
    out = out.strip().split("\n")
    
    headers = out[0].split()
    mem = out[1].split()[1:]
    split = out[2].split()[1:]

    both_dict = dict()
    mem_dict = dict()
    for i in range(len(headers)):
        mem_dict[headers[i]] = mem[i]

    swap_dict = dict()
    for i in range(len(split)):
        swap_dict[headers[i]] = split[i]

    return jsonify({"mem:": mem_dict, "swap": swap_dict})

@app.route("/api/network")
def network():
    wan_out = subprocess.run(["dig", "TXT", "+short", "o-o.myaddr.l.google.com", "@ns1.google.com"], capture_output = True, text = True).stdout.strip()[1:-1]
    lan_out = subprocess.run(["ip", "addr"], capture_output = True, text = True).stdout.strip()

    lan_dict = dict()
    interface = ""
    for line in lan_out.split("\n"):
        if line[0].isdigit():
            interface = line.split()[1][:-1]
            lan_dict[interface] = dict()
        elif "inet " in line:
            lan_dict[interface]["inet"] = line.split()[1].split("/")[0]
        elif "inet6" in line:
            lan_dict[interface]["inet6"] = line.split()[1].split("/")[0]

    return jsonify({"wan": wan_out, "lan": lan_dict})