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
with a string name.  The class tries to parse the name into its constituent parts.  It then allows comparisons between
`MemberNames` or distance measures for fuzzy matches.

## Searching the database
