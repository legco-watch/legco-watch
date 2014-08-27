# Strategy for handling member name matching

## Overview

This document discusses strategies for handling matching of plain text LegCo Member names with
database objects.  The main challenge is matching various representations of the names
representation (e.g. Jasper TSANG Yok-sing vs Jasper TSANG)

## Related documents

  - [This](https://docs.google.com/document/d/12IMmSGvUXftSi_ly2cNT4crdTJClF8S8oXygiUiY2vQ/edit) doc was an early
  planning document discussing names on the Members List
  - [This](https://docs.google.com/spreadsheets/d/1swMi5dNFJvEp53XGze7zUOQmyZAD02zXc4qk4W-ebQk/edit#gid=0) spreadsheet
  lists some of the different forms that members' names have taken
  
## Structure of names

The structure of a member's name in English can be broken down as following:

  1. Titles - Honourable, Mr, Miss
  2. English Name - Ronny, Jasper
  3. Surname - usually in caps, TONG, TSANG
  4. Chinese Name - Ka-wah, Yok-sing
  5. Honours - GBS, JP
  
In Chinese, the structure is usually as follows:

  1. Full Chinese name - 潘兆平
  2. Title - 議員, there does not appear to be any other titles
  
Honours may be present, but would still be English letter abbreviations.

In official texts, the names can appear as any combination of the components.  At minimum, it would usually include 
the surname and either the English name or Chinese name.

## Datastructure

To handle the name matching, it seems like a viable strategy would be to create a class `MemberName` that is initialized
with a string name or the components of a name as strings.  The class tries to parse the name into its constituent parts.
 It then allows comparisons between `MemberNames` or distance measures for fuzzy matches.

## Matching names to the database

Postgres has some [fuzzy matching capabilities](http://www.postgresql.org/docs/9.1/static/fuzzystrmatch.html), but not all
of our `Member` objects have the same name format, so we'll need to handle the matching logic in the application.

We don't want to hit the database every time we encounter a name to find, so we'll use some sort of matcher object
that caches the names and performs multiple searches on that cache.  The `NameMatcher` will need to work on different
kinds of Member profiles, for example `RawMember` and `RawScheduleMember`.  It will need to store the `MemberName` object
and its corresponding model object.

We'll do the matching in the view or in the matching script.  Eventually, the canonical database itself will store
the foreign keys to the member object.

