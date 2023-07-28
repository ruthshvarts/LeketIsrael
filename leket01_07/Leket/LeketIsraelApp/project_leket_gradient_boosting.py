import sqlite3
import pandas as pd
import pandasql as ps
from django.contrib.auth.models import User
from django.conf import settings

def run():
    all_records = User.objects.all()
    # print("Connection Successful",conn)
    results = []
    for user in all_records:
        results.append(user.username)
    return results


print('------------------ Here are the users in USER database: ------------------')
results = run()
for name in results: print(name)
