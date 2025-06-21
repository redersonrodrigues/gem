from app.utils.cache import cache

def test_cache_set_get_invalidate():
    cache.clear()
    cache.set('foo', 123)
    assert cache.get('foo') == 123
    cache.invalidate('foo')
    assert cache.get('foo') is None

def test_cache_clear():
    cache.set('a', 1)
    cache.set('b', 2)
    cache.clear()
    assert cache.get('a') is None
    assert cache.get('b') is None
