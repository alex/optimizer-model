class PersistentDict(object):
    def __init__(self):
        super(PersistentDict, self).__init__()
        self._root = None
        self._count = 0
        self._has_none = False
        self._none_val = None

    @classmethod
    def _new(cls, count, root, has_none, none_val):
        self = cls.__new__(cls)
        self._count = count
        self._root = root
        self._has_none = has_none
        self._none_val = none_val
        return self

    def __len__(self):
        return self._count

    def __iter__(self):
        return self.iterkeys()

    def __contains__(self, key):
        try:
            self.getitem(key)
        except KeyError:
            return False
        else:
            return True

    def getitem(self, key):
        if key is None:
            if self._has_none:
                return self._none_val
            else:
                raise KeyError(key)
        if self._root is not None:
            return self._root.getitem(0, key, hash(key))
        raise KeyError(key)

    def setitem(self, key, val):
        if key is None:
            if self._has_none and val == self._none_val:
                return self
            return self._new(self._count if self._has_none else self._count + 1, self._root, True, val)
        root = (BitmapIndexedNode.EMPTY if self._root is None else self._root)
        new_root, added = root.setitem(0, key, hash(key), val)
        if new_root is root:
            return self
        return self._new(self._count + 1 if added else self._count, new_root, self._has_none, self._none_val)

    def delitem(self, key):
        if key is None:
            if self._has_none:
                return self._new(self._count - 1, self._root, False, None)
            else:
                raise KeyError(key)
        if self._root is None:
            raise KeyError(key)
        new_root = self._root.delitem(0, key, hash(key))
        return self._new(self._count - 1, new_root, self._has_none, self._none_val)

    def get(self, key, default=None):
        try:
            return self.getitem(key)
        except KeyError:
            return default

    def iterkeys(self):
        for k, v in self.iteritems():
            yield k

    def itervalues(self):
        for k, v in self.iteritems():
            yield v

    def iteritems(self):
        if self._root is None:
            return iter([])
        return self._root.iteritems()

    def keys(self):
        return [k for k, v in self.iteritems()]

    def values(self):
        return [v for k, v in self.iteritems()]

    def items(self):
        return list(self.iteritems())


class Node(object):
    pass


class BitmapIndexedNode(Node):
    def __init__(self, bitmap, data):
        super(BitmapIndexedNode, self).__init__()
        self.bitmap = bitmap
        self.data = data

    def index(self, bit):
        return bitcount(self.bitmap & (bit - 1))

    def getitem(self, shift, key, hash_val):
        bit = bitpos(hash_val, shift)
        if (self.bitmap & bit) == 0:
            raise KeyError(key)
        idx = self.index(bit)
        key_or_none = self.data[2 * idx]
        val_or_node = self.data[2 * idx + 1]
        if key_or_none is None:
            return val_or_node.getitem(shift + 5, key, hash_val)
        if key == key_or_none:
            return val_or_node
        raise KeyError(key)

    def setitem(self, shift, key, hash_val, val):
        bit = bitpos(hash_val, shift)
        idx = self.index(bit)
        if (self.bitmap & bit) != 0:
            key_or_none = self.data[2 * idx]
            val_or_node = self.data[2 * idx + 1]
            if key_or_none is None:
                n, added = val_or_node.setitem(shift + 5, key, hash_val, val)
                if n is val_or_node:
                    return self, False
                data = self.data[:]
                data[2 * idx + 1] = n
                return BitmapIndexedNode(self.bitmap, data), added
            if key == key_or_none:
                if val == val_or_node:
                    return self, False
                data = self.data[:]
                data[2 * idx + 1] = val
                return BitmapIndexedNode(self.bitmap, data), False
            data = self.data[:]
            data[2 * idx] = None
            data[2 * idx + 1] = create_node(shift + 5, key_or_none, val_or_node, key, hash_val, val)
            return BitmapIndexedNode(self.bitmap, data), True
        else:
            n = bitcount(self.bitmap)
            if n >= 16:
                nodes = [None] * 32
                jdx = mask(hash_val, shift)
                nodes[jdx], added = BitmapIndexedNode.EMPTY.setitem(shift + 5, key, hash_val, val)
                j = 0
                for i in xrange(32):
                    if (self.bitmap >> i) & 1 != 0:
                        if self.data[j] is None:
                            nodes[i] = self.data[j + 1]
                        else:
                            nodes[i], _ = BitmapIndexedNode.EMPTY.setitem(shift + 5, self.data[j], hash(self.data[j]), self.data[j + 1])
                            added = True
                        j += 2
                return ArrayNode(n + 1, nodes), added
            else:
                new_data = [None] * (2 * (n + 1))
                new_data[:2 * idx] = self.data[:2 * idx]
                new_data[2 * idx] = key
                new_data[2 * idx + 1] = val
                new_data[2 * (idx + 1):2 * (n - idx)] = self.data[2 * idx:2 * (n - idx)]
                return BitmapIndexedNode(self.bitmap | bit, new_data), True

    def delitem(self, shift, key, hash_val):
        bit = bitpos(hash_val, shift)
        if (self.bitmap & bit) == 0:
            raise KeyError(key)
        idx = self.index(bit)
        key_or_none = self.data[2 * idx]
        val_or_node = self.data[2 * idx + 1]
        if key_or_none is None:
            n = val_or_node.delitem(shift + 5, key, hash_val)
            if n is not None:
                data = self.data[:]
                data[2 * idx + 1] = n
                return BitmapIndexedNode(self.bitmap, data)
            if self.bitmap == bit:
                return None
            data = self.data[:2 * idx] + self.data[2 * idx + 2:]
            return BitmapIndexedNode(self.bitmap ^ bit, data)
        if key == key_or_none:
            data = self.data[:]
            data = self.data[:2 * idx] + self.data[2 * idx + 2:]
            return BitmapIndexedNode(self.bitmap ^ bit, data)
        raise KeyError(key)

    def iteritems(self):
        for i in xrange(0, len(self.data), 2):
            if self.data[i] is None:
                for item in self.data[i + 1].iteritems():
                    yield item
            else:
                yield (self.data[i], self.data[i + 1])

