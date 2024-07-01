# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 19:57:01 2024

@author: JtekG
"""

import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit.components.v1 import html
import json
import os

st.set_page_config(page_title='CT-07 Remote Screener',  page_icon='https://noctrixhealth.com/wp-content/uploads/2021/05/cropped-SiteIcon-32x32.jpg')



# def send_email(user_id, results, network_type):
#     email = "ct_07@noctrixhealth.com"
#     password = os.environ.get("EMAIL_PASSWORD", "password")  # Preferably use environment variable

#     message = MIMEMultipart()
#     message["From"] = email
#     message["To"] = email
#     message["Subject"] = f"Speed Test Results for User ID: {user_id} - {network_type}"

#     body = f"""
#     Speed Test Results for User ID: {user_id} on {network_type}:
#     Download Speed: {results['download']} Mbps
#     Upload Speed: {results['upload']} Mbps
#     Ping: {results['ping']} ms
#     Jitter: {results['jitter']} ms
#     """

#     message.attach(MIMEText(body, "plain"))

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(email, password)
#         server.sendmail(email, email, message.as_string())

# Get user_id from URL parameter
params = st.query_params.to_dict()
st.image('https://noctrixhealth.com/wp-content/uploads/2023/07/noctrix-horiz-logo-tipo.svg')
st.title("Nidra Internet Speed Test")

st.write(f"{params['patientName']}, Thank you for following the link to your titration system test.  Dr. {params['doctorName']} has sent a prescription for a remote titraion for your Nidra Therapya and this link will help your specialist, {params['specialistName']}, determine if you have the connectivitiy required to compleet this process in your home.")


# JavaScript code to interact with OpenSpeedTest and send results back to Streamlit
js_code = """
<!--OST Widget code start--><div style="text-align:right;"><div style="min-height:360px;"><div style="width:100%;height:0;padding-bottom:50%;position:relative;"><iframe style="border:none;position:absolute;top:0;left:0;width:100%;height:100%;min-height:360px;border:none;overflow:hidden !important;" src="//openspeedtest.com/speedtest?run=0"></iframe></div></div></a></div><!-- OST Widget code end -->
"""

# Embed OpenSpeedTest
html(js_code, height=400)

st.write(f"Once the test is complete, please click this link to send the results to {params['specialistName']}.")
sent = st.button("Send Results")

if sent:
    st.balloons()
    st.info("Please disable Wi-Fi and repat the test using cellular data.")
    cellular = st.button("Click after using cellular")
    if cellular:
        st.rerun()




# # JavaScript code to listen for messages from the iframe
# st.markdown("""
# <script>
# window.addEventListener('message', function(e) {
#     if (e.data.type === 'FROM_OPENSPEEDTEST') {
#         window.Streamlit.setComponentValue(JSON.stringify(e.data.data));
#     }
# }, false);
# </script>
# """, unsafe_allow_html=True)

# st.session_state

# # Listen for results from JavaScript
# if 'test_results' not in st.session_state:
#     st.session_state.test_results = None

# component_value = st.components.v1.get_component_value()
# if component_value is not None:
#     st.session_state.test_results = json.loads(component_value)

# if st.session_state.test_results:
#     results = st.session_state.test_results
#     results_placeholder.write("Speed Test Results:")
#     results_placeholder.write(f"Download Speed: {results['download']} Mbps")
#     results_placeholder.write(f"Upload Speed: {results['upload']} Mbps")
#     results_placeholder.write(f"Ping: {results['ping']} ms")
#     results_placeholder.write(f"Jitter: {results['jitter']} ms")

#     if st.button("Send Results for Current Network"):
#         send_email(user_id, results, "Current Network")
#         st.success(f"Results for User ID: {user_id} sent to ct_07@noctrixhealth.com")

# st.write("Please switch to your cellular network and run the test again.")

# if st.button("Run Test on Cellular Network"):
#     st.session_state.test_results = None
#     st.experimental_rerun()