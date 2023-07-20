import gradio
from transformers import pipeline


#文本分类demo

pipe = pipeline("text-classification")

def clf(text):
    result = pipe(text)
    label = result[0]["label"]
    score = result[0]["score"]
    res = {label:score,'POSITIVE' if label=='NEGATIVE' else 'NEGATIVE': 1-score}
    return res
demo = gradio.Interface(fn=clf,inputs="text",outputs="label")
gradio.close_all()

app,local_url,shar_url = demo.launch()
