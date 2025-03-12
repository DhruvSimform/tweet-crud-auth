from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo, db

class UserNode(StructuredNode):
    username = StringProperty(unique=True)

    # Users this user follows
    following = RelationshipTo("UserNode", "FOLLOWS")

    # Users who follow this user
    followers = RelationshipFrom("UserNode", "FOLLOWS")

    def count_followers(self):
        query = """
        MATCH (user:UserNode {username: $username})<-[:FOLLOWS]-()
        RETURN COUNT(*) AS followers_count
        """
        result, _ = db.cypher_query(query, {'username': self.username})
        return result[0][0]

    def count_following(self):
        query = """
        MATCH (user:UserNode {username: $username})-[:FOLLOWS]->()
        RETURN COUNT(*) AS following_count
        """
        result, _ = db.cypher_query(query, {'username': self.username})
        return result[0][0]