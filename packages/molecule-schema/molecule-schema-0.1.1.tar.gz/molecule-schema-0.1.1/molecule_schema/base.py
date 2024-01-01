from abc import ABC, abstractmethod
import io


class SchemaABC(ABC):
    @classmethod
    @abstractmethod
    def pack(cls, value, out=io.BytesIO()):
        """
        Pack value into bytes.

        If `out` is provided, use it as an instance of io.BytesIO and append bytes to it.

        Return a memoryview of the packed bytes.
        """
        pass

    @classmethod
    @abstractmethod
    def unpack(cls, buffer):
        """
        Unpack value from the bytes-like buffer.

        This method copy all the data and create the return value. See `attach` which reads data on demand.
        """
        pass

    @classmethod
    @abstractmethod
    def attach(cls, buffer):
        """
        Attach to the buffer and return a object to read data from buffer on demand.

        It's the undefined behavior to modify the buffer when the returned object is still alive. The returned
        object can take this as an advantage to add cache for better performance.

        See also `unpack` which copies the data from buffer.
        """
        pass


class ReaderABC(ABC):
    @abstractmethod
    def getbuffer(self):
        """
        Get the underlying buffer of the type this reader is reading.
        """
        pass
