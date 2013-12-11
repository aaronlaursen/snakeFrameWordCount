#no input to generated function
#returns True/False for success/failure
def work_gen(unit_id):
	return (lambda x: True)

#return iterator of dpendencies for task unit_id
def deps_gen(unit_id):
	return []

#run when all tasks completed
def task_final():
    return

#run when a task fails, before cleanup
def task_fail():
    return
