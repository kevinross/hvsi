#!/usr/bin/env python
import os
if '_devel' not in os.getcwd():
	os.chdir(os.path.expanduser('~/hvsi'))
import sys
sys.path.append('.')
from database import Session, AND


sessions = Session.select(AND(Session.q.user == None, Session.q.language != 'f'))
for i in sessions:
	i.destroySelf()
