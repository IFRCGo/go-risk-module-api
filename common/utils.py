import requests


def logging_context(context) -> dict:
    return {
        "context": context,
    }


def logging_response_context(response: requests.Response) -> dict:
    return logging_context(
        {
            "url": response.url,
            "response": {
                "content": response.content,
                "status_code": response.status_code,
            },
        }
    )


def sort_dict_recursively(d):
    if isinstance(d, dict):
        return {k: sort_dict_recursively(d[k]) for k in sorted(d)}
    elif isinstance(d, list):
        return [sort_dict_recursively(item) for item in d]
    else:
        return d


def postprocess_schema(result, **kwargs):
    return sort_dict_recursively(result)
