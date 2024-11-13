from neo4j import GraphDatabase

NEO4J_URI = "neo4j://localhost"
NEO4J_AUTH = ("neo4j", "password")
db_driver: GraphDatabase = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
