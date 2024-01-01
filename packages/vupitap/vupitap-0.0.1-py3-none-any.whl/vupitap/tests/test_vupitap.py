from vupitap.vupitap import hello_world


class TestVupitap:
    def test_hello_world(self):
        assert hello_world() == "hello world"
