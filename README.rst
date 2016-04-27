How to start
============

API
===

- ``/service/<project>/<status>`` (GET): get the current ``status`` of ``project``. Supports ``format`` parameter with values ``svg``.
- ``/service/<project>/<status>`` (POST): set the current ``status`` of ``project``, creating both and the transition.


Roadmap
=======


- **1.0.0**: to be able to autodiscover status
- **2.0.0**: it renders the status to SVG
- **3.0.0**: it has a dashboard to see several status at time.
