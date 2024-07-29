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
