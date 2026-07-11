from app.rag.chunker import chunk_text


def test_single_chunk():
    text = "Hello world"

    result = chunk_text(text)

    assert result == ["Hello world"]

def test_multiple_chunks():
    text = "A" * 500

    result = chunk_text(text)

    assert len(result) > 1

    assert all(
        len(chunk) <= 200
        for chunk in result
    )

def test_overlap():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    result = chunk_text(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert result[0].endswith("IJ")
    assert result[1].startswith("IJ")
    
    assert result[1].endswith("QR")
    assert result[2].startswith("QR")

def test_empty_text():
    result = chunk_text("")

    assert result == []

def test_exact_chunk_size():
    text = "A" * 200

    result = chunk_text(text)

    assert result == [text]

def test_custom_chunk_size():
    text = "A" * 120

    result = chunk_text(
        text,
        chunk_size=50,
        overlap=10,
    )

    assert len(result) == 3

    assert all(
        len(chunk) <= 50
        for chunk in result
    )

    assert result[0][-10:] == result[1][:10]
    assert result[1][-10:] == result[2][:10]