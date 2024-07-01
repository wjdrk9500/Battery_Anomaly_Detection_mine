import streamlit as st
from libraries.result_true import *
import plotly.express as px
from libraries.load_data import load_data

st.set_page_config(
    page_title = "Result",
    page_icon = "📋",
    layout = "wide"
)

st.title("결과 확인")

if not result_true():
    st.warning("test 페이지에서 시험을 진행하세요.")


else:
    tab1, tab2, tab3 = st.tabs(['score', 'Voltage', 'Temperature'])
    result = load_result()
    data = load_data(str(result['data_num'][2]))
    
    CV = data.iloc[:, 23 : 199]
    TE = data.iloc[:, 199 : 231]
    time = pd.to_datetime(data.iloc[:, 1])
    
    with tab1:
        with st.container():
            st.subheader("Anomaly score Chart")
            st.write("배터리 탐지 시험 결과 차트입니다.")  
            result['pred_name'] = result['pred'].map({0:'정상', 1:'비정상'})
            result.rename(columns={'Unnamed: 0':'idx'}, inplace=True)
            
            fig = px.line(result, y = "final_score", x = 'idx', color = "pred_name", 
                        color_discrete_map = {'정상' : 'blue',
                                                '비정상' : 'red'},
                        labels = {'final_score' : 'Anomaly-score',
                                  'pred_name' : '탐지결과',
                                  'idx' : 'Time'})
            st.plotly_chart(fig)
        
    with tab2:
        
        with st.container():
            fig1 = px.line(CV, x=time, y=CV.columns,
                           labels = {'x' : 'Time',
                                     'value' : 'Voltage'})

            pred = result['pred']

            start = None

            for i in range(len(pred)):
                if pred[i] == 1 and start is None:
                    start = time[i]
                if pred[i] == 0 and start is not None:
                    end = time[i]
                    fig1.add_vrect(x0=start, x1=end, fillcolor="green", opacity=0.25, line_width=0)
                    start = None

            if start is not None:
                fig1.add_vrect(x0=start, x1=time.iloc[-1], fillcolor="green", opacity=0.25, line_width=0)
            
            st.subheader("Voltage Chart")
            st.write("전압 차트와 함께 이상치 발생 부분을 확인할 수 있습니다.")
            st.plotly_chart(fig1)
                
    with tab3:
        with st.container():   
            fig2 = px.line(TE, x=time, y=TE.columns,
                           labels = {'x' : 'Time',
                                     'value' : 'Temperature'})
            
            start = None

            for i in range(len(pred)):
                if pred[i] == 1 and start is None:
                    start = time[i]
                if pred[i] == 0 and start is not None:
                    end = time[i]
                    fig2.add_vrect(x0=start, x1=end, fillcolor="green", opacity=0.25, line_width=0)
                    start = None

            if start is not None:
                fig2.add_vrect(x0=start, x1=time.iloc[-1], fillcolor="green", opacity=0.25, line_width=0)   
                
            st.subheader("Temperature Chart")
            st.write("온도 차트와 함께 이상치 발생 부분을 확인할 수 있습니다.")
            st.plotly_chart(fig2)
                
    st.button("새로운 데이터를 시험하세요!", on_click = remove_result)