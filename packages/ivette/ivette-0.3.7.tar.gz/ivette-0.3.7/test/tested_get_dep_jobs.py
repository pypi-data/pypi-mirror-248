# Test
from ivette.run_module import run_job
from ivette.supabase_module import get_dep_jobs


if __name__ == "__main__":
    jobs = get_dep_jobs('4dff0e5c-76cb-4efd-852f-4cf33facd8fa')
    for job in jobs:
      print(job.get('id'))
