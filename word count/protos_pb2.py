# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cprotos.proto\x12\twordcount\"S\n\nJobRequest\x12\x16\n\x0einput_location\x18\x01 \x01(\t\x12\x17\n\x0foutput_location\x18\x02 \x01(\t\x12\t\n\x01m\x18\x03 \x01(\x05\x12\t\n\x01r\x18\x04 \x01(\x05\"-\n\x04node\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\x05\"\x17\n\x05reply\x12\x0e\n\x06\x61nswer\x18\x01 \x01(\t\"&\n\x08MapInput\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t\"\'\n\tMapOutput\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05\"8\n\rmapOutputList\x12\'\n\tmapOutput\x18\x01 \x03(\x0b\x32\x14.wordcount.MapOutput\"*\n\x0bReduceInput\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0e\n\x06values\x18\x02 \x03(\x05\"*\n\x0cReduceOutput\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05\"A\n\x10reduceOutputList\x12-\n\x0creduceOutput\x18\x01 \x03(\x0b\x32\x17.wordcount.ReduceOutput\"\x15\n\x05\x66iles\x12\x0c\n\x04\x66ile\x18\x01 \x03(\t2\xbc\x03\n\tWordCount\x12\x32\n\rclientStartup\x12\x0f.wordcount.node\x1a\x10.wordcount.reply\x12\x34\n\x0fregister_mapper\x12\x0f.wordcount.node\x1a\x10.wordcount.reply\x12\x35\n\x10register_reducer\x12\x0f.wordcount.node\x1a\x10.wordcount.reply\x12\x34\n\tSubmitJob\x12\x15.wordcount.JobRequest\x1a\x10.wordcount.reply\x12\x30\n\ncallMapper\x12\x10.wordcount.files\x1a\x10.wordcount.reply\x12\x34\n\x03Map\x12\x13.wordcount.MapInput\x1a\x18.wordcount.mapOutputList\x12\x31\n\x0b\x63\x61llReducer\x12\x10.wordcount.files\x1a\x10.wordcount.reply\x12=\n\x06Reduce\x12\x16.wordcount.ReduceInput\x1a\x1b.wordcount.reduceOutputListb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _JOBREQUEST._serialized_start=27
  _JOBREQUEST._serialized_end=110
  _NODE._serialized_start=112
  _NODE._serialized_end=157
  _REPLY._serialized_start=159
  _REPLY._serialized_end=182
  _MAPINPUT._serialized_start=184
  _MAPINPUT._serialized_end=222
  _MAPOUTPUT._serialized_start=224
  _MAPOUTPUT._serialized_end=263
  _MAPOUTPUTLIST._serialized_start=265
  _MAPOUTPUTLIST._serialized_end=321
  _REDUCEINPUT._serialized_start=323
  _REDUCEINPUT._serialized_end=365
  _REDUCEOUTPUT._serialized_start=367
  _REDUCEOUTPUT._serialized_end=409
  _REDUCEOUTPUTLIST._serialized_start=411
  _REDUCEOUTPUTLIST._serialized_end=476
  _FILES._serialized_start=478
  _FILES._serialized_end=499
  _WORDCOUNT._serialized_start=502
  _WORDCOUNT._serialized_end=946
# @@protoc_insertion_point(module_scope)
