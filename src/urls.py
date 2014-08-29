from handlers.foo import FooHandler
from handlers.form import FormHandler
from handlers.feed import FeedHandler
from handlers.feedlist import FeedListHandler

url_patterns = [
    (r"/", FooHandler),
    (r"/form", FormHandler),
    (r"/feeds", FeedListHandler),
    (r"/feed/Q([0-9a-h]+)", FeedHandler),
]
