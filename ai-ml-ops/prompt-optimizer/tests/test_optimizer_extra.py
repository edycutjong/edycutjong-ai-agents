def test_optimizer_long_prompt():
    from agent.optimizer import analyze_prompt
    long_prompt = "word " * 501
    result = analyze_prompt(long_prompt)
    assert any("Prompt is very long" in w for w in result.weaknesses)

def test_optimize_long_prompt_missing_step():
    from agent.optimizer import optimize_prompt
    prompt = "This is a long prompt " * 10
    optimized = optimize_prompt(prompt)
    assert "Please think step-by-step" in optimized
