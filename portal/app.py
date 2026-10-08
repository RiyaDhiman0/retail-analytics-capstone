from flask import Flask, render_template_string
app=Flask(__name__)
HTML='''<!doctype html><html><head><title>Retail Internal Portal</title><style>body{font-family:Arial;margin:40px}iframe{width:100%;height:650px;border:1px solid #ddd}</style></head><body><h1>Retail Operations Portal</h1><p>Embedded analytics workspace</p><iframe src="http://localhost:8501"></iframe></body></html>'''
@app.get('/')
def home(): return render_template_string(HTML)
if __name__=='__main__': app.run(port=5000,debug=False)
