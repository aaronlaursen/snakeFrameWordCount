#!/usr/bin/python3
from snakes import deps_gen, work_gen, task_final, task_fail
import time,sys,os
class SnakeFrame():
    def __init__(confpath,statpath,self):
        self.parse_config(confpath)
        self.parse_status(statpath)
    def parse_status(statuspath, self):
        self.statuspath=statuspath
        with open(statuspath) as statfile:
            self.stats={"done":set(),"working":{}}
            for x in statfile:
                task, time = int(x.split(":")[0].strip()), int(x.split(":")[1].strip())
                if time == 0: self.stats["done"].add(task)
                else: self.stats["working"][task]=time
    def parse_config(configpath, self):
        self.configpath=configpath
        with open(configpath) as confile:
            self.config={l.split(":")[0].strip() : l.split(":")[1].strip() for l in confile}
    def get_next_free_task(self):
        t=nxt_free_helper(int(self.config["init_task"]),self)
        if t or len(self.status["working"])==0: return t, False
        return min(self.status["working"].keys(), key=(lambda x: self.status["working"][x])), True
    def nxt_free_helper(task,self):
        deps=deps_gen(task)
        if len(deps)==0: return task
        if set(deps) <= self.stats["done"]:return task
        for dep in deps_gen(task):
            x=self.nxt_free_helper(dep,self)
            if x: return x
        return False
    def claim_task(tid,self):
        os.popen("git pull")
        with open(self.satuspath,"a") as statfile:
            statfile.write(""+str(tid)+":"+str(time.time()))
        os.popen("git commit -a -m 'claim "+str(tid)+"'")
        os.popen("git push")
    def end_task(tid,self):
        os.popen("git pull")
        with open(self.satuspath,"a") as statfile:
            statfile.write(""+str(tid)+":0")
        os.popen("git commit -m -a 'finish "+str(tid)+"'")
        os.popen("git push")
    def setup_branch(branch,deps,in_use,self):
        self.claim_task(branch)
        if not in_use:
            os.popen("git checkout -b " + str(branch))
            for d in deps: os.popen("git merge "+str(d))
            os.popen("git mv out/* src/")
            os.popen("git commit -a -m 'init'")
            os.popen("git push")
        else: os.popen("git checkout "+str(branch))
    def teardown_branch(branch,self):
        os.popen("git rm src/")
        os.popen("git commit -a -m 'final'")
        os.popen("git push")
        os.popen("git checkout HEAD")
        self.end_task(branch)
        if int(branch)==int(self.config["init_task"]):
            os.popen("git merge "+str(self.config["init_task"]))
            os.popen("git commit -a -m 'DONE!'")
            self.parse_status(self.statuspath)
            for t in self.stats["done"]: os.popen("git branch -d "+str(t))
            os.popen("git push")
            task_final()

def main():
    frame=SnakeFrame("config","status")
    task,in_use=frame.get_nest_free_task()
    if not task: return
    frame.claim_task(task)
    deps=deps_gen(int(task))
    frame.setup_branch(task,deps,in_use)
    func=work_gen(task)
    if not work_gen(task): return task_fail()
    self.teardown_branch(task)
    return

#main()
