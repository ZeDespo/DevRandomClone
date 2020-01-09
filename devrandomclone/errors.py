class EAGAIN(Exception):

    def __init__(self, error: str):
        super(EAGAIN, self).__init__(error)


class RedditAuthenticationError(Exception):

    def __init__(self, error: str):
        super(RedditAuthenticationError, self).__init__(error)


if __name__ == '__main__':
    exit()
