from concurrent import futures

import grpc
import protos_pb2
import protos_pb2_grpc
import multiprocessing
import os
import mapper
import reducer
input_location = ""
output_location = ""
m = 0
r = 0
class Master(protos_pb2_grpc.WordCountServicer):
    
    def clientStartup(self, request, context):
        print("Received connect request from client: " + str(request.ip) + ":" + str(request.port))
        
        # print("list:",replicaList)
        # print("primaryServer: ",primaryServer)
        context.set_code(grpc.StatusCode.OK)

        return protos_pb2.reply(answer="success")

    def register_mapper(self, request, context):
        print("Mapper "+ str(request.key)+" started at: " + str(request.ip) + ":" + str(request.port))
        context.set_code(grpc.StatusCode.OK)

        return protos_pb2.reply(answer="success")

    def register_reducer(self, request, context):
        print("Reducer "+ str(request.key)+" started at: " + str(request.ip) + ":" + str(request.port))
        context.set_code(grpc.StatusCode.OK)

        return protos_pb2.reply(answer="success")


    def SubmitJob(self,request,context):
        print("Received job request from client: " + str(request.input_location) + " " + str(request.output_location) + " " + str(request.m) + " " + str(request.r))
        global input_location
        global output_location
        global m
        global r
        if(os.path.isdir(request.input_location) and os.path.isdir(request.output_location) and request.m > 0 and request.r > 0):
            input_location = request.input_location
            output_location = request.output_location
            m = request.m
            r = request.r
            context.set_code(grpc.StatusCode.OK)
            # call mapper and reducer here
            print("spawning mapper processes...")
            for i in range(m):
                port = str(606) + str(i)
                # print(port)
                process = multiprocessing.Process(target=mapper.serve, args=(port,i,r))
                # print(process)
                try:
                    process.start()
                    # print("Mapper "+str(i)+" started at port "+port)
                except:
                    print("Error: unable to start process")
            
            print("distributing input files to mappers...")

            fileslist = [[] for i in range(m)]

            files = os.listdir(input_location)

            for i in range(len(files)):
                fileslist[i%m].append(input_location+"/"+files[i])
            
            print(fileslist)
            count = 0
            if(len(files)<m):
                m = len(files)
            for i in range(min(m,len(files))):
                print("entered in the loop..")
                port = str(606) + str(i)
                with grpc.insecure_channel("localhost:"+port) as channel:
                    stub = protos_pb2_grpc.WordCountStub(channel)
                    try:
                        response = stub.callMapper(protos_pb2.files(file=fileslist[i]))
                        if response.answer == "success":
                            print("successfully distributed files to mapper "+str(i))
                            count +=1
                        else:
                            print("failed to distribute files to mapper "+str(i))
                    except Exception as e:
                        print("exception: failed to distribute files to mapper "+str(i),e)
                    channel.close()
            if count == min(m,len(files)):
                print("spawning reducer processes...")
                for i in range(r):
                    port = str(707) + str(i)
                    print(port)
                    process = multiprocessing.Process(target=reducer.serve, args=(port,i,m,output_location))
                    # print(process)
                    try:
                        process.start()
                        # print("Reducer "+str(i)+" started at port "+port)
                    except:
                        print("Error: unable to start process")
            reducer_files = [[] for i in range(r)]
            

            for j in range(r):
                for i in range(m):
                    reducer_files[j].append("intermediate_files/if"+str(i)+"/p"+str(j)+".txt")
            
            print(reducer_files)
            count = 0
            for i in range(r):
                # print("entered in the loop..")
                port = str(707) + str(i)
                with grpc.insecure_channel("localhost:"+port) as channel:
                    stub = protos_pb2_grpc.WordCountStub(channel)
                    try:
                        response = stub.callReducer(protos_pb2.files(file=reducer_files[i]))
                        if response.answer == "success":
                            print("successfully distributed files to reducer "+str(i))
                            count +=1
                        else:
                            print("failed to distribute files to reducer "+str(i))
                    except Exception as e:
                        print("exception: failed to distribute files to reducer "+str(i),e)
                    channel.close()
            if count == r:
                return protos_pb2.reply(answer="success")
            else:
                return protos_pb2.reply(answer="failure")
        
        else:
        
            return protos_pb2.reply(answer="failure")
        # return protos_pb2.reply(answer="success")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos_pb2_grpc.add_WordCountServicer_to_server(Master(), server)
    server.add_insecure_port('localhost:50050')
    print("Master started on port 50050")
    
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()