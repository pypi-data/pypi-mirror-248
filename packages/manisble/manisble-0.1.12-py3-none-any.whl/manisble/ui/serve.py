import os
import sys
from ..common import prettyllog




def main():
    prettyllog("ui", "ui", "ui", "new", "000", "ui")
    manisble_ui_port  = os.environ.get("MANISBLE_UI_PORT", "8000")
    manisble_ui_host = os.environ.get("MANISBLE_UI_HOST", "manisble.openknowit.com")
    manisble_ui_debug = os.environ.get("MANISBLE_UI_DEBUG", "True")
    manisble_


                          
