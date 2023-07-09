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

def divide_list(lst, r):
        chunk_size = len(lst) // r
        remainder = len(lst) % r
        result = []
        index = 0
        for i in range(r):
            if i < remainder:
                result.append(lst[index:index+chunk_size+1])
                index += chunk_size+1
            else:
                result.append(lst[index:index+chunk_size])
                index += chunk_size
        return result
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
            table = 1
            with open(file,"r") as f:
                c = 0
                for line in f:
                    # mapoutputlist.append(self.Map(protos_pb2.MapInput(key=c,value = line),context))
                    if(c==0):
                        c1 = line.split(",")[0]
                        c2 = line.split(",")[1].rstrip('\n')
                        c2 = c2.strip()

                        if((c1=="Age" and c2=="Name") or (c1=="Name" and c2=="Age")):
                            table = 1
                        else:
                            table = 2
                    else:
                        
                        mapoutputlist.append(self.Map(protos_pb2.MapInput(table=table,row = line),context))
                        
                    c+=1
        print("Mapper "+str(id)+" completed mapping")
        # partitioning here and write to partitioned files
        if os.path.isdir("intermediate_files")==False:  #changed the name of directory from partitioned_files to intermediate_files
            os.mkdir("intermediate_files")
        if os.path.isdir("intermediate_files/"+"if"+str(id))==False:
            os.mkdir("intermediate_files/"+"if"+str(id))
        
        
        print(mapoutputlist)
        
        # mapoutputlist = divide_list(mapoutputlist,r)
        # print(mapoutputlist)
        for i in range(r):
            # rem = len(item.common_column)%r
            with open("intermediate_files/if"+str(id)+"/p"+str(i)+".txt","w") as f:
                pass
        
        
        for item in mapoutputlist:
            rem = len(item.common_column)%r
            with open("intermediate_files/if"+str(id)+"/p"+str(rem)+".txt","a+") as f:
                f.write(item.common_column+","+str(item.table)+","+item.value+"\n")
            
        
        context.set_code(grpc.StatusCode.OK)
        return protos_pb2.reply(answer="success")
    
    def Map(self,request,context):
        print("inside map...")
        # key = request.key
        # value = request.value
        common = request.row.split(",")[0]
        value = request.row.split(",")[1].rstrip('\n')
        value = value.strip()

        return protos_pb2.MapOutput(common_column=common,table = request.table,value=value)

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