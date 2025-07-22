from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

async def orm_add_user(session: AsyncSession, data: dict):
    session.add(User(
        id_user = data['id_user'],
        payload = data['payload'],
        data_buy = data['data_buy'],
        data_end = data['data_end'],
    ))
    await session.commit()


async def orm_get_user(session: AsyncSession, id_user: int):
    query = select(User).where(User.id_user == id_user)
    result = await session.execute(query)
    return result.scalar()