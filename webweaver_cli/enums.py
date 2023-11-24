
class ParamTypeEnum:
    """Types of parameters that can be passed into a Spider."""
    QUERY = "query"         # Goes in URL: ?param1=foo&param2=bar
    POST = "post"           # send with the request as POST data
    JSON = "json"           # send with the request as JSON data
    INPUT = "input"         # HTML <input> element or other form data
    HEADER = "header"       # API keys, tokens, etc..
    DIRECTORY = "directory" # domain.com/directory/path/here/