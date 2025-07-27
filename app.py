from flask import Flask, render_template, request
from markupsafe import Markup
from openai import OpenAI
import markdown

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_query = request.form.get("query")
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": user_query}],
            temperature=0.5,
            top_p=1,
            max_tokens=500
        )
        response_text = completion.choices[0].message.content
    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
