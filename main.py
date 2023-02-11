from rklib.network import connect_router, setup_ap
from OTTOServer import OTTOServer

# STA mode: Usually use this mode at home.
# connect_router('SSID', 'password')  # Please replace the SSID and password according to your network environment.

# AP mode: Usually use this mode when no accessible WIFI network.
setup_ap('OTTO_on_ESP', 'otto1234')  # You may change the SSID and the password for your need.

# setup and start the OTTO web server which hosts a console page to enable you to control your OTTO by web browser.
OTTOServer.setup()
OTTOServer.start()
