
async def paginator(qs, page: int = 1, page_size: int = 15) -> list:
    offset = (page - 1) * page_size
    limit = page_size
    return await qs.offset(offset).limit(limit)
