from task import Task, Status

def test_mark_done():
    task = Task("Teksti ülesanne", Status.TODO)
    task.set_status(Status.DONE)
    assert task.get_status() == Status.DONE
    print(123)

test_mark_done()