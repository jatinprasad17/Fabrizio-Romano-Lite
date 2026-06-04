from supabase_client import add_subscriber, get_all_subscribers, subscriber_exists, remove_subscriber

add_subscriber("test@gmail.com", "Manchester City")
print("Added!")

print(get_all_subscribers())

print(subscriber_exists("test@gmail.com"))

remove_subscriber("test@gmail.com")
print("Removed!")

print(get_all_subscribers())