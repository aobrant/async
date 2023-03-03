import asyncio
from datetime import datetime
from aiohttp import ClientSession
from more_itertools import chunked
from db import Session, engine, Base, People


CHUNK_SIZE = 10
PEOPLE_NUMBER = 100


async def get_urls(urls, key, session):
    tasks = (asyncio.create_task(get_urls(url, key, session)) for url in urls)
    for task in tasks:
        yield await task


async def get_data(urls, key, session):
    result_list = []
    async for item in get_urls(urls, key, session):
        result_list.append(item)
    return ', '.join(result_list)


async def paste_to_db(results):
    async with Session() as session:
        async with ClientSession() as session_in:
            for person_json in results:
                homeworld_str = await get_data([person_json['homeworld']], 'name', session_in)
                films_str = await get_data(person_json['films'], 'title', session_in)
                species_str = await get_data(person_json['species'], 'name', session_in)
                starships_str = await get_data(person_json['starships'], 'name', session_in)
                vehicles_str = await get_data(person_json['vehicles'], 'name', session_in)
                newperson = People(
                    birth_year=person_json['birth_year'],
                    eye_color=person_json['eye_color'],
                    gender=person_json['gender'],
                    hair_color=person_json['hair_color'],
                    height=person_json['height'],
                    mass=person_json['mass'],
                    name=person_json['name'],
                    skin_color=person_json['skin_color'],
                    homeworld=homeworld_str,
                    films=films_str,
                    species=species_str,
                    starships=starships_str,
                    vehicles=vehicles_str,
                )
                session.add(newperson)
                await session.commit()


async def get_person(people_id: int, session: ClientSession):
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        return await response.json()


async def get_people():
    async with ClientSession() as session:
        coros = (get_person(people_id=i, session=session) for i in range(1, PEOPLE_NUMBER))
        for coros_chunk in chunked((coros, CHUNK_SIZE)):
            result = await asyncio.gather(*coros_chunk)
            return await result


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with ClientSession() as session:
        coros = (get_person(people_id=i, session=session) for i in range(1, PEOPLE_NUMBER))
        for coros_chunk in chunked((coros, CHUNK_SIZE)):
            result = await asyncio.gather(*coros_chunk)
            asyncio.create_task(paste_to_db(result))
        await session.close()
        tasks = asyncio.all_tasks()
        for task in tasks:
            if task != asyncio.current_task():
                await task




if __name__ == '__main__':

    start = datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
