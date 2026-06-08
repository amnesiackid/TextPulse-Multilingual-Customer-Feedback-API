from fastapi import Request
def get_settings():
    return {"min_word_count": 2, "max_word_count": 5000,
             "app_version": "1.0.0"}

def get_nlp(request:Request):
    return request.app.state.nlp
# TO DO: solve about multi-word aspects like "customer service", "battery life", "delivery time", etc.
ASPECT_VOCAB = {"delivery", "packaging", "quality", "price", "value", "usability", "performance", "design", "durability", "battery", "screen", "camera", "sound", "comfort", "fit", "size", "color", "material", "warranty", "installation", "setup", "compatibility", "features", "functionality", "reliability", "speed", "accuracy", "interface", "support", "tracking", "communication"}