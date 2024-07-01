import streamlit as st
import time
import os, sys
from libraries.load_data import load_data
from libraries.result_true import result_true
import subprocess
import warnings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

warnings.filterwarnings("ignore") # subprocess오류 무시

###################### page 구성 #########################################


st.set_page_config(
    page_title = "Test",
    page_icon = "⚙️",
    layout = "wide"
)

st.title('배터리 셀 이상치 탐지')

col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("데이터 선택")
    st.caption("*데이터를 선택해주세요*.")
    st.markdown(
        """
        <style>
        [data-baseweb="select"] {
            margin-top: -50px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    ) # st.selectbox 띄어쓰기 없애기
    option = st.selectbox("", 
                        options = ('','1','2','3','4','5','6','7','8')
                        )  
    cmd = [f"{sys.executable}", os.path.join(os.getcwd(), 'Modeling', 'run.py'), str(option)]
    test = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)

# 같은 자리에 버ㅓ튼이 바뀜 근데 그냥 버튼 새로 만드는게 좋을 듯.

if 'test' not in st.session_state:
    st.session_state.test = False

def start_click():
    st.session_state.test = True
    # st.session_state.test = not st.session_state.test
    
def end_click():
    st.session_state.test = False
    with st.sidebar:
        warn = st.warning("분석이 취소되었습니다. 다시 시도하세요.")
        time.sleep(2)
        warn.empty()
    
with col2:
    if option != '':
        st.subheader(f"{option}번")
    else:
        st.subheader("데이터를 선택하세요")
    st.caption("*분석을 시작하세요*.")
    button = st.empty()
    start = button.button('분석 시작', on_click = start_click)
    if start:
        if option != "":
            button.empty()
            end = button.button('분석 중단', on_click = end_click)
        else:
            warn = st.warning("데이터를 선택하세요")
            end_click()
            warn.empty()



with st.sidebar:
    before = st.info("시험 전입니다.")

####################### test 시작 ############################
if start and st.session_state.test:
    data = load_data(str(option))
    with st.sidebar:
        before.empty()
        during = st.warning("시험 중입니다.")
        
    # 실시간 plot
    placeholder = st.empty()
    
    for seconds in range(len(data)//100):
        df = data.iloc[:100 * (seconds + 1), :]
    
        with placeholder.container():
            # columns 만들기
            plot1, plot2 = st.columns(2)

            # fill in columns
            with plot1:
                st.markdown("### Voltage Chart")
                TIME = df.iloc[:, 1]
                TIME = pd.to_datetime(TIME)
                CV = df.iloc[:, 23 : 199]
                fig, ax = plt.subplots(figsize = (6,5))
                
                # plt.style.use(['ggplot'])
                for i in CV.columns:
                    plt.plot(TIME, CV[i], linewidth = 1)
                ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                plt.xticks(rotation=45)
                plt.xlabel("Time")
                plt.ylabel("Voltage")
                plt.ylim(min(CV.min() * 0.99), max(CV.max()) * 1.01)
                st.pyplot(fig)
                
            with plot2:
                st.markdown("### Temperature Chart")
                TE = df.iloc[:, 199 : 231]
                fig2, ax = plt.subplots(figsize = (6,5))
                
                # plt.style.use(['ggplot'])
                for i in TE.columns:
                    plt.plot(TIME, TE[i], linewidth = 1)
                ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                plt.xticks(rotation=45)
                plt.xlabel("Time")
                plt.ylabel("Temperature")
                plt.ylim(min(TE.min() * 0.9), max(TE.max()) * 1.1)
                st.pyplot(fig2)
            time.sleep(0.2)
    
    test.communicate()
    if result_true():
        test = None
        st.session_state.test = False
        with st.sidebar:
            during.empty()
            st.success("분석이 끝났습니다.")

else:
    test.kill()    
    

    # test.kill()

        
    
# st.write(error)    



    

# if start_b and option != "":
#     test.communicate() 
    


# if st.button("분석 시작") and option != "": 
#     test.communicate()
    

# with st.sidebar:
#     if all(df) != None:
#         st.info("데이터로드 성공") 
#     with st.spinner("분석중"):
#         time.sleep(3)
#     st.success("끝났습니다. 결과를 확인하세요.")



