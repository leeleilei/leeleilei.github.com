One of the equipment component is using the oracle DBMS to store the history
provisioning commands, however due to the capacity limitation, the log could
not be saved forever. So the old ones are overwrite with the rotation
mechanism.

The log is important for the revenue assurance and audition, anyway we have to
keep it somewhere else to query for kind of purpose.

Here's the solution to dump the oracle data and transfer it to a specific ftp
server,

  1. login the secure ftp address 10.1.1.1, port 22
  2. change the directory to /opt/pub/software/tmp/pgw.archive
  3. you will get the daily provisioning log named with YYYY-MM-DD.pgw.log.gz, e.g. 2011-04-26.pgw.log.gz

	 **tip: use the "date -d" to get the "relative date"**

		#!/bin/sh
		# file name: pgwbk.sh
		# usage:
		# for backup the daily pgw provisoning log
		# put it in crontab if you need it regularly run
		today=`date +"%Y%m%d"`
		day=`date -d "$today 1 day ago" + "%d"`
		yesterday=`date -d "$today 1 day ago" + "%Y-%m-%d"`
		/home/oracle/sqluldr2_linux32_10204.bin user=pgw/huawei field=”|” query=”select OPERATOR_NAME, OPERATION_TIME, MML_COMMAND, CMDRESULT, ERRORCODE from OPERATION_LOG_TABLE_$day whe re OPERATION_TIME like ‘$yesterday%’” file=$yesterday.pgw.log log=sqluldr.runlog gzip $yesterday.pgw.log 2>>sqluldr.runlog
		scp $yesterday.pgw.log.gz omu@172.16.128.1:/opt/pub/software/tmp/pgw.archive/ >> sqluldr.runlog
		rm $yesterday.pgw.log.gz`

---
Last Update: Sep 6, 2013 23:22 @Manila
