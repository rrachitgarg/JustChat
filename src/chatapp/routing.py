from channels.routing import ProtocolTypeRouter as PTR,URLRouter
from channels.auth import AuthMiddlewareStack
from chatroom import routing

application = PTR(
    {
        'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
    }
)