BitmapIndexedNode.EMPTY = BitmapIndexedNode(0, [])


class ArrayNode(Node):
    def __init__(self, count, data):
        super(ArrayNode, self).__init__()
        self.count = count
        self.data = data

    def getitem(self, shift, key, hash_val):
        idx = mask(hash_val, shift)
        node = self.data[idx]
        if node is None:
            raise KeyError(key)
        return node.getitem(shift + 5, key, hash_val)

    def setitem(self, shift, key, hash_val, val):
        idx = mask(hash_val, shift)
        node = self.data[idx]
        if node is None:
            data = self.data[:]
            data[idx], _ = BitmapIndexedNode.EMPTY.setitem(shift + 5, key, hash_val, val)
            return ArrayNode(self.count + 1, data), True
        n, added = node.setitem(shift + 5, key, hash_val, val)
        if n is node:
            return self, False
        data = self.data[:]
        data[idx] = n
        return ArrayNode(self.count, data), True

    def delitem(self, shift, key, hash_val):
        idx = mask(hash_val, shift)
        node = self.data[idx]
        if node is None:
            raise KeyError(key)
        n = node.delitem(shift + 5, key, hash_val)
        if n is None:
            if self.count < 8:
                raise NotImplementedError
            else:
                data = self.data[:]
                data[idx] = n
                return ArrayNode(self.count - 1, data)
        else:
            data = self.data[:]
            data[idx] = n
            return ArrayNode(self.count, data)


class HashCollisionNode(Node):
    def __init__(self, hash_val, count, data):
        super(HashCollisionNode, self).__init__()
        self.hash_val = hash_val
        self.count = count
        self.data = data

    def find_index(self, key):
        for i in xrange(0, 2 * self.count, 2):
            if key == self.data[i]:
                return i
        return -1

    def getitem(self, shift, key, hash_val):
        idx = self.find_index(key)
        if idx < 0:
            raise KeyError(key)
        if key == self.data[idx]:
            return self.data[idx + 1]
        raise KeyError

    def setitem(self, shift, key, hash_val, val):
        if hash_val == self.hash_val:
            idx = self.find_index(key)
            if idx < 0:
                return HashCollisionNode(self.hash_val, self.count + 1, self.data + [key, val]), True
            elif self.data[idx + 1] == val:
                return self, False
            else:
                data = self.data[:]
                data[idx + 1] = val
                return HashCollisionNode(self.hash_val, self.count, data), True
        return BitmapIndexedNode(bitpos(self.hash_val, shift), [None, self]).setitem(shift, key, hash_val, val)

    def delitem(self, shift, key, hash_val):
        idx = self.find_index(key)
        if idx < 0:
            raise KeyError(key)
        if self.count == 0:
            return None
        data = self.data[:idx] + self.data[idx + 2:]
        return HashCollisionNode(self.hash_val, self.count - 1, data)

    def iteritems(self):
        for i in xrange(0, len(self.data), 2):
            yield self.data[i], self.data[i + 1]


def create_node(shift, key1, val1, key2, hash_val2, val2):
    hash_val1 = hash(key1)
    if hash_val1 == hash_val2:
        return HashCollisionNode(hash_val1, 2, [key1, val1, key2, val2])
    node, _ = BitmapIndexedNode.EMPTY.setitem(shift, key1, hash_val1, val1)
    node, _ = node.setitem(shift, key2, hash_val2, val2)
    return node


def bitpos(hash_val, shift):
    return 1 << mask(hash_val, shift)


def mask(hash_val, shift):
    return (hash_val >> shift) & 0x01F


def bitcount(n):
    i = 0
    while n:
        if n & 1:
            i += 1
        n >>= 1
    return i
