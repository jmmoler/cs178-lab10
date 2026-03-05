# name: Joseph Moler
# date: 3/5/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5/5

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    """Create a new movie item in the DynamoDB table."""
    title = input("Enter the movie title: ").strip()
    year = input("Enter the release year: ").strip()
    ratings = input("Enter the ratings (comma-separated): ").strip()
    genre = input("Enter the genre: ").strip()

    # Create a new movie item
    movie_item = {
        "Title": title,
        "Year": year,
        "Ratings": ratings.split(","),
        "Genre": genre
    }

    # Put the item into the DynamoDB table
    table.put_item(Item=movie_item)
    print(f"\nMovie '{title}' created successfully.")

def print_all_movies():
    """Scan the entire Movies table and print each item."""
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

def print_movie(movie):
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    ratings = movie.get("Ratings", "No ratings")
    genre = movie.get("Genre", "No genre")

    print(f"  Title  : {title}")
    print(f"  Year   : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Genre  : {genre}")
    print()

def update_rating():
    try:
        title = input("What is the movie title? ")
        rating = int(input("What is the rating (integer): "))

        # Ensure the rating is a valid integer
        if rating < 1 or rating > 100:  # Adjust based on valid rating range
            raise ValueError("Rating must be between 1 and 100.")
        
        # Assuming 'table' is already initialized as a DynamoDB resource
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
        print("Rating updated successfully.")

    except Exception as e:
        print(f"Error in updating movie rating")


def delete_movie():
    """Delete a movie item from the DynamoDB table based on the title."""
    title = input("Enter the movie title to delete: ").strip()

    # Delete the item from the DynamoDB table
    response = table.delete_item(
        Key={"Title": title}
    )

    if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
        print(f"\nMovie '{title}' deleted successfully.")

def query_movie():
    # a function that returns the average rating for a given movie.
    title = input("What is the movie title? ")
    response = table.get_item(Key={"Title": title})
    movie = response.get("Item")
    if movie and "Ratings" in movie:
        ratings = movie["Ratings"]
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            print(f"\nAverage rating for '{title}': {average_rating:.2f}")
        else:
            print(f"\nNo ratings found for '{title}'.")
    else:
        print(f"\nMovie '{title}' not found or has no ratings.")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
