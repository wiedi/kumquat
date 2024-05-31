#!/usr/bin/env python

from django.conf import settings
from subprocess import check_output
import os
import json
import socket


def meminfo():
		try:
			out = check_output(["kstat", "-p", "memory_cap:*:*:"]).decode("utf-8").strip()
			mem = dict([(x[0].split(':')[-1], x[1]) for x in (l.split() for l in out.split("\n"))])
			return {
				'mem_cap':   int(mem['physcap']),
				'mem_used':  int(mem['rss']),
				'mem_free':  int(mem['physcap']) - int(mem['rss']),
				'mem_use':   int((int(mem['rss']) / float(mem['physcap'])) * 100),

				'swap_cap':  int(mem['swapcap']),
				'swap_used': int(mem['swap']),
				'swap_free': int(mem['swapcap']) - int(mem['swap']),
				'swap_use':  int((int(mem['swap']) / float(mem['swapcap'])) * 100),

				'mem_nover': mem['nover'],
			}
		except:
			return {}

def sysinfo():
		try:
			return json.loads(check_output(["sysinfo"]).decode("utf-8"))
		except:
			return {}

def imageinfo():
		try:
			return dict(l.split(': ') for l in open('/etc/product').read().strip().split('\n'))
		except:
			return {}

def diskinfo():
		if settings.KUMQUAT_USE_ZFS:
				vals = check_output(["zfs", "list", "-pH", "/"]).split(b'\t')
				size = int(vals[1]) + int(vals[2])
				used = int(vals[1])
				free = int(vals[2])
		else:
				out = check_output(["df", "-k", "/"]).strip().split(b'\n')
				vals = out[-1].split()
				size = int(vals[1]) * 1024
				used = int(vals[2]) * 1024
				free = int(vals[3]) * 1024

		return {
				'size': size,
				'used': used,
				'free': free,
				'use':  int((used / size) * 100)
		}

def info():
		sys = sysinfo()
		img = imageinfo()
		return {
				'mem':        meminfo(),
				'disk':       diskinfo(),
				'loadavg':    os.getloadavg(),
				'cpu_cores':  sys.get('CPU Total Cores', ''),
				'live_image': sys.get('Live Image', ''),
				'hostname':   socket.gethostname(),
				'image':      img.get('Image'),
				'base_image': img.get('Base Image', '').replace(' ', '-'),
		}
