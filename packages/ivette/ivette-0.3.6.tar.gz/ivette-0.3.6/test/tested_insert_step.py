from ivette.file_io_module import get_step_data
from ivette.supabase_module import insert_step


print(get_step_data('a74c60e6-1737-4e97-bd35-9e0d76cbc9b9'))
step_data = get_step_data('a74c60e6-1737-4e97-bd35-9e0d76cbc9b9')

if step_data:
  print(insert_step('a74c60e6-1737-4e97-bd35-9e0d76cbc9b9',
        'a74c60e6-1737-4e97-bd35-9e0d76cbc9b9',
        step_data))
