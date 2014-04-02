RHN-Scripts
===========

Scripts interfacing with RHN Satellite server directly to bypass restrictions &amp; facilitate programatic control of managed systems.

Purpose
-------

I made this when I became frustrated at my organization's inability to give me access to the rhn-channel tool, so I can programatically add and remove channel subscriptions from my registered RHEL hosts. To be fair, their hands are tied as Satellite does not offer granular enough control, and my account does not need administrator access: Satellite accounts are more of an all or nothing switch.

These scripts interface directly with the API and unlock the functionality you should have had with RHEL's built in tools.

Resources
---------

The [RHN Satellite 5.5 API](https://access.redhat.com/site/documentation/en-US/Red_Hat_Network_Satellite/5.5/html/API_Overview/files/html/handlers/SystemHandler.html#setChildChannels) is good enough and available on an all-inclusive single HTML page.

The scripts are written in Python 2.6. They should be Python 3 compatible, let me know (send pull request) if there are issues.

Scripts
-------

* rhn-channel-add-scl &lt;hostname&gt; [hostname] ...
  * Takes at least one argument. Searches for any systems in Satellite that begin with the given hostnames and enables [Software Collections](http://developerblog.redhat.com/2013/01/28/software-collections-on-red-hat-enterprise-linux/) by adding the SCL channel, if available.
