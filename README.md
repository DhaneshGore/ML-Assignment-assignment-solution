# MultiLLM Cost-Optimized API 

This is a Flask-based microservice to access the Hugging Face LLaMA model.

## Installation
1. Create a virtual environment (optional, but recommended) to isolate dependencies:
    ```bash
    python -m venv venv
    ```
Activate the virtual environment: 
    ```bash
   venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install dependencies:  if You get this error then install this 
(venv) PS G:\Totem> python app.py
Traceback (most recent call last):
  File "G:\Totem\app.py", line 1, in <module>
    from flask import Flask, request, jsonify
  File "G:\Totem\venv\lib\site-packages\flask\__init__.py", line 5, in <module>
    from .app import Flask as Flask
  File "G:\Totem\venv\lib\site-packages\flask\app.py", line 30, in <module>
    from werkzeug.urls import url_quote
ImportError: cannot import name 'url_quote' from 'werkzeug.urls' (G:\Totem\venv\lib\site-packages\werkzeug\urls.py)
   
    ```bash
    pip install --upgrade flask werkzeug
    ```

4. Check and past your API key 'providers.yaml'
![image](https://github.com/user-attachments/assets/221de133-4950-4b22-a61d-799e433f4f1e)


5. Run the service:
    ```bash
    python app.py
    ```
### after Running python app.py
you will get this output
```bash
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
Copy http://127.0.0.1:5000

## API

## Next open postman and paste the url http://127.0.0.1:5000/generate # in this '/generate' in last add. 
## In the "Body" tab, select raw and choose JSON from the dropdown
![image](https://github.com/user-attachments/assets/8fc55936-318a-4cfe-98bf-586984bb3d47)


### POST /generate
Submit a prompt to the gateway:
```json
{
    "prompt": "What is AI?"
}
```

### Response
```json
{
    "modelUsed": "Hugging Face LLaMA",
    "cost": 0.01,
    "tokens": 150,
    "response": "AI stands for Artificial Intelligence..."
}
```

### Checking Logs:
## All API requests are logged in To view logs:
```bash
cat request_logs.json
```
![alt text](image.png)
