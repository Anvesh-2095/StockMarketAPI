def parseQuery(features : dict) -> str:
    """
    returns a sql query string based on the provided features dictionary.
    features dict is extracted from the request body json on route /screener
    :param features: Dictionary containing feature names and their values.
    :return: SQL query string.
    """
    res = "SELECT * FROM stocks WHERE "