import csv
import json

print("Converting users...")
users = []
with open("data/users.dat") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for row in reader:
        users.append({"model": "ratings.Rater",
                      "pk": row[0],
                      "fields": {
                          "age": int(row[2]),
                          "zip_code": row[4]
                      }})

with open("./fixtures/users.json", "w") as outfile:
    outfile.write(json.dumps(users))

print("Converting movies...")
movies = []
with open("data/movies.dat", encoding="windows-1252") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for row in reader:
        movies.append({"model": "ratings.Movie",
                       "pk": row[0],
                       "fields": {
                           "title": row[1]
                       }})

with open("./fixtures/movies.json", "w") as outfile:
    outfile.write(json.dumps(movies))

print("Converting ratings...")
ratings = []
with open("data/ratings.dat") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for idx, row in enumerate(reader):
        ratings.append({"model": "ratings.Rating",
                        "pk": idx + 1,
                        "fields": {
                            "rater": row[0],
                            "movie": row[1],
                            "rating": float(row[2])
                        }})

with open("./fixtures/ratings.json", "w") as outfile:
    outfile.write(json.dumps(ratings))
