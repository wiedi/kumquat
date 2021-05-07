# Copyright (C) 2006, 2007, 2010, 2011 Google Inc.
# Copyright (C) 2016 Sebastian Wiedenroth
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import time
import OpenSSL
import re
import datetime
from django.utils.timezone import get_fixed_timezone

#: ASN1 time regexp
_ASN1_TIME_REGEX = re.compile(r"^(\d+)([-+])(\d\d)(\d\d)$")

def parseAsn1Generalizedtime(value):
	"""
	Parses an ASN1 GENERALIZEDTIME timestamp as used by pyOpenSSL.

	@type value: string
	@param value: ASN1 GENERALIZEDTIME timestamp
	@return: datetime in UTC

	"""
	value = value.decode('utf-8')
	m = _ASN1_TIME_REGEX.match(value)
	if m:
		# We have an offset
		asn1time  = m.group(1)
		sign      = m.group(2)
		hours     = int(m.group(3))
		minutes   = int(m.group(4))
		utcoffset = 60 * hours + minutes
		if sign == '-':
			utcoffset = -utcoffset
	else:
		if not value.endswith("Z"):
			raise ValueError("Missing timezone")
		asn1time = value[:-1]
		utcoffset = 0
	parsed = time.strptime(asn1time, "%Y%m%d%H%M%S")
	return datetime.datetime(*(parsed[:7]), tzinfo=get_fixed_timezone(utcoffset))


def x509name_to_str(on):
	return ', '.join(b'='.join(x).decode() for x in on.get_components())

def serial_to_hex(serial):
	return ':'.join(map(''.join, zip(*[iter(hex(serial)[2:].strip('L')[::])]*2)))

