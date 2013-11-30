#!/usr/bin/python3
from snakes import deps_gen, work_gen, task_final, task_fail
import time,sys,os,subprocess
class SnakeFrame():
    def __init__(self,confpath,statpath):
        self.parse_config(confpath)
        self.parse_status(statpath)
    def parse_status(self,statuspath):
        self.statuspath=statuspath
        with open(statuspath) as statfile:
            self.stats={"done":set(),"working":{}}
            for x in statfile:
                if len(x.split(":")) !=2: continue
                task, time = int(x.split(":")[0].strip()), int(x.split(":")[1].strip())
                if time == 0: self.stats["done"].add(task)
                else: self.stats["working"][task]=time
    def parse_config(self, configpath):
        self.configpath=configpath
        with open(configpath) as confile:
            self.config={l.split(":")[0].strip() : l.split(":")[1].strip() for l in confile}
    def get_next_free_task(self):
        t=self.nxt_free_helper(int(self.config["init_task"]))
        if t or len(self.status["working"])==0: return t, False
        return min(self.status["working"].keys(), key=(lambda x: self.status["working"][x])), True
    def nxt_free_helper(self,task):
        deps=deps_gen(task)
        if len(deps)==0: return task
        if set(deps) <= self.stats["done"]:return task
        for dep in deps_gen(task):
            x=self.nxt_free_helper(dep)
            if x: return x
        return False
    def claim_task(self,tid):
        subprocess.Popen("git pull", shell=True)
        with open(self.statuspath,"a") as statfile:
            statfile.write(""+str(tid)+":"+str(time.time())+"\n")
        subprocess.Popen("git commit -a -m 'claim "+str(tid)+"'", shell=True)
        subprocess.Popen("git push", shell=True)
    def end_task(self,tid):
        subprocess.Popen("git pull", shell=True)
        with open(self.statuspath,"a") as statfile:
            statfile.write(""+str(tid)+":0"+"\n")
        subprocess.Popen("git commit -m -a 'finish "+str(tid)+"'", shell=True)
        subprocess.Popen("git push", shell=True)
    def setup_branch(self,branch,deps,in_use):
        self.claim_task(branch)
        if not in_use:
            subprocess.Popen("git checkout -b " + str(branch), shell=True)
            for d in deps: subprocess.Popen("git merge "+str(d), shell=True)
            subprocess.Popen("mkdir src out", shell=True)
            subprocess.Popen("git mv out/* src/", shell=True)
            subprocess.Popen("git commit -a -m 'init'", shell=True)
            subprocess.Popen("git push", shell=True)
        else: subprocess.Popen("git checkout "+str(branch), shell=True)
    def teardown_branch(self,branch):
        subprocess.Popen("git rm src/*", shell=True)
        subprocess.Popen("git add out/*", shell=True)
        subprocess.Popen("git commit -a -m 'final'", shell=True)
        subprocess.Popen("git push", shell=True)
        subprocess.Popen("git checkout HEAD", shell=True)
        self.end_task(branch)
        if int(branch)==int(self.config["init_task"]):
            subprocess.Popen("git merge "+str(self.config["init_task"]), shell=True)
            subprocess.Popen("git commit -a -m 'DONE!'", shell=True)
            self.parse_status(self.statuspath)
            for t in self.stats["done"]: subprocess.Popen("git branch -d "+str(t), shell=True)
            subprocess.Popen("git push", shell=True)
            task_final()

def main():
    frame=SnakeFrame("config","status")
    task,in_use=frame.get_next_free_task()
    if not task: return
    frame.claim_task(task)
    deps=deps_gen(int(task))
    frame.setup_branch(task,deps,in_use)
    func=work_gen(task)
    if not work_gen(task): return task_fail()
    frame.teardown_branch(task)
    return

main()
