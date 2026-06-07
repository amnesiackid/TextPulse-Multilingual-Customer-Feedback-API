from fastapi import Request
def get_settings():
    return {"min_word_count": 2, "max_word_"
    "count": 5000, "app_version": "1.0.0"}

def get_nlp(request:Request):
    return request.app.state.nlp