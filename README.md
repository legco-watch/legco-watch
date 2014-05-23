LegCo Watch
===========

Join our [mailing list](https://groups.google.com/forum/#!forum/legco-watch) and introduce yourself if you'd
like to contribute.  Or check out our issue tracker.

Overview
========

LegCo Watch is a parliamentary monitoring website in the same vein as [openparliament.ca](http://openparliament.ca),
[GovTrack.us](http://govtrack.us), and [TheyWorkForYou](http://theyworkforyou.com).

One of the first challenges is that we need to parse much of the data that is stored on the LegCo's
[official website](http://legco.gov.hk).  Some of it is accessible as XML or in an API, but the majority
is in HTML or PDF.

Once the data is parsed, we'll store the it in a structured database format, and make it accessible via API and via our site.

Technology stack
================

We use Django for our backend and various Python packages to conduct our scraping.  The
[Pombola](https://github.com/mysociety/pombola/) and [Poplus](http://poplus.org/) projects have been very
helpful as a guide for how to implement some of our components in Django.

Contributing
============

For non-developers, you can contribute by helping us by telling us what you want to use the data for.
We're constantly collecting new use cases to guide our design of the site.

For developers, you can contribute by forking this repository.  Create a branch on your fork for the feature you
want to work on, then submit a pull request when you're ready.  Be sure to communicate with us on our
mailing list so that we can coordinate our work.  We also have a Vagrantfile set up for the local development
environment that you can use.  Learn more about Vagrant from
[their docs](http://docs.vagrantup.com/v2/getting-started/index.html)

Deploying
=========

Certificates and private keys are not stored in this repo.  You'll need to copy them into `devops/certs`
or `devops/roles/common/files` before some of the Ansible deployment scripts will work.
