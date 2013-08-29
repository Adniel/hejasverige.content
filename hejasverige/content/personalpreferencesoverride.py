from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.app.users.browser.register import BaseRegistrationForm
import logging
logger = logging.getLogger(__name__)

class CustomizedUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('accept')
        self.form_fields = self.form_fields.omit('kollkoll')


class CustomizedBaseRegistrationForm(BaseRegistrationForm):
    def validate_registration(self, action, data):
    	logger.info('Doing super stuff')
    	super().validate_registration(action, data)