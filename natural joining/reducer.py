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
                    if line.split(",")[0] not in dict:
                        list = []
                        dict[line.split(",")[0]] = []
                        list.append(line.split(",")[1])
                        value = line.split(",")[2].rstrip('\n')
                        value = value.strip()
                        list.append(value)
                        dict[line.split(",")[0]].append(list)
                    else:
                        list = []
                        list.append(line.split(",")[1])
                        value = line.split(",")[2].rstrip('\n')
                        value = value.strip()
                        list.append(value)
                        dict[line.split(",")[0]].append(list)
        #                 dict[line.split(" ")[0]].append(int(line.split(" ")[1]))
        print(dict)
        reduceroutputlist = []
        for key in dict:
            input = protos_pb2.ReduceInput()
            input.common_column = key
            
            list = []
            for value in dict[key]:
                # print("value",value)
                val = protos_pb2.value(table=int(value[0]),val=value[1])
                input.values.append(val)
            # input = protos_pb2.ReduceInput(common_column=key,values = list)
            # print("input: ",input)
            # input.values = list
            reduceroutputlist.append(self.Reduce(input,context))

        #     reduceroutputlist.append(self.Reduce(protos_pb2.ReduceInput(key=key,values = dict[key]),context))

        print(reduceroutputlist)

        if os.path.isdir("output")==False:
            os.mkdir("output")
        with open("output/output"+str(id)+".txt","w") as f:
            f.write("Name, Age, Role\n")

        with open("output/output"+str(id)+".txt","a+") as f:
            for item in reduceroutputlist:
                # print("while writing",item+"\n")
                for val in item.reduceOutput:
                    f.write(val.common_column+", "+val.value1+", "+val.value2+"\n")

                
            
        print("Reducer "+str(id)+" completed reducing")
        return protos_pb2.reply(answer="success")
    
    def Reduce(self,request,context):
        list1 = []
        list2 = []
        # print("inside reduce func",request)
        for value in request.values:
            if(value.table==1):
                list1.append(value.val)
            else:
                list2.append(value.val)
        # print("list1",list1)
        # print("list2",list2)
        list =[]
        for item1 in list1:
            for item2 in list2:
                list.append(protos_pb2.ReduceOutput(common_column=request.common_column,value1=item1,value2=item2))
        # print(list)
        return protos_pb2.reduceOutputList(reduceOutput=list)
        


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