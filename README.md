# vpn-mobileconfig-generator
Generates a macOS VPN .mobileconfig file without needing ProfileManager on macOS Server

Run it like so:
./generator.py --username=kai --password=Password123 --secret=Shared$ecret! —vpn=vpn.automatica.com.au —company=Automatica

Please note that a configuration profile from Profile Manager will mask the Shared Secret in the plist file by base64 encoding it. This generator puts it in as a string so it's visible in the plist if anyone cares to look. It's trivial to decode the base64 string anyway, and as I couldn't easily work out how to put a <data> object in the plist, I didn't bother.