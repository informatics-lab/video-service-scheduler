#!/usr/bin/env python

import boto

import sys
sys.path.append("./config")
import analysis_config as config


class ImgJob(object):
    def __init__(self, message):
        self.data_file = message["data_file"]
        self.profile_name = message["profile_name"]
        self.model = message["model"]
        self.variable = message["variable"]
        self.id = self.data_file + "_" + self.profile_name
        self.time_step = message["time_step"]
        self.frame = message["frame"]
        self.nframes = message["nframes"]
        self.message = message

    def __str__(self):
        return __dict__

    def __repr__(self):
        return __dict__


class NoJobsError(Exception):
    def __init__(self, value=""):
        self.value = value
    def __str__(self):
        return repr(self.value)


def getReadyImages(queue, visibility_timeout=60):
    messages = queue.get_messages(visibility_timeout, number_messages=999999999) #get all messages
    try:
        jobs = [ImgJob(message) for message in messages]
    except IndexError:
        raise NoJobsError()

    return jobs


def getMatchingSetOfJobs(jobs):
    ids = set([job.id for job in jobs])
    for id in ids:
        these_jobs = [job for job in jobs if job.id == id]
        these_frames = set([job.frame for job in these_jobs])
        if len(these_frames) == these_jobs[0].nframes:
            return these_jobs
    return None


def getQueue(queue_name):
    conn = boto.sqs.connect_to_region(os.getenv("AWS_REGION"),
                                      aws_access_key_id=os.getenv("AWS_KEY"),
                                      aws_secret_access_key=os.getenv("AWS_SECRET_KEY"))
    queue = conn.get_queue(queue_name)
    return queue


def deleteJobs(queue, jobs):
    for job in jobs:
        queue.delete(job.message)


def postVideoServiceJob(queue, msg):
    m = boto.sqs.message.Message()
    m.message_attributes(msg)
    queue.write(m)


if __name__ == "__main__":
    image_ready_queue = getQueue("image_ready_queue")
    video_service_queue = getQueue("video_service_queue")

    jobs = getReadyImages(image_ready_queue)
    full_set = getMatchingSetOfJobs(jobs)

    if full_set:
        frame = full_set[0]
        print "Picked up " + frame.data_file + " " + frame.profile_name
        deleteJobs(image_ready_queuem, full_set)
        postVideoServiceJob(video_service_queue, {"model": frame.model,
                                                  "variable": frame.variable,
                                                  "profile_name": frame.profile_name})

    sys.exit()