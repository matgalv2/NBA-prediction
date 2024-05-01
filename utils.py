def generateSeasons(first, last):
    for year in range(first, last + 1):
        yield f"{year}-{str(year + 1)[2:]}"