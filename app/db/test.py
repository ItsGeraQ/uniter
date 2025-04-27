

def test_db():
	from app.db import db
	print(db)
	assert db is not None
	assert db.engine is not None
	assert db.session is not None
	assert db.Base is not None
	assert db.Base.metadata is not None
	assert db.Base.metadata.tables is not None
	assert len(db.Base.metadata.tables) > 0
	