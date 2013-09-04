from five import grok
from hejasverige.content.sports import IClub
from plone.indexer.decorator import indexer

@grok.adapter(IClub, name='personal_id')
@indexer(IClub)
def clubPersonalIdIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``personal_id`` index with the related VatNo of the club.
    """
    personal_id = context.VatNo
    personal_id = personal_id.replace('-','')
    print "Indexing", personal_id, "as external id for Club with id ", context.UID(), "."
    #import pdb; pdb.set_trace()
    return personal_id
#grok.global_adapter(clubPersonalIdIndexer, name="personal_id")
