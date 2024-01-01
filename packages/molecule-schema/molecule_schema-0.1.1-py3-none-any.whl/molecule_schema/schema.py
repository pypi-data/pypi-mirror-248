import sys
import io
import struct
from abc import ABCMeta
from collections import OrderedDict

from molecule_schema.base import SchemaABC, ReaderABC

TopmostOrderedDict = dict if sys.version_info >= (3, 7) else OrderedDict
NoneView = memoryview(b"")


def ensure_memoryview(buffer):
    return buffer if isinstance(buffer, memoryview) else memoryview(buffer)


class ByteReader(ReaderABC):
    def __init__(self, buffer):
        if len(buffer) != 1:
            raise ValueError(f"Expect buffer of length 1, got {len(buffer)}")
        self.__view = ensure_memoryview(buffer)

    @property
    def value(self):
        return self.__view[0]

    def getbuffer(self):
        return self.__view


class Byte(SchemaABC):
    @classmethod
    def pack(cls, value, out=None):
        """
        Pack int as a molecule byte.
        """
        out = out or io.BytesIO()

        out.write(bytes([value]))
        return out.getbuffer()[-1:]

    @classmethod
    def attach(cls, buffer):
        return ByteReader(buffer)

    @classmethod
    def unpack(cls, buffer):
        return buffer[0]


class BytesReader(ReaderABC):
    def __init__(self, buffer):
        (size,) = struct.unpack("<i", buffer[:4])
        if len(buffer) != 4 + size:
            raise ValueError(f"Expect buffer of length {4 + size}, got {len(buffer)}")
        self.__view = ensure_memoryview(buffer)
        self.__value = self.__view[4:]

    @property
    def value(self):
        return self.__value

    def getbuffer(self):
        return self.__view


class Bytes(bytearray, SchemaABC):
    @classmethod
    def pack(cls, value, out=None):
        """
        Pack bytes-like object into molecule vector<byte>
        """
        out = out or io.BytesIO()

        size = len(value)
        out.write(struct.pack("<i", size))
        out.write(value)
        return out.getbuffer()[-(size + 4) :]

    @classmethod
    def unpack(cls, buffer):
        """
        Unpack vector<byte> into bytearray
        """
        return bytearray(cls.attach(buffer).value)

    @classmethod
    def attach(cls, buffer):
        return BytesReader(buffer)


class SchemaFieldsMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        if SchemaABC not in bases and "__fields__" not in attrs:
            attrs_fields = [k for k in attrs.keys() if not k.startswith("__")]
            annotations = attrs.get("__annotations__", {})
            if len(attrs_fields) > 0 and len(annotations) > 0:
                raise TypeError(
                    f"{name} fields order is not guaranteed. Use __fields__ to list field names."
                )
            elif len(attrs_fields) > 0:
                if not isinstance(attrs, TopmostOrderedDict):
                    raise TypeError(
                        f"{name} fields order is not guaranteed. Use __fields__ to list field names."
                    )
                attrs["__fields__"] = attrs_fields
            elif len(annotations) > 0:
                if not isinstance(annotations, TopmostOrderedDict):
                    raise TypeError(
                        f"{name} fields order is not guaranteed. Use __fields__ to list field names."
                    )
                attrs["__fields__"] = list(annotations.keys())
            else:
                raise TypeError("Fields not found")

            for field in attrs["__fields__"]:
                if field not in annotations:
                    annotations[field] = attrs[field].__class__
            for field, cls in annotations.items():
                if not issubclass(cls, SchemaABC):
                    raise TypeError(
                        f"{name} field `{field}` is not an instance of molecule schema type."
                    )
            attrs["__annotations__"] = annotations

        return super().__new__(mcs, name, bases, attrs)


class TableReader(ReaderABC):
    def __init__(self, buffer):
        (size, offset0) = struct.unpack("<2i", buffer[:8])
        if len(buffer) != size:
            raise ValueError(f"Expect buffer of length {size}, got {len(buffer)}")
        self.__view = ensure_memoryview(buffer)
        bounds = [offset0]
        offsets_len = offset0 // 4 - 1
        if offsets_len > 0:
            bounds.extend(struct.unpack(f"<{offsets_len-1}i", buffer[8:offset0]))
        bounds.append(size)
        self.__fields = [
            self.__view[bounds[i] : bounds[i + 1]] for i in range(offsets_len)
        ]

    def __getitem__(self, k):
        """
        Get the buffer view of the k-th field
        """
        try:
            return self.__fields[k]
        except IndexError:
            return NoneView

    def getbuffer(self):
        return self.__view


def make_table_reader_property(field_cls, i):
    @property
    def get_property(self):
        return field_cls.attach(self[i])

    return get_property


class TableMeta(SchemaFieldsMeta):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        if SchemaABC not in bases:
            reader_attrs = TopmostOrderedDict(
                {"__annotations__": cls.__annotations__, "__fields__": cls.__fields__}
            )
            for [i, field] in enumerate(cls.__fields__):
                field_cls = cls.__annotations__[field]
                reader_attrs[field] = make_table_reader_property(field_cls, i)
            cls.Reader = type(f"{name}Reader", (TableReader,), reader_attrs)

        return cls


class Table(SchemaABC, metaclass=TableMeta):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.__fields__:
                raise AttributeError(f"Unexpected field {k}")
            setattr(self, k, v)

    @classmethod
    def pack(cls, value=None, out=None, **kwargs):
        out = out or io.BytesIO()

        if value is not None and len(kwargs):
            raise ValueError("value and kwargs cannot be provided together")

        value = value if isinstance(value, cls) else cls(**(value or kwargs))

        start_pos = out.tell()
        header = [0] * (1 + len(cls.__fields__))
        out.seek(4 * len(cls.__fields__) + 4)
        for i, field in enumerate(cls.__fields__):
            header[i + 1] = out.tell() - start_pos
            field_value = getattr(value, field, None)
            field_cls = cls.__annotations__[field]
            field_cls.pack(field_value, out)
        end_pos = out.tell()

        header[0] = end_pos - start_pos
        out.seek(start_pos)
        out.write(struct.pack(f"<{len(header)}i", *header))
        out.seek(end_pos)

        return out.getbuffer()[start_pos:end_pos]

    @classmethod
    def unpack(cls, buffer):
        reader = cls.attach(buffer)
        value = cls()
        for [i, field] in enumerate(cls.__fields__):
            buffer = reader[i]
            setattr(value, field, cls.__annotations__[field].unpack(buffer))

        return value

    @classmethod
    def attach(cls, buffer):
        return cls.Reader(buffer)


class SchemaValueFieldMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        if SchemaABC not in bases:
            annotations = attrs.get("__annotations__", {})
            if "value" not in annotations:
                if "value" not in attrs:
                    raise TypeError(f"{name} field `value` is not provided.")
                annotations["value"] = attrs["value"].__class__
            if not issubclass(annotations["value"], SchemaABC):
                raise TypeError(
                    f"{name} field `value` is not an instance of molecule schema type."
                )
            attrs["__annotations__"] = annotations

        return super().__new__(mcs, name, bases, attrs)


class Option(SchemaABC, metaclass=SchemaValueFieldMeta):
    @classmethod
    def pack(cls, value, out=None):
        out = out or io.BytesIO()

        if value is not None:
            return cls.__annotations__["value"].pack(value, out)

        return NoneView

    @classmethod
    def unpack(cls, buffer):
        if len(buffer) != 0:
            return cls.__annotations__["value"].unpack(buffer)

        return None

    @classmethod
    def attach(cls, buffer):
        if len(buffer) != 0:
            return cls.__annotations__["value"].attach(buffer)

        return None
