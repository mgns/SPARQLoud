from handlers.foo import FooHandler
from handlers.form import FormHandler
from handlers.feed import FeedHandler

url_patterns = [
    (r"/", FooHandler),
    (r"/form", FormHandler),
    (r"/feed/Q([0-9a-h]+)", FeedHandler),
]
