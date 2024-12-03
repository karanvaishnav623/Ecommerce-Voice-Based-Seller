
def brand_search(url, brands):
    query = url
    for brand in brands:
        query += "&p[]=facets.brand[]="+brand
    return query


def price_search(url, low="MIN", high="MAX"):
    query = url
    query += "&p[]=facets.price_range.from="+low+"&p[]=facets.price_range.to="+high
    return query


def brand_search(brands, url):
    query = url
    for brand in brands:
        query += "&p[]=facets.brand[]="+brand
    return query

# """
# itm59e288d010cef?pid=COMGAX8EEYFKCESS
# https://www.flipkart.com/hp-15s-2024-amd-ryzen-3-quad-core-5300u-8-gb-512-gb-ssd-windows-11-home-15s-eq2143au-thin-light-laptop/product-reviews/itm59e288d010cef?pid=COMGAX8EEYFKCESS
# """
