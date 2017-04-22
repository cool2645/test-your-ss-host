# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import config

apiKey = config.API_KEY
apiUrl = config.API_URL
tryMax = config.TRY_MAX
runHost = config.HOST_NAME


def get_queuing_job_list():
    r = requests.get(apiUrl + "/jobs/queue")
    queue = r.json()
    return queue


def assign_job(queue, count=0):
    if len(queue) > 0:
        payload = {'key': apiKey, 'run_host': runHost}
        r = requests.post(apiUrl + "/jobs/" + str(queue[0]['id']), params=payload)
        res = r.json()
        if res['result']:
            return {'id': res['id'], 'json': res['json'], 'docker': res['docker']}
        else:
            print(res['msg'])
            if count < tryMax:
                print("Retrying")
                return assign_job(get_queuing_job_list(), count + 1)
            else:
                print("Failed too many times, giving up")
                return False
    else:
        return False


def sync_log(id, log):
    payload = {'key': apiKey, 'log':  log}
    r = requests.post(apiUrl + "/jobs/" + str(id) + "/log", params=payload)
    res = r.json()
    if res['result']:
        return True
    else:
        print(res['msg'])
        return False


def cancel_job(id, count=0):
    payload = {'key': apiKey, '_method': 'DELETE'}
    r = requests.post(apiUrl + "/jobs/" + str(id), params=payload)
    res = r.json()
    if res['result']:
        return True
    else:
        print(res['msg'])
        if count < tryMax:
            print("Retrying")
            return cancel_job(id, count + 1)
        else:
            print("Failed too many times, giving up")
            return False


def call_judge(id):
    payload = {'key': apiKey}
    r = requests.get(apiUrl + "/jobs/" + str(id) + "/judge", params=payload)
    res = r.json()
    if res['result']:
        return True
    else:
        print(res['msg'])
        return False