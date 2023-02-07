import requests

subjects = {
    'Dante1': '25',
    'Dante2': '27',
    'SO2': '29'
}


def fetch_units(cookies, url, subject_id):
    rq = requests.get(url + subject_id, cookies=cookies)
    return rq.json()


def fetch_tasks(cookies, url, subject_id, topic_id):
    fetch_url = url + subject_id + '&topicid=' + topic_id
    rq = requests.get(fetch_url, cookies=cookies)
    return rq.json()
