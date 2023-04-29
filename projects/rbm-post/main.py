from src.runs import RunObject

if __name__=="__main__":
    run = RunObject("run_000")
    assert run.config.get("version")
