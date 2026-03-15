from agent.summarizer import summarize

def test_summarize_empty():
    res = summarize("Short", ratio=0.5)
    assert res.summary == "Short"
    assert res.summary_length == 5
    assert len(res.keywords) == 0

