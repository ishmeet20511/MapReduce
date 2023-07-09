from concurrent import futures

import grpc
import protos_pb2
import protos_pb2_grpc
import uuid
import random

ip = "localhost"
port = "50060"

pr_ip = ""
pr_port = ""


def Submit(inputfilelocation, outputfilelocation, m, r):
    with grpc.insecure_channel("localhost:50050") as channel:
        stub = protos_pb2_grpc.WordCountStub(channel)
        response = stub.SubmitJob(protos_pb2.JobRequest(input_location=inputfilelocation, output_location=outputfilelocation, m=m, r=r))
        if(response.answer == "success"):
            print("Work is done! You can check the files in the output folder...")
            

        else:
            print("Something wrong happend... Please try again later...")
        # print("response: ",response)

def run():
    with grpc.insecure_channel("localhost:50050") as channel:
        stub = protos_pb2_grpc.WordCountStub(channel)
        nd = protos_pb2.node()
        nd.ip = ip
        nd.port = port
        response = stub.clientStartup(nd)
        print(response)
        if(response.answer == "success"):
            print("Client successfully connected to master...")
        else:
            print("Client failed to connect to master...")
        

        inputfilelocation = input("Enter the input file location: ")
        outputfilelocation = input("Enter the output file location: ")
        m = int(input("Enter the number of mappers: "))
        r = int(input("Enter the number of reducers: "))
        # inputfilelocation ="input"
        # outputfilelocation = "output"
        # m = 2
        # r = 2
        Submit(inputfilelocation, outputfilelocation, m, r)
        channel.close()
        
if __name__ == '__main__':
    run()