""" Serializing data """
import csv
import datetime
from ast import literal_eval

from app.schema import DocumentSchema
from app.models import Document, Rubric

if __name__ == "__main__":
    file_out = open('documents.txt', 'w', encoding='utf-8')
    documentSchema = DocumentSchema()

    with open("posts.csv", encoding="utf-8") as csv_file:
        rows = csv.DictReader(csv_file, delimiter=",", quotechar='"')
        for row in rows:
            text = row["text"]
            created = datetime.datetime.fromisoformat(row["created_date"])
            rubrics = literal_eval(row["rubrics"])
            rubrics = [Rubric(rubric=rubric) for rubric in rubrics]

            document = Document(text=text, created_date=created, rubrics=rubrics)

            document_serial = documentSchema.dump(document)

            file_out.write(str(document_serial) + "\n")
