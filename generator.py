#!/usr/local/munki/python

# Kai Howells
# kai@automatica.com.au
# 

import os
import sys
import uuid
import optparse
from munkilib import FoundationPlist


def build_plist(sharedSecret, username, password, company, server):

	uuidOne = str(uuid.uuid4())
	uuidTwo = str(uuid.uuid4())

	plist = dict(
		PayloadContent = [ dict(
				DisconnectOnIdle = 0,
				IPSec = dict(
					AuthenticationMethod = "SharedSecret",
					OnDemandEnabled = 0,
					PromptForVPNPIN = False,
					# this somehow needs to be a data object, not a string
					# so it's masked as base64 in the plist...
					# but I don't know how to use FoundationPlist to create
					# a data object, so it's a plain string at the moment
					SharedSecret = sharedSecret
					),
				IPv4 = dict(
					OverridePrimary = False,
					),
				PPP = dict(
					AuthName = username,
					AuthPassword = password,
					AuthenticationMethod = "Password",
					CommRemoteAddress = server,
					OnDemandEnabled = 0,
					),
				PayloadDisplayName = "VPN (" + company +")",
				PayloadEnabled = True,
				PayloadIdentifier = "com.apple.mdm." + company.lower() + ".private." + uuidOne + ".alacarte.vpn." + uuidTwo,
				PayloadType = "com.apple.vpn.managed",
				PayloadUUID = uuidTwo,
				PayloadVersion = 1,
				Proxies = dict(
					),
				UserDefinedName = company + " VPN",
				VPNType = "L2TP",
				)
		],
		PayloadDisplayName = company + " VPN",
		PayloadIdentifier = "com.apple.mdm." + company.lower().replace(" ", "") + ".private." + uuidOne + ".alacarte",
		PayloadOrganization = company,
		PayloadRemovalDisallowed = False,
		PayloadScope = "User",
		PayloadType = "Configuratrion",
		PayloadUUID = uuidOne,
		PayloadVersion = 1,
		)
	return plist

def write_plist(plist,filename):
	FoundationPlist.writePlist(plist, filename)

def main():
	"""Main routine"""

	usage = """usage: %prog [options] [/path/to/profile.mobileconfig]
	   Creates a configuration profile, profile.mobileconfig
	   To configure a L2TP VPN on a macOS machine without needing
	   to have Profile Manager running on a macOS Server just to
	   build some basic configuration profiles.
	   """

	parser = optparse.OptionParser(usage=usage)

	parser.add_option('--username', '-u',
	                  help='The username for the L2TP VPN Server.')
	parser.add_option('--password', '-p',
	                  help='The password for the L2TP VPN Server.')
	parser.add_option('--secret', '-s',
	                  help='The shared secret for the L2TP VPN Server.')
	parser.add_option('--company', '-c',
	                  help='The company name for the generated Configuration Profile.')
	parser.add_option('--vpn', '-v',
	                  help='The IP Address or hostname of the VPN Endpoint.')
	
	if len(sys.argv) == 1:
		parser.print_usage()
		exit(0)

	options, arguments = parser.parse_args()

	if not options.username or not options.password or not options.secret or not options.company or not options.vpn:
		parser.print_help()
		exit(0)

	sharedSecret = options.secret
	username = options.username
	password = options.password
	company = options.company
	server = options.vpn

	mobileConfig = None
	if arguments:
		mobileConfig = arguments[0]
	else:
		mobileConfig = os.getcwd() +"/" + company + " VPN for " + username + ".mobileconfig"

	print ("Created Configuration Profile: " + mobileConfig)

	plist = build_plist(sharedSecret, username, password, company, server)
	write_plist(plist,mobileConfig)

if __name__ == '__main__':
    main()
