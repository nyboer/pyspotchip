#!/usr/bin/env python

from __future__ import print_function
import liblo, sys

# send all messages to port 4242 on the local machine

def oscsend(path,val):
    port = 4242
    target = liblo.Address(port)
    msg = liblo.Message('/spot'+path)
    msg.add(val)
    liblo.send(target,msg)
