#!/usr/bin/python
import xmlrpclib
import sys, array

"""RHN Satellite API setup"""
SATELLITE_URL = "https://rhn.domain.tld/rpc/api"
SATELLITE_LOGIN = "username"
SATELLITE_PASSWORD = "password"

"""If the user didn't specify any hosts, show usage."""
if len(sys.argv) < 2:
    sys.exit("Usage:\n\t"+sys.argv[0]+" <hostname> [hostname] ...")

"""Connect to RHN Satellite API"""
client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

# systems we will add channel to
ids = array.array('i')
# channel we will add to systems
to_add = ''

for hostname in sys.argv[1:]:
    """
    Assume every argument is a hostname.
    Search my RHN Satellite systems for any
      system whose hostname starts with any
      the arguments given.
    Takes the IDs of all found systems and
      stores them in a (global) variable.
    """
    
    # get a list of all systems that have this hostname
    systems = client.system.search.hostname(key, hostname)
    
    # add these system's ids to the list of global ids
    for system in systems:
        ids.append(system['id'])

if len(ids) != 0:
    """
    If systems were found, get the first
      one and find the name of the optional
      channel.
    Otherwise, throw an error and exit.
    """
    
    # try to find optional in the list of channels this system is
    #   NOT currently subscribed to
    channels = client.system.listSubscribableChildChannels(key, ids[0])
    
    for channel in channels:
        """
        Search through all returned channels for
          the optional channel and save its name.
        """
        if channel['label'].find('optional') != -1:
            to_add = channel['label']
            break

    if len(to_add) < 2:
        """
        If the channel was not found, try to find optional in the list
          of channels this system IS subscribed to. The API
          doesn't allow listing of all channels associated with a sys.
        """
        
        channels = client.system.listSubscribedChildChannels(key, ids[0])
        
        for channel in channels:
            """
            Search through all returned channels for
              the optional channel and save its name.
            """
            if channel['label'].find('optional') != -1:
                to_add = channel['label']
                break
else:
    sys.stderr.write('No systems were found')
    exit(1)

for id in ids:
    """
    Add the optional channel to every system found above.
    """
    
    # need to get all subscribed channels first
    #   since setChildChannels is absolute.
    current_channels = client.system.listSubscribedChildChannels(key, id)
    
    # create an array of the channels system will be subscribed to
    #   and include existing channels.
    channels = []
    for channel in current_channels:
        channels.append(channel['label'])

    for channel in channels:
        # if the channel to be added already exists, don't double add
        if channel == to_add:
            break
    else:
        # if the channel doesn't already exist, add it!
        channels.append(to_add)

    # finally, set all those channels as the current subscriptions
    client.system.setChildChannels(key, id, channels)

    # write a success message
    print("\033[1;32mSuccess:\033[1;m\nSystem "+str(id)+": "+str(channels))

"""Kill the connection to RHN"""
client.auth.logout(key)
