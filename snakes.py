#no input to generated function
#returns True/False for success/failure
urls = [ "http://mirror.csclub.uwaterloo.ca/gutenberg/7/76/76.txt"
    , "http://mirror.csclub.uwaterloo.ca/gutenberg/1/3/4/1342/1342.txt"
    , "http://mirror.csclub.uwaterloo.ca/gutenberg/1/3/135/135.txt"]
#    , "http://mirror.csclub.uwaterloo.ca/gutenberg/1/6/6/1661/1661.txt"
#    , "http://mirror.csclub.uwaterloo.ca/gutenberg/1/11/11.txt"
#    , "http://mirror.csclub.uwaterloo.ca/gutenberg/1/6/3/2/16328/16328.txt"
#    , "http://mirror.csclub.uwaterloo.ca/gutenberg/1/2/3/1232/1232.txt"
#    , "http://mirror.csclub.uwaterloo.ca/gutenberg/2/5/9/2591/2591.txt"        
#    , "http://mirror.csclub.uwaterloo.ca/gutenberg/5/2/0/5200/5200.txt"
#    , "http://mirror.csclub.uwaterloo.ca/gutenberg/8/4/844/844.txt"]

def work_gen(unit_id):
    unit_id=int(unit_id)
    if unit_id >1000:
        def count_a_book(unit_id):
            print("asdfasdfasdf")
            url=urls[unit_id-1000]
            import urllib.request
            print("fetching:",url)
            text=urllib.request.urlopen(url).read()
            counts={}
            for word in text.split():
                if word not in counts: counts[word]=0
                counts[word]+=1
            import pickle
            with open("out/"+str(unit_id-1000)+".pickle", "wb") as outfile:
                pickle.dump(counts,outfile,2)
            return True
        return count_a_book
    else:
        def reducer(unit_id):
            total_counts={}
            import pickle
            for dep in range(len(urls)):
                with open("src/"+str(dep)+".pickle","rb") as infile:
                    dep_counts=pickle.load(infile)
                    for k, v in dep_counts.items():
                        if k not in total_counts: total_counts[k]=0
                        total_counts[k]+=v
            import operator
            sorted_count = sorted(total_counts.iteritems(),operator.itemgetter(1))
            with open("out/final_counts","w") as outfile:
                for k,v in sorted_count:
                    outfile.write(""+str(v)+"\t"+str(k)+"\n")
            return True
    return (lambda x: False)

def deps_gen(unit_id):
    if int(unit_id)==0: return set([x +1000 for x in range(len(urls))])
    return set()

def task_final():
    print("DONE!!! WHOOP! WHOOP!")
    return

def task_fail():
    print("FAIL!!!")
    return
