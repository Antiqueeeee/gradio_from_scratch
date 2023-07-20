#进阶用法
#   Interface状态
#       可以使用全局变量存储数据，方便业务逻辑中交互
import gradio
import random
scores = list()
def track_score(score):
    scores.append(score)
    top_scores = sorted(scores,reverse=True)[:3]
    return top_scores

demo = gradio.Interface(fn=track_score,inputs=gradio.Number(label="Score"),outputs=gradio.JSON(label="Top three scores"))

#   会话状态
#       Gradio支持的另一种数据持久性是会话状态，数据在一个页面会话中的多次提交中持久存在。
#       典型应用就是聊天机器人,数据不会在用户之间共享.你想访问用户之前提交的信息,
#       但不能将聊天记录存储在一个变量中,否则用户之间的数据会乱作一团
#       要在会话状态下存储数据需要做三件事:
#           在函数中传入一个额外的参数,代表界面的状态.
#           在函数最后,将状态的更新值作为一个额外的返回值返回.
#           在添加输入和输出时添加state组件

def chat(message,history):
    history = history or []
    message = message.lower()
    if message.startswith("how many"):
        response = random.randint(1, 10)
    elif message.startswith("how"):
        response = random.choice(["Great", "Good", "Okay", "Bad"])
    elif message.startswith("where"):
        response = random.choice(["Here", "There", "Somewhere"])
    else:
        response = "I don't know"
    history.append((message,response))
    return history,history

chatbot = gradio.Chatbot().style(color_map=("green","pink"))
demo = gradio.Interface(fn=chat,inputs=["text","state"],outputs=[chatbot,"state"],allow_flagging="never")

#   interface交互
#       1.Interface(live=True)
#       2.输入是视频流、音频流时，可以使用streaming模型
import numpy as np
def flip(image):
    return np.flipud(image)
demo = gradio.Interface(
    fn = flip
    ,inputs = gradio.Image(source="webcam",streaming=True)
    ,outputs = "image"
    ,live = True
)

# app,local_url,share_url = demo.launch()


#   自定制组件：Blocks构建应用
#   Blocks可以用于设计更灵活布局的数据流和网络应用。
#   Blocks中，允许控制组件在页面上出现的位置，处理复杂的数据流
#   比如输出可以作为其他函数的输入，并根据用户交互更新组件的属性和可见性
#   也可以定制更多组件   https://gradio.app/docs/

def greeting(name):
    return f"Hello {name} !"
with gradio.Blocks() as demo:
    name = gradio.Textbox(label="name")
    output = gradio.Textbox(label="output box")
    greet_btn = gradio.Button("Greet")
    greet_btn.click(fn=greeting,inputs=name,outputs=output)




#   多选项卡应用
import numpy as np
def flip_text(x):
    return x[::-1]
def flip_image(x):
    return np.fliplr(x)
with gradio.Blocks() as demo:
    gradio.Markdown("Flip text or image files using this demo.")
    # 一个Tab就是一个选项卡
    with gradio.Tab("Flip Text"):
        # Row Column用来布局
        with gradio.Row():
            text_input = gradio.Textbox()
            text_output = gradio.Textbox()
        with gradio.Column():
            text_button = gradio.Button("Flip")
    with gradio.Tab("Flip Image"):
        with gradio.Row():
            image_input = gradio.Image()
            image_output = gradio.Image()
        image_button = gradio.Button("Flip")
    
    with gradio.Accordion("Open for More!"):
        gradio.Markdown("Look at me...")
    text_button.click(flip_text,inputs=text_input,outputs=text_output)
    image_button.click(flip_image,inputs=image_input,outputs=image_output)


#   Flagging标记
#       用户测试时，可是使用flagging标记将发生错误的输入返回给开发者
#       导致错误的输入会保存在一个csv文件中，保存路径由Interface的flagging_dir参数指定，默认为“flagged”

#   样式
#       Gradio可以给不同组件加.style 如 image.style ，可以获取该组件的样式参数设置样例。
#       （好像已经被舍弃了）
# ```python
# img = gradio.Image("lion.jpg").style(height='24', rounded=False)
# ```




#   队列
#       如果函数推理时间较长，或者应用程序处理流量过大，需要使用queue方法进行排队。
#       queue方法使用websockets，可以防止网络超时。
# ```python
# demo = gr.Interface(...).queue()
# demo.launch()
# #或
# with gr.Blocks() as demo:
#     #...
# demo.queue()
# demo.launch()
# ```

#   生成器
#       如果需要显示一连串的输出，比如图像生成模型，显示各个步骤生成的图像，从而得到最终的图像
#       此时可以向Gradio提供一个生成器函数
import numpy as np
import time
def fake_diffusion(steps):
    for i in range(steps):
        time.sleep(1)
        image = np.random.randint(255,size=(200,200,3))
        yield image
demo = gradio.Interface(fn=fake_diffusion,inputs=gradio.Slider(minimum=1,maximum=10,value=3,step=1),outputs="image")
demo.queue()


#Blocks进阶使用
#   任何输入组件中的内容都是可编辑的，但是输出组件默认不可编辑，
#   可以设置interactivate=True，即可更改输出组件中的内容
def greet(name):
    return "Hello " + name + "!"
with gradio.Blocks() as demo:
    name = gradio.Textbox(label="Name")
    # 不可交互
    # output = gr.Textbox(label="Output Box")
    # 可交互
    output = gradio.Textbox(label="Output", interactive=True)
    greet_btn = gradio.Button("Greet")
    greet_btn.click(fn=greet, inputs=name, outputs=output)


