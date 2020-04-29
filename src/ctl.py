import json
import time
from threading import Timer
import requests
from bs4 import BeautifulSoup as bs

requests.packages.urllib3.disable_warnings()

bs_lxml = lambda text: bs(text, 'lxml')

class CTL:
    def __init__(self):
        self.url = 'https://ctl.kduniv.ac.kr/'
        self.session = requests.Session()
        self.rooms = []
        self.lectures = []

    def login(self, id: str, pw: str):
        self.rooms = []
        self.session.get(f'{self.url}main/MainView.dunet', verify=False)
        res = self.session.post(
            f'{self.url}login/doGetUserCountId.dunet',
            data = {
                'user_id': id,
                'user_password': pw,
                'is_local': 'Y',
                'group_cd': 'UN'
            }
        )
        if 'alert' in res.text:
            return '로그인 실패'
        soup = bs_lxml(self.session.get(f'{self.url}main/MainView.dunet').text)
        for val in soup.find_all(attrs={'class': 'lecName'}):
            self.rooms.append([val.a.text.strip(), *val.a['id'].split('_')[1:]])
        return '로그인 성공'

    def enter_room(self, idx: int):
        self.lectures = []
        course_id = self.rooms[idx][1]
        class_no = self.rooms[idx][2]
        res = self.session.post(
            f'{self.url}lms/class/classroom/doViewClassRoom_new.dunet',
            data = {
                'mnid': '201008254671',
                'course_id': course_id,
                'class_no': class_no
            }
        )
        soup = bs_lxml(res.text)
        for lecture in soup.find_all(attrs={'class': 'lectureWindow'}):
            video = self.session.post(
                f'{self.url}lms/class/lectureWindow/doViewLectureWindow.dunet',
                data = {
                  'weekseq_no': lecture['weekseq_no'],
                  'review': lecture['review'],
                  'asp_id': 'ASP00001',
                  'contents_height': lecture['window_height'],
                  'tool_gubun': lecture['toolgubun'],
                  'contents_reg_method': lecture['regmethod'],
                  'study_able_status': 'STUDY',
                  'contents_id': lecture['contents_id'],
                  'contents_type': lecture['contents_type']
                }
            )
            soup = bs_lxml(video.text)
            form = soup.find('form', attrs={'id': 'preForm'})
            course_attend_log_no = form.find(attrs={'id': 'course_attend_log_no'})['value']
            course_study_time = form.find(attrs={'id': 'course_study_time'})['value']
            basic_time = form.find(attrs={'id': 'basic_time'})['value']
            max_study_time = int(basic_time) - int(course_study_time) / 60
            if int(course_study_time) < int(basic_time) * 60:
                self.lectures.append({
                    'course_attend_log_no': course_attend_log_no,
                    'weekseq_no': lecture['weekseq_no'],
                    'course_id': course_id,
                    'class_no': class_no,
                    'asp_id': 'ASP00001',
                    'study_time': 0,
                    'basic_time': basic_time,
                    'review': lecture['review'],
                    'study_able_status': '',
                    'max_study_time': max_study_time + 1
                })
        return True

    def run(self, state: dict):
        if (state['study_time'] < state['max_study_time']):
            self.session.post(
                f'{self.url}lms/class/lectureWindow/doUpdateTrackingProgress.dunet',
                data = {
                    'course_attend_log_no': state['course_attend_log_no'],
                    'weekseq_no': state['weekseq_no'],
                    'course_id': state['course_id'],
                    'class_no': state['class_no'],
                    'asp_id': state['asp_id'],
                    'study_time': f'{state["study_time"] * 60}',
                    'basic_time': state['basic_time'],
                    'progress_check_gubun': 'PROGRESSCHECKGUBUN_T',
                    'review': state['review'],
                    'study_able_status': state['study_able_status']
                }
            )
            state['study_time'] += 1
            Timer(60, self.run, [state]).start()
        else:
            return 'Study Finishied'

    def run_lecture(self, idx: int):
        p = len(self.lectures)
        if p == 0:
            return '이미 모든 강의가 완료되어있습니다'
        return self.run(self.lectures[idx])