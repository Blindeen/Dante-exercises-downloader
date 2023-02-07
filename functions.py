import requests

subjects = {
    'Dante1': '25',
    'Dante2': '27',
    'SO2': '29'
}

urls = {
    'units_url': 'https://dante.iis.p.lodz.pl/api/student/topicbrowser/getTopics?subjectid=',
    'tasks_url': 'https://dante.iis.p.lodz.pl/api/student/taskbrowser/getTasks?subjectid=',
    'reply_url': 'https://dante.iis.p.lodz.pl/api/student/reply/getReplyHistory?subjectid='
}


def fetch_units(cookies, url, subject_id):
    rq = requests.get(url + subject_id, cookies=cookies)
    units = rq.json()
    return units['Entries']


def fetch_tasks(cookies, url, subject_id, topic_id):
    fetch_url = url + subject_id + '&topicid=' + topic_id
    rq = requests.get(fetch_url, cookies=cookies)
    tasks = rq.json()
    return tasks['Entries']
