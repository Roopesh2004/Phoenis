from flask import Flask, render_template, request
from openai import OpenAI
import os

# Initialize OpenAI Client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    selected_language = "telugu"  # default

    if request.method == "POST":
        user_query = request.form.get("query")
        selected_language = request.form.get("language", "telugu")

        # Append language instruction
        if selected_language == "telugu":
            modified_query = f"{user_query}\n(Answer in Telugu)"
        else:
            modified_query = f"{user_query}\n(Answer in English)"

        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": modified_query}],
            temperature=0.5,
            top_p=1,
            max_tokens=500
        )
        response_text = completion.choices[0].message.content

    return render_template("index.html", response=response_text, language=selected_language)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
