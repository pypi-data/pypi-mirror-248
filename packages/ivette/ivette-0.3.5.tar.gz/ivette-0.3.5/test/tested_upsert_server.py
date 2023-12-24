from ivette.IO_module import system_info
from ivette.supabase_module import upsert_server


print(upsert_server(system_info=system_info()))