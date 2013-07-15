# -*- coding: utf-8 -*-

from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
#from Acquisition import aq_inner


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    """ Use UserDataPanelAdapter and add additional new fields
        _getProperty is defined in UserPanelAdapter and returns the
        value as safe_unicode
    """

    def get_address1(self):
        return self._getProperty('address1')

    def set_address1(self, value):
        return self.context.setMemberProperties({'address1': value})

    address1 = property(get_address1, set_address1)

    def get_address2(self):
        return self._getProperty('address2')

    def set_address2(self, value):
        return self.context.setMemberProperties({'address2': value})

    address2 = property(get_address2, set_address2)

    def get_postal_code(self):
        return self._getProperty('postal_code')

    def set_postal_code(self, value):
        return self.context.setMemberProperties({'postal_code': value})

    postal_code = property(get_postal_code, set_postal_code)

    def get_city(self):
        return self._getProperty('city')

    def set_city(self, value):
        return self.context.setMemberProperties({'city': value})

    city = property(get_city, set_city)

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
