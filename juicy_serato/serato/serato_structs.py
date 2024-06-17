import struct


class Entry(object):
    FIELDS = ()

    def __init__(self, *args, **kwargs):
        if len(kwargs.keys()) > 0:
            for key, value in kwargs.items():
                setattr(self, key, value)

        else:
            assert len(args) == len(self.FIELDS)
            for field, value in zip(self.FIELDS, args):
                setattr(self, field, value)

    def __repr__(self):
        return '{name}({data})'.format(
            name=self.__class__.__name__,
            data=', '.join('{}={!r}'.format(name, getattr(self, name))
                           for name in self.FIELDS))


class UnknownEntry(Entry):
    NAME = None
    FIELDS = ('data',)

    @classmethod
    def load(cls, data):
        return cls(data)

    def dump(self):
        return self.data


class BpmLockEntry(Entry):
    NAME = 'BPMLOCK'
    FIELDS = ('enabled',)
    FMT = '?'

    @classmethod
    def load(cls, data):
        return cls(*struct.unpack(cls.FMT, data))

    def dump(self):
        return struct.pack(self.FMT, *(getattr(self, f) for f in self.FIELDS))


class ColorEntry(Entry):
    NAME = 'COLOR'
    FMT = 'c3s'
    FIELDS = ('field1', 'color',)

    @classmethod
    def load(cls, data):
        return cls(*struct.unpack(cls.FMT, data))

    def dump(self):
        return struct.pack(self.FMT, *(getattr(self, f) for f in self.FIELDS))


class CueEntry(Entry):
    NAME = 'CUE'
    FMT = '>cBIc3s2s'
    FIELDS = ('field1', 'index', 'position', 'field4', 'color', 'field6',
              'name',)

    @classmethod
    def load(cls, data):
        info_size = struct.calcsize(cls.FMT)
        info = struct.unpack(cls.FMT, data[:info_size])
        name, null_byte, other = data[info_size:].partition(b'\x00')
        assert null_byte == b'\x00'
        assert other == b''
        return cls(*info, name.decode('utf-8'))

    def dump(self):
        struct_fields = self.FIELDS[:-1]
        return b''.join((
            struct.pack(self.FMT, *(getattr(self, f) for f in struct_fields)),
            self.name.encode('utf-8'),
            b'\x00',
        ))


class LoopEntry(Entry):
    NAME = 'LOOP'
    FMT = '>cBII4s4sB?'
    FIELDS = ('field1', 'index', 'startposition', 'endposition', 'field5',
              'field6', 'color', 'locked', 'name',)

    @classmethod
    def load(cls, data):
        info_size = struct.calcsize(cls.FMT)
        info = struct.unpack(cls.FMT, data[:info_size])
        name, null_byte, other = data[info_size:].partition(b'\x00')
        assert null_byte == b'\x00'
        assert other == b''
        return cls(*info, name.decode('utf-8'))

    def dump(self):
        struct_fields = self.FIELDS[:-1]
        return b''.join((
            struct.pack(self.FMT, *(getattr(self, f) for f in struct_fields)),
            self.name.encode('utf-8'),
            b'\x00',
        ))


class FlipEntry(Entry):
    NAME = 'FLIP'
    FMT1 = 'cB?'
    FMT2 = '>BI'
    FMT3 = '>BI16s'
    FIELDS = ('field1', 'index', 'enabled', 'name', 'loop', 'num_actions',
              'actions')

    @classmethod
    def load(cls, data):
        info1_size = struct.calcsize(cls.FMT1)
        info1 = struct.unpack(cls.FMT1, data[:info1_size])
        name, null_byte, other = data[info1_size:].partition(b'\x00')
        assert null_byte == b'\x00'

        info2_size = struct.calcsize(cls.FMT2)
        loop, num_actions = struct.unpack(cls.FMT2, other[:info2_size])
        action_data = other[info2_size:]
        actions = []
        for i in range(num_actions):
            type_id, size = struct.unpack(cls.FMT2, action_data[:info2_size])
            action_data = action_data[info2_size:]
            if type_id == 0:
                payload = struct.unpack('>dd', action_data[:size])
                actions.append(("JUMP", *payload))
            elif type_id == 1:
                payload = struct.unpack('>ddd', action_data[:size])
                actions.append(("CENSOR", *payload))
            action_data = action_data[size:]
        assert action_data == b''

        return cls(*info1, name.decode('utf-8'), loop, num_actions, actions)

    def dump(self):
        raise NotImplementedError('FLIP entry dumps are not implemented!')
