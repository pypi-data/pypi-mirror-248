import requests

__all__ = ["getNotifyFunc"]


def getNotifyFunc(token: str):
    def _func(msg):
        res = requests.post(
            "https://notify-api.line.me/api/notify",
            headers={"Authorization": f"Bearer {token}"},
            files={"message": (None, msg)},
        )
        return res.status_code

    return _func
