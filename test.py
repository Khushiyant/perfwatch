from perfwatch import profile_decorator


@profile_decorator(["line", "cpu", "time"])
def test():
    for _ in range(1000000):
        pass


if __name__ == "__main__":
    test()
