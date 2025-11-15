from settings import config
from database.db import Database
from database.model import user,user_messages
from sqlalchemy.dialects.postgresql import insert as pginsert
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import asyncio
import requests
import uuid

async def _insert_data(data: list):
    async with Database().get_session() as session:
        try:
            for item in data['items']:

                user_stmt = pginsert(user).values(
                    user_id=uuid.UUID(item['user_id']),
                    user_name= item['user_name']
                ).on_conflict_do_update(
                    index_elements=[user.user_id],          # PK/unique column
                    set_={"user_name": item["user_name"]}      # keep latest name
                )

                await session.execute(user_stmt)

                user_msg = pginsert(user_messages).values(
                    message_id = uuid.UUID(item['id']),
                    user_id= uuid.UUID(item['user_id']),
                    timestamp = datetime.fromisoformat(item['timestamp']),
                    message = item['message']
                )
                await session.execute(user_msg)

            await session.commit()
            print(f"All {len(data['items'])} inserted sucessfully")
        except SQLAlchemyError as e:
            await session.rollback()
            print("❌ DB ERROR:", getattr(e, "orig", e))
            raise

async def main():
    data = requests.get(config.public_data_url,config.data_api_param)
    data = data.json()
    await _insert_data(data)

if __name__ == '__main__':
    asyncio.run(main())


