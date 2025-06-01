import requests

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-aff234ca657a42e2a011f94bd9c5ad25"  # 请替换为你的真实API KEY

def analyze_watering(plant, humidity, time_str, season):
    prompt = (
        f"植物：{plant}\n"
        f"当前湿度：{humidity}\n"
        f"上传时间：{time_str}\n"
        f"季节：{season}\n"
        "请根据这些信息判断该植物是否需要浇水，并简要说明理由。"
    )
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个智能农业助手，负责判断植物是否需要浇水。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256,
        "temperature": 0.5
    }
    try:
        resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"分析失败: {e}"