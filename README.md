# recalls-dashboard

## Instructions

To get started, first clone this repo:

```
git clone https://github.com/EdmilsonSantana/recalls-dashboard.git
cd recalls-dashboard
```

You can create virtual environments or build docker images to run these apps.

### Virtual Environment

Create and activate a venv:

```
python -m venv venv
source venv/bin/activate  # for Windows, use venv\Scripts\activate.bat
```

Install all the requirements:

```
pip install -r requirements.txt
```

You can now run the apps:

Streamlit
```
streamlit run app.py --server.maxUploadSize=1028
```

and visit http://127.0.0.1:8501

Dash
```
python app.py
```

and visit http://127.0.0.1:8050

### Docker

If you have Docker and Docker Compose installed, you can build and run with:

```
docker-compose up -d
```

and visit http://127.0.0.1:80

