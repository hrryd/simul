# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import chord_pb2 as chord__pb2


class ChordStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PutKey = channel.unary_unary(
                '/Chord/PutKey',
                request_serializer=chord__pb2.PutKeyRequest.SerializeToString,
                response_deserializer=chord__pb2.GetKeyResponse.FromString,
                )
        self.GetKey = channel.unary_unary(
                '/Chord/GetKey',
                request_serializer=chord__pb2.GetKeyRequest.SerializeToString,
                response_deserializer=chord__pb2.PutKeyResponse.FromString,
                )
        self.Ping = channel.unary_unary(
                '/Chord/Ping',
                request_serializer=chord__pb2.Empty.SerializeToString,
                response_deserializer=chord__pb2.Empty.FromString,
                )
        self.FindSuccessor = channel.unary_unary(
                '/Chord/FindSuccessor',
                request_serializer=chord__pb2.Key.SerializeToString,
                response_deserializer=chord__pb2.Node.FromString,
                )
        self.Notify = channel.unary_unary(
                '/Chord/Notify',
                request_serializer=chord__pb2.Node.SerializeToString,
                response_deserializer=chord__pb2.Empty.FromString,
                )
        self.GetPredecessor = channel.unary_unary(
                '/Chord/GetPredecessor',
                request_serializer=chord__pb2.Empty.SerializeToString,
                response_deserializer=chord__pb2.Node.FromString,
                )


class ChordServicer(object):
    """Missing associated documentation comment in .proto file"""

    def PutKey(self, request, context):
        """Application level
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetKey(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Ping(self, request, context):
        """Protocol level
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindSuccessor(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Notify(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPredecessor(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChordServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PutKey': grpc.unary_unary_rpc_method_handler(
                    servicer.PutKey,
                    request_deserializer=chord__pb2.PutKeyRequest.FromString,
                    response_serializer=chord__pb2.GetKeyResponse.SerializeToString,
            ),
            'GetKey': grpc.unary_unary_rpc_method_handler(
                    servicer.GetKey,
                    request_deserializer=chord__pb2.GetKeyRequest.FromString,
                    response_serializer=chord__pb2.PutKeyResponse.SerializeToString,
            ),
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=chord__pb2.Empty.FromString,
                    response_serializer=chord__pb2.Empty.SerializeToString,
            ),
            'FindSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.FindSuccessor,
                    request_deserializer=chord__pb2.Key.FromString,
                    response_serializer=chord__pb2.Node.SerializeToString,
            ),
            'Notify': grpc.unary_unary_rpc_method_handler(
                    servicer.Notify,
                    request_deserializer=chord__pb2.Node.FromString,
                    response_serializer=chord__pb2.Empty.SerializeToString,
            ),
            'GetPredecessor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPredecessor,
                    request_deserializer=chord__pb2.Empty.FromString,
                    response_serializer=chord__pb2.Node.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Chord', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Chord(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def PutKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/PutKey',
            chord__pb2.PutKeyRequest.SerializeToString,
            chord__pb2.GetKeyResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/GetKey',
            chord__pb2.GetKeyRequest.SerializeToString,
            chord__pb2.PutKeyResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/Ping',
            chord__pb2.Empty.SerializeToString,
            chord__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FindSuccessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/FindSuccessor',
            chord__pb2.Key.SerializeToString,
            chord__pb2.Node.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Notify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/Notify',
            chord__pb2.Node.SerializeToString,
            chord__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPredecessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/GetPredecessor',
            chord__pb2.Empty.SerializeToString,
            chord__pb2.Node.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
