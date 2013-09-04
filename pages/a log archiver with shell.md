# [David Lee ](http://leeleilei.github.com/)

  * [misc](http://leeleilei.github.com/category/misc.html)

#  [A Log Archiver with shell](http://leeleilei.github.com/a-log-archiver-
with-shell.html)

Tue 03 September 2013  By [leeleilei@gmail.com](http://leeleilei.github.com/au
thor/leeleileigmailcom.html)

In [misc](http://leeleilei.github.com/category/misc.html).

tags: [sqluldr](http://leeleilei.github.com/tag/sqluldr.html)[shell](http://le
eleilei.github.com/tag/shell.html)

One of the equipment component is using the oracle DB to store the history
provisioning commands, however due to the capacity limitation, the log could
not be saved forever. So the old ones are overwrite with the rotation
mechanism.

The log is important for the revenue assurance and audition, anyway we have to
keep it somewhere else to query for kind of purpose.

Here’s the solution to dump the oracle data and transfer it to a specific ftp
server,

  1. login the secure ftp address 10.1.1.1, port 22
  2. change the directory to /opt/pub/software/tmp/pgw.archive
  3. you will get the daily provisioning log named with “YYYY-MM-DD.pgw.log.gz”, e.g. “2011-04-26.pgw.log.gz”

> tip: use the “date -d” to get the “relative date”

`shell #!/bin/sh # # 2011-04-26, leeleilei<at>gmail<dot>com # used for backup
the daily pgw provisoning log # today=`date +”%Y%m%d”` day=`date -d “$today 1
day ago” +”%d”` yesterday=`date -d “$today 1 day ago” +”%Y-%m-%d”`
/home/oracle/sqluldr2_linux32_10204.bin user=pgw/huawei field=”|”
query=”select OPERATOR_NAME, OPERATION_TIME, MML_COMMAND, CMDRESULT, ERRORCODE
from OPERATION_LOG_TABLE_$day whe re OPERATION_TIME like ‘$yesterday%’”
file=$yesterday.pgw.log log=sqluldr.runlog gzip $yesterday.pgw.log
2>>sqluldr.runlog scp $yesterday.pgw.log.gz
omu@172.16.128.1:/opt/pub/software/tmp/pgw.archive/ >> sqluldr.runlog rm
$yesterday.pgw.log.gz`

## social

  * [atom feed](http://leeleilei.github.com/feeds/all.atom.xml)

Proudly powered by [Pelican](http://getpelican.com/), which takes great
advantage of [Python](http://python.org).

The theme is by [Smashing
Magazine](http://coding.smashingmagazine.com/2009/08/04/designing-a-html-5
-layout-from-scratch/), thanks!

  *[
                Tue 03 September 2013
        ]: 2013-09-03T21:00:00

