from task import change_task_state


def test_change_task():
    tasks = "task1#0|task2#1"
    task = "task1"
    state = "1"
    tasks = change_task_state(tasks, task, state)
    assert tasks == "task1#1|task2#1"


if __name__ == "__main__":
    test_change_task()
