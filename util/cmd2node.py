#! /usr/bin/env python
# -*- coding: utf-8 -*-

from v2ray.models import Server
from base.models import Setting
from init import db
from socket import *
import os
import json
import struct


def config_changed():
    svrs = Server.query.all()
    config_path = Setting.query.filter_by(key="v2_config_path").first()
    total = len(svrs)
    suc = 0
    for svr in svrs:
        cli = socket(AF_INET, SOCK_STREAM)
        cli.settimeout(5)
        print("[I] Ready to send config file to server: %s(%s)..." % (svr.address, svr.remark))
        try:
            cli.connect((svr.address, 40001))
        except Exception as e:
            print('[E] Send config file to server [%s] failed: %s' % (svr.remark, str(e)))
            continue
        filename = config_path.value
        filebytes = os.path.getsize(filename)
        header = {
            "command": "config_changed",
            "filename": filename,
            "filesize": filebytes
        }
        header = json.dumps(header)
        header_len = struct.pack('i', len(header))
        cli.send(header_len)
        cli.send(header.encode("utf-8"))
        with open(filename, "rb") as f:
            data = f.read()
            cli.sendall(data)
        print("[I] Send config file to server [%s] success." % svr.remark)
        cli.close()
        suc += 1
    print("[I] %d/%d successfully synced." % (suc, total))


def node_added(address, remark):
    cli = socket(AF_INET, SOCK_STREAM)
    try:
        cli.connect((address, 40001))
    except Exception as e:
        print("[E] Adding node server failed: %s" % str(e))
        return -1
    header = {"command": "node_added"}
    header = json.dumps(header)
    header_len = struct.pack('i', len(header))
    cli.send(header_len)
    cli.send(header.encode("utf-8"))
    data = cli.recv(1024).decode("utf-8")
    if data == "ack":
        print("[I] Confirmed")
        print("[I] Adding node: %s(%s)..." % (address, remark), end='')
        svr = Server(address, remark)
        db.session.add(svr)
        db.session.commit()
        print("done.")
    else:
        print(data)
    cli.close()


def list_nodes():
    svrs = Server.query.all()
    for svr in svrs:
        print("%02d: %s %s" % (svr.id, svr.address, svr.remark))


def del_node(id):
    Server.query.filter_by(id=id).delete()
    db.session.commit()
    print("Server with id: %d has been deleted" % id)

def list_nodes_status():
    svrs = Server.query.all()
    svrs_status = []
    for i, svr in enumerate(svrs):
        svr_status = node_status(svr)
        svrs_status.append(svr_status)
    return svrs_status

def node_status(svr):
    cli = socket(AF_INET, SOCK_STREAM)
    cli.settimeout(5)
    print("[I] Start getting node status: %s(%s)..." % (svr.address, svr.remark), end='')
    try:
        cli.connect((svr.address, 40001))
    except Exception as e:
        print('[E] Send config file to server [%s] failed: %s' % (svr.remark, str(e)))
        return -1

    header = {"command": "node_status"}
    header = json.dumps(header)
    header_len = struct.pack('i', len(header))
    cli.send(header_len)
    cli.send(header.encode("utf-8"))
    print("[I] Send CMD to server [%s] success." % svr.remark)

    data_len = cli.recv(4)
    if data_len:
        print("[I] Ready to receive data.")
    data_len = struct.unpack('i', data_len)[0]
    data = cli.recv(data_len).decode("utf-8")
    data = {**json.loads(data), **{"remark": svr.remark, "address":svr.address}}
    cli.close()
    print("[I] Received data")
    return data
