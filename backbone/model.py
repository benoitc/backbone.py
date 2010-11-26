# -*- coding: utf-8 -*-
#
# This file is part of backbone released under the Apache 2 license. 
# See the NOTICE for more information.


class Model(object):
    _dynamic_properties = None

    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)

    def __setattr__(self, key, value):
        if key not in dir(self):
            if not self._dynamic_properties:
                self._dynamic_properties = {}
            self._dynamic_properties[key] = value
            print "ici"
        else:
            object.__setattr__(self, key, value)

    def __delattr__(self, key):
        if self._dynamic_properties and \
                key in self._dynamic_properties:
            del self._dynamic_properties[key]
        else:
            object.__delattr__(self, key)

    def __getattr__(self, key):
        if self._dynamic_properties and \
                key in self._dynamic_properties:
            return self._dynamic_properties[key]
        return self.__dict__[key]

    def __getitem__(self, key):
        try:
            attr = getattr(self, key)
            if callable(attr):
                raise AttributeError
            return attr
        except AttributeError, e:
            if key in self._doc:
                return self._doc[key]
            raise

    def __setitem__(self, key, value):
        """ add a property """
        setattr(self, key, value)


    def __delitem__(self, key):
        """ delete a property """
        try:
            delattr(self, key)
        except AttributeError, e:
            raise KeyError, e


    def __contains__(self, key):
        """ does object contain this propery ?

        @param key: name of property

        @return: True if key exist.
        """
        if key in self._dynamic_properties:
            return True

        return False

    def __iter__(self):
        """ iter document instance properties """
        for k in self._dynamic_properies:
            yield k, self[k]
        raise StopIteration

    def attributes(self):
        return self._dynamic_properies
    attributes = property(attributes)

    def fetch(*args, **optiosn):
        raise NotImplementedError


