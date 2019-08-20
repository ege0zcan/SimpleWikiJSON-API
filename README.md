# SimpleWikiJSON-API
A simple JSON API for managing documents with different revisions in a wiki backend, written in Python using the Flask framework

## List of Commands: ##

***GET /documents***

Returns a list of available titles.

***GET /documents/<title>***

Returns a list of available revisions for a document.


***GET /documents/<title>/<timestamp>***

Returns the document as it was at that timestamp.


***GET /documents/<title>/latest***

Returns the current latest version of the document.


***POST /documents/<title>***

This allows users to post a new revision of a document.
