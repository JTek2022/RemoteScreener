import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit.components.v1 import html

# Function to send email
def send_email(subject, body):
    sender_email = "remotetitration@gmail.com"  # Replace with your email
    receiver_email = "remotetitration@gmail.com"
    password = "CT_07_Email"  # Replace with your email password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(message)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 0

if 'test_results' not in st.session_state:
    st.session_state.test_results = []

# Page 0: Introduction
if st.session_state.page == 0:
    st.title("Bandwidth Test")
    st.write("We need to perform the measurement in the same area where the study would be conducted.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, I'm in the correct area"):
            st.session_state.page = 1
    with col2:
        if st.button("No, I'm not in the correct area"):
            st.error("Please revisit this link when you are in the correct area for testing.")

# Page 1: Speed Test
elif st.session_state.page == 1:
    st.title("Speed Test")
    st.write("Please perform the speed test using the tool below:")
    
    # JavaScript code to interact with OpenSpeedTest and send results back to Streamlit
    js_code = """
    <!--OST Widget code start--><div style="text-align:right;"><div style="min-height:360px;"><div style="width:100%;height:0;padding-bottom:50%;position:relative;"><iframe style="border:none;position:absolute;top:0;left:0;width:100%;height:100%;min-height:360px;border:none;overflow:hidden !important;" src="//openspeedtest.com/speedtest?run=0"></iframe></div></div></a></div><!-- OST Widget code end -->
    """

    # # Embed OpenSpeedTest
    html(js_code, height=400)
    
    with st.form("speed_test_form"):
        download = st.number_input("Download Speed (Mbps)", min_value=0.0, step=1.0)
        upload = st.number_input("Upload Speed (Mbps)", min_value=0.0, step=1.0)
        ping = st.number_input("Ping (ms)", min_value=0, step=1)
        jitter = st.number_input("Jitter (ms)", min_value=0, step=1)
        
        if st.form_submit_button("Submit"):
            st.session_state.test_results.append({
                "download": download,
                "upload": upload,
                "ping": ping,
                "jitter": jitter
            })
            st.session_state.page = 2

# Page 2: Connection Type
elif st.session_state.page == 2:
    st.title("Connection Type")
    connection_type = st.radio("How are you connected to the internet?", ["WiFi", "Mobile Data", "Unsure"])
    
    if connection_type == "WiFi":
        st.warning("Please disable WiFi and repeat the test on Mobile Data.")
        if st.button("I've switched to Mobile Data"):
            st.session_state.page = 1
    elif connection_type == "Mobile Data":
        wifi_available = st.radio("Is WiFi available at your location?", ["Yes", "No"])
        if wifi_available == "Yes":
            st.info("Please repeat the test on WiFi.")
            if st.button("I've switched to WiFi"):
                st.session_state.page = 1
        else:
            st.session_state.page = 3
    else:  # Unsure
        st.warning("Please try to determine your connection type and select either WiFi or Mobile Data.")
        if st.button("I've determined my connection type"):
            st.session_state.page = 2

# Page 3: Results and Email
elif st.session_state.page == 3:
    st.title("Test Results")
    for i, result in enumerate(st.session_state.test_results):
        st.write(f"Test {i+1}:")
        st.write(f"Download: {result['download']} Mbps")
        st.write(f"Upload: {result['upload']} Mbps")
        st.write(f"Ping: {result['ping']} ms")
        st.write(f"Jitter: {result['jitter']} ms")
        st.write("---")
    
    if st.button("Send Results"):
        subject = "Bandwidth Test Results"
        body = "Bandwidth Test Results:\n\n"
        for i, result in enumerate(st.session_state.test_results):
            body += f"Test {i+1}:\n"
            body += f"Download: {result['download']} Mbps\n"
            body += f"Upload: {result['upload']} Mbps\n"
            body += f"Ping: {result['ping']} ms\n"
            body += f"Jitter: {result['jitter']} ms\n\n"
        
        try:
            send_email(subject, body)
            st.success("Test results have been sent successfully!")
        except Exception as e:
            st.error(f"An error occurred while sending the email: {str(e)}")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.page > 0 and st.button("Previous"):
        st.session_state.page -= 1
with col2:
    if st.session_state.page < 3 and st.button("Next"):
        st.session_state.page += 1











# -*- coding: utf-8 -*-
# """
# Created on Sun Jun 30 19:57:01 2024

# @author: JtekG
# """

# import streamlit as st
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from streamlit.components.v1 import html
# import json
# import os

# st.set_page_config(page_title='CT-07 Remote Screener',  page_icon='https://noctrixhealth.com/wp-content/uploads/2021/05/cropped-SiteIcon-32x32.jpg')



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
#params = experimental_get_query_params() #st.query_params.to_dict()
# params = {'patientName':'Stephanie', 'doctorName':'Clayton','specialistName':'Leticia'}

# st.image('https://noctrixhealth.com/wp-content/uploads/2023/07/noctrix-horiz-logo-tipo.svg')
# st.title("Nidra Internet Speed Test")

# st.write(f"{params['patientName']}, Thank you for following the link to your titration system test. Dr. {params['doctorName']} has sent a prescription for a remote titration for your Nidra Therapy, and this link will help your specialist, {params['specialistName']}, determine if you have the connectivity required to complete this process in your home.")


# # JavaScript code to interact with OpenSpeedTest and send results back to Streamlit
# js_code = """
# <!--OST Widget code start--><div style="text-align:right;"><div style="min-height:360px;"><div style="width:100%;height:0;padding-bottom:50%;position:relative;"><iframe style="border:none;position:absolute;top:0;left:0;width:100%;height:100%;min-height:360px;border:none;overflow:hidden !important;" src="//openspeedtest.com/speedtest?run=0"></iframe></div></div></a></div><!-- OST Widget code end -->
# """

# # Embed OpenSpeedTest
# html(js_code, height=400)

# st.write(f"Once the test is complete, please click this link to send the results to {params['specialistName']}.")
# sent = st.button("Send Results")

# if sent:
#     st.balloons()
#     st.info("Please disable Wi-Fi and repat the test using cellular data.")
#     cellular = st.button("Click after using cellular")
#     if cellular:
#         st.rerun()




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
