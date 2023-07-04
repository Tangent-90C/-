import streamlit
import streamlit.web.cli
from streamlit.web import bootstrap

if __name__ == '__main__':
    streamlit._is_running_with_streamlit = True
    print('寡人最近这几周，时间紧任务重，忙着期末考试和接踵而至的Hackathon比赛，没空完善和开发剩下功能了，先凑合着用。')
    print('体验网址：http://127.0.0.1:8501')
    print('打开后会有6个warning，这是没开发完导致的，不用管它，只要你不使用还未开发的功能就行。')
    bootstrap.run('前端.py', 'streamlit run', [], {})