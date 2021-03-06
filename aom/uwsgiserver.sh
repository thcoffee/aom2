if [ ! -n "$1" ]
then
    echo "Usages: sh uwsgiserver.sh [start|stop|restart]"
    exit 0
fi

if [ $1 = start ]
then
    psid=`ps aux | grep "uwsgi" | grep -v "grep" | wc -l`
    echo $psid
    if [ $psid -gt 2 ]
    then
        echo "uwsgi is running!"
        exit 0
    else
        uwsgi django.ini
        echo "Start uwsgi service [OK]"
    fi


elif [ $1 = stop ];then
    killall -9 uwsgi
    echo "Stop uwsgi service [OK]"
elif [ $1 = restart ];then
    killall -9 uwsgi
    uwsgi --ini django.ini
    echo "Restart uwsgi service [OK]"

else
    echo "Usages: sh uwsgiserver.sh [start|stop|restart]"
fi

