from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.uix.switch import Switch
from kivy.uix.dropdown import DropDown
from kivy.core.text import LabelBase
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import calendar
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import json
import telegram
import asyncio
from telegram.ext import Updater, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread
import requests
from kivy.uix.behaviors import DragBehavior
from kivy.properties import ObjectProperty, StringProperty
import os
import platform
import subprocess
from kivy.graphics import Color, Rectangle

class ImageButton(ButtonBehavior, Image):
    pass

class MyLabel(Label):
   def on_size(self, *args):
      self.text_size = self.size