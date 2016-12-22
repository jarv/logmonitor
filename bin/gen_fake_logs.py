#!/usr/bin/env python3
import datetime
import numpy
import random
from faker import Faker
from random import randrange


def gen_fake_log_lines(num_lines=1):
    """
    Generates fake log lines in "Common Log Format"
    Returns a list of fake lines.
    """

    # Some dummy sections
    # Should be copied from real data
    sections = ["/pages/create", "/foo/create", "/bar/create", "/posts/1/display", "/posts/2/display", "/posts/foo?appID=xxxx"]
    statuses = [200, 500, 404, 502]
    users = ["frank", "john", "alice", "bob", "mike"]
    verbs = ["GET", "POST", "DELETE", "PUT"]
    lines = []
    otime = datetime.datetime.now()
    faker = Faker()
    while True:
        if num_lines < 1:
            break
        increment = datetime.timedelta(seconds=random.randint(30, 300))
        otime += increment

        ip = faker.ipv4()
        dt = otime.strftime('%d/%b/%Y:%H:%M:%S%z')
        size = randrange(1024, 4096)
        section = random.choice(sections)
        user = random.choice(users)
        status = numpy.random.choice(statuses, p=[0.7, 0.1, 0.1, 0.1])
        verb = numpy.random.choice(verbs, p=[0.7, 0.1, 0.1, 0.1])
        lines.append('{ip} user-identifier {user} [{datetime} +0100] "{verb} {section} HTTP/1.0" {status} {size}'.format(
            ip=ip,
            user=user,
            datetime=dt,
            verb=verb,
            section=section,
            status=status,
            size=size))
        num_lines -= 1
    return lines


if __name__ == '__main__':
    print("\n".join(gen_fake_log_lines(1)))
