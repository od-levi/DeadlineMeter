from utils.supabase_client import supabase

def add_task_db(user, task):
    supabase.table("tasks").insert({
        "user_id": user,
        "name": task["name"],
        "deadline": str(task["deadline"]),
        "status": task["status"],
        "days_left": task["days_left"]
    }).execute()

def load_data(user):
    response = supabase.table("tasks") \
        .select("*") \
        .eq("user_id", user) \
        .execute()
    
    return response.data

def delete_task_db(task_id):
    supabase.table("tasks") \
        .delete() \
        .eq("id", task_id) \
        .execute()

def update_task_db(task_id, updates):
    supabase.table("tasks") \
        .update(updates) \
        .eq("id", task_id) \
        .execute()