from neomodel import StructuredNode, StringProperty, RelationshipTo

class UserNode(StructuredNode):
    username = StringProperty(unique=True)
    follows = RelationshipTo("UserNode", "FOLLOWS")  # User follows another user

    