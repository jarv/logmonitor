# Summary

## Installation

    # Install requirements
    easy_install3 pip
    pip3 install -r requirements.txt


## Instructions

    # Edit config.yml to point to a log in "Common Log Format" or
    # run the following to generate dummy data:

    ./bin/gen_fake_logs 1 > /tmp/access.log

    # Run the log watcher

    ./logmonitor

    # You should see the stats for the single log line appear
    # Example:
    #   Top 3 with the most hits
    #   Type     Name, Count
    #   -------  ---------------
    #   section  [('/posts', 1)]
    #   status   [('200', 1)]
    #   verb     [('GET', 1)]
    #   size     [('2497', 1)]

    # You can add more lines by running `./bin/gen_fake_logs 1 >> /tmp/access.log`
    # and watch the stats increase.

## Showing Alerts

    # By default we will alert when the avg traffic is greater than 1 over the previous
    # 2 minutes

    # This will forward-fill the access.log with 200
    # random requests
    ./gen_fake_logs 100 > /tmp/access.log

    ./logmonitor

    # Wait 2 minutes for the requisite number of datapoints
    # Will ALERT after 2 minutes if over the threshold
    # Note: Because the script will fill in log events that occur in the future
    #       they will be counted multiple times (see TODO).

## Tests

    nosetests

# TODO Improvements

* Improve the regex for parsing logs, handle malformed input.
* Add the ability to monitor a directory as well as a single file with handling of log rotation.
* Use a threaded timer, async io
* More tests, load testing
* Add more alert dimensions:
    * GETS, POSTS, PUTS, 500s, etc.
    * Add p90, p50 as well as averages
* Currently we count log lines occur in the future which may not be the desirable behavior.
* Prettier output, ncurses.

## Description (pasted from assignment)

HTTP log monitoring console program
Create a simple console program that monitors HTTP traffic on your machine:
Consume an actively written-to w3c-formatted HTTP access log (https://en.wikipedia.org/wiki/Common_Log_Format)
Make sure a user can keep the console app running and monitor traffic on their machine

* Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what's before the second '/' in a URL. i.e. the section for "http://my.site.com/pages/create' is "http://my.site.com/pages"), as well as interesting summary statistics on the traffic as a whole.

* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}”
* Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered
* Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons.
* Write a test for the alerting logic
* Explain how you’d improve on this application design