#   可以为不同组件设置不同时间，如在输入组件中添加change事件。
#   具体可以添加那些时间需要查看官方文档
#   （怎么change？修改输入框中内容也没反应啊？）
def greeting(name):
    return f"Welcome to Gradio, {name}!"
with gradio.Blocks() as demo:
    gradio.Markdown(
        """
        Hello World !
        Start typing below to see the output.
        """
    )
    inputs = gradio.Textbox(placeholder="What is your name? ")
    outputs = gradio.Textbox()
    inputs.change(fn = greeting,inputs=inputs,outputs=outputs)

#   多数据流
def increase(num):
    return num + 1
with gradio.Blocks() as demo:
    num1 = gradio.Number(label="num1")
    num2 = gradio.Number(label="num2")
    atob = gradio.Button("b > a")
    atob.click(fn=increase,inputs=num1,outputs=num2)
    
    btoa = gradio.Button("a > b")
    btoa.click(fn=increase,inputs=num2,outputs=num1)

#   多输出值
def eat(food):
    if food > 0:
        return food - 1 , "full"
    else:
        return 0, "hungry"
with gradio.Blocks() as demo:
    food_box = gradio.Number(value=10,label="Food Count")
    status_box = gradio.Textbox()
    gradio.Button("EAT").click(fn=eat,inputs=food_box,outputs=[food_box,status_box])
    

#   组件配置修改
#       事件监听器函数的返回值通常是相应的输出组件的更新值。有时可能会需要更新组件的配置，比如可见性
#       可以通过返回update函数更新组件的配置
#       (这个update是怎么找到组件的？嗷嗷，radio.change | 谁的值变了就更新谁？ )
def change_textbox(choice):
    method = {
        "short" : gradio.update(lines=2,visible=True,value="Short story:")
        ,"long" : gradio.update(lines=8,visible=True,value="Long story:")
    }
    return method.get(choice,gradio.update(visible=False))
with gradio.Blocks() as demo:
    radio = gradio.Radio(["short","long","none"],label="Essay Length to Write?")
    text = gradio.Textbox(lines=2,interactive=True)
    radio.change(fn=change_textbox,inputs=radio,outputs=text)

#   组件水平排列
#       with gradio.Row():
#           ....

#   组件垂直排列
#       with gradio.Column():
#
#       Column有scale参数，表示与相邻列相比的相对宽度，总之就是数越大的组件越大
#             有min_width参数，表示最小宽度，防止列太窄

#   组件可视化
#       可以通过visible和update来构建更为复杂的应用
with gradio.Blocks() as demo:
    # 出错提示框
    error_box = gradio.Textbox(label="Error", visible=False)
    # 输入框
    name_box = gradio.Textbox(label="Name")
    age_box = gradio.Number(label="Age")
    symptoms_box = gradio.CheckboxGroup(["Cough", "Fever", "Runny Nose"])
    submit_btn = gradio.Button("Submit")
    # 输出不可见
    with gradio.Column(visible=False) as output_col:
        diagnosis_box = gradio.Textbox(label="Diagnosis")
        patient_summary_box = gradio.Textbox(label="Patient Summary")
    def submit(name, age, symptoms):
        if len(name) == 0:
            return {error_box: gradio.update(value="Enter name", visible=True)}
        if age < 0 or age > 200:
            return {error_box: gradio.update(value="Enter valid age", visible=True)}
        return {
            output_col: gradio.update(visible=True),
            diagnosis_box: "covid" if "Cough" in symptoms else "flu",
            patient_summary_box: f"{name}, {age} y/o"
        }
    submit_btn.click(
        submit,
        [name_box, age_box, symptoms_box],
        [error_box, diagnosis_box, patient_summary_box, output_col],
    )

#   组件渲染：将用户选中作为输入
#       假设需要在gradio.Textbox上方显示gradio.examples示例
#       由于gradio.Examples需要输入组件对象作为参数，因此需要先定义输入组件
#       然后在定义gradio.Examples对象后再进行渲染。
#       解决方法是：在gradio.Blocks()范围外定义gradio.Textbox，并在UI中希望放置的
#       任何位置使用组件的.render()方法
input_textbox = gradio.Textbox()
with gradio.Blocks() as demo:
    gradio.Examples(["hello","bonjour","merhaba"],input_textbox)
    input_textbox.render()


#   自定义css
#       Blocks(css="...") as demo
#
#       可以设置css属性，将任何样式应用于应用程序


#   元素选择
#       可以通过elem_id为组件指定id，这样css就可以定位到元素并进行相应渲染
with gradio.Blocks(css="#warning {background-color: red}") as demo:
    box1 = gradio.Textbox(value="Good Job", elem_id="warning")
    box2 = gradio.Textbox(value="Failure")
    box3 = gradio.Textbox(value="None", elem_id="warning")

#   互联网分享
#       demo.launch中设置share=True，会分配一个地址，有效期内免费

#   huggingface托管
#       可以将gradio模型部署到HuggingFace的Space托管空间中，完全免费
#       （1）注册HuggingFace账号，https://huggingface.co/join
#       （2）在Space空间中创建项目：https://huggingface.co/spaces
#       （3）创建好的项目有一个Readme文档，根据操作说明编辑app.py和requirements.txt文件

#   局域网分享
#       demo.launch中设置server_name="0.0.0.0"，server_port=7860即可访问

#   密码验证
#       首次打开网页前，可以设置账户密码
#       demo.launch(auth=("username","password"))

app,local_url,share_url = demo.launch()
