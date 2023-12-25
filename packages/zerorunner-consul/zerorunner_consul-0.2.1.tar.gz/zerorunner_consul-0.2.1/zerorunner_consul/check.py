# -*- coding: utf-8 -*-
# @author: xiao bai
import logging
import typing
import warnings

log = logging.getLogger(__name__)


class Check(object):
    """检查服务的健康状态 script http tcp ttl docker grpc 等"""

    @classmethod
    def script(cls, args: typing.List, interval: str) -> dict:
        """
        Run the script *args* every *interval* (e.g. "10s") to peform health
        check
        """
        if isinstance(args, str) \
                or isinstance(args, bytes):
            warnings.warn(
                "Check.script should take a list of arg", DeprecationWarning)
            args = ["sh", "-c", args]
        return {'args': args, 'interval': interval}

    @classmethod
    def http(cls, url: str,
             name: str,
             interval: str,
             notes: str,
             method: str = "GET",
             body: str = "",
             status: str = "passing",
             timeout: str = None,
             deregister: str = None,
             header: dict = None,
             tls_skip_verify: bool = None) -> dict:
        """
        Perform a HTTP GET against *url* every *interval* (e.g. "10s") to
        perform health check with an optional *timeout* and optional
        *deregister* after which a failing service will be automatically
        deregistered. Optional parameter *header* specifies headers sent in
        HTTP request. *header* parameter is in form of map of lists of
        strings, e.g. {"x-foo": ["bar", "baz"]}. Optional parameter
        *tls_skip_verify* allow to skip TLS certificate verification.
        """

        ret = {'http': url,
               'interval': interval,
               'name': name,
               'notes': notes,
               'status': status,
               'method': method.upper(),
               'body': body}
        if timeout:
            ret['timeout'] = timeout
        if deregister:
            ret['DeregisterCriticalServiceAfter'] = deregister
        if header:
            ret['header'] = header
        if tls_skip_verify:
            ret['TLSSkipVerify'] = tls_skip_verify
        return ret

    @classmethod
    def tcp(cls, host: str, port: int, interval: str, timeout: str = None, deregister: bool = None) -> dict:
        """
        Attempt to establish a tcp connection to the specified *host* and
        *port* at a specified *interval* with optional *timeout* and optional
        *deregister* after which a failing service will be automatically
        deregistered.
        """
        ret = {
            'tcp': '{host:s}:{port:d}'.format(host=host, port=port),
            'interval': interval
        }
        if timeout:
            ret['timeout'] = timeout
        if deregister:
            ret['DeregisterCriticalServiceAfter'] = deregister
        return ret

    @classmethod
    def ttl(cls, ttl: int):
        """
        Set check to be marked as critical after *ttl* (e.g. "10s") unless the
        check is periodically marked as passing.
        """
        return {'ttl': ttl}

    @classmethod
    def docker(cls, container_id: str, shell: str, script: str, interval: str, deregister: bool = None) -> dict:
        """
        Invoke *script* packaged within a running docker container with
        *container_id* at a specified *interval* on the configured
        *shell* using the Docker Exec API.  Optional *register* after which a
        failing service will be automatically deregistered.
        """
        ret = {
            'docker_container_id': container_id,
            'shell': shell,
            'script': script,
            'interval': interval
        }
        if deregister:
            ret['DeregisterCriticalServiceAfter'] = deregister
        return ret

    @classmethod
    def grpc(cls, grpc: str, interval: str, deregister: bool = None) -> dict:
        """
        grpc (string: "") - Specifies a gRPC check's endpoint that
        supports the standard gRPC health checking protocol.
        The state of the check will be updated at the given
        Interval by probing the configured endpoint. Add the
        service identifier after the gRPC check's endpoint in the
        following format to check for a specific service instead of
        the whole gRPC server /:service_identifier.
        """
        ret = {
            'GRPC': grpc,
            'Interval': interval
        }
        if deregister:
            ret['DeregisterCriticalServiceAfter'] = deregister
        return ret

    @classmethod
    def _compat(
            cls,
            script: str = None,
            interval: str = None,
            ttl: int = None,
            http: str = None,
            timeout: str = None,
            deregister: bool = None):

        if not script and not http and not ttl:
            return {}

        log.warning(
            'DEPRECATED: use consul.Check.script/http/ttl to specify check')

        ret: typing.Any = {'check': {}}

        if script:
            assert interval and not (ttl or http)
            ret['check'] = {'script': script, 'ttl': interval}
        if ttl:
            assert not (interval or script or http)
            ret['check'] = {'ttl': ttl}
        if http:
            assert interval and not (script or ttl)
            ret['check'] = {'http': http, 'interval': interval}
        if timeout:
            assert http
            ret['check']['timeout'] = timeout

        # if deregister:
        #     ret['check']['DeregisterCriticalServiceAfter'] = deregister

        return ret
