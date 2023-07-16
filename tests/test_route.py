from neopoint.http.request import Request
from neopoint.http.request_method import RequestMethod
from neopoint.routing import Route


def test_adding_controller_get():
    route = Route()

    @route.get("/theme")
    def controller(*_: Request) -> bytes:
        return b"aboba"

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][0] == RequestMethod.GET
    assert route._urls["/theme"][1](None) == b"aboba"


def test_adding_controller_post():
    route = Route()

    @route.post("/theme")
    def controller(*_: Request) -> bytes:
        return b"aboba"

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][0] == RequestMethod.POST
    assert route._urls["/theme"][1](None) == b"aboba"


def test_adding_controller_put():
    route = Route()

    @route.put("/theme")
    def controller(*_: Request) -> bytes:
        return b"aboba"

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][0] == RequestMethod.PUT
    assert route._urls["/theme"][1](None) == b"aboba"


def test_adding_controller_delete():
    route = Route()

    @route.delete("/theme")
    def controller(*_: Request) -> bytes:
        return b"aboba"

    # pylint: disable=protected-access
    assert route._urls.get("/theme", None) is not None
    assert route._urls["/theme"][0] == RequestMethod.DELETE
    assert route._urls["/theme"][1](None) == b"aboba"
