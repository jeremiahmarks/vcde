# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-03-28 17:55:54
# @Last Modified by:   jemarks
# @Last Modified time: 2017-03-28 18:02:57

import win32com.client as win32

def sendEmail(toAddress, Subject, HTMLBody, textBody=''):
	outlook = win32.Dispatch('outlook.application')
	surveysEmail = outlook.CreateItem(0)
	surveysEmail.To = toAddress
	surveysEmail.Subject = Subject
	surveysEmail.Body = textBody
	surveysEmail.HTMLBody = HTMLBody
	surveysEmail.Send()

if __name__ == '__main__':
	sendEmail("Jeremiah.Marks@vixxo.com", "This is a test email", HTMLBody = "<p>Hello!  This is simply a test</p>")