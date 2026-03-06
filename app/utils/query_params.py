from fastapi import Query

class CommonQueryParams:
    def __init__(
        self,
        skip: int = Query(0, description="Items to skip", ge=0),
        limit: int = Query(10, description="Items to limit", ge=1, le=100),
        sort_by: str | None = Query(None, description="Field to sort by"),
        sort_desc: bool = Query(True, description="Sort descending")
    ):
        self.skip = skip
        self.limit = limit
        self.sort_by = sort_by
        self.sort_desc = sort_desc
        self.page = (skip // limit) + 1 if limit > 0 else 1
