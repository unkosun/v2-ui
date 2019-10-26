import logging
import time

import psutil

from util import cmd_util
from util.schedule_util import schedule_job

__node_status = {}
__node_last_access = time.time()
__node_last_get = time.time()
__node_access_interval = 0
__node_get_interval = 0
__node_last_ct = psutil.cpu_times()
__node_last_net_io = psutil.net_io_counters()


def get_status():
    global __node_last_access
    __node_last_access = time.time()
    return __node_status


def refresh_node_status():
    global __node_access_interval
    try:
        now = time.time()
        __node_access_interval = now - __node_last_access
        if __node_access_interval <= 60:
            global __node_get_interval, __node_last_get
            __node_get_interval = now - __node_last_get
            __node_last_get = now
            node_v2_status()
            __node_status['uptime'] = time.time() - psutil.boot_time()
            node_cpu()
            node_memory()
            node_disk()
            node_net()
    except Exception as e:
        logging.warning('Failed to get system status information: ' + str(e))


def node_v2_status():
    result, code = cmd_util.exec_cmd('systemctl is-active v2ray')
    results = result.split('\n')
    has_result = False
    for result in results:
        if result.startswith('active'):
            code = 0
            has_result = True
            break
        elif result.startswith('inactive'):
            code = 1
            has_result = True
            break

    if not has_result:
        code = 2
    __node_status['v2'] = {
        'code': code
    }


def node_cpu():
    global __node_last_ct
    cur_ct = psutil.cpu_times()

    last_total = sum(__node_last_ct)
    cur_total = sum(cur_ct)

    total = cur_total - last_total
    idle = cur_ct.idle - __node_last_ct.idle

    percent = (total - idle) / total * 100
    __node_last_ct = cur_ct
    __node_status['cpu'] = {
        'percent': percent
    }


def node_memory():
    mem = psutil.virtual_memory()
    __node_status['memory'] = {
        'used': mem.used,
        'total': mem.total
    }


def node_disk():
    d = psutil.disk_usage('/')
    __node_status['disk'] = {
        'total': d.total,
        'used': d.used
    }


def __node_get_net_tcp_udp_count():
    conns = psutil.net_connections()
    tcp_count = 0
    udp_count = 0
    for conn in conns:
        if conn.type == 1:
            tcp_count += 1
        elif conn.type == 2:
            udp_count += 1
    return tcp_count, udp_count


def node_net():
    global __node_last_net_io
    cur_net_io = psutil.net_io_counters()
    sent = cur_net_io.bytes_sent
    recv = cur_net_io.bytes_recv
    up = (sent - __node_last_net_io.bytes_sent) / __node_get_interval
    down = (recv - __node_last_net_io.bytes_recv) / __node_get_interval
    tcp_count, udp_count = __node_get_net_tcp_udp_count()
    __node_status['net_io'] = {
        'up': up,
        'down': down
    }
    __node_status['net_traffic'] = {
        'sent': sent,
        'recv': recv
    }
    __node_status['tcp_count'] = tcp_count
    __node_status['udp_count'] = udp_count
    __node_last_net_io = cur_net_io


schedule_job(refresh_node_status, 2)
