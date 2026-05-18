from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="sk-ochgtwsfzxnhlmrhnoxhhejwzkfvmmwtkjgvcrbvqwobptxp",
    base_url="https://api.siliconflow.cn/v1"
)

HTML = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>AI论文助手</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; height: 150px; margin: 10px 0; padding: 10px; font-size: 14px; }
        select, button { padding: 10px 20px; font-size: 16px; margin: 10px 0; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; border-radius: 5px; }
        #result { background: #f5f5f5; padding: 15px; margin-top: 20px; border-radius: 5px; min-height: 100px; }
    </style>
</head>
<body>
    <h1>📝 AI论文助手</h1>
    <textarea id="text" placeholder="请输入需要处理的段落..."></textarea>
    <br>
    <select id="mode">
        <option value="润色">润色</option>
        <option value="降重">降重</option>
        <option value="扩写">扩写</option>
    </select>
    <button onclick="process()">开始处理</button>
    <div id="result">结果将显示在这里...</div>

    <script>
        async function process() {
            const text = document.getElementById('text').value;
            const mode = document.getElementById('mode').value;
            document.getElementById('result').innerText = '处理中，请稍候...';
            const res = await fetch('/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, mode})
            });
            const data = await res.json();
            document.getElementById('result').innerText = data.result;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data['text']
    mode = data['mode']
    
    prompts = {
        "润色": f"请帮我改写以下段落，使语言更流畅自然，避免重复表达，保持学术风格，直接输出结果：\n\n{text}",
        "降重": f"请用完全不同的句式和词汇改写以下段落，保持原意但表达方式要有明显差异，直接输出结果：\n\n{text}",
        "扩写": f"请将以下段落扩写得更加详细丰富，增加论据和细节，保持学术风格，直接输出结果：\n\n{text}"
    }
    
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": prompts[mode]}]
    )
    
    return jsonify({"result": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True, port=5000)