# -*- coding: utf-8 -*-

from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from Acquisition import aq_inner

class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    """ Use UserDataPanelAdapter and add additional new fields
        _getProperty is defined in UserPanelAdapter and returns the 
        value as safe_unicode 
    """

    def get_personal_id(self):
        return self._getProperty('personal_id')

    def set_personal_id(self, value):
        return self.context.setMemberProperties({'personal_id': value})

    personal_id = property(get_personal_id, set_personal_id)

    def get_kollkoll(self):
        return self._getProperty('kollkoll')

    def set_kollkoll(self, value):
        return self.context.setMemberProperties({'kollkoll': value})

    kollkoll = property(get_kollkoll, set_kollkoll)

    def get_accept(self):
        return self._getProperty('accept')

    def set_accept(self, value):
        return self.context.setMemberProperties({'accept': value})

    accept = property(get_accept, set_accept)

