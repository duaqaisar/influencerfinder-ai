from core.database import Base, engine
from models.influencer import Influencer
from models.post import Post

# Create all database tables defined by models that inherit from Base
# (imports above ensure Influencer and Post models are registered with Base's metadata)
Base.metadata.create_all(bind=engine)

# Confirmation message once tables are created
print("Database created successfully!")
