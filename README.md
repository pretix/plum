![plum logo](https://raw.githubusercontent.com/pretix/plum/master/res/banner.png)

This repository contains the source code of the application at [marketplace.pretix.eu](https://marketplace.pretix.eu).
It was originally designed as a platform to distribute plugins for the Python-based web application pretix. However,
it is designed in a way that makes it usable by other projects besides pretix as well. Over time, we have also
broadened the scope beyond server-side plugins to also distribute client applications such as our Android and Desktop
applications. Our goal is to turn this into our central hub for software distribution.

The application is currently working in production with a limited feature set. It can be used to present software 
products  created by multiple vendors and distribute free plugins.
Admin-level management is handled through Django admin and therefore requires some familiarity with the concepts of the
software.

For Python plugins, it can be used as a ``pip`` package index. For Android apps, it can be used as an F-Droid repository.

While the long-term goal of this software also includes license and subscription handling for paid software, this part
has not been implemented yet except for a few singular puzzle pieces.

We do not offer support for this software, feel free to use it, report issues, or contribute to it, but please don't
expect us to invest much time in it beyond the functionality we need for our use case.

## Security

If you notice a security problem with this application, please reach out to security@pretix.eu privately instead
of opening an issue.

## License

Copyright 2019-2020 Raphael Michel

Copyright 2021-present rami.io GmbH

Released under GNU Affero General Public License 3.0.