#!/usr/bin/env sh
command -v systemctl >> /dev/null || exit 1
service=postgresql.service
if ! systemctl check $service >> /dev/null && [ "$1" = "start" ] ; then
	systemctl start $service
elif [ "$1" != "start" ] ; then
	systemctl ${1:-status} $service
fi
