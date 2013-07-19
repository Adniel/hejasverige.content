from plone.app.users.browser.personalpreferences import UserDataPanel


class CustomizedUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('accept')
        self.form_fields = self.form_fields.omit('kollkoll')
