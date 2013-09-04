
# not yet running, might be needed to ensure that index imported in catalog.xml is not pruned
def importFinalSteps(context): 
    """
    The last bit of code that runs as part of this setup profile.
    """
    site = context.getSite()
    site.portal_catalog.manage_reindexIndex(ids=['corporateId','supplierId', 'customerId', 'discount', 'storeId', 'posId', 'externalId', 'personal_id'])
