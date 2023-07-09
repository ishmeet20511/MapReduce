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


class Mapper(protos_pb2_grpc.WordCountServicer):
    def callMapper(self,request,context):
        print("Received call from master for mapper "+str(id))
        # print(request.file)
        files = request.file
        mapoutputlist = []
        if(len(files)==0):
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.reply(answer="success")
        for file in files:

            with open(file,"r") as f:
                c = 0
                for line in f:
                    mapoutputlist.append(self.Map(protos_pb2.MapInput(key=c,value = line),context))
                    c+=1
        print("Mapper "+str(id)+" completed mapping")
        # partitioning here and write to partitioned files
        if os.path.isdir("intermediate_files")==False:  #changed the name of directory from partitioned_files to intermediate_files
            os.mkdir("intermediate_files")
        if os.path.isdir("intermediate_files/"+"if"+str(id))==False:
            os.mkdir("intermediate_files/"+"if"+str(id))
        
        
        print(mapoutputlist)
        sortedlist = []
        for item in mapoutputlist:
            for mapoutput in item.mapOutput:
                sortedlist.append(mapoutput.key)
        
        sortedlist.sort()

        for item in sortedlist:
            rem = len(item)%r
            with open("intermediate_files/if"+str(id)+"/p"+str(rem)+".txt","w") as f:
                pass
        for item in sortedlist:
            
            rem = len(item)%r
            with open("intermediate_files/if"+str(id)+"/p"+str(rem)+".txt","a+") as f:
                f.write(item+" "+str(1)+"\n")
        
        context.set_code(grpc.StatusCode.OK)
        return protos_pb2.reply(answer="success")
    
    def Map(self,request,context):
        print("inside map...")
        key = request.key
        value = request.value

        list = protos_pb2.mapOutputList()

        for word in value.split():
            list.mapOutput.add(key=word,value=1)
        

        # print(list)

        return list

def run():
    with grpc.insecure_channel("localhost:50050") as channel:
        stub = protos_pb2_grpc.WordCountStub(channel)
        nd = protos_pb2.node()
        nd.ip = ip
        nd.port = port
        nd.key = id
        response = stub.register_mapper(nd)
        if response.answer == "success":
            print("Mapper connected to Master ")
        else:
            print("Mapper not able connect to Master ")
        
        
        channel.close()


def serve(prt,i,red):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos_pb2_grpc.add_WordCountServicer_to_server(Mapper(), server)
    global port
    global id
    global r
    port = prt
    id = i
    r = red
    server.add_insecure_port(ip + ':' + port)
    # print("Mapper "+id+ " started on port " + port)
    server.start()
    run()
    server.wait_for_termination()