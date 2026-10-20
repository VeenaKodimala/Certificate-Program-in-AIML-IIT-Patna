from log_processing import logText_splitter1

sample_logs="""2026-10-20 10:00:01 INFO Service started
2026-10-20 10:00:05 ERROR Database connection failed
2026-10-20 10:00:06 INFO Retrying connection
"""

chunks = logText_splitter1(sample_logs,"serverlogs",50,10)


print(chunks)