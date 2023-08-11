import psycopg2
import os

password = os.getenv("API_SECRET")
# Database connection parameters
db_params = {
    "dbname": "yelpbusinesses",
    "password": password,
    "host": "localhost",
    "port": "5433"
}

# Establish a connection
conn = psycopg2.connect(**db_params)

# Create a cursor
cur = conn.cursor()


# Display businesses
query = "SELECT id, name, address FROM businesses;"
cur.execute(query)
businesses = cur.fetchall()

for business in businesses:
    print("Yelp Business Explorer")
    print(f"name: {business[1]}")
    print(f"address: {business[2]}")

# Business Details
if input("Do you want to look at Business Details (y/n)") == "y":
    # business_id = int(
    #     input("Look at details for which business id? (enter id)"))
    business_details_query = """
    SELECT b.id AS business_id, b.name AS business_name, b.address AS business_address,
       r.score AS review_score, r.text AS review_text, r.reviewer_name, r.reviewer_email
    FROM businesses AS b
    LEFT JOIN reviews AS r ON b.id = r.business_id;
    """
    cur.execute(business_details_query)
    businesses_with_reviews = cur.fetchall()
    print(businesses_with_reviews)
    for row in businesses_with_reviews:
        print("Business ID:", row[0])
        print("Business Name:", row[1])
        print("Business Address:", row[2])
        print("Review Score:", row[3])
        print("Review Text:", row[4])
        print("Reviewer Name:", row[5])
        print("Reviewer Email:", row[6])
        print("-" * 20)


# Ask user for more details
if input("Make a Review? (press 1)\n") == "1":
    business_id = int(
        input("Enter the ID of the business you want to review: "))
    review_score = int(input("Enter your review score (0 to 5): "))
    review_text = input("Enter your review text: ")
    reviewer_name = input("Enter your name: ")
    reviewer_email = input("Enter your email: ")

    # Insert the review
    insert_review_query = """
    INSERT INTO reviews (business_id, score, text, reviewer_name, reviewer_email)
    VALUES (%s, %s, %s, %s, %s);
    """
    cur.execute(
        insert_review_query,
        (business_id, review_score, review_text, reviewer_name, reviewer_email)
    )
    conn.commit()
    print("Review added successfully!")

# Close cursor and connection
cur.close()
conn.close()
