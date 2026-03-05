# name: Joseph Moler
# date: 3/5/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 2/2

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Playlist')

def create_song():
    """Create a new song item in the DynamoDB table."""
    title = input("Enter the song title: ").strip()
    artist = input("Enter the artist: ").strip()
    time = input("Enter the length of the song: ").strip()

    # Create a new song item
    song_item = {
        "Title": title,
        "Artist": artist,
        "Time": time,
    }

    # Put the item into the DynamoDB table
    table.put_item(Item=song_item)
    print(f"\nSong '{title}' by {artist} created successfully.")

def print_all_songs():
    """Scan the entire Playlist table and print each song."""
    # scan() retrieves ALL items in the table.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No songs found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} song(s):\n")
    for song in items:
        print_song(song)

def print_song(song):
    title = song.get("Title", "Unknown Title")
    artist = song.get("Artist", "Unknown Artist")
    time = song.get("Time", "Unknown Time")

    print(f"  Title  : {title}")
    print(f"  Artist : {artist}")
    print(f"  Time   : {time}")
    print()

def update_song():
    try:
        title = input("What is the song title? ")
        time = input("What is the new length of the song: ").strip()

        # Ensure the time is valid (assuming it's a valid string for song length)
        if not time:
            raise ValueError("Song length cannot be empty.")
        
        # Update the song's length in the table
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Time = :t",
            ExpressionAttributeValues={':t': time}
        )
        print("Song length updated successfully.")

    except Exception as e:
        print(f"Error in updating song length: {e}")

def delete_song():
    """Delete a song item from the DynamoDB table based on the title."""
    title = input("Enter the song title to delete: ").strip()

    # Delete the item from the DynamoDB table
    response = table.delete_item(
        Key={"Title": title}
    )

    if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
        print(f"\nSong '{title}' deleted successfully.")

def query_song():
    """Query a song based on its title."""
    title = input("What is the song title? ")
    response = table.get_item(Key={"Title": title})
    song = response.get("Item")
    
    if song:
        print(f"\nSong '{title}' details:")
        print(f"  Artist: {song['Artist']}")
        print(f"  Time  : {song['Time']}")
    else:
        print(f"\nSong '{title}' not found.")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (change the length)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song by title")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_all_songs()
        elif input_char.upper() == "U":
            update_song()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_song()
        elif input_char.upper() == "X":
            print("Exiting...")
        else:
            print("Not a valid option. Try again.")

main()