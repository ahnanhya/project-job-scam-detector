from services.job_search import search_jobs


result = search_jobs(
    "software developer",
    "Chennai"
)


print("\n==============================")
print("JOB API TEST")
print("==============================")

print(
    "Success:",
    result.get("success")
)

print(
    "Message:",
    result.get("message")
)

print(
    "Total jobs:",
    result.get("total")
)


print("\nJobs:")

for job in result.get(
    "jobs",
    []
):

    print(
        "\n------------------------------"
    )

    print(
        "Title:",
        job.get("title")
    )

    print(
        "Company:",
        job.get("company")
    )

    print(
        "Location:",
        job.get("location")
    )

    print(
        "Salary:",
        job.get("salary")
    )

    print(
        "Source:",
        job.get("source")
    )

    print(
        "Link:",
        job.get("link")
    )