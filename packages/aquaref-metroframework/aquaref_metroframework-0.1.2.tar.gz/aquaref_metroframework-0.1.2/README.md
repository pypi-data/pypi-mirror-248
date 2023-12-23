# aquaref
 `aquaref`是使用`.NET WinForms`开发的界面库

---

## 例子
```Python
from aquaref.winforms.metro import *
from aquaref import *

from os import environ

window = MetroForm()
window.Title = "aquaref.Metro"

tooltip = MetroToolTip()

tab = window.Create(MetroTab)
tab.Pack(Dock="Fill")

tab1 = tab.CreatePage("Tiles && Buttons")
button3 = tab1.Create(MetroButton)
button3.Text = "System"
button3.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("System"))
button3.Pack(Dock="Top")

tooltip.SetToolTip(button3, "Button3")

button2 = tab1.Create(MetroButton)
button2.Text = "Dark"
button2.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("Dark"))
button2.Pack(Dock="Top")
button2.ToolTip = "Button2"

button = tab1.Create(MetroButton)
button.Text = "Light"
button.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("Light"))
button.Pack(Dock="Top", Margin=10)

label = tab1.Create(MetroLabel)
label.Text = "Theme"
label.Pack(Dock="Top")

tab2 = tab.CreatePage("Options")

window.StyleManager.Theme = "Dark"
window.StyleManager.Style = "Red"

window.AppRun()
```

### 浅亮
![](light.png)

### 深黑
![](dark.png)

## 教程
### 基本窗口
```Python
from aquaref import Form
window = Form()
window.AppRun()
```

## 导入
默认`aquaref.__init__`是不会直接导入额外的组件库的

### MetroFramework
```python
import aquaref.winforms.metro as metro
```


## 打包
建议不要启用单文件