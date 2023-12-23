from os import environ
environ["aquaref.LOG.ENABLE"] = "true"

from aquaref.winforms.metro import *
from aquaref import *

from os import environ

window = MetroForm()
window.Title = "aquaref.Metro"

tooltip = MetroToolTip()

tab = window.Create(MetroTab)
tab.Pack(Dock="Fill")

input = tab.CreatePage("Inputs")

button1 = input.Create(MetroButton)
button1.Text = "A Base Button"
button1.Pack(Dock="Top")

config = tab.CreatePage("Config")
system = config.Create(MetroButton)
system.Text = "System"
system.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("System"))
system.Pack(Dock="Top")

dark = config.Create(MetroButton)
dark.Text = "Dark"
dark.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("Dark"))
dark.Pack(Dock="Top")

light = config.Create(MetroButton)
light.Text = "Light"
light.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("Light"))
light.Pack(Dock="Top", Margin=10)

theme = config.Create(MetroLabel)
theme.Text = "Theme"
theme.Pack(Dock="Top")

window.StyleManager.Theme = "Dark"
window.StyleManager.Style = "Red"

window.AppRun()

SaveLog("test.metro.1.log")
