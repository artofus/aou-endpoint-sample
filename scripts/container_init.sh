#!/bin/sh
RTM=python
APP=server.py

STOP_TIMEOUT=10

function sigterm() {
    echo "Signal detected, shutting down..."
    kill -s TERM ${SUBPROC}

    let count=0
    echo -n 'Waiting for process to die...'
    while kill -0 ${SUBPROC} 2>/dev/null; do
        if [ ${count} -lt ${STOP_TIMEOUT} ]; then
            let count++
            sleep 1
            echo -n '.'
        else
            echo -e "\nTimed out waiting for process to stop, killing it..."
            kill -s KILL ${SUBPROC}
        fi
    done
    echo "Done."
}

trap sigterm SIGTERM SIGINT

${RTM} ${APP}

SUBPROC=$!
echo "Manager PID: ${$}"
echo "Process PID: ${SUBPROC}"

wait