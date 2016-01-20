# ![http://code.google.com/p/google-sites-mirror/logo?logo_id=1266411067&nonsense=image.png](http://code.google.com/p/google-sites-mirror/logo?logo_id=1266411067&nonsense=image.png) Google Sites Mirroring & Backup Script #

A Python module and script, which is able to download content from [Google Sites](http://sites.google.com) (via [Sites Data API](http://code.google.com/apis/sites/)) and create a mirror of the original web sites, but with a custom design (via Cheetah template) - for hosting on a traditional webserver.

Google Sites then become just an editing interface for the content, which is displayed somewhere else - with the possibility to completely customize the design of the websites.

The complete Sites structure is preserved, including the attachments. The script creates directories and files emulating the original Sites on the local disk. To publish such mirror of the Google Sites, it is enough to  copy this directories via FTP to any webserver.
We plan to support also direct hosting on the Google App Engine.

Development is supported by [Moravian Library in Brno](http://www.mzk.cz/) and R&D grant DC08P02OUK006 - [Old Maps Online](http://www.oldmapsonline.org) from Ministry of Culture of the Czech Republic.