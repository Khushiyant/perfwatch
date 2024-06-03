import pytest
from perfwatch import PerformanceProfiler


def test_performance_profile(dummy_function):
    @PerformanceProfiler.performance_profile
    def test():
        dummy_function()

    test()
    assert PerformanceProfiler.get_performance_profile() == {
        "test": {"total_time": 0.0, "total_calls": 1, "average_time": 0.0}
    }


if __name__ == "__main__":
    pytest.main()
