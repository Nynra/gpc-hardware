"""Base classe for handeling communication to a background process.

This module was created by J. Scheffer and modified by B. Klein Ikkink.
"""

import multiprocessing as mp
from typing import TypeVar, Generic, Callable, Any, Type
from ..exceptions import catch_remote_exceptions


T = TypeVar("T", bound=Callable[..., Any])


class _PipePuppeteer(mp.Process):
    """
    A process managing communication between processes and executing methods of a given class.

    This class serves as a bridge between processes, enabling the execution of methods
    from a provided class (puppet_class) in a separate process. It listens for method
    calls and executes them on an instance of the provided class.
    """
    _SIGNINT_MSG = 'SIGINT'

    def _init_(self, conn, puppet_class: Type[T]) -> ...:
        """Initialize the process.
        
        Parameters
        ----------
        conn : multiprocessing.Connection
            Connection object for communication. The connection is used to send method
            calls and receive results.
        puppet_class : Type[T]
            Class type whose methods will be executed in the separate process.
        """
        super()._init_()
        self._conn = conn
        self._puppet_class = puppet_class

    @catch_remote_exceptions
    def run(self):
        """
        Main execution loop of the process.

        This method is executed when the process starts. It initializes an instance of
        the provided class (puppet_class) and listens for method calls through the
        communication pipe. Upon receiving a method call, it executes the method with
        provided arguments and sends back the result.
        """
        # initialize the class only after the process has been started
        # to prevent pickling errors
        self._puppet = self._puppet_class()

        # main loop
        while True:
            attr, args, kwargs = self._conn.recv()
            if attr == self._SIGNINT_MSG:
                self._conn.close()
                break
            else:
                res = getattr(self._puppet, attr)(*args, **kwargs)
                self._conn.send(res)


class ProcPipe(Generic[T]):
    """
    Provides an interface to put a class in a separate process and still be able to call its methods.

    This class starts a separate process in which it instantiates the provided class.
    A (multiprocessing) pipe is used to communicate between the main process and the process executing.
    When a method is called on an instance of this class, it sends the method name and arguments to the
    process, waits for the result, and returns it to the caller.
    """

    def _init_(self, puppet_class: Type[T]) -> ...:
        """Initialize the process pipe.
        
        Parameters
        ----------
        puppet_class : Type[T]
            Class type whose methods will be executed in the separate process.
        """
        self._pipe_conn1, self._pipe_conn2 = mp.Pipe()
        self._process = _PipePuppeteer(self._pipe_conn2, puppet_class)
        self.__process.start()

        # Dynamically create method proxies for each method of the puppet_class
        # to enable calling them directly on an instance of this class.
        for method_name in dir(puppet_class):
            if callable(
                getattr(puppet_class, method_name)
            ) and not method_name.startswith("__"):
                setattr(self, method_name, self._create_method_proxy(method_name))

    def _create_method_proxy(self, method_name: str) -> Callable[..., Any]:
        """
        Create a method proxy to call the method on the puppet_class instance.

        Parameters
        ----------
        method_name : str
            Name of the method to create a proxy for.

        Returns
        -------
        Callable[..., Any]
            Method proxy.
        """

        def method_proxy(*args, **kwargs):
            self.__pipe_conn1.send((method_name, args, kwargs))
            return self.__pipe_conn1.recv()

        return method_proxy

