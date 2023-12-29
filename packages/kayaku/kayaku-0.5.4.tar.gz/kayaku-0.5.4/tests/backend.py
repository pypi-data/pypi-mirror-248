import io

import pytest

from kayaku import backend
from kayaku.backend.types import Comment, JWrapper, WhiteSpace, convert
from kayaku.backend.wsc import encode_wsc

test_input = """\
{
    "base":{
        /*
        * More annotations
        *
        * @type: int
        */
        "account": 0,
        "multi": "abc\\
def\\
lll\\
",
        'pragma': '中文。\\
asd'
    },
    "next":{
        /*@type: List[dict]*/
        "dct":[
            {"3": 5}
        ],
        /*
        * Test annotating
        * What about double line
        *
        * @type: Optional[P]
        */
        "p": null,
        "q": true, // attempt
        "v": false, /* wow */
        "s": "trail",
        "mult": "abc\\
def",
    },
    identifier: 'SINGLE',
    numbers: [+NaN, -Infinity, 0x7b, +0.5e10, .777, 777.],
    "$schema": "file:///F:/PythonProjects/Graiax/kayaku/config.schema.json"
}
"""


def test_backend_round_trip():
    import kayaku.backend.env
    from kayaku import backend

    in_io = io.StringIO(test_input)
    out_io = io.StringIO()

    assert backend.dumps(backend.loads(test_input)) == test_input
    obj = backend.load(in_io)
    assert obj["base"]["multi"] == "abcdeflll"
    assert obj["base"]["pragma"] == "中文。asd"
    backend.dump(obj, out_io)
    assert out_io.getvalue() == test_input

    backend.env.DEBUG.set(True)

    in_io = io.StringIO(test_input)
    out_io = io.StringIO()

    assert backend.dumps(backend.loads(test_input)) == test_input
    backend.dump(backend.load(in_io), out_io)
    assert out_io.getvalue() == test_input


def test_round_trip_raw():
    commented = "/*abc*/ 5"
    assert backend.dumps(backend.loads(commented)) == commented


def test_load_repr():
    assert str(backend.loads("123")) == "123"
    assert str(backend.loads("0x123")) == "0x123"
    assert backend.loads("null") == None
    assert backend.loads("true") == True
    assert {None: 5}[backend.loads("null")]


def test_dump_val():
    assert backend.dumps(123) == "123"
    assert backend.dumps(True) == "true"
    assert backend.dumps(False) == "false"
    assert backend.dumps("plural") == '"plural"'
    float_val = backend.loads("0.5e10")
    float_val.origin = "123"
    assert backend.loads(backend.dumps(float_val)) == float_val
    assert backend.loads(backend.dumps(0.5)) == 0.5
    hex_val = backend.loads("0xccc")
    hex_val.origin = "45"
    assert backend.loads(backend.dumps(hex_val)) == hex_val
    with pytest.raises(NotImplementedError):
        backend.dumps(object())
    with pytest.raises(NotImplementedError):
        backend.dumps(JWrapper(NotImplemented))


def test_convert():
    for obj in [1, 1.0, True, False, None, {}, []]:
        assert convert(obj) == obj
    with pytest.raises(TypeError):
        convert(object())


def test_wsc():
    v = backend.loads("/*123*/[]")
    v.__json_clear__()
    assert backend.dumps(v) == "[]"
    assert encode_wsc(WhiteSpace("     \n")) == "     \n"
    with pytest.raises(NotImplementedError):
        encode_wsc(Comment("abstract"))


def test_horrible_quote():
    target_single = r"""{"a": '"\'"\'"\'"\''}"""
    target_double = r"""{"a": "\"'\"'\"'\"'"}"""
    assert backend.loads(target_double) == {"a": """"'"'"'"'"""}
    assert backend.loads(target_single) == {"a": """"'"'"'"'"""}
    assert (
        backend.dumps({"a": """"'"'"'"'"""}) == '{"a":"\\"\'\\"\'\\"\'\\"\'"}'
    )  # default: condense
    assert backend.dumps(backend.loads(target_single)) == target_single
    assert backend.dumps(backend.loads(target_double)) == target_double
