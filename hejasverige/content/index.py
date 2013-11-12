# -*- coding: utf-8 -*-

from five import grok
from hejasverige.content.sports import IClub
from hejasverige.content.person import IRelation
from plone.indexer.decorator import indexer
from plone.app.uuid.utils import uuidToObject


#@grok.adapter(IClub, name='personal_id')
@indexer(IClub)
def clubPersonalIdIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``personal_id`` index with the related VatNo of the club.
    """
    try:
        vat_no = context.VatNo
        vat_no = vat_no.replace('-', '')
        print "Indexing", vat_no, "as personal_id for Club with id ", context.UID(), "."
        #import pdb; pdb.set_trace()

        # TODO: Reindex also relations.
        # Vat_no används i api för att filtrera bort föreningar.
        return vat_no
    except Exception:
        #import pdb; pdb.set_trace()
        print 'index failed'
    return ''

grok.global_adapter(clubPersonalIdIndexer, name="personal_id")


# Indexersers does not work. They do for some reason not index content correct,
# fix, fix, fix.
# when it work, change object retreiavel in my-person view
#@grok.adapter(IRelation, name='Title')
@indexer(IRelation)
def relationTitleIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``title`` index with the related name of the club.
    """
    try:
        print "Indexing title for a relation. J!"
        #import pdb; pdb.set_trace()
        return uuidToObject(context.foreign_id).Title()
    except Exception:
        print 'index failed'
        #import pdb; pdb.set_trace()
    return ''
grok.global_adapter(relationTitleIndexer, name="Title")


#@grok.adapter(IRelation, name='externalId')
@indexer(IRelation)
def relationExternalIdIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``externalId`` index with the related uid of the club.
    """
    try:
        externalId = uuidToObject(context.foreign_id).UID()
        print "Indexing", externalId, "as external id for a relation with id", context.UID(), "."
        return externalId
    except Exception:
        print 'index failed'
        #import pdb; pdb.set_trace()
    return ''
grok.global_adapter(relationExternalIdIndexer, name="externalId")

#@grok.adapter(IRelation, name='Sport')
@indexer(IRelation)
def relationSportIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``Sport`` index with the related uid of the club.
    """
    try:
        sport = uuidToObject(context.foreign_id).Sport
        print "Indexing", sport, "as external id for a relation with id", context.UID(), "."
        #import pdb; pdb.set_trace()
        return sport
    except Exception:
        print 'index failed'
        #import pdb; pdb.set_trace()
    return ''
grok.global_adapter(relationSportIndexer, name="Sport")


@indexer(IRelation)
def relationPersonalIdIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``Sport`` index with the related uid of the club.
    """
    try:
        vat_no = uuidToObject(context.foreign_id).VatNo
        vat_no = vat_no.replace('-','')
        print "Indexing", vat_no, "as personal_id for a relation with id", context.UID(), "."
        #import pdb; pdb.set_trace()
        return vat_no
    except Exception:
        print 'index failed'
        #import pdb; pdb.set_trace()
    return ''
grok.global_adapter(relationPersonalIdIndexer, name="personal_id")
