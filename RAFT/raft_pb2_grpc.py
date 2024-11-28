# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import raft_pb2 as raft__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in raft_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RAFTStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RequestVote = channel.unary_unary(
                '/raft.RAFT/RequestVote',
                request_serializer=raft__pb2.request_vote_message.SerializeToString,
                response_deserializer=raft__pb2.reply_vote_mesage.FromString,
                _registered_method=True)
        self.ReplicateLog = channel.unary_unary(
                '/raft.RAFT/ReplicateLog',
                request_serializer=raft__pb2.request_replicate_message.SerializeToString,
                response_deserializer=raft__pb2.reply_replicate_massage.FromString,
                _registered_method=True)
        self.AddEntry = channel.unary_unary(
                '/raft.RAFT/AddEntry',
                request_serializer=raft__pb2.request_entry.SerializeToString,
                response_deserializer=raft__pb2.reply_entry.FromString,
                _registered_method=True)


class RAFTServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RequestVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateLog(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddEntry(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RAFTServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RequestVote': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestVote,
                    request_deserializer=raft__pb2.request_vote_message.FromString,
                    response_serializer=raft__pb2.reply_vote_mesage.SerializeToString,
            ),
            'ReplicateLog': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateLog,
                    request_deserializer=raft__pb2.request_replicate_message.FromString,
                    response_serializer=raft__pb2.reply_replicate_massage.SerializeToString,
            ),
            'AddEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.AddEntry,
                    request_deserializer=raft__pb2.request_entry.FromString,
                    response_serializer=raft__pb2.reply_entry.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'raft.RAFT', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('raft.RAFT', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RAFT(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RequestVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/raft.RAFT/RequestVote',
            raft__pb2.request_vote_message.SerializeToString,
            raft__pb2.reply_vote_mesage.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateLog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/raft.RAFT/ReplicateLog',
            raft__pb2.request_replicate_message.SerializeToString,
            raft__pb2.reply_replicate_massage.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/raft.RAFT/AddEntry',
            raft__pb2.request_entry.SerializeToString,
            raft__pb2.reply_entry.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
