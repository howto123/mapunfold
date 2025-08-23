import asyncio

from src.mapunfold import get_description_for_list

example_id_list = [
    "a",
    "b",
    "c"
]

async def main():
    print("mapunfold runs...")

    # get id list
    # -> e.g. read filename from config
    id_list = example_id_list

    descriptions = await get_description_for_list(id_list)

    # store to database




if __name__ == "__main__":
    asyncio.run(main())