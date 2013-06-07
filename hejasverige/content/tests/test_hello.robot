*** Settings ***

Resource  ./eggs/plone.app.robotframework-0.5.0-py2.7.egg/plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${DISTIRCT_FOLDER_DESCRIPTION}  Blah, description
${DISTRICT_FOLDER_NAME}  Distrikt

*** Test Cases ***

Plone is installed
    Go to  ${PLONE_URL}
    Page should contain  Powered by Plone

Site Administrator can access control panel
    Given I'm logged in as a 'Site Administrator'
     When I open the personal menu
     Then I see the Site Setup -link

Site Administrator can create a district folder
	Given I'm logged in as a 'Site Administrator'
	 When I create a district folder 
	 Then Page should contain  Changes savedd



#Let me think what to do next
#    Enable autologin as  Site Administrator
#    Go to  ${PLONE_URL}
#    Import library  Dialogs
#    Pause execution

*** Keywords ***

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

I open the personal menu
    Click link  css=#user-name

I see the Site Setup -link
    Element should be visible  css=#personaltools-plone_setup

I create a district folder
    Go to  ${PLONE_URL}/createObject?type_name=hejasverige.DistrictFolder
    Input text  name=form.widgets.IDublinCore.title  ${DISTRICT_FOLDER_NAME}
    Input text  name=form.widgets.IDublinCore.description  ${DISTIRCT_FOLDER_DESCRIPTION}
    Select From List  xpath=//select[@name="form.widgets.text.mimeType"]  text/x-plone-outputfilters-html
    Input text  form.widgets.text  ${DISTIRCT_FOLDER_DESCRIPTION}
    Click Button  Save

#four districts in district folder
#    a districts 'Distrikt1' in the distict folder
#    a districts 'Distrikt2' in the distict folder
#    a districts 'Distrikt3' in the distict folder
#    a districts 'Distrikt4' in the distict folder


#a district '${title}' in the distict folder
#    Go to  ${PLONE_URL}/${DISTRICT_FOLDER}/createObject?type_name=hejasverige.District
#    Input text  name=title  ${title}
#    Click Button  Save