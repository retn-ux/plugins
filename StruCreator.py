import argparse
import idc
import idautils

import sys
import argparse

from retsync.rsconfig import rs_log


arg_parser=argparse.ArgumentParser()
arg_parser.add_argument("-t",'--type',type=str,help="Types of members")
arg_parser.add_argument("-s",'--size',type=int,help="The size of the structure in bytes")
args=arg_parser.parse_args()


member_type=idc.FF_BYTE
member_size=1
if args.type=="Fword":
    member_type=idc.FF_QWORD
    member_size=8

elif args.type=="Dword":
    member_type=idc.FF_DWORD
    member_size=4

elif args.type=="Word":
    member_type=idc.FF_WORD
    member_size=2

elif args.type=="Byte":
    member_type=idc.FF_BYTE
    member_size=1

struct_name="Unknown"
struct_sid=-1
index=0
while struct_sid==-1 or struct_sid==0xFFFFFFFF:
    
    struct_sid=idc.add_struc(-1,struct_name+str(index),0,)
    
    index+=1


rs_log("[StruCreator] The structure creation is complete and the members are created.")

loop_count=args.size//member_size
member_name="uk"
member_offset=0
for i in range(loop_count):
    errcode=idc.add_struc_member(
        struct_sid,
        member_name+str(i),
        member_offset,
        member_type,
        -1,
        member_size
    )
    if(errcode!=0):
        rs_log(
            "[StruCreator] Failed to create member {},error code: {}" 
            .format(member_name+str(i),errcode) 
            )
    member_offset+=member_size

if (args.size%member_size)!=0:
    for i in range((args.size % member_size)):
        errcode=idc.add_struc_member(
            struct_sid,
            member_name+str(loop_count+i),
            member_offset,
            idc.FF_BYTE,
            -1,
            1
        )
        if(errcode!=0):
            rs_log("[StruCreator] Failed to create member {},error code:{}"
            .format(member_name+str(i),errcode))
        member_offset+=1

rs_log("[StruCreator] The structure is created. The structure name is %s" % struct_name+str(index))
