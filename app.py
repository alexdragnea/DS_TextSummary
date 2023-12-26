from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import traceback
import time

app = Flask(__name__, template_folder='templates', static_folder='static')

model_name = "alexdg19/bart-large-cnn-reddit-summary-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        post_body = request.form['post_body']

        input_word_count = len(post_body.split())

    
        min_length_ratio = 0.4 
        max_length_ratio = 0.8 

        min_length = int(input_word_count * min_length_ratio)
        max_length = int(input_word_count * max_length_ratio)

    
        inputs = tokenizer.encode(post_body, return_tensors="pt", max_length=1024, truncation=True)
        outputs = model.generate(
            inputs,
            do_sample=False,
            min_new_tokens=min_length,
            max_new_tokens=max_length
        )

        generated_summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({
            'original_text': post_body,
            'generated_summary': generated_summary,
            'input_word_count': input_word_count,
            'summary_word_count': len(generated_summary.split())
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)})

@app.route('/liveness')
def healthx():
  return "<h1><center>Liveness check completed</center><h1>"
  
@app.route('/readiness')
def healthz():
  return "<h1><center>Readiness check completed</center><h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
