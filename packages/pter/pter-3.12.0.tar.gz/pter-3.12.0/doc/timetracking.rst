Time Tracking
=============

pter can track the time you spend on a task. By default, type "t" to
start tracking. This will add a ``tracking:`` attribute with the current local
date and time to the task.

When you select that task again and type "t", the ``tracking:`` tag will be
removed and the time spent will be saved in the tag ``spent:`` as hours and
minutes.

If you start and stop tracking multiple times, the time in ``spent:`` will
accumulate accordingly. The smallest amount of time tracked is one minute.

