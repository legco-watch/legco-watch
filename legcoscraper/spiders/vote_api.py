# -*- coding: utf-8 -*-
"""
Scraper for the XML vote API
Such as http://www.legco.gov.hk/general/english/open-legco/cm-201213.html

This page is kind of ridiculous.  The raw HTML is an empty table that lists
each of the possible dates that a vote could have occurred (these should correspond to
meeting dates), but there are no links to the XML files.  Once the page
loads, a script runs that queries urls like http://www.legco.gov.hk/php/detect.php?date=20130703
for each date.  If the query returns "SUCCESS,1,1", it fills in the link to something
like http://www.legco.gov.hk/yr12-13/chinese/counmtg/voting/cm_vote_20130130.xml.
If the query returns 404, then no link is created.

The strategy for handling this is the same as the page.  We'll scrape the index pages
and create items for each date.  We'll download each XML file separately and save.
The processor will load the XML into the database, then we'll parse the XML with
an object abstraction at the parsing stage.
"""