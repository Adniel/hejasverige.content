from Products.CMFPlone.utils import safe_unicode
from ZODB.POSException import ConflictError
from BTrees.Length import Length
from BTrees.IIBTree import IITreeSet

from logging import getLogger
import sys

_marker = []
LOG = getLogger('Zope.UnIndex')

def patchedRemoveForwardIndexEntry(self, entry, documentId):
    """Take the entry provided and remove any reference to documentId
    in its entry in the index.
    """
    #print 'PATCH: removeForwardIndexEntry -> patchedRemoveForwardIndexEntry'
    entry = safe_unicode(entry)

    indexRow = self._index.get(entry, _marker)
    if indexRow is not _marker:
        try:
            indexRow.remove(documentId)
            if not indexRow:
                del self._index[entry]
                self._length.change(-1)

        except ConflictError:
            raise

        except AttributeError:
            # index row is an int
            try:
                del self._index[entry]
            except KeyError:
                # XXX swallow KeyError because it was probably
                # removed and then _length AttributeError raised
                pass 
            if isinstance(self.__len__, Length):
                self._length = self.__len__
                del self.__len__ 
            self._length.change(-1)

        except:
            LOG.error('%s: unindex_object could not remove '
                      'documentId %s from index %s.  This '
                      'should not happen.' % (self.__class__.__name__,
                       str(documentId), str(self.id)),
                       exc_info=sys.exc_info())
    else:
        LOG.error('%s: unindex_object tried to retrieve set %s '
                  'from index %s but couldn\'t.  This '
                  'should not happen.' % (self.__class__.__name__,
                  repr(entry), str(self.id)))

def patchedInsertForwardIndexEntry(self, entry, documentId):
    """Take the entry provided and put it in the correct place
    in the forward index.

    This will also deal with creating the entire row if necessary.
    """
    #print 'PATCH: insertForwardIndexEntry -> patchedInsertForwardIndexEntry'

    # this makes it possible to import external xml data but distroys when creating invoices
    # what to do? what to do?
    entry = safe_unicode(entry)
    indexRow = self._index.get(entry, _marker)

    # Make sure there's actually a row there already. If not, create
    # a set and stuff it in first.
    if indexRow is _marker:
        # We always use a set to avoid getting conflict errors on
        # multiple threads adding a new row at the same time
        self._index[entry] = IITreeSet((documentId, ))
        self._length.change(1)
    else:
        try:
            indexRow.insert(documentId)
        except AttributeError:
            # Inline migration: index row with one element was an int at
            # first (before Zope 2.13).
            indexRow = IITreeSet((indexRow, documentId))
            self._index[entry] = indexRow


# Products.CMFCore-2.2.7-py2.7.egg/Products/CMFCore/ActionInformation.py
from Acquisition import aq_parent
from zope.i18nmessageid import Message

def patchedGetInfoData(self):
    """ Get the data needed to create an ActionInfo.
    """
    #print "Using monkey patched getInfoData..."
    category_path = []
    lazy_keys = []
    lazy_map = {}

    lazy_map['id'] = self.getId()

    parent = aq_parent(self)
    while parent is not None and parent.getId() != 'portal_actions':
        category_path.append( parent.getId() )
        parent = aq_parent(parent)
    lazy_map['category'] = '/'.join(category_path[::-1])

    for id, val in self.propertyItems():
        if id.endswith('_expr'):
            id = id[:-5]
            if val:
                val = getattr(self, '%s_expr_object' % id)
                lazy_keys.append(id)
            elif id == 'available':
                val = True
        elif id == 'i18n_domain':
            continue
        elif id == 'link_target':
            val = val or None
        elif self.i18n_domain and id in ('title', 'description'):
            val = Message(safe_unicode(val), self.i18n_domain)
        lazy_map[id] = val

    return (lazy_map, lazy_keys)

from zope.formlib.interfaces import ConversionError
from zope.formlib.i18n import _

def _patchedToFieldValue(self, input):
    #print 'Patched!!!'
    from Products.CMFPlone.utils import safe_unicode               
    #if self.convert_missing_value and input == self._missing:
    if self.convert_missing_value and safe_unicode(input) == self._missing:
        value = self.context.missing_value
    else:
        # We convert everything to unicode. This might seem a bit crude,
        # but anything contained in a TextWidget should be representable
        # as a string. Note that you always have the choice of overriding
        # the method.
        try:
            value = safe_unicode(input)
            #value = unicode(input)
        except ValueError, v:
            raise ConversionError(_("Invalid text data"), v)
    return value
