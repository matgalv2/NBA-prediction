def generateSeasons(start, end):
    for year in range(start, end + 1):
        yield f"{year}-{str(year + 1)[2:]}"