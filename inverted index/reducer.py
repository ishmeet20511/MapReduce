from concurrent import futures
import os
import grpc
import protos_pb2
import protos_pb2_grpc
import datetime
import time

ip = "localhost"
port = ""
id = -1
r = 0
files = []   #mapping of uuid to file names and their versions


class Reducer(protos_pb2_grpc.WordCountServicer):
    def callReducer(self,request,context):
        print("Received call from master for reducer "+str(id))
        print(request.file)
        files = request.file
        dict = {}
        for file in files:
            with open(file,"r") as f:
                for line in f:
                    if line.split(" ")[0] not in dict:
                        dict[line.split(" ")[0]] = [int(line.split(" ")[1])]
                    else:
                        dict[line.split(" ")[0]].append(int(line.split(" ")[1]))
        print(dict)

        reduceroutputlist = []
        for key in dict:
            reduceroutputlist.append(self.Reduce(protos_pb2.ReduceInput(key=key,values = dict[key]),context))

        # print(reduceroutputlist)

        if os.path.isdir("output")==False:
            os.mkdir("output")
        
        with open("output/output"+str(id)+".txt","w") as f:
            for item in reduceroutputlist:
                f.write(item.key+" "+str(item.value)+"\n")
            
        print("Reducer "+str(id)+" completed reducing")
        return protos_pb2.reply(answer="success")
    
    def Reduce(self,request,context):
        # count = 0
        # for value in request.values:
        #     count+=value
        listi = request.values
        listi = list(set(listi))
        return protos_pb2.ReduceOutput(key=request.key,value=listi)
        


def run():
    with grpc.insecure_channel("localhost:50050") as channel:
        stub = protos_pb2_grpc.WordCountStub(channel)
        nd = protos_pb2.node()
        nd.ip = ip
        nd.port = port
        nd.key = id
        response = stub.register_reducer(nd)
        if response.answer == "success":
            print("reducer connected to Master ")
        else:
            print("reducer not able connect to Master ")
        
        
        channel.close()


def serve(prt,i,mappers,red):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos_pb2_grpc.add_WordCountServicer_to_server(Reducer(), server)
    global port
    global id
    global r
    global m
    m = mappers
    port = prt
    id = i
    r = red
    server.add_insecure_port(ip + ':' + port)
    # print("Mapper "+id+ " started on port " + port)
    server.start()
    run()
    server.wait_for_termination()