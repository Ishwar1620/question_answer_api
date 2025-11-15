from sqlalchemy import Column,String,Text,TIMESTAMP,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Database

class user(Database().base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'qa_db'}
    user_id = Column(UUID(as_uuid=True),primary_key=True)
    user_name = Column(Text,nullable=False)

class user_messages(Database().base):
    __tablename__ = 'user_messages'
    __table_args__ = {'schema':'qa_db'}

    message_id  = Column(UUID(as_uuid=True),primary_key=True)
    user_id = Column(UUID(as_uuid=True),ForeignKey('qa_db.users.user_id',ondelete='CASCADE'),nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True),nullable=False)
    message = Column(Text,nullable=False)
