from flask import Flask, render_template, request
import pandas as pd
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
PARQUET_FILE = "sector.parquet"
MODEL_NAME = "google/flan-t5-xl"

# Load model and tokenizer once at startup
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_summary(data_df, max_length=500):
    if data_df.empty:
        return "No data available for summary."
    
    # Create a simple data summary first
    unique_platforms = data_df['kundengleisnummer'].nunique()
    platforms_summary = {}
    
    for platform in data_df['kundengleisnummer'].unique():
        sectors = data_df[data_df['kundengleisnummer'] == platform]['sektor_vorderseite'].tolist()
        platforms_summary[platform] = sectors
    
    # Create prompt with the structured data
    prompt = f"""I have data about a train station with {unique_platforms} platforms. 
    
Platform sectors:
"""
    
    for platform, sectors in platforms_summary.items():
        prompt += f"Platform {platform}: Sectors {', '.join(map(str, sectors))}\n"
    
    prompt += "\nPlease provide a concise summary of this station's platform and sector configuration."
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    
    try:
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error generating summary: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    query = None
    results = None
    summary = None

    if request.method == "POST":
        query = request.form.get("search", "").strip()
        if os.path.exists(PARQUET_FILE) and query:
            df = pd.read_parquet(PARQUET_FILE)
            # Search by bps_name
            results_df = df[df["bps_name"].str.contains(query, case=False, na=False)]
            
            if not results_df.empty:
                results = results_df.to_dict(orient="records")
                # Generate detailed summary using Flan-T5
                summary = generate_summary(results_df)
            else:
                results = []
                summary = "No matching results found."
    
    return render_template("index.html", query=query, results=results, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
