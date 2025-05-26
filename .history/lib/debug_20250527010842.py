#!/usr/bin/env python3

from lib.models import Base, engine, session, User, Client, Job, Payment
import ipdb

#  Ensure tables are created
Base.metadata.create_all(engine)

print("\n✅ Loaded. Type `exit` or press Ctrl+D to quit.")
ipdb.set_trace()
