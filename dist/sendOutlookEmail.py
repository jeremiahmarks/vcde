# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-03-28 17:55:54
# @Last Modified by:   jemarks
# @Last Modified time: 2017-03-31 15:41:16

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



#########################################
##
##  Example of attaching an item
##
##
## import win32com.client
## 
## s = win32com.client.Dispatch("Mapi.Session")
## o = win32com.client.Dispatch("Outlook.Application")
## s.Logon("Outlook2003")
##     
## Msg = o.CreateItem(0)
## Msg.To = "recipient@domain.com"
##     
## Msg.CC = "more email addresses here"
## Msg.BCC = "more email addresses here"
##     
## Msg.Subject = "The subject of you mail"
## Msg.Body = "The main body text of you mail"
##     
## attachment1 = "Path to attachment no. 1"
## attachment2 = "Path to attachment no. 2"
## Msg.Attachments.Add(attachment1)
## Msg.Attachments.Add(attachment2)
##  
## Msg.Send()	