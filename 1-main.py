
# https://mdnice.com/writing/a40f4bcd3b3e40d8931512186982b711

import gradio

def greeting(name):
    return "Hello" + name + "!"

# gradio基础模块
#   简易场景使用gradio.Interface    定制场景使用gradio.Blocks
#   输入输出包括：
#       gradio.Image    gradio.Textbox  gradio.DataFrame    gradio.Dropdown gradio.Number   gradio.Markdown gradio.Files
#   控制组件：
#       gradio.Button
#   布局组件：
#       gradio.Tab（标签页）    gradio.Row(行布局)  gradio.Column(列布局)

# Interface 类初始化需要fn、inputs、outputs三个参数进行初始化
#   fn 封装的函数
#   inputs 输入组件的类型   如text、image
#   outputs输出组件的类型   如text、image

demo = gradio.Interface(fn=greeting,inputs="text",outputs="text")


demo = gradio.Interface(
    fn = greeting
    ,inputs = gradio.Textbox(lines=3,placeholder="Name Here",label="my input")
    ,outputs = "text"
)


#多个输入和输出
#   输入列表中每个元素按顺序对应函数的一个参数
#   输出列表中每个元素按顺序排列对应与函数返回的一个值

def greeting(name,is_morning,temperautre):
    soluation = "Good morning" if is_morning else "Good evening"
    response = f"{soluation} {name}.It is {temperautre} degrees today"
    celsius = (temperautre - 32) * 5 / 9
    return response,round(celsius,2)

demo = gradio.Interface(
    fn = greeting
    ,inputs = ["text","checkbox",gradio.Slider(0,100)]
    ,outputs = ["text","number"]
)


# 图像组件
#   Gradio支持许多类型的组件，如Image、dataframe、video
import numpy as np
def sepia(input_img):
    sepia_filter = np.array([
        [0.393,0.769,0.189],
        [0.349,0.686,0.168],
        [0.272,0.534,0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

demo = gradio.Interface(fn=sepia,inputs=gradio.Image(shape=(200,200)),outputs="image")

#动态界面接口：简单计算器模板实时变化
#   Interface中添加live=True，只要输入发生变化，结果也随之改变
def calculator(num1,operation,num2):
    method = {
        "add" : lambda num1,num2 : num1 + num2
        ,"subtract" : lambda num1,num2 : num1 - num2 
        ,"multiply" : lambda num1,num2 : num1 * num2
        ,"divide" : lambda num1,num2 : num1 / num2
    }
    return method[operation](num1,num2)

demo = gradio.Interface(
    fn = calculator
    ,inputs = ["number",gradio.inputs.Radio(["add", "subtract", "multiply", "divide"]),"number"]
    ,outputs = "text"
    ,examples = [[5,"add",3],[4,"divide",2],[-4,"multiply",2.5],[0,"subtract",1.2]]
    ,title = "Toy Calculator"
    ,article = "Check out the examples"
    ,live = True
    )



#Interface.launch()
#   有app/local_url/share_url 三个返回值
#   app 为gradio演示提供支持的FastAPI应用程序
#   local_url   为本地地址
#   share_url   公共地址，当share=True时生成
app,local_url,share_url = demo.launch()