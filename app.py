import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit.components.v1 import html
from streamlit_geolocation import streamlit_geolocation
import plotly.express as px
import smtplib
from email.message import EmailMessage

def check_location(location):
    expected_location = {
        "latitude": None,
        "longitude": None,
        "altitude": None,
        "accuracy": None,
        "altitudeAccuracy": None,
        "heading": None,
        "speed": None
    }
    return location != expected_location

def send_email(location):
    # Email settings
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "remotetitration@gmail.com"
    receiver_email = "remotetitration@gmail.com"
    #password = "CT_07_Email"  # Remember to use an app-specific password
    password = "rinu mwtn tdhf zzvl"

    # Create the email content
    subject = "Current Location Information"
    body = f"""
    Your current location:
    Latitude: {location['latitude']}
    Longitude: {location['longitude']}
    Accuracy: {location['accuracy']} meters
    """

    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        st.success("📨 Email sent successfully!")
        st.balloons()
        st.info("💡Please return to the form, enter your result and continue to the next section.")
    except Exception as e:
        st.error(f"⚠️ An error occurred while sending the email: {e}")
        st.info("💡Please return to the form, enter your result and continue to the next section.")
    finally:
        server.quit()

st.markdown("# Nidra Geolocation App")
st.markdown("### We will use your location to determine cellular coverage.")
st.markdown("### Tap the button and then allow the app to know your location.")
st.markdown("""
<style>
div.stButton > button:first-child {
    font-size: 24px;
    padding: 20px 40px;
    height: auto;
    width: auto;
    min-width: 300px;
    white-space: normal;
}
</style>
""", unsafe_allow_html=True)
location = streamlit_geolocation()
#location
if check_location(location):
    st.write("Your current location:")
    st.write(f"Latitude: {location['latitude']}")
    lat = location['latitude']
    st.write(f"Longitude: {location['longitude']}")
    lon = location['longitude']
    st.info(f"📍Accuracy: {int(location['accuracy'])} meters")
    send_email(location)
    #fig = px.scatter_mapbox(lat=lat, lon=lon, zoom=10)
    #st.plotly_chart(fig)
    #st.map(data={"lat": [location['latitude']], "lon": [location['longitude']]})
    
# Display additional information if available
if location['altitude']:
    st.write(f"Altitude: {location['altitude']} meters")
if location['altitudeAccuracy']:
    st.write(f"Altitude Accuracy: {location['altitudeAccuracy']} meters")
if location['heading']:
    st.write(f"Heading: {location['heading']} degrees")
if location['speed']:
    st.write(f"Speed: {location['speed']} m/s")



#st.markdown("![Image](https://media.licdn.com/dms/image/C5612AQF9nqixPk6_sA/article-cover_image-shrink_720_1280/0/1643020458617?e=2147483647&v=beta&t=Cc_pg65PM_kod0jmrYKc7vRdGjzBaQ_ucjfIsoEe9mQ){width=10%}")